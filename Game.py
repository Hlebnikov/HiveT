from Board import *
from HistorySaver import *
from RandomPlayer import *

import threading
import time

class Game:
    def __init__(self, white_player, black_player):
        self.desk = Board()
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
            # move.print()
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

def playFromFile(file):
    games = 0
    wins = [0, 0]
    with open(file, "r") as f:
        line = f.readline()
        while line:
            board = Board()
            while line != ".\n":
                # print(line)
                board.doMoveFromString(line)
                # board.print()
                line = f.readline()
            games += 1
            if board.isQueenSurrounded(Color.WHITE):
                wins[0] += 1
            else:
                wins[1] += 1
            line = f.readline()
    print("Played games: {0}. White wins: {1}. Black wins: {2}".format(games, wins[0], wins[1]))


if __name__ == "__main__":
    start = time.time()
    # play()

    playFromFile("./saves/games2")
    # t1 = threading.Thread(target=play)
    # t1.start()
    # t1.join()

    # t2 = threading.Thread(target=play)
    # t3 = threading.Thread(target=play)
    # t4 = threading.Thread(target=play)

    # t2.start()
    # t3.start()
    # t4.start()

    # t2.join()
    # t3.join()
    # t4.join()

    end = time.time()

    print("Время: {0}".format(end - start))