# coding: utf-8
from npi.core.Screen import *


# 加法器的“环境”
class AdditionEnv:
    def __init__(self, height, width, num_chars):
        self.screen = Screen(height, width)
        self.num_chars = num_chars      #chars的类别数
        self.pointers = [0] * height            #指针位置
        self.reset()

    def reset(self):
        self.screen.fill(0)
        self.pointers = [self.screen.width-1] * self.screen.height  # rightmost

    def get_observation(self):
        value = []
        for row in range(len(self.pointers)):
            value.append(self.to_one_hot(self.screen[row, self.pointers[row]]))
        return np.array(value)  # shape of FIELD_ROW * FIELD_DEPTH

    def to_one_hot(self, ch):
        ret = np.zeros((self.num_chars,), dtype=np.int8)
        if 0 <= ch < self.num_chars:
            ret[ch] = 1
        else:
            raise IndexError("ch must be 0 <= ch < %s, but %s" % (self.num_chars, ch))
        return ret

    def setup_problem(self, num1, num2):
        for i, s in enumerate(reversed("%s" % num1)):
            self.screen[0, -(i+1)] = int(s) + 1     #0~9 -> 1~10
        for i, s in enumerate(reversed("%s" % num2)):
            self.screen[1, -(i+1)] = int(s) + 1

    def move_pointer(self, row, left_or_right):
        if 0 <= row < len(self.pointers):
            self.pointers[row] += 1 if left_or_right == 1 else -1  # LEFT is 0, RIGHT is 1
            self.pointers[row] %= self.screen.width

    def write(self, row, ch):
        if 0 <= row < self.screen.height and 0 <= ch < self.num_chars:
            self.screen[row, self.pointers[row]] = ch

    def get_output(self):
        s = ""
        for ch in self.screen[3]:
            if ch > 0:
                s += "%s" % (ch-1)
        return int(s or "0")