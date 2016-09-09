# coding: utf-8
import numpy as np

def to_one_hot_array(idx, size, dtype=np.int8):
    ret = np.zeros((size, ), dtype=dtype)
    ret[idx] = 1
    return ret

if __name__ == '__main__':
	A = to_one_hot_array(2, 5)
	print A