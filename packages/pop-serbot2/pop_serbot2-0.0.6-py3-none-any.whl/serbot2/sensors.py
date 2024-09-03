

import time
import struct
import threading
import numpy as np

from .config import IP, GROUP, __version__
from .Util import ICAN


class Constants:
    US = 1e-6
    US_10 = 1e-5
    US_100 = 1e-4
    MS = 1e-3
    MS_10 = 1e-2
    MS_100 = 1e-1
    MS_1000 = 1.0


class KalmanFilter:
    def __init__(
        self,
        num_sensors,
        measurement_time=Constants.MS,
        initial_state=None,
        initial_covariance=None,
    ):
        self.num_sensors = num_sensors
        self.dt = measurement_time

        self.x = (
            initial_state if initial_state is not None else np.zeros((num_sensors, 1))
        )

        self.P = (
            initial_covariance
            if initial_covariance is not None
            else np.eye(num_sensors) * 100
        )

        self.F = np.eye(num_sensors)
        self.B = np.zeros((num_sensors, num_sensors))
        self.u = np.zeros((num_sensors, 1))
        self.H = np.eye(num_sensors)
        self.Q = np.eye(num_sensors) * 0.1
        self.R = np.eye(num_sensors) * 3

    def predict(self):
        self.x = np.dot(self.F, self.x) + np.dot(self.B, self.u)
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q

    def update(self, z):
        K = np.dot(
            np.dot(self.P, self.H.T),
            np.linalg.inv(np.dot(np.dot(self.H, self.P), self.H.T) + self.R),
        )
        self.x = self.x + np.dot(K, (z - np.dot(self.H, self.x)))
        self.P = self.P - np.dot(np.dot(K, self.H), self.P)


class ExponentialSmoothingFilter:
    def __init__(self, window_size=5, alpha=0.15):
        self.__window_size = window_size
        self.__alpha = alpha
        self.__data_list = []

    def update(self, data):
        self.__data_list.append(data)
        if len(self.__data_list) > self.__window_size:
            self.__data_list.pop(0)
        if len(self.__data_list) == 1:
            filtered_value = data
        else:
            filtered_value = (
                self.__alpha * data + (1 - self.__alpha) * self.__data_list[-2]
            )

        return filtered_value
    
    
class IGroup(ICAN):
    ican_groups = {}
    
    def __init__(self, ip, group):
        if group not in IGroup.ican_groups:
            super().__init__(ip, group)
            IGroup.ican_groups[group] = self.ican
        else:
            self.ican = IGroup.ican_groups[group]            
            if ip is not IP:
                self.ican.appendRemote(ip)
            
    def __del__(self):
        pass
    

class IMU:
    class Sensor(IGroup):
        def __init__(self, ip=IP, group=GROUP):
            IMU_ID = self.__class__.ID
            IMU_GPORT = self.__class__.GPORT
            
            super().__init__(ip, group)
            self.__ican = self.ican_groups[group]
            self.__ican.addMcastReceiver(
                IMU_GPORT,
                IMU_ID,
            )

        def __del__(self):
            pass

        def __unpack(self, data):
            if self.ID == IMU.Accel.ID:
                data_scale = struct.unpack("hhh", struct.pack("6B", *data))
                data = tuple(map(lambda n: n / 100, data_scale[:]))
                return data
            elif self.ID == IMU.Gravity.ID:
                data_scale = struct.unpack("hhh", struct.pack("6B", *data))
                data = tuple(map(lambda n: n / 100, data_scale[:]))
                return data
            elif self.ID == IMU.Gyro.ID:
                data_scale = struct.unpack("hhh", struct.pack("6B", *data))
                data = tuple(map(lambda n: n / 916, data_scale[:]))
                return data
            elif self.ID == IMU.Magnetic.ID:
                data_scale = struct.unpack("hhh", struct.pack("6B", *data))
                data = tuple(map(lambda n: n / 16, data_scale[:]))
                return data
            elif self.ID == IMU.Euler.ID:
                data_scale = struct.unpack("hhh", struct.pack("6B", *data))
                data = tuple(map(lambda n: n / 16, data_scale[:]))
                return data
            elif self.ID == IMU.Quat.ID:
                data_scale = struct.unpack("hhhh", struct.pack("8B", *data))
                data = tuple(map(lambda n: n / (1 << 14), data_scale[:]))
                return data

        @property
        def id(self):
            return self.ID

        @property
        def gport(self):
            return self.GPORT

        def decode(self, raw):
            unpacked_value = self.__unpack(raw)
            return unpacked_value

    class Accel(Sensor):
        ID = 0x121
        GPORT = 3208

    class Gravity(Sensor):
        ID = 0x125
        GPORT = 3209

    class Gyro(Sensor):
        ID = 0x123
        GPORT = 3210

    class Magnetic(Sensor):
        ID = 0x122
        GPORT = 3211

    class Euler(Sensor):
        ID = 0x124
        GPORT = 3212

    class Quat(Sensor):
        ID = 0x126
        GPORT = 3213
        

class Ultrasonic(IGroup):
    """
    Forwarding standard:
        FRONT_LIGHT -> FRONT_RIGHT -> RIGHT -> REAR_RIGHT -> REAR_LEFT -> LEFT
        
      1)   /-----\   2)
          /   F   \
      6)  |       |  3)
          \   R   /  
      5)   \...../   4)
    """

    ID_ULTRASONIC = 0x130
    GPORT_ULTRASONIC = 3202

    NUM_SENSORS = 6
    MIN_DISTANCE = 10
    MAX_DISTANCE = 180

    def __init__(self, ip=IP, group=GROUP):
        super().__init__(ip, group)
        self.__ican = self.ican_groups[group]
        self.__ican.addMcastReceiver(
            Ultrasonic.GPORT_ULTRASONIC,
            Ultrasonic.ID_ULTRASONIC,
        )
        self.__kf = KalmanFilter(self.NUM_SENSORS)

    def __del__(self):
        pass

    @property
    def id(self):
        return self.ID_ULTRASONIC

    @property
    def gport(self):
        return self.GPORT_ULTRASONIC

    def decode(self, raw):
        z = np.array(raw).reshape(-1, 1)
        self.__kf.predict()
        self.__kf.update(z)
        filtered_distances = self.__kf.x.flatten()

        return filtered_distances


class Psd(IGroup):
    """
    Forwarding standard:
        FRONT -> REAR_RIGHT -> REAR_LEFT
                
              1)
           /-----\ 
          /   F   \
          |       |
          \   R   /  
      3)   \...../   2)
    """

    ID_PSD = 0x140
    GPORT_PSD = 3203

    NUM_SENSORS = 3

    def __init__(self, ip=IP, group=GROUP):
        super().__init__(ip, group)
        self.__ican = self.ican_groups[group]
        self.__ican.addMcastReceiver(
            Psd.GPORT_PSD,
            Psd.ID_PSD,
        )
        self.__kf = KalmanFilter(self.NUM_SENSORS)

    @property
    def id(self):
        return self.ID_PSD

    @property
    def gport(self):
        return self.GPORT_PSD

    def decode(self, raw):
        z = np.array(raw).reshape(-1, 1)
        self.__kf.predict()
        self.__kf.update(z)
        filtered_distances = self.__kf.x.flatten()

        return filtered_distances


class Encoder(IGroup):
    """
    Forwarding standard:
        LEFT -> RIGHT -> REAR               

        1)  /-----\  2)
           /   F   \
           |       |
           \   R   /  
            \...../  
               3)
    """

    ID_ENCODER_RST = 0x012
    ID_ENCODER = 0x111
    GPORT_ENCODER = 3204

    ENCODER_0 = 0x01
    ENCODER_1 = 0x02
    ENCODER_2 = 0x04

    def __init__(self, ip=IP, group=GROUP):
        super().__init__(ip, group)
        self.__ican = self.ican_groups[group]
        self.__ican.addMcastReceiver(
            Encoder.GPORT_ENCODER,
            Encoder.ID_ENCODER,
        )
        self.reset()

    @property
    def id(self):
        return self.ID_ENCODER

    @property
    def gport(self):
        return self.GPORT_ENCODER

    def reset(self, value=(ENCODER_0 | ENCODER_1 | ENCODER_2)):
        self.__ican.write(self.ID_ENCODER_RST, [value & 0x07])

    def decode(self, raw):
        return struct.unpack("hhh", struct.pack("BBBBBB", *raw))


class Light(IGroup):
    ID_LIGHT = 0x1B0
    GPORT_LIGHT = 3205

    def __init__(self, ip=IP, group=GROUP, window_size=7, alpha=0.15):
        super().__init__(ip, group)
        self.__ican = self.ican_groups[group]
        self.__ican.addMcastReceiver(
            Light.GPORT_LIGHT,
            Light.ID_LIGHT,
        )
        self.__smf = ExponentialSmoothingFilter()

    @property
    def id(self):
        return self.ID_LIGHT

    @property
    def gport(self):
        return self.GPORT_LIGHT

    def decode(self, raw):
        data = ((raw[0] << 8) | raw[1]) / 2.4
        filtered_value = self.__smf.update(data)

        return filtered_value


class Battery(IGroup):
    ID_BATTERY = 0x1A0
    GPORT_BATTERY = 3206

    def __init__(self, ip=IP, group=GROUP):
        super().__init__(ip, group)
        self.__ican = self.ican_groups[group]
        self.__ican.addMcastReceiver(
            Battery.GPORT_BATTERY,
            Battery.ID_BATTERY,
        )

    @property
    def id(self):
        return self.ID_BATTERY

    @property
    def gport(self):
        return self.GPORT_BATTERY

    def decode(self, raw):
        return round((((raw[1] & 0x0F) << 8) | raw[0]) / 10, 1)
