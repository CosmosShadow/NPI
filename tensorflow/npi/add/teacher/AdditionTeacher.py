# coding: utf-8
import numpy as np

from npi.core.StepInputOutput import *
from npi.core.NPIStep import *
from npi.core.IntegerArguments import *
from npi.add.base.config import *
from npi.add.base.AdditionProgramSet import *


class AdditionTeacher(NPIStep):
    def __init__(self, program_set):
        self.pg_set = program_set
        self.step_queue = None
        self.step_queue_stack = []
        self.sub_program = {}
        self.register_subprogram(program_set.MOVE_PTR, self.pg_primitive)
        self.register_subprogram(program_set.WRITE   , self.pg_primitive)
        self.register_subprogram(program_set.ADD     , self.pg_add)
        self.register_subprogram(program_set.ADD1    , self.pg_add1)
        self.register_subprogram(program_set.CARRY   , self.pg_carry)
        self.register_subprogram(program_set.LSHIFT  , self.pg_lshift)
        self.register_subprogram(program_set.RSHIFT  , self.pg_rshift)

    def reset(self):
        NPIStep.reset(self)
        # super(AdditionTeacher, self).reset()
        self.step_queue_stack = []
        self.step_queue = None

    def register_subprogram(self, pg, method):
        self.sub_program[pg.program_id] = method

    @staticmethod
    def decode_params(env_observation, arguments):
        return env_observation.argmax(axis=1), arguments.decode_all()

    def enter_function(self):
        self.step_queue_stack.append(self.step_queue or [])
        self.step_queue = None

    def exit_function(self):
        self.step_queue = self.step_queue_stack.pop()

    def step(self, env_observation, pg, arguments):
        if not self.step_queue:
            self.step_queue = self.sub_program[pg.program_id](env_observation, arguments)
        if self.step_queue:
            ret = self.convert_for_step_return(self.step_queue[0])
            self.step_queue = self.step_queue[1:]
        else:
            ret = StepOutput(PG_RETURN, None, None)
        return ret

    @staticmethod
    def convert_for_step_return(step_values):
        if len(step_values) == 2:
            return StepOutput(PG_CONTINUE, step_values[0], IntegerArguments(ARG_NUM, ARG_DEPTH, step_values[1]))
        else:
            return StepOutput(step_values[0], step_values[1], IntegerArguments(ARG_NUM, ARG_DEPTH, step_values[2]))

    @staticmethod
    def pg_primitive(env_observation, arguments):
        return None

    def pg_add(self, env_observation, arguments):
        ret = []
        (in1, in2, carry, output), (a1, a2, a3) = self.decode_params(env_observation, arguments)
        if in1 == 0 and in2 == 0 and carry == 0:
            return None
        ret.append((self.pg_set.ADD1, None))
        ret.append((self.pg_set.LSHIFT, None))
        return ret

    def pg_add1(self, env_observation, arguments):
        ret = []
        p = self.pg_set
        (in1, in2, carry, output), (a1, a2, a3) = self.decode_params(env_observation, arguments)
        result = self.sum_ch_list([in1, in2, carry])
        ret.append((p.WRITE, (p.WRITE.WRITE_TO_OUTPUT, result % 10)))
        if result > 9:
            ret.append((p.CARRY, None))
        ret[-1] = (PG_RETURN, ret[-1][0], ret[-1][1])
        return ret

    @staticmethod
    def sum_ch_list(ch_list):
        ret = 0
        for ch in ch_list:
            if ch > 0:
                ret += ch - 1
        return ret

    def pg_carry(self, env_observation, arguments):
        ret = []
        p = self.pg_set
        ret.append((p.MOVE_PTR, (p.MOVE_PTR.PTR_CARRY, p.MOVE_PTR.TO_LEFT)))
        ret.append((p.WRITE, (p.WRITE.WRITE_TO_CARRY, 1)))
        ret.append((PG_RETURN, p.MOVE_PTR, (p.MOVE_PTR.PTR_CARRY, p.MOVE_PTR.TO_RIGHT)))
        return ret

    def pg_lshift(self, env_observation, arguments):
        ret = []
        p = self.pg_set
        ret.append((p.MOVE_PTR, (p.MOVE_PTR.PTR_IN1, p.MOVE_PTR.TO_LEFT)))
        ret.append((p.MOVE_PTR, (p.MOVE_PTR.PTR_IN2, p.MOVE_PTR.TO_LEFT)))
        ret.append((p.MOVE_PTR, (p.MOVE_PTR.PTR_CARRY, p.MOVE_PTR.TO_LEFT)))
        ret.append((PG_RETURN, p.MOVE_PTR, (p.MOVE_PTR.PTR_OUT, p.MOVE_PTR.TO_LEFT)))
        return ret

    def pg_rshift(self, env_observation, arguments):
        ret = []
        p = self.pg_set
        ret.append((p.MOVE_PTR, (p.MOVE_PTR.PTR_IN1, p.MOVE_PTR.TO_RIGHT)))
        ret.append((p.MOVE_PTR, (p.MOVE_PTR.PTR_IN2, p.MOVE_PTR.TO_RIGHT)))
        ret.append((p.MOVE_PTR, (p.MOVE_PTR.PTR_CARRY, p.MOVE_PTR.TO_RIGHT)))
        ret.append((PG_RETURN, p.MOVE_PTR, (p.MOVE_PTR.PTR_OUT, p.MOVE_PTR.TO_RIGHT)))
        return ret