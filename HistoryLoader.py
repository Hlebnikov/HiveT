import Figure
from Board import Board

class HistoryLoader:

    def loadGameFromFile(self, file):
        board = Board()

        with open(file, "r") as f:
             m = f.readline()
             while not m == ".\n":
                m = m.replace("\n", "")
                print(m)
                splitline = m.split(" ")
                print(splitline)
                m = f.readline()

hl = HistoryLoader()
hl.loadGameFromFile("hist")