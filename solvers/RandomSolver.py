import random 

from solvers.BaseSolver import BaseSolver

class RandomSolver(BaseSolver):
    def __init__(self, word_list):
        self.name = "RandomSolver"
        self.word_list = word_list
        
    def reset(self):
        pass
    
    def choose_word(self, history):
        return self.word_list[random.randint(0, len(self.word_list)-1)]
    