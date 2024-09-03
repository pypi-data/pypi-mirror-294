from .CAN import Can
import threading


class RGB:
    ACT_RGB = 0x250

    def __init__(self, dev="can0", bitrate=500000):
        self.__can = Can(dev, bitrate)

    def __del__(self):
        self.stop()

    def on(self, r=255, g=255, b=255):
        self.__can.write(RGB.ACT_RGB, [0x0F, r, g, b])

    def off(self):
        self.__can.write(RGB.ACT_RGB, [0x0F, 0, 0, 0])

    def stop(self):        
        self.__can.write(RGB.ACT_RGB, [0x0F, 0, 0, 0])
