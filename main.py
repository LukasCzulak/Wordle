import random
from enum import Enum

class Grade(Enum):
    Incorrect = 0
    Wrong_Pos = 1
    Correct = 2

def check(guess, secret_word, words):
    if not guess in words:
        return "Incorrect guess", False
    
    remaining = list(secret_word)
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
            
    correct = True            
    if Grade.Incorrect in res or Grade.Wrong_Pos in res:
        correct = False

    return res, correct
        
with open("words.txt") as f:
    words = f.read()

words = words.split('\n')

secret_word = words[random.randint(0, len(words)-1)]

secret_word = "aaaab"
print(secret_word)

for i in range(6): 
    guess = input()
    result, correct = check(guess, secret_word, words)
    print(result)
    if correct:
        break