# coding: utf-8

class StepInput:
    def __init__(self, env, program, arguments):
        self.env = env
        self.program = program
        self.arguments = arguments

    def __str__(self):
        env_decode = []
        for i in range(len(self.env)):
            env_decode.append(self.env[i].argmax()-1)
        return "<StepInput: env=%s pg=%s arg=%s>" % (env_decode, self.program, self.arguments)


class StepOutput:
    def __init__(self, r, program, arguments):
        self.r = r
        self.program = program
        self.arguments = arguments

    def __str__(self):
        return "<StepOutput: r=%s pg=%s arg=%s>" % (self.r, self.program, self.arguments)


class StepInOut:
    def __init__(self, input, output):
        self.input = input
        self.output = output