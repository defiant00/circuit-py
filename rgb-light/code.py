import board
import adafruit_is31fl3741
from adafruit_is31fl3741.adafruit_rgbmatrixqt import Adafruit_RGBMatrixQT
from input import Keyboard
from light import Light

# i2c = board.I2C()
# is31 = Adafruit_RGBMatrixQT(i2c, allocate=adafruit_is31fl3741.PREFER_BUFFER)

# is31.set_led_scaling(0xFF)
# is31.global_current = 0xFF
# is31.enable = True

STEP = 32


class RgbLight:
    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0
        self.light_mod = 2
        self.light_mod_offset = 0

    def update(self):
        # input
        Keyboard.update()

        # r 6 11, g 7 12, b 8 13
        if Keyboard.Keys[6].just_pressed:
            self.r += STEP
            if self.r > 0xFF:
                self.r = 0xFF
        elif Keyboard.Keys[11].just_pressed:
            self.r -= STEP
            if self.r < 0:
                self.r = 0

        if Keyboard.Keys[7].just_pressed:
            self.g += STEP
            if self.g > 0xFF:
                self.g = 0xFF
        elif Keyboard.Keys[12].just_pressed:
            self.g -= STEP
            if self.g < 0:
                self.g = 0

        if Keyboard.Keys[8].just_pressed:
            self.b += STEP
            if self.b > 0xFF:
                self.b = 0xFF
        elif Keyboard.Keys[13].just_pressed:
            self.b -= STEP
            if self.b < 0:
                self.b = 0

        # light mod 5 10
        if Keyboard.Keys[5].just_pressed:
            self.light_mod += 1
        elif Keyboard.Keys[10].just_pressed:
            self.light_mod -= 1
            if self.light_mod < 1:
                self.light_mod = 1
            self.light_mod_offset %= self.light_mod

        # light mod offset 0
        if Keyboard.Keys[0].just_pressed:
            self.light_mod_offset = (self.light_mod_offset + 1) % self.light_mod

    def draw(self):
        pass
        # is31.fill(0)
        # self.light.draw(is31, total)
        # is31.show()


rgbl = RgbLight()

while True:
    rgbl.update()
    rgbl.draw()
