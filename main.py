import random
from enum import Enum

class Grade(Enum):
    Incorrect = 0
    Wrong_Pos = 1
    Correct = 2

def check(guess, secret_word, words):
    if not guess in words:
        return "Incorrect guess"
    
    remaining = list(secret_word)
    res = []
    
    correct = True

    for i in range(5):
        if guess[i] == remaining[i]:
            remaining[i] = '#'
            res.append(Grade.Correct)
        elif guess[i] in remaining:
            remaining[remaining.index(guess[i])] = '#'
            res.append(Grade.Wrong_Pos)
            correct = False
        else:
            res.append(Grade.Incorrect)
            correct = False

    return res, correct
        
with open("words.txt") as f:
    words = f.read()

words = words.split('\n')

secret_word = words[random.randint(0, len(words)-1)]
print(secret_word)

for i in range(6): 
    guess = input()
    result, correct = check(guess, secret_word, words)
    print(result)
    if correct:
        break