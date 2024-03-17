# Install nano-gui and ili93xx driver first
# import mip
# mip.install("github:peterhinch/micropython-nano-gui")
# mip.install("github:peterhinch/micropython-nano-gui/drivers/ili93xx")

from color_setup import ssd
from gui.core.colors import *  # Standard color constants
import os
import time

ssd.fill(0)
ssd.show()

class Life:
    def __init__(self, rows, cols, px_size, offset_y):
        self.rows = rows
        self.cols = cols
        self.iterations = 0
        self.alive = 0
        self.offset_y = offset_y
        self.px_size = px_size
        # init blank array
        start = time.ticks_ms()
        self.arr1 = [[0 for i in range(cols + 2)] for j in range(rows + 2)]
        self.arr2 = [[0 for i in range(cols + 2)] for j in range(rows + 2)]
        end = time.ticks_ms()
        print("time to init blank array:\t" + str(end - start) + " ms")
        # init random
        start = time.ticks_ms()
        for i in range(1, self.rows + 1):
            for j in range(1, self.cols + 1):
                tmp = int.from_bytes(os.urandom(1), "little")
                # 192/256 chance of being 0
                if tmp < 230:
                    self.arr1[i][j] = 0
                else:
                    self.arr1[i][j] = 1
        end = time.ticks_ms()
        print("time to init random array:\t" + str(end - start) + " ms")

    def printarr2(self):
        # print arr2 to console
        start = time.ticks_ms()
        print("arr2")
        for i in range(self.rows):
            for j in range(self.cols):
                if self.arr2[i][j] == 0:
                    print(".", end="")
                else:
                    print("#", end="")
            print()
        end = time.ticks_ms()
        print("time to print to console:\t" + str(end - start) + " ms")

    @micropython.native
    def process_next(self):
        self.iterations += 1
        print("iteration:\t" + str(self.iterations))
        start = time.ticks_ms()

        for i in range(1, self.rows):
            for j in range(1, self.cols):
                n = (
                    self.arr1[i - 1][j - 1]
                    + self.arr1[i - 1][j]
                    + self.arr1[i - 1][j + 1]
                    + self.arr1[i][j - 1]
                    + self.arr1[i][j + 1]
                    + self.arr1[i + 1][j - 1]
                    + self.arr1[i + 1][j]
                    + self.arr1[i + 1][j + 1]
                )
                if (self.arr1[i][j]) == 1 and ((n < 2) or (n > 3)):
                    self.arr2[i][j] = 0
                if (self.arr1[i][j] == 0) and (n == 3):
                    self.arr2[i][j] = 1

        end = time.ticks_ms()
        print("time to process next iteration:\t" + str(end - start) + " ms")

    @micropython.native
    def copy(self):
        # copy back to arr1 and to oled buffer
        start = time.ticks_ms()
        self.arr2 = self.arr1
        self.alive = 0
        ssd.fill(0)
        for i in range(1, self.rows + 1):
            for j in range(1, self.cols + 1):
                if self.arr1[i][j]:
                    ssd.rect(
                        (j - 1) * self.px_size,
                        (i - 1) * self.px_size + self.offset_y,
                        self.px_size,
                        self.px_size,
                        1,
                        True,
                    )
                    self.alive += 1
        end = time.ticks_ms()
        print("time to copy back and to oled buffer:\t" + str(end - start) + " ms")


# "main" function
SIZE = 5
OFFSET_Y = 10
GRID_H = 240 // SIZE
GRID_W = 320 // SIZE
life = Life(GRID_H, GRID_W, SIZE, OFFSET_Y)

while True:
    life.process_next()
    life.copy()
    ssd.text(f"Gen={life.iterations}", 0, 0, RED)
    ssd.text("GAME OF LIFE", 100, 0, YELLOW)
    ssd.text(f"Vivi={life.alive}", 240, 0, BLUE)
    ssd.show()
