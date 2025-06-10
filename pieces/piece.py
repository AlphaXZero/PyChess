from abc import ABC,abstractmethod

class Piece(ABC):
    def __init__(self, color):
        self.color=color
    
    @abstractmethod
    def get_deplacements(self,position,exhiquier):
        pass
