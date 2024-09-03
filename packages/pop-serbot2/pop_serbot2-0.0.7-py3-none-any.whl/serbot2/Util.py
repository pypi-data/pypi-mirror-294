import cv2
import librosa
import math
import time
import threading
import ipywidgets as widgets
import numpy as np
from IPython.display import display

from genlib.ican import InetCAN
from .config import __version__


def _image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation=inter)

    return resized


windows = {}


def imshow(title, image, width=300, height=300, mode="BGR"):
    import __main__

    global windows
    if not title in windows:
        windows[title] = {
            "widget": widgets.Image(width=width, height=height),
            "kernel": [],
        }
    elif (
        windows[title]["widget"].width != width
        or windows[title]["widget"].height != height
    ):
        if windows[title]["widget"].width != width:
            windows[title]["widget"].width = width

        if windows[title]["widget"].height != height:
            windows[title]["widget"].height = height

    _image = windows[title]["widget"]

    h, w = image.shape[:2]
    ih = int(_image.height)
    iw = int(_image.width)

    w_ratio = abs(h / w - ih / iw)
    h_ratio = abs(w / h - ih / iw)

    if w_ratio <= h_ratio:
        img = _image_resize(image, width=iw)
    else:
        img = _image_resize(image, height=ih)

    if mode.lower == "rgb":
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    img = bytes(cv2.imencode(".jpg", img)[1])
    _image.value = img

    kernel_num = len(__main__.In) - 1

    if not kernel_num in windows[title]["kernel"]:
        windows[title]["kernel"].append(kernel_num)
        display(_image)


def enable_imshow():
    import __main__

    if "get_ipython" in dir(__main__):
        if not ("cv2" in dir(__main__)):
            import cv2

            __main__.cv2 = cv2

        __main__.cv2.imshow = imshow


def toMFCC(file_path, duration=1.0, rate=8000):
    wave, sr = librosa.load(file_path, mono=True, sr=rate)

    padlen = math.ceil(duration * (sr / int(0.048 * sr)))

    wave = librosa.util.normalize(wave)
    mfcc = librosa.feature.mfcc(
        wave, sr=sr, n_mfcc=40, hop_length=int(0.048 * sr), n_fft=int(0.096 * sr)
    )
    mfcc -= np.mean(mfcc, axis=0) + 1e-8

    pad_width = padlen - mfcc.shape[1]
    if pad_width > 0:
        mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode="constant")
    elif pad_width < 0:
        mfcc = mfcc[:, :padlen]

    return np.expand_dims(mfcc, -1)


def gstrmer(width=640, height=480, fps=30, flip=0):
    capture_width = width
    capture_height = height
    display_width = width
    display_height = height
    framerate = fps
    flip_method = flip

    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%s ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink drop=1"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )
    

class Constants:
    US = 1e-6
    US_10 = 1e-5
    US_100 = 1e-4
    MS = 1e-3
    MS_10 = 1e-2
    MS_100 = 1e-1
    MS_1000 = 1.0


class ICAN:
    def __init__(self, ip, group):
        self.ican = InetCAN(ip, group)
        self.__thread = None

    def __del__(self):
        if self.__thread:
            self.__running = False
            self.__thread.join()

    def __on_read(self):
        while self.__running:
            arbitration_id, data = self.read(timeout=Constants.MS_100)
            if arbitration_id == self.id:
                data = self.decode(data)
                if isinstance(data, np.ndarray):
                    data = data.tolist()
                self.__callback(data, *self.args, **self.kwargs)

    @property
    def id(self):
        raise NotImplementedError()

    @property
    def gport(self):
        raise NotImplementedError()

    def decode(self, raw):
        raise NotImplementedError()
    
    def read(self, gport=None, timeout=Constants.MS_100):
        start_time = time.time()
        self.ican.emptyBuffer(gport or self.gport)
        while timeout is None or time.time() - start_time < timeout: 
            arbitration_id, data = self.ican.read(gport or self.gport) # need to empty the buffer.
            if arbitration_id == self.id:
                data = self.decode(data)
                if isinstance(data, np.ndarray):
                    data = data.tolist()
                return data

        return None

    def register_callback(self, callback, *args, **kwargs):
        self.__callback = callback
        self.__args = args
        self.__kwargs = kwargs

        self.__running = True
        self.__thread = threading.Thread(target=self.__on_read, daemon=True)
        self.__thread.start()
        