from Board import *
from HistorySaver import *
from RandomPlayer import *

import random as rand
import threading
import time

class Game:
    def __init__(self, white_player, black_player):
        self.whiteQueen = Queen(Color.WHITE)
        self.blackQueen = Queen(Color.BLACK)
        figures = [self.whiteQueen, self.blackQueen]
        figures += [Ant(Color.WHITE), Ant(Color.WHITE), Ant(Color.WHITE),
                    Ant(Color.BLACK), Ant(Color.BLACK), Ant(Color.BLACK)]
        figures += [Grasshoper(Color.WHITE), Grasshoper(Color.WHITE), Grasshoper(Color.WHITE),
                    Grasshoper(Color.BLACK), Grasshoper(Color.BLACK), Grasshoper(Color.BLACK)]
        figures += [Spider(Color.WHITE), Spider(Color.WHITE),
                    Spider(Color.BLACK), Spider(Color.BLACK)]
        figures += [Bug(Color.WHITE), Bug(Color.WHITE),
                    Bug(Color.BLACK), Bug(Color.BLACK)]
        self.desk = Board(figures)
        self.winner = None
        self.steps = 0
        white_player.color = Color.WHITE
        black_player.color = Color.BLACK
        self.players = [white_player, black_player]
        self.history = []

    def start(self):
        curColor = Color.BLACK
        self.steps = 1
        while not self.gameOver():
            curColor = Color.WHITE if curColor == Color.BLACK else Color.BLACK

            move = self.players[curColor.value].getMove(self.desk)
            move.print()
            self.desk.doMove(move)
            self.history += [move]
            self.steps += 1

            # self.desk.print()

            if not self.desk.isSolid():
                # self.desk.print()
                # print(self.desk.figuresOnBoard())
                raise Exception("Hive not solid!")

            if self.steps > 200:
                raise Exception("Слишком долго")
        print("Ходов", self.steps, end=" ")

        if self.desk.isQueenSurrounded(Color.WHITE):
            self.winner = Color.BLACK
        else:
            self.winner = Color.WHITE

    def printHistory(self):
        for move in self.history:
            move.print()

    def gameOver(self):
        return self.desk.isQueenSurrounded(Color.WHITE) or self.desk.isQueenSurrounded(Color.BLACK)


def play():
    success=0
    saver = HistorySaver()
    while success < 1:
        white_player = RandomPlayer()
        black_player = RandomPlayer()
        game = Game(white_player, black_player)
        try:
            game.start()
            print("Победитель:{0}".format(game.winner.name))
            # saver.saveHistoryToFile(game.history, "games2")
            success += 1
        except Exception as e:
            print(str(e))
            pass


if __name__ == "__main__":
    start = time.time()
    # play()


    t1 = threading.Thread(target=play)
    t2 = threading.Thread(target=play)
    t3 = threading.Thread(target=play)
    t4 = threading.Thread(target=play)

    t1.start()
    # t2.start()
    # t3.start()
    # t4.start()

    t1.join()
    # t2.join()
    # t3.join()
    # t4.join()

    end = time.time()

    print("Время: {0}".format(end - start))