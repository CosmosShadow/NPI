# coding: utf-8

import numpy as np
from random import random
from copy import copy

from npi.core.NPIRunner import *
from npi.core.IntegerArguments import *

from npi.add.base.config import *
from npi.add.base.AdditionProgramSet import *
from npi.add.base.AdditionEnv import *
from npi.add.teacher.AdditionTeacher import *



def create_char_map():
    char_map = dict((i+1, "%s" % i) for i in range(10))
    char_map[0] = ' '
    return char_map

def create_questions(num=100, max_number=10000):
    questions = []
    for in1 in range(10):
        for in2 in range(10):
            questions.append(dict(in1=in1, in2=in2))

    # TODO: comment
    return questions

    for _ in range(100):
        questions.append(dict(in1=int(random() * 100), in2=int(random() * 100)))

    for _ in range(100):
        questions.append(dict(in1=int(random() * 1000), in2=int(random() * 1000)))

    questions += [
        dict(in1=104, in2=902),
    ]

    questions += create_random_questions(num=num, max_number=max_number)
    return questions


def create_random_questions(num=100, max_number=10000):
    questions = []
    for _ in range(num):
        questions.append(dict(in1=int(random() * max_number), in2=int(random() * max_number)))
    return questions


def create_train_data():
    program_set = AdditionProgramSet()
    addition_env = AdditionEnv(FIELD_ROW, FIELD_WIDTH, FIELD_DEPTH)
    num = 10
    questions = create_questions(num)
    teacher = AdditionTeacher(program_set)
    npi_runner = NPIRunner(teacher, recording=True)
    npi_runner.verbose = True
    steps_list = []
    for data in questions:
        addition_env.reset()
        q = copy(data)
        run_npi(addition_env, npi_runner, program_set.ADD, data)
        steps_list.append({"q": q, "steps": npi_runner.step_list})

    return steps_list

def create_one_train_data(input1, input2):
    data = dict(in1=input1, in2=input2)
    q = copy(data)
    
    program_set = AdditionProgramSet()
    addition_env = AdditionEnv(FIELD_ROW, FIELD_WIDTH, FIELD_DEPTH)
    teacher = AdditionTeacher(program_set)
    npi_runner = NPIRunner(teacher, recording=True)
    npi_runner.verbose = True
    addition_env.reset()
    run_npi(addition_env, npi_runner, program_set.ADD, data)

    step_list = {"q": q, "steps": npi_runner.step_list}

    return step_list


def run_npi(addition_env, npi_runner, program, data):
    data['expect'] = data['in1'] + data['in2']

    addition_env.setup_problem(data['in1'], data['in2'])

    npi_runner.reset()
    npi_runner.npi_program_interface(addition_env, program, IntegerArguments(ARG_NUM, ARG_DEPTH))

    data['result'] = addition_env.get_output()
    data['correct'] = data['result'] == data['expect']


if __name__ == '__main__':
    step_list = create_one_train_data(12, 34)
    print step_list
    print step_list['q']
    print step_list['steps'][0].input
    print step_list['steps'][0].output
    print step_list['steps'][1]
