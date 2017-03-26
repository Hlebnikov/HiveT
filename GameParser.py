from Board import *
from Figure import *

import numpy as np
# 0 - количество своих фигур на доске
# 1 - количество противника
# 2 - количество заблокированых своих
# 3 - кол-во заблокированных противника
# 4 - кол-во вокруг своей королевы
# 5 - кол-во вокруг чужой королевы
# 6:115 - соседи для каждой своей фигуры
# 116:226 - соседи для каждой чужой фигуры

class GameParser:
    # def __init__(self, states, color):
    #     self.states = states
    #     self.color = color

    @classmethod
    def getFeatures(clr, states):
        features = []
        for state in states:
            features += GameParser.getFeaturesForState(state)
        return np.array(features).reshape(1, -1)

    @classmethod
    def getFeaturesForState(cls, state):
        features = []
        color = Color.WHITE
        features += [state.figuresOnBoard(color)/11]
        features += [state.figuresOnBoard(color.inverse())/11]
        features += [countOfBlocked(state, color)/11]
        features += [countOfBlocked(state, color.inverse)/11]
        features += [countNeigboursOfQueen(state, color)/6]
        features += [countNeigboursOfQueen(state, color.inverse)/6]
        features += getAllNeighblorsCount(state).tolist()
        return np.array(features).reshape(1,-1)


def countOfBlocked(state, color):
    c = 0
    for figure in state.figures:
        if figure.coord and figure.color == color:
            moves = figure.getMoves(state)
            if len(moves) == 0:
                c += 1
    return c


def countNeigboursOfQueen(state, color):
    c = 0
    if color == Color.WHITE:
        queen = state.whiteQueen
    else:
        queen = state.blackQueen

    for near in queen.nearests():
        if isinstance(state.figureAt(near), Figure):
            c += 1
    return c


def getNeigboursCount(state, figure):
    format = "QAGSBqagsb"
    total = np.array([1, 1, 3, 3, 2, 2, 1, 3, 3, 2, 2])
    nearests = figure.nearests()
    res = np.array([0.] * 11)
    for near in nearests:
        n = state.figureAt(near)
        if n:
            i = format.index(n.letter)
            res[i+1] += 1
    res /= total
    if len(nearests) > 0:
        res[0] = 1
    return res


def getAllNeighblorsCount(state):
    res = np.array([])
    for figure in state.figures:
        res = np.append(res, getNeigboursCount(state, figure))
    return res
