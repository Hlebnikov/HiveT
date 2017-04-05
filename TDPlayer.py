from Board import *
from GameParser import GameParser
import copy

class TDAgent(object):

    def __init__(self, model):
        self.color = None
        self.model = model
        self.name = 'TD-Gammon'

    def getMove(self, board):
        """
        Return best action according to self.evaluationFunction,
        with no lookahead.
        """
        v_best = 0
        a_best = None

        all_moves = board.getAllMoves(self.color)
        for a in all_moves:
            board.doMove(a)
            features = GameParser.getFeaturesForState(board)
            v = self.model.get_output(features)
            v = 1. - v if self.color == Color.BLACK else v
            if v > v_best:
                v_best = v
                a_best = a
            board.undoMove(a)
        # print(v_best)
        return a_best
