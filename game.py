from grade import Grade 
import random 

def check(guess: str, target: str) -> tuple[list[Grade], bool]:
    remaining = list(target)
    res = [Grade.Incorrect] * 5
    
    for i in range(5):
        if guess[i] == remaining[i]:
            remaining[i] = '#'
            res[i] = Grade.Correct

    for i in range(5):
        if res[i] == Grade.Correct:
            continue
        if guess[i] in remaining:
            remaining[remaining.index(guess[i])] = '#'
            res[i] = Grade.Wrong_Pos
            
    
    won = False
    if not (Grade.Wrong_Pos in res or Grade.Incorrect in res):
        won = True

    return res, won#

  
class Game:
    def __init__(self, filename: str = "words.txt", max_attempts: int = 6):
        self.valid_words = self.parse_input(filename)
        self.secret_word = self.select_secret_word()
        self.max_attempts = max_attempts
        self.attempts = 0
        self.history: list[tuple[str, list[Grade]]] = []
        self.won = False
        
        
    def parse_input(self, filename: str) -> tuple[str, list[str]]:
        with open(filename) as f:
            words = f.read()

        return words.split('\n')
    
    
    def select_secret_word(self):
        secret_word = self.valid_words[random.randint(0, len(self.valid_words)-1)]
        return secret_word
        
        
    def guess(self, word: str) -> tuple[list[Grade], bool]:
        if not word in self.valid_words:
            print("\'word\' is not a valid word!")
            return 

        self.attempts += 1
        result, self.won = check(word, self.secret_word)
        self.history.append((word, result))
            
        return result, self.won
    
    
    def over(self) -> bool:
        return self.won or self.attempts >= self.max_attempts
    
    
    def reset(self):
        self.secret_word = self.select_secret_word()
        self.attempts = 0
        self.history = []
        self.won = False
        