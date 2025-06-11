from abc import ABC,abstractmethod

class Piece(ABC):
    def __init__(self, color,x,y):
        self.color = color
        self.x = x
        self.y = y

    @staticmethod
    def get_starting_cell():
        pass

    def convert_chess_standard(self): 
        return (self.x,self.y)
    

    
