from solvers.BaseSolver import BaseSolver
from grade import Grade

ALPHABET = list("abcdefghijklmnopqrstuvwxyz")

class HeuristicSolver(BaseSolver):
    def __init__(self, word_list):
        self.name = "HeuristicSolver"
        self.initial_word_list = word_list
        self.reset()
        
    def reset(self):
        self.word_list = self.initial_word_list
        self.exact = [None, None, None, None, None] # save green letters that must be at this position 
        self.must_include = set() # yellows are in the must_include
        self.forbidden = [set() for _ in range(5)] # yellow and nones tell that the letter cant be at this position
    
    def choose_word(self, history):
        if not history:
            return self.get_best_word()
        
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
        
        return self.get_best_word()
        
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
    
    def score(self, word: str, ranks: dict):
        sum = 0
        used_letters = []
        for letter in word:
            if letter not in used_letters:
                sum += ranks[letter]
                used_letters.append(letter)
        return sum
    
    def get_best_word(self):
        # build dictionary and count letters in the remaining word list
        letter_counts = {}
        for letter in ALPHABET:
            letter_counts[letter] = 0
        for word in self.word_list:
            for letter in list(word):
                letter_counts[letter] += 1
                
        # Sort based on the counts
        sorted = []
        for letter, count in letter_counts.items():
            sorted.append((count, letter))
        
        sorted.sort(reverse=True)
        
        # sorted is now a list like this: [(1000, 'e'), (900, 'n'), (880, 'r'), ...]
        
        # now build dict for the scores
        
        placements = {}
        for i in range(len(sorted)):
            _, letter = sorted[i]
            placements[letter] = 26 - i # give a reverse rank, such that the first element gets the highest score
            
        # now sort self.word_list based on these ranks
        self.word_list.sort(key=lambda word: self.score(word, placements), reverse=True)
        
        return self.word_list[0]
        