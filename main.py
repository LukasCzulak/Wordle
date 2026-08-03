from dataclasses import dataclass
import random
from rich.progress import Progress

from game import Game
from grade import Grade
from solvers.BaseSolver import BaseSolver
from solvers.RandomSolver import RandomSolver
from solvers.FilterSolver import FilterSolver
from solvers.RemainsSolver import RemainsSolver
    
@dataclass    
class EvaluationResult:
    solver_name: str
    games_played: int
    win_rate: float
    avg_attempts: float
    distribution: dict
    last_history: list
    secret_word: str

def benchmark(solver: BaseSolver, max_attempts: int = 6, num_samples: int | None = None, seed: int | None = None) -> EvaluationResult:
    distribution = {}
    for i in range(1, max_attempts + 1):
        distribution[i] = 0
    distribution['Failed'] = 0
    total_attempts = 0
    
    game = Game()
    
    words_to_test = game.valid_words
    if num_samples is not None and num_samples < len(game.valid_words):
        if seed is not None:
            random.seed(seed)
        words_to_test = random.sample(words_to_test, num_samples)
    
    with Progress() as progress_bar:
        t = progress_bar.add_task("Benchmark running", total=len(words_to_test))
        
        for word in words_to_test:
            game.reset()
            game.secret_word = word
            solver.reset()
            
            progress_bar.advance(t, 1)
            
            while not game.over():
                guessed_word = solver.choose_word(game.history)
                game.guess(guessed_word)
                
            if game.won:
                distribution[game.attempts] += 1
                total_attempts += game.attempts
            else:
                distribution['Failed'] += 1
            
    games_played = len(words_to_test)
    wins = games_played - distribution['Failed']
    win_rate = (wins / games_played) * 100
    last_history = list(game.history)
    last_word = game.secret_word
        
    if wins > 0:
        avg_attempts = total_attempts / wins
    else:
        avg_attempts = 7.0
    
    return EvaluationResult(
        solver.name,
        games_played,
        win_rate,
        avg_attempts,
        distribution,
        last_history,
        last_word
    )
        
game = Game()
solver = RemainsSolver(game.valid_words)

LARGE_TEST = False
if LARGE_TEST:
    result = benchmark(solver)
else: 
    result = benchmark(solver, num_samples=100)

DEBUG = True

GRADE_MAP = {
    Grade.Correct: "🟩",
    Grade.Wrong_Pos: "🟨",
    Grade.Incorrect: "⬛",
}

if DEBUG:
    print(f"Secret word: {result.secret_word}")
    print("guesses:")
    for word, grades in result.last_history:
        tiles = "".join(GRADE_MAP[g] for g in grades)
        print(f"{word}  {tiles}")

print(f"solver \'{result.solver_name}\' achieved following stats:\n")
print(f"total games played: {result.games_played}")
print(f"winrate: {result.win_rate:.5}%")
print(f"average attempts when winning: {result.avg_attempts:.5}")
print(f"distribution:")
print(f"---")
for i in range(1, 7):
    print(f"{i}: {result.distribution[i]}")
print(f"Failed: {result.distribution['Failed']}")
