# coding: utf-8
from npi.core.Program import *
from npi.add.base.MovePtrProgram import *
from npi.add.base.WriteProgram import *


# 函数集
class AdditionProgramSet:
    NOP = Program('NOP')
    MOVE_PTR = MovePtrProgram('MOVE_PTR', 4, 2)  # PTR_KIND(4), LEFT_OR_RIGHT(2)
    WRITE = WriteProgram('WRITE', 2, 10)       # CARRY_OR_OUT(2), DIGITS(10)
    ADD = Program('ADD')
    ADD1 = Program('ADD1')
    CARRY = Program('CARRY')
    LSHIFT = Program('LSHIFT')
    RSHIFT = Program('RSHIFT')

    def __init__(self):
        self.map = {}
        self.program_id = 0
        self.register(self.NOP)
        self.register(self.MOVE_PTR)
        self.register(self.WRITE)
        self.register(self.ADD)
        self.register(self.ADD1)
        self.register(self.CARRY)
        self.register(self.LSHIFT)
        self.register(self.RSHIFT)

    def register(self, pg):
        pg.program_id = self.program_id
        self.map[pg.program_id] = pg
        self.program_id += 1

    def get(self, i):
        return self.map.get(i)