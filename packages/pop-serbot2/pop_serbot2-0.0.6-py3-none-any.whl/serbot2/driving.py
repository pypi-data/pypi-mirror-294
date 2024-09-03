import math
import numpy as np

from .config import IP, GROUP, __version__
from .Util import ICAN


class Driving(ICAN):
    """
    Forwarding standard:
        FRONT_LIGHT, FRONT_RIGHT, LEFT
        
      1)   /-----\   2)
          /   F   \
          |       |  
          \   R   /  
           \...../   
              3)
    """

    ID_DRIVING = 0x010

    THROTTLE_0POINT = 100
    WHEEL_POS_LEFT = 0x01
    WHEEL_POS_RIGHT = 0x02
    WHEEL_POS_REAR = 0x04
    WHEEL_POS_ALL = WHEEL_POS_LEFT | WHEEL_POS_RIGHT | WHEEL_POS_REAR
    SPIN_RIGHT = 0x01
    SPIN_LEFT = 0x02

    def __init__(self, ip=IP, group=GROUP):
        super().__init__(ip, group)
        self.__ican = self.ican
        self.__angle = 0
        self.__steering = 0.0
        self.__throttle = 0
        self.__wheel_pos = self.WHEEL_POS_ALL
        self.__spin = None
        self.__max_value = 80
        self.__spin_offset = 10
        self.__move_offset = 20
        self.__steering_offset = 10
        self.stop()

    def __calculate_omni_wheel(self):
        if self.__spin:
            if self.__spin == self.SPIN_RIGHT:
                for i in range(3):
                    self.__wheel_vec[i] = (
                        Driving.THROTTLE_0POINT
                        - round(
                            0.01
                            * self.throttle
                            * (self.__max_value - self.__spin_offset)
                            + self.__spin_offset
                        )
                        if self.throttle != 0
                        else Driving.THROTTLE_0POINT
                    )
            elif self.__spin == self.SPIN_LEFT:
                for i in range(3):
                    self.__wheel_vec[i] = (
                        Driving.THROTTLE_0POINT
                        + round(
                            0.01
                            * self.throttle
                            * (self.__max_value - self.__spin_offset)
                            + self.__spin_offset
                        )
                        if self.throttle != 0
                        else Driving.THROTTLE_0POINT
                    )
        else:
            angle_condition = (self.__angle % 180) == 0
            if angle_condition:
                __move_offset = self.__move_offset
            else:
                __move_offset = self.__move_offset * 1.4
            weight = (
                0.01 * self.__throttle * (self.__max_value - __move_offset)
                + __move_offset
                if self.throttle != 0
                else 0
            )
            Vx = math.sin(math.radians(self.__angle)) * weight
            Vy = math.cos(math.radians(self.__angle)) * weight

            self.__wheel_vec[0] = Driving.THROTTLE_0POINT - round(
                (1 / 2) * Vx + (math.sqrt(3) / 2) * Vy
            )
            self.__wheel_vec[1] = Driving.THROTTLE_0POINT - round(
                (1 / 2) * Vx - (math.sqrt(3) / 2) * Vy
            )
            self.__wheel_vec[2] = Driving.THROTTLE_0POINT - round(-1 * Vx)

            if angle_condition and self.__steering != 0:
                self.__calculate_steering()

    def __calculate_steering(self):
        F_lat = int(abs(self.__wheel_vec[0] - self.__wheel_vec[1]) * 0.866)  # sin(60)
        F_long = int(F_lat * np.sin(self.__steering * np.pi * 0.1666))  # tan(30)
        self.__wheel_vec[2] = (
            Driving.THROTTLE_0POINT
            + round(
                0.01 * F_long * (self.__max_value - self.__steering_offset)
                + np.sign(self.__steering) * self.__steering_offset
            )
            if self.__steering != 0
            else Driving.THROTTLE_0POINT
        )

    def __transfer(self):
        self.__ican.write(
            Driving.ID_DRIVING, [self.WHEEL_POS_ALL] + self.__wheel_vec, False
        )

    def move(self, angle, throttle=None):
        if throttle is not None:
            self.__throttle = throttle

        self.__angle = angle
        self.__spin = None

        self.__calculate_omni_wheel()
        self.__transfer()

    def spinRight(self, throttle=None):
        if throttle is not None:
            self.__throttle = throttle

        self.__spin = self.SPIN_RIGHT

        self.__calculate_omni_wheel()
        self.__transfer()

    def spinLeft(self, throttle=None):
        if throttle is not None:
            self.__throttle = throttle

        self.__spin = self.SPIN_LEFT

        self.__calculate_omni_wheel()
        self.__transfer()

    def stop(self):
        self.__wheel_vec = [
            self.THROTTLE_0POINT,
            self.THROTTLE_0POINT,
            self.THROTTLE_0POINT,
        ]
        self.__transfer()

    @property
    def throttle(self):
        return self.__throttle

    @throttle.setter
    def throttle(self, throttle):
        if self.__throttle == throttle:
            return

        self.__throttle = throttle
        self.__calculate_omni_wheel()
        self.__transfer()

    @property
    def steering(self):
        return self.__steering

    @steering.setter
    def steering(self, steering):
        class ConditionError(Exception):
            def __init__(self, message):
                print(
                    f"{message} Hint: Steering can only be set during straight-forward movement."
                )
                super().__init__(message)

        if (self.__spin is not None) or ((self.__angle % 180) != 0):
            raise ConditionError("[Errno 18] Cannot set steering!")

        self.__steering = steering
        self.__calculate_steering()
        self.__transfer()

    def forward(self, throttle=None):
        self.move(0, throttle)

    def backward(self, throttle=None):
        self.move(180, throttle)
