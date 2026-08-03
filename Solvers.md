## RandomSolver
Simplest Variant: Always chooses a random word without any constraints

Usual Winrate: ~0.05%

## FilterSolver
When choosing a word, first go through the history and filter out those words that are not possible. Then choose randomly from the remaining words.

Usual Winrate: ~60%

## RemainsSolver
Keep 5 alphabets for each position. Then look at most recent result and update the alphabets such that letters are removed if they don't fit.

Usual Winrate: ~20%