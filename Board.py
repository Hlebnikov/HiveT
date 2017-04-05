from Figure import *

w = 25
h = 25


class Board:
    def __init__(self):

        self.whiteQueen = Queen(Color.WHITE)
        self.blackQueen = Queen(Color.BLACK)
        figures = [self.whiteQueen, self.blackQueen]  # 0
        figures += [Ant(Color.WHITE), Ant(Color.WHITE), Ant(Color.WHITE),  # 2
                    Ant(Color.BLACK), Ant(Color.BLACK), Ant(Color.BLACK)]  # 5
        figures += [Grasshoper(Color.WHITE), Grasshoper(Color.WHITE), Grasshoper(Color.WHITE),  # 8
                    Grasshoper(Color.BLACK), Grasshoper(Color.BLACK), Grasshoper(Color.BLACK)] # 11
        figures += [Spider(Color.WHITE), Spider(Color.WHITE),  # 14
                    Spider(Color.BLACK), Spider(Color.BLACK)]  # 16
        figures += [Bug(Color.WHITE), Bug(Color.WHITE),  # 18
                    Bug(Color.BLACK), Bug(Color.BLACK)]  # 20

        self.x0 = w // 2
        self.y0 = h // 2
        self.figures = figures
        self.fields = [[None for x in range(w)] for y in range(h)]
        # self.levelsCount = 0
        for figure in figures:
            if isinstance(figure, Queen):
                if figure.color == Color.WHITE:
                    self.whiteQueen = figure
                else:
                    self.blackQueen = figure

    # def __copy__(self):


    def print(self):
        for j in range(h):
            print(" " * j, repr(j - self.y0).rjust(3), end="")
            for i in range(w):
                print("|", end="")
                figure = self.fields[i][j]
                if isinstance(figure, Figure):
                    if figure.underBug:
                        figure.printBug()
                    else:
                        print(figure.letter, end="")

                    if not figure.coord == [i - self.x0, j - self.y0]:
                        raise Exception("Figure {0} have wrong coord {1}. Expected {2}". format(figure, figure.coord, [i - self.x0, j - self.y0]))
                else:
                    print(" ", end="")
            print("|")

    def setFigure(self, figure, to_coord):
        if to_coord is None: return
        x = self.x0 + to_coord[0]
        y = self.y0 + to_coord[1]
        if isinstance(figure, Bug):
            f = self.figureAt(to_coord)
            if f:
                f.setBug(figure)
                return

        if isinstance(figure, Figure):
            figure.coord = [to_coord[0], to_coord[1]]
        self.fields[x][y] = figure

    def pullOffFigureAt(self, coord):
        if coord is None:
            return

        x = self.x0 + coord[0]
        y = self.y0 + coord[1]
        f = self.fields[x][y]

        if f:
            if f.underBug:
                f.pullOffBug()
                return

            f.coord = None
            self.fields[x][y] = None

    def doMove(self, move):
        try:
            self.pullOffFigureAt(move.from_coord)
        except:
            move.print()
            raise Exception("oops")
        self.setFigure(move.figure, move.to_coord)

    def undoMove(self, move):
        back_move = Move(move.figure, move.from_coord)
        self.doMove(back_move)

    def doMoveFromString(self, string):
        string = string.replace("\n", "")
        splitLine = string.split(" ")
        f = splitLine[0]
        if f == "Q":
            figureClass = Queen
            color = Color.WHITE
        elif f == "q":
            figureClass = Queen
            color = Color.BLACK
        elif f == "A":
            figureClass = Ant
            color = Color.WHITE
        elif f == "a":
            figureClass = Ant
            color = Color.BLACK
        elif f == "S":
            figureClass = Spider
            color = Color.WHITE
        elif f == "s":
            figureClass = Spider
            color = Color.BLACK
        elif f == "G":
            figureClass = Grasshoper
            color = Color.WHITE
        elif f == "g":
            figureClass = Grasshoper
            color = Color.BLACK
        elif f == "B":
            figureClass = Bug
            color = Color.WHITE
        elif f == "b":
            figureClass = Bug
            color = Color.BLACK
        else:
            raise Exception("Unknown figure letter")

        to_coord = [int(splitLine[1]), int(splitLine[2])]

        if splitLine[3] == "N":
            from_coord = None
        else:
            from_coord = [int(splitLine[3]), int(splitLine[4])]

        for figure in self.figures:
            if isinstance(figure, figureClass) and \
                            figure.color == color and \
                            figure.coord == from_coord and \
                            figure.underBug is None:
                concreteFigure = figure
                break
        else:
            raise Exception("Wrong move", string)

        move = Move(concreteFigure, to_coord)
        # print(move)
        self.doMove(move)

    def figureAt(self, coord):
        if coord is None:
            return None
        x = self.x0 + coord[0]
        y = self.y0 + coord[1]
        return self.fields[x][y]

    def getAllMoves(self, color):
        out = []

        onlySets = False
        figsOnBoard = self.figuresOnBoard(color)
        if figsOnBoard < 2 and not self.queenOnBoard(color):
            onlySets = True
        elif figsOnBoard == 2 and not self.queenOnBoard(color):
            if color == Color.WHITE:
                return self.whiteQueen.getMoves(self)
            else:
                return self.blackQueen.getMoves(self)

        for f in self.figures:
            if f.color == color:
                out += f.getMoves(self, onlySets)
        return out

    def getBoundary(self):
        out = []
        for f in self.figures:
            if f.coord:
                nearests = f.nearests()
                for neighbor in nearests:
                    if not self.figureAt([neighbor[0], neighbor[1]]):
                        self.setFigure(1, [neighbor[0], neighbor[1]])
                        out += [[neighbor[0], neighbor[1]]]

        for t in out:
            self.setFigure(None, [t[0], t[1]])

        if len(out) == 0:
            out = [[0, 0]]
        return out

    def isSolid(self):
        # self.print()

        T = []
        i = 0
        rightCount = self.figuresOnBoard()
        for f in self.figures:
            if f.coord:
                T = [f]
                break
        if rightCount > 0:
            if isinstance(T[0], Bug) and self.figureAt(T[0].coord) != T[0]:
                T[0] = self.figureAt(T[0].coord)
        # print("rightCount: {0}".format(rightCount))
        Q = set()
        while len(T) > 0:
            Q.add(T[0])
            # print("step ", i)
            # print("T", T)
            # print("Q", Q)
            f = T[0]
            neighbors = f.nearests()
            for neighbor in neighbors:
                fig = self.figureAt(neighbor)
                if isinstance(fig, Figure) and not (fig in Q):
                    # print("{0} with {1} added".format(fig, fig.coord))
                    T += [fig]
                    Q.add(fig)
            T.pop(0)
            i += 1
            i += f.countBugs()
            # print()
        # print("stoped")
        # print(rightCount, i)
        return rightCount == i

    def isQueenSurrounded(self, color):
        if color == Color.WHITE:
            return self.whiteQueen.isSurrounded(self)
        else:
            return self.blackQueen.isSurrounded(self)

    def queenOnBoard(self, color):
        if color == Color.WHITE:
            return self.whiteQueen.coord is not None
        else:
            return self.blackQueen.coord is not None

    def figuresOnBoard(self, color=None):
        i = 0
        for figure in self.figures:
            if figure.coord:
                if color:
                    if figure.color == color:
                        i += 1
                else:
                    i+=1
        return i