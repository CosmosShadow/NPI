# coding: utf-8

class NPIStep:
    def reset(self):
        pass

    def enter_function(self):
        pass

    def exit_function(self):
        pass

    def step(self, env_observation, pg, arguments):
        raise NotImplementedError()