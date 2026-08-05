import gymnasium as gym

from solvers.BaseSolver import BaseSolver
from grade import Grade

class TrainingEnv(gym.Env):
    def __init__(self):
        pass

    def step():
        pass
    
    def reset():
        pass
    

class DQNWordSolver(BaseSolver):
    def __init__(self, word_list):
        self.name = "DQNWordSolver"
        self.initial_word_list = word_list
        self.reset()
        
    def reset(self):
        pass
    
    def choose_word(self, history):
        pass