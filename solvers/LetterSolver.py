import random 

from solvers.BaseSolver import BaseSolver
from grade import Grade

ALPHABET = list("abcdefghijklmnopqrstuvwxyz")

class LetterSolver(BaseSolver):
    def __init__(self, word_list):
        self.name = "LetterSolver"
        self.initial_word_list = word_list
        self.reset()
        
    def reset(self):
        self.word_list = self.initial_word_list
        self.exact = [None, None, None, None, None] # save green letters that must be at this position 
        self.must_include = set() # yellows are in the must_include
        self.forbidden = [set() for _ in range(5)] # yellow and nones tell that the letter cant be at this position
    
    def choose_word(self, history):
        if not history:
            return random.choice(self.word_list)
        
        # gather all information from the newest history
        last_word, last_grades = history[-1]
        
        # get all the letters that need to be in the word
        for i in range(5):
            letter = last_word[i]
            grade = last_grades[i]
            if grade == Grade.Correct or grade == Grade.Wrong_Pos:
                self.must_include.add(letter)
                
        for i in range(5):
            letter = last_word[i]
            grade = last_grades[i]
            match grade:
                case Grade.Correct:
                    self.exact[i] = letter # must be there
                case Grade.Wrong_Pos:
                    self.forbidden[i].add(letter)
                case Grade.Incorrect:
                    if letter in self.must_include: # somewhere else
                        self.forbidden[i].add(letter) # only ban here
                    else:
                        for j in range(5):
                            self.forbidden[j].add(letter) # add everywhere
                    
        # Filter out all elements that are not possible
        self.word_list = [
            word for word in self.word_list
            if self.is_ok(word)
        ]
        
        if not self.word_list:
            return random.choice(self.initial_word_list)
        else:
            return random.choice(self.word_list)
        
    def is_ok(self, word):
        for i in range(5):
            if self.exact[i] is not None and word[i] != self.exact[i]:
                return False
            
        for letter in self.must_include:
            if letter not in word:
                return False
        
        for i in range(5):
            if word[i] in self.forbidden[i]:
                return False
                
        return True