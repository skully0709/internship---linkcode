from abc import ABC, abstractmethod

class Login(ABC):

    @abstractmethod
    def authentication(self):
        pass