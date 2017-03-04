from Figure import *

class HistorySaver:

    def saveHistoryToFile(self, history, file_name):
        with open("./saves/"+file_name, 'w') as f:
            for move in history:
                f.write(self.stringFromMove(move))
            f.write(".\n")

    @staticmethod
    def stringFromMove(move):
        to = str(move.to_coord[0]) + " " + str(move.to_coord[1])
        fr = str(move.from_coord[0]) + " " + str(move.from_coord[1]) if move.from_coord else "N"
        return move.figure.letter + " " + to + " " + fr + "\n"