# coding: utf-8
from npi.core.Program import *

class MovePtrProgram(Program):
	output_to_env = True
	PTR_IN1 = 0         #pointer input
	PTR_IN2 = 1         #pointer input
	PTR_CARRY = 2   #pointer carry
	PTR_OUT = 3         #pointer output

	TO_LEFT = 0
	TO_RIGHT = 1

	# 1: 哪一行，2: 左移或者右移
	def do(self, env, args):
		ptr_kind = args.decode_at(0)
		left_or_right = args.decode_at(1)
		env.move_pointer(ptr_kind, left_or_right)