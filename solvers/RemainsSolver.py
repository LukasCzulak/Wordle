import random 

from solvers.BaseSolver import BaseSolver
from grade import Grade


ALPHABET = list("abcdefghijklmnopqrstuvwxyz")

class RemainsSolver(BaseSolver):
    def __init__(self, word_list):
        self.name = "RemainsSolver"
        self.initial_word_list = word_list
        self.word_list = word_list
        
        self.possible_letters = [ALPHABET.copy() for _ in range(5)]
        
    def reset(self):
        self.word_list = self.initial_word_list
        self.possible_letters = [ALPHABET.copy() for _ in range(5)]
    
    def choose_word(self, history):
        if not history:
            return random.choice(self.word_list)
        
        # gather all information from the newest history
        last_word, last_grades = history[-1]
        
        for i in range(5):
            letter = last_word[i]
            grade = last_grades[i]
            
            match grade:
                case Grade.Correct:
                    self.possible_letters[i] = [letter]
                case Grade.Wrong_Pos:
                    self.possible_letters[i].remove(letter)
                case Grade.Incorrect:
                    self.possible_letters[i].remove(letter)
                    
        # Filter out all elements that are not possible
        self.word_list = [
            word for word in self.word_list
            if all(word[i] in self.possible_letters[i] for i in range(5))
        ]
        
        if not self.word_list:
            return random.choice(self.initial_word_list)
        else:
            return random.choice(self.word_list)