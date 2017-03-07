from enum import Enum


class Color(Enum):
    WHITE = 0
    BLACK = 1

    def inverse(self):
        if self == Color.WHITE:
            return Color.BLACK
        else:
            return Color.WHITE


class Move:
    def __init__(self, figure, to_coord):
        self.figure = figure
        self.to_coord = to_coord
        self.from_coord = figure.coord

    def print(self):
        print("F: {0} to: {1} from: {2}".format(self.figure.letter, self.to_coord, self.from_coord))

adjacents = [[0, 1],
             [1, 0],
             [1, -1],
             [0, -1],
             [-1, 0],
             [-1, 1]]

class Figure:
    def __init__(self, letter, color):
        if color == Color.WHITE:
            letter = letter.upper()
        self.color = color
        self.letter = letter
        self.coord = None
        self.underBug = None
        self.adjacents = [[0, 1],
                         [1, 0],
                         [1, -1],
                         [0, -1],
                         [-1, 0],
                         [-1, 1]]

    def setBug(self, bug):
        if self.underBug:
            self.underBug.setBug(bug)
        else:
            self.underBug = bug
            bug.coord = self.coord

    def pullOffBug(self):
        t = self
        while t.underBug:
            t = t.underBug
        t.underBug = None

    def printBug(self):
        t = self
        while t.underBug:
            t = t.underBug
        print(t.letter, end="")

    def countBugs(self):
        t = self
        i = 0
        while t.underBug:
            i += 1
            t = t.underBug
        return i

    def getMoves(self, board, onlySets = False):
        out = []
        if self.coord: return out
        if board.figuresOnBoard() == 1:
            for field in board.getBoundary():
                out += [Move(self, field)]
        else:
            boundary = board.getBoundary()
            for field in boundary:
                nearests = self.nearCoords([field[0], field[1]])
                for near in nearests:
                    nearFigure = board.figureAt([near[0], near[1]])
                    if isinstance(nearFigure, Figure) and nearFigure.color != self.color:
                        break
                else:
                    out += [Move(self, field)]
        return out

    def getCoord(self):
        return self.coord

    def nearests(self) -> list:
        if self.coord:
            return self.nearCoords(self.coord)
        else:
            return []

    def nearCoords(self, coords):
        return list(map(lambda x: sumCoords(x, coords), adjacents))

    def canBePullOffFromBoard(self, board):
        if self.coord:
            temp_coord = self.coord
            board.pullOffFigureAt(self.coord)
            if not board.isSolid():
                board.setFigure(self, temp_coord)
                return False
            board.setFigure(self, temp_coord)
        return True

def sumCoords(a, b):
    return [a[0] + b[0], a[1] + b[1]]


class Ant(Figure):
    def __init__(self, color):
        letter = "a"
        super().__init__(letter, color)

    def getMoves(self, board, onlySets = False):
        out = []
        if self.underBug:
            return out

        if self.coord and not onlySets:
            temp_coord = self.coord
            board.pullOffFigureAt(self.coord)
            if not board.isSolid():
                board.setFigure(self, temp_coord)
                return []
            boundary = board.getBoundary()
            board.setFigure(self, temp_coord)

            boundary.remove(self.coord)
            for field in boundary:
                figCount = 0
                neighbours = self.nearCoords(field)
                for neighbour in neighbours:
                    if isinstance(board.figureAt(neighbour), Figure):
                        figCount += 1
                if figCount < 5:
                    to_coord = [field[0], field[1]]
                    out += [Move(self, to_coord)]
        else:
            out += super().getMoves(board)
        return out


class Grasshoper(Figure):
    def __init__(self, color):
        letter = "g"
        super().__init__(letter, color)

    def getMoves(self, board, onlySets = False):
        out = []
        if self.underBug:
            return out

        if not self.canBePullOffFromBoard(board): return []

        nearests = self.nearests()
        if len(nearests) > 0 and not onlySets:
            for field in nearests:
                figure = board.figureAt(field)
                if isinstance(figure, Figure):
                    t_coord = field
                    d = [field[0]-self.coord[0], field[1]-self.coord[1]]
                    while isinstance(board.figureAt(t_coord), Figure):
                        t_coord = [t_coord[0]+d[0], t_coord[1]+d[1]]
                    to_coord = [t_coord[0], t_coord[1]]
                    out += [Move(self, to_coord)]
        else:
            out += super().getMoves(board)
        return out


class Queen(Figure):
    def __init__(self, color):
        letter = "q"
        super().__init__(letter, color)

    def getMoves(self, board, onlySets = False):
        out = []

        if self.underBug:
            return out

        if not self.canBePullOffFromBoard(board):
            return out

        nearests = self.nearests()
        if len(nearests) > 0 and not onlySets:
            for field in nearests:
                if not board.figureAt(field):
                    for f in self.nearCoords(field):
                        if isinstance(board.figureAt(f), Figure) and board.figureAt(f)!=self:
                            to_coord = [field[0], field[1]]
                            out += [Move(self, to_coord)]
                            break
        else:
            out += super().getMoves(board)
        return out

    def isSurrounded(self, board):
        nears = self.nearests()
        c = 0
        for near in nears:
            if isinstance(board.figureAt(near), Figure):
                c += 1
        return c == 6

class Bug(Figure):
    def __init__(self, color):
        letter = "b"
        super().__init__(letter, color)

    def getMoves(self, board, onlySets = False):
        out = []

        if self.underBug:
            return out
        if self.coord and board.figureAt(self.coord) != self:
            nearests = self.nearests()
            for field in nearests:
                to_coord = [field[0], field[1]]
                out += [Move(self, to_coord)]
            return out
        if not self.canBePullOffFromBoard(board):
            return []
        nearests = self.nearests()
        if len(nearests) > 0 and not onlySets:
            for field in nearests:
                for f in self.nearCoords(field):
                    if isinstance(board.figureAt(f), Figure) and board.figureAt(f) != self:
                        to_coord = [field[0], field[1]]
                        out += [Move(self, to_coord)]
                        break
        else:
            out += super().getMoves(board)
        return out


class Spider(Figure):
    def __init__(self, color):
        letter = "s"
        super().__init__(letter, color)

    def getMoves(self, board, onlySets = False):
        out = []
        if self.underBug:
            return out

        if self.coord and not onlySets:
            temp_coord = self.coord
            board.pullOffFigureAt(self.coord)
            if not board.isSolid():
                board.setFigure(self, temp_coord)
                return []

            t_coord = self.clockStep(board, temp_coord)
            board.setFigure(self, temp_coord)
            out += [Move(self, t_coord)]

            board.pullOffFigureAt(temp_coord)
            t_coord2 = self.unclockStep(board, temp_coord)
            board.setFigure(self, temp_coord)

            if t_coord != t_coord2:
                out += [Move(self, t_coord2)]

        else:
            out += super().getMoves(board)

        return out

    def clockStep(self, board, start):
        t_coord = start

        for i in range(3):
            neigbours = self.nearCoords(t_coord)

            if isinstance(board.figureAt(neigbours[0]), Figure):
                for neigbour in reversed(neigbours):
                    if not isinstance(board.figureAt(neigbour), Figure):
                        t_coord = neigbour
                        break
            else:
                for neigbour in neigbours:
                    if isinstance(board.figureAt(neigbour), Figure):
                        t_coord = neigbours[neigbours.index(neigbour) - 1]
                        break
        return t_coord

    def unclockStep(self, board, start):
        t_coord = start

        for i in range(3):
            neigbours = self.nearCoords(t_coord)
            if isinstance(board.figureAt(neigbours[0]), Figure):
                for neigbour in neigbours:
                    if not isinstance(board.figureAt(neigbour), Figure):
                        t_coord = neigbour
                        break
            else:
                for neigbour in reversed(neigbours):
                    if isinstance(board.figureAt(neigbour), Figure):
                        t_coord = neigbours[(neigbours.index(neigbour) + 1) % 6]
                        break
        return t_coord