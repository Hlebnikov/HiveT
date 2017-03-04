from Figure import *
from Board import *

import random as rand


class Game:
    def __init__(self):
        self.whiteQueen = Queen(Color.WHITE)
        self.blackQueen = Queen(Color.BLACK)
        figures = [self.whiteQueen, self.blackQueen]
        figures += [Ant(Color.WHITE), Ant(Color.WHITE), Ant(Color.WHITE),
                    Ant(Color.BLACK), Ant(Color.BLACK), Ant(Color.BLACK)]
        # figures += [Grasshoper(Color.WHITE), Grasshoper(Color.WHITE), Grasshoper(Color.WHITE),
        #             Grasshoper(Color.BLACK), Grasshoper(Color.BLACK), Grasshoper(Color.BLACK)]
        # figures += [Spider(Color.WHITE), Spider(Color.WHITE),
        #             Spider(Color.BLACK), Spider(Color.BLACK)]
        figures += [Bug(Color.WHITE), Bug(Color.WHITE),
                    Bug(Color.BLACK), Bug(Color.BLACK)]
        self.desk = Board(figures)
        self.winner = None
        self.steps = 0

    def start(self):
        curColor = Color.BLACK
        self.steps = 1

        moves = []
        while not self.gameOver():
            curColor = Color.WHITE if curColor == Color.BLACK else Color.BLACK

            try:
                moves = self.desk.getAllMoves(curColor)
            except IndexError:
                raise Exception("Выход за пределы")
            # print("{0} ход:".format(self.steps))
            if len(moves) == 0: continue
            # print(len(moves))
            # for move in moves:
            #     move.print()
            randMove = moves[int(rand.random() * len(moves))]
            randMove.print()
            self.desk.doMove(randMove)
            self.steps += 1

            # self.desk.print()

            if not self.desk.isSolid():
                self.desk.print()
                print(self.desk.figuresOnBoard())
                raise Exception("Hive not solid!")

            if self.steps > 200:
                raise Exception("Слишком долго")
        print("Ходов ", self.steps, end=" ")

        if self.desk.isQueenSurrounded(Color.WHITE):
            self.winner = Color.BLACK
        else:
            self.winner = Color.WHITE

    def gameOver(self):
        return self.desk.isQueenSurrounded(Color.WHITE) or self.desk.isQueenSurrounded(Color.BLACK)


if __name__ == "__main__":
    # loss = 0
    game = Game()
    try:
        game.start()
        print("Winner: {0}".format(game.winner))
    except Exception as e:
        print(str(e))
        # loss += 1
    # print("Неудачных ", i)
