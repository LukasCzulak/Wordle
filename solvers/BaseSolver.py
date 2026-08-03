from abc import ABC, abstractmethod
from grade import Grade

class BaseSolver(ABC): 
    @abstractmethod
    def __init__(self, word_list: list[str]):
        self.name = "BaseSolver" # overwrite this
        self.word_list = word_list

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def choose_word(self, history: list[tuple[str, list[Grade]]]) -> str:
        pass