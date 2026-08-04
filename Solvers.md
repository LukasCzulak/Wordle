## RandomSolver
Simplest Variant: Always chooses a random word without any constraints

Usual Winrate: ~0.05%


## FilterSolver
When choosing a word, first go through the history and filter out those words that are not possible. Then choose randomly from the remaining words.

Usual Winrate: ~60%


## RemainsSolver
Keep 5 alphabets for each position. Then look at most recent result and update the alphabets such that letters are removed if they don't fit.

Usual Winrate: ~20%


## LetterSolver
Keeps track of letter that
- MUST be at a certain position
- MUST be included
- are forbidden to be used at certain positions
Then filters based on these 3 constraints and pick a random word from the remaining words

Usual Winrate: ~80%


## HeuristicSolver
Uses the same logic as LetterSolver, but now doesn't simply guess a random valid word, but instead use a heuristic to count all remaining letters, then build a ranking system and guess the best word based on this heuristic score, e.g. always guess "aeros" first, since 'a', 'e', 'r', 'o' and 's' appear very often in the initial list. 

Usual Winrate: ~88%


## ImprovedHeuristicSolver
An upgrade to HeuristicSolver: Instead of counting all letters over all words, now count letters for every position, thus making the guesses smarter (starting word now is "pares", since 'a' and 'e' are much more likely to be at the 2nd and 4th position instead of 1st and 2nd as in "aeros")

Usual Winrate: ~90%