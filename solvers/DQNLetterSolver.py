import gymnasium as gym
import numpy as np
import random

from solvers.BaseSolver import BaseSolver
from grade import Grade
from game import Game

from stable_baselines3 import DQN

Grade_to_Int = {
    Grade.Correct: 0,
    Grade.Wrong_Pos: 1,
    Grade.Incorrect: 2
}

class TrainingEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.game = Game()
        self.action_space = gym.spaces.Discrete(26)
        
        # 780 for history letters
        # 90 for grades
        # 130 for current word
        # -> 1000
        self.observation_space = gym.spaces.Box(low=0.0, high=1.0, shape=(1000,), dtype=np.float32)
        
        self.current_word = []
        
        self.game.reset()
        
    def get_obs(self):
        # fill obs space with -1s
        obs = np.zeros(1000, dtype=np.float32)
        
        for history_index in range(len(self.game.history)):
            word, grades = self.game.history[history_index]
            for pos in range(5):
                letter_idx = ord(word[pos]) - ord('a')
                base_letter_index = (history_index * 5 * 26) + (pos * 26)
                obs[base_letter_index + letter_idx] = 1.0
                
                grade_idx = Grade_to_Int[grades[pos]]
                base_grade_index = 780 + (history_index * 5 * 3) + (pos * 3)
                obs[base_grade_index + grade_idx] = 1.0
        
        for i in range(len(self.current_word)):
            letter_idx = ord(self.current_word[i]) - ord('a')
            base_current_index = 870 + (i * 26)
            obs[base_current_index + letter_idx] = 1.0
                
        return obs
        

    def step(self, action: int):
        letter = chr(action + ord('a'))
        self.current_word.append(letter)
        
        # word not yet done
        if len(self.current_word) < 5:
            return self.get_obs(), 0.0, False, False, {}
        
        word = "".join(self.current_word)
        
        if not self.game.valid_word(word):
            # invalid word: punish? or don't do anything
            self.current_word = []
            return self.get_obs(), -10.0, True, False, {"error": "word not ok"}
        
        result, correct = self.game.guess(word)
        self.current_word = []
        
        if correct:
            reward = 100.0      # Huge reward for winning
            terminated = True 
        else:
            # small reward for getting a word at all
            reward = 10.0       
            terminated = self.game.over()
        
        
        # optional rewards based on result
        for grade in result:
            match grade:
                case Grade.Correct:
                    reward += 5.0
                case Grade.Wrong_Pos:
                    reward += 1.0
                case Grade.Incorrect:
                    pass # no reward
        
        truncated = False
        
        return self.get_obs(), reward, terminated, truncated, {}
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.game.reset()
        self.current_word = []
        return self.get_obs(), {}
    

class DQNLetterSolver(BaseSolver):
    def __init__(self, word_list):
        self.name = "DQNLetterSolver"
        self.word_list = word_list
        self.training_env = TrainingEnv()
        
        policy_kwargs = dict(net_arch=[256, 256, 256])
        self.agent = DQN("MlpPolicy", self.training_env, buffer_size=100_000, policy_kwargs=policy_kwargs, verbose=0)
        
    def reset(self):
        pass
    
    def choose_word(self, history):
        current_word = []
        
        for i in range(5):
            obs = self.history_to_obs(history, current_word)
            
            action, _ = self.agent.predict(obs, deterministic=True)
            
            num = int(action)
            letter = chr(num + ord('a'))
            current_word.append(letter)
            
        word = "".join(current_word)
        
        if word not in self.word_list:
            return random.choice(self.word_list)
            
        return word
    
    def history_to_obs(self, history, current_word):
        # fill obs space with 0s
        obs = np.zeros(1000, dtype=np.int32)
        
        for history_index in range(len(history)):
            word, grades = history[history_index]
            for pos in range(5):
                letter_idx = ord(word[pos]) - ord('a')
                base_letter_index = (history_index * 5 * 26) + (pos * 26)
                obs[base_letter_index + letter_idx] = 1.0
                
                grade_idx = Grade_to_Int[grades[pos]]
                base_grade_index = 780 + (history_index * 5 * 3) + (pos * 3)
                obs[base_grade_index + grade_idx] = 1.0
                
        for i in range(len(current_word)):
            letter_idx = ord(current_word[i]) - ord('a')
            base_current_index = 870 + (i * 26)
            obs[base_current_index + letter_idx] = 1.0
            
        return obs
    
    def train(self, timesteps=100):
        self.agent.learn(total_timesteps=timesteps, progress_bar=True)
    
    def save_model(self, filepath="solvers/NNs/dqn_letter_solver"):
        self.agent.save(filepath)
        
    def load_model(self, filepath="solvers/NNs/dqn_letter_solver"):
        self.agent = DQN.load(filepath, env=self.training_env)
        
        
if __name__ == "__main__":
    game = Game()
    solver = DQNLetterSolver(game.valid_words)

    solver.train(timesteps=2_000_000)

    solver.save_model()

    first_guess = solver.choose_word(history=[])
    print(f"First guess: \"{first_guess}\"")