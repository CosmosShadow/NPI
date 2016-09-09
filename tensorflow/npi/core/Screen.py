# coding: utf-8
# import numpy as np

# 屏幕(内容): 一定宽高的数据(二维数据)
class Screen:
    data = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.init_screen()

    def init_screen(self):
        self.data = np.zeros([self.height, self.width], dtype=np.int8)

    def fill(self, ch):
        self.data.fill(ch)

    def as_float32(self):
        return self.data.astype(np.float32)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, item):
        return self.data[item]