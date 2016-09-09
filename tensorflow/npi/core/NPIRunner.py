# coding: utf-8

class NPIRunner:
    # model: NPIStep
    def __init__(self, model=None, recording=True, max_depth=10, max_step=1000):
        self.model = model              #模型
        self.steps = 0
        self.step_list = []
        self.alpha = 0.5        #return threshold
        self.verbose = True                     #显示详情
        self.recording = recording          #是否记录
        self.max_depth = max_depth  #最大深度
        self.max_step = max_step        #最大长度

    def reset(self):
        self.steps = 0
        self.step_list = []
        self.model.reset()

    # program: Program, arguments: IntegerArguments
    def npi_program_interface(self, env, program, arguments, depth=0):
        if self.max_depth < depth or self.max_step < self.steps:
            raise StopIteration()

        self.model.enter_function()

        result = StepOutput(0, None, None)
        while result.r < self.alpha:
            self.steps += 1
            if self.max_step < self.steps:
                raise StopIteration()

            env_observation = env.get_observation()
            result = self.model.step(env_observation, program, arguments.copy())
            if self.recording:
                self.step_list.append(StepInOut(StepInput(env_observation, program, arguments.copy()), result))
            self.display_information(program, arguments, result, depth)

            if program.output_to_env:
                program.do(env, arguments.copy())
                self.display_env(env)
            else:
                if result.program:  # modify original algorithm
                    self.npi_program_interface(env, result.program, result.arguments, depth=depth+1)

        self.model.exit_function()


