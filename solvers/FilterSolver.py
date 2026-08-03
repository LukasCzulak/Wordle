import random 

from solvers.BaseSolver import BaseSolver
from grade import Grade

class FilterSolver(BaseSolver):
    def __init__(self, word_list):
        self.name = "FilterSolver"
        self.initial_word_list = word_list
        self.word_list = word_list
        self.letters_in_word: set = set({})
        self.guessed_words: set = set({})
        
    def reset(self):
        self.word_list = self.initial_word_list
        self.letters_in_word = set({})
        self.guessed_words = set({})
    
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
                    
                    match g:
                        case Grade.Correct:
                            self.letters_in_word.add(letter)
                            if existing_word[i] != letter:
                                add = False
                        case Grade.Wrong_Pos:
                            self.letters_in_word.add(letter)
                            if letter not in existing_word:
                                add = False
                        case Grade.Incorrect:
                            if (letter in existing_word) and (letter not in self.letters_in_word):
                                add = False
                
                if not add:
                    break
            
            if add and not existing_word in self.guessed_words:
                new_list.append(existing_word)
                
        self.word_list = new_list
        
        if not self.word_list:
            chosen_word = random.choice(self.initial_word_list)
        else:
            chosen_word = random.choice(self.word_list)
        
        self.guessed_words.add(chosen_word)
        
        return chosen_word