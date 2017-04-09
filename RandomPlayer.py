import random as rand
from Figure import Color

class RandomPlayer:

    def __init__(self):
        self.color = Color.WHITE
        self.name = "Randy"

    def getMove(self, board):
        moves = board.getAllMoves(self.color)
        if len(moves) == 0:
            return None
        random_move = moves[int(rand.random() * len(moves))]
        return random_move
