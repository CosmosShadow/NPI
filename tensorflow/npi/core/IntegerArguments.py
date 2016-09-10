# coding: utf-8
import numpy as np

# 参数: arg_num * arg_depth
class IntegerArguments:
	def __init__(self, arg_num, arg_depth, args=None, values=None):
		self.max_arg_num = arg_num
		self.depth = arg_depth
		self.size_of_arguments = self.max_arg_num * self.depth
		# 
		if values is not None:
			self.values = values.reshape((self.max_arg_num, self.depth))
		else:
			self.values = np.zeros((self.max_arg_num, self.depth), dtype=np.float32)
		if args:
			for i, v in enumerate(args):
				self.update_to(i, v)

	def copy(self):
		obj = IntegerArguments(self.max_arg_num, self.depth)
		obj.values = np.copy(self.values)
		return obj

	def decode_all(self):
		return [self.decode_at(i) for i in range(len(self.values))]

	def decode_at(self, index):
		return self.values[index].argmax()

	# 第index位参数设置成integer大小(one-hot)
	def update_to(self, index, integer):
		self.values[index] = 0
		self.values[index, int(np.clip(integer, 0, self.depth-1))] = 1

	def __str__(self):
		return "<IA: %s>" % self.decode_all()













