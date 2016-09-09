# coding: utf-8

# enviroment
FIELD_ROW = 4     # Input1, Input2, Carry, Output
FIELD_WIDTH = 9   # number of columns
FIELD_DEPTH = 11  # number of characters(0~9 digits) and white space, per cell. one-hot-encoding

# program coding
PROGRAM_VEC_SIZE = 10
PROGRAM_KEY_VEC_SIZE = 5
MAX_PROGRAM_NUM = 10

# arguments coding
MAX_ARG_NUM = 3
ARG_DEPTH = 10   # 0~9 digit. one-hot.

# program continure, program return?
PG_CONTINUE = 0
PG_RETURN = 1