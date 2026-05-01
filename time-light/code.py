import time
import board
import adafruit_is31fl3741
from adafruit_is31fl3741.adafruit_rgbmatrixqt import Adafruit_RGBMatrixQT
from input import Keyboard
from light import Light

i2c = board.I2C()
is31 = Adafruit_RGBMatrixQT(i2c, allocate=adafruit_is31fl3741.PREFER_BUFFER)

is31.set_led_scaling(0xFF)
is31.global_current = 0xFF
is31.enable = True

SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = SECONDS_IN_MINUTE * 60
SECONDS_IN_DAY = SECONDS_IN_HOUR * 24

c_hour = 0x000001
c_minute = 0x000100
c_second = 0x010100


class TimeLight:
    def __init__(self):
        self.light = Light()
        self.start = time.time()
        self.current = self.start
        self.hour = 0
        self.minute = 0
        self.prior_total = -1

    def update(self):
        # input
        Keyboard.update()
        if Keyboard.Keys[5].just_pressed:
            self.start += SECONDS_IN_HOUR
        elif Keyboard.Keys[6].just_pressed:
            self.start -= SECONDS_IN_HOUR
        elif Keyboard.Keys[7].just_pressed:
            self.start += SECONDS_IN_MINUTE
        elif Keyboard.Keys[8].just_pressed:
            self.start -= SECONDS_IN_MINUTE

        # time
        self.current = time.time()
        while self.start > self.current:
            self.start -= SECONDS_IN_DAY

        # hour and minute
        in_day = (self.current - self.start) % SECONDS_IN_DAY
        self.hour = in_day // SECONDS_IN_HOUR
        self.minute = (in_day - (self.hour * SECONDS_IN_HOUR)) // SECONDS_IN_MINUTE

    def draw(self):
        total = self.hour * 60 + self.minute
        if total == self.prior_total:
            self.draw_time()
        else:
            self.prior_total = total
            is31.fill(0)
            self.draw_time()
            self.light.draw(is31, total)
        is31.show()

    def draw_time(self):
        # hour in binary
        is31.pixel(0, 0, c_hour if self.hour & 16 else 0)
        is31.pixel(1, 0, c_hour if self.hour & 8 else 0)
        is31.pixel(2, 0, c_hour if self.hour & 4 else 0)
        is31.pixel(3, 0, c_hour if self.hour & 2 else 0)
        is31.pixel(4, 0, c_hour if self.hour & 1 else 0)

        # minute in binary
        is31.pixel(6, 0, c_minute if self.minute & 32 else 0)
        is31.pixel(7, 0, c_minute if self.minute & 16 else 0)
        is31.pixel(8, 0, c_minute if self.minute & 8 else 0)
        is31.pixel(9, 0, c_minute if self.minute & 4 else 0)
        is31.pixel(10, 0, c_minute if self.minute & 2 else 0)
        is31.pixel(11, 0, c_minute if self.minute & 1 else 0)

        # second blinker
        is31.pixel(12, 0, c_second if self.current & 1 else 0)


tl = TimeLight()

while True:
    tl.update()
    tl.draw()
