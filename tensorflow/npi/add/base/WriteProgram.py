# coding: utf-8
from npi.core.Program import *

# 函数: 写
class WriteProgram(Program):
    output_to_env = True
    WRITE_TO_CARRY = 0
    WRITE_TO_OUTPUT = 1

    # 1: 哪一行(2, 3)，写什么
    def do(self, env, args):
        row = 2 if args.decode_at(0) == self.WRITE_TO_CARRY else 3
        digit = args.decode_at(1)
        env.write(row, digit+1)