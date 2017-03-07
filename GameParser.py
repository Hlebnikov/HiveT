from Board import *
from Figure import *

# 0 - количество своих фигур на доске
# 1 - количество противника
# 2 - количество заблокированых своих
# 3 - кол-во заблокированных противника
# 4 - кол-во вокруг своей королевы
# 5 - кол-во вокруг чужой королевы
# 6:115 - соседи для каждой своей фигуры
# 116:226 - соседи для каждой чужой фигуры

class GameParser:
    def __init__(self, states, color):
        self.states = states
        self.color = color

    def getFeatures(self):
        features = []
        for state in self.states:
            features += self.getFeaturesForState(state)
        return features

    def getFeaturesForState(self, state):
        features = []
        features += [state.figuresOnBoard(self.color)]
        features += [state.figuresOnBoard(self.color.inverse())]
        features += [self.countOfBlocked(state, self.color)]
        features += [self.countOfBlocked(state, self.color.inverse)]
        features += [self.countNeigboursOfQueen(state, self.color)]
        features += [self.countNeigboursOfQueen(state, self.color.inverse)]
        features += self.getAllNeighblorsCount(state)
        return features

    def countOfBlocked(self, state, color):
        c = 0
        for figure in state.figures:
            if figure.coord and figure.color == color:
                moves = figure.getMoves(state)
                if len(moves) == 0:
                    c += 1
        return c

    def countNeigboursOfQueen(self, state, color):
        c = 0
        if color == Color.WHITE:
            queen = state.whiteQueen
        else:
            queen = state.blackQueen

        for near in queen.nearests():
            if isinstance(state.figureAt(near), Figure):
                c += 1
        return c

    def getNeigboursCount(self, state, figure):
        format = "QAGSBqagsb"
        nearests = figure.nearests()
        res = [0] * 10
        for near in nearests:
            n = state.figureAt(near)
            if n:
                res[format.index(n.letter)] += 1
        return res

    def getAllNeighblorsCount(self, state):
        res = []
        for figure in state.figures:
            res += self.getNeigboursCount(state, figure)

        return res