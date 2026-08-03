import random 

from solvers.BaseSolver import BaseSolver
from grade import Grade

class SemiRandomSolver(BaseSolver):
    def __init__(self, word_list):
        self.name = "RandomSolver"
        self.initial_word_list = word_list
        self.word_list = word_list
        
    def reset(self):
        self.word_list = self.initial_word_list
    
    def choose_word(self, history):
        if not history:
            return random.choice(self.word_list)
        
        new_list = []
        
        for existing_word in self.word_list:
            add = True
            
            for word, result in history:
                for i in range(5):
                    letter = word[i]
                    g = result[i]
                    
                    if ((g == Grade.Correct and existing_word[i] != letter)
                        or (g == Grade.Wrong_Pos and letter not in existing_word)
                        or (g == Grade.Incorrect and letter in existing_word)
                    ):
                        add = False
                
                if not add:
                    break
            
            if add:
                new_list.append(existing_word)
                
        if not new_list:
            return random.choice(self.word_list)
        return random.choice(new_list)