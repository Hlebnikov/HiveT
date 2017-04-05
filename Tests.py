import unittest
from Figure import *
from Board import *
from GameParser import *
import random as rand
from GameParser import *

class TestFigureMethods(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.whiteQueen = self.board.whiteQueen
        self.blackQueen = self.board.blackQueen

    def test_nearests2(self):
        self.board.setFigure(self.board.figures[0], [2, 3])
        expected = [[2, 4], [3, 3], [3, 2], [2, 2], [1, 3], [1, 4]]
        self.assertEqual(self.board.figures[0].nearests(), expected)

    def test_getBoundary(self):
        self.assertTrue(self.board.getBoundary() == [[0, 0]])
        self.board.setFigure(self.board.figures[0], [0, 0])
        self.board.setFigure(self.board.figures[1], [0, 1])
        self.board.setFigure(self.board.figures[18], [0, 1])
        self.assertCountEqual(self.board.getBoundary(), [[-1, 2], [0, 2], [1, 1], [1, 0], [1, -1], [0, -1], [-1, 0], [-1, 1]])


    def test_noSolid(self):
        self.board.setFigure(self.board.figures[0], [0, 0])
        self.board.setFigure(self.board.figures[1], [0, 1])
        self.board.setFigure(self.board.figures[2], [-1, 0])
        self.board.setFigure(self.board.figures[18], [-1, 0])

        self.board.setFigure(self.board.figures[3], [3, 3])
        self.board.setFigure(self.board.figures[4], [3, 2])
        self.assertFalse(self.board.isSolid())



    def test_solid(self):
        self.assertTrue(self.board.isSolid())
        self.board.setFigure(self.board.figures[0], [0, 0])
        self.board.setFigure(self.board.figures[1], [-1, 0])
        self.board.setFigure(self.board.figures[2], [1, -1])
        self.board.setFigure(self.board.figures[3], [-2, 1])
        self.board.setFigure(self.board.figures[4], [-3, 2])
        self.board.setFigure(self.board.figures[5], [-4, 3])
        self.board.setFigure(self.board.figures[18], [-4, 3])
        # self.board.doMove(Move(self.board.figures[18], [-3, 2]))
        self.assertTrue(self.board.isSolid())

    def test_solid2(self):

        self.board.doMove(Move(self.board.figures[2], [0, 0]))
        self.board.doMove(Move(self.board.figures[5], [1, -1]))
        self.board.doMove(Move(self.board.figures[0], [-1, 0]))
        self.board.doMove(Move(self.board.figures[1], [2, -1]))
        self.board.doMove(Move(self.board.figures[3], [-2, 1]))
        self.board.doMove(Move(self.board.figures[20], [3, -1]))
        self.board.doMove(Move(self.board.figures[3], [1, -2]))
        self.board.doMove(Move(self.board.figures[6], [4, -2]))
        self.board.doMove(Move(self.board.figures[3], [-1, -1]))
        self.board.doMove(Move(self.board.figures[6], [4, -1]))
        self.board.doMove(Move(self.board.figures[18], [-1, -2]))
        self.board.doMove(Move(self.board.figures[6], [3, 0]))
        self.board.doMove(Move(self.board.figures[19], [0, -3]))
        self.board.doMove(Move(self.board.figures[6], [-2, -2]))
        self.board.doMove(Move(self.board.figures[19], [-1, -2]))

        self.assertTrue(self.board.isSolid())


    def test_setAndGetFigure(self):
        self.board.setFigure(self.board.figures[3], [3, 7])
        self.assertEqual(self.board.figures[3], self.board.figureAt([3, 7]))
        self.assertEqual(self.board.figures[3], self.board.fields[self.board.x0 + 3][self.board.x0 + 7])
        self.assertEqual(self.board.figureAt([3, 7]).coord, [3, 7])
        self.board.pullOffFigureAt([3, 7])
        self.assertEqual(self.board.figureAt([3, 7]), None)
        self.assertTrue(self.board.getBoundary() == [[0, 0]])

    def test_figCounter(self):
        self.assertEqual(self.board.figuresOnBoard(), 0)
        self.board.setFigure(self.board.figures[0], [0, 0])
        self.board.setFigure(self.board.figures[1], [0, 1])
        self.board.setFigure(self.board.figures[2], [-1, 0])
        self.board.setFigure(self.board.figures[18], [-1, 0])

        self.assertEqual(self.board.figuresOnBoard(), 4)

    def test_getMoves(self):
        self.board.setFigure(self.board.figures[0], [0, 0])
        self.board.setFigure(self.board.figures[1], [0, 1])
        self.board.setFigure(self.board.figures[2], [0, -1])
        expectedMovesForBlack = [[-1, 2], [0, 2], [1, 1]]
        expectedMovesForWhite = [[-1, 0], [-1, -1], [0, -2], [1, -2], [1, -1]]
        moves = self.board.figures[5].getMoves(self.board)
        blackMoves = []
        for move in moves:
            blackMoves += [move.to_coord]
        self.assertCountEqual(expectedMovesForBlack, blackMoves)



    def test_Queen(self):
        self.board.setFigure(self.whiteQueen, [0, -1])
        self.board.setFigure(self.board.figures[2], [0, 0])
        self.board.setFigure(self.board.figures[3], [-1, 0])
        self.board.setFigure(self.board.figures[4], [-1, -1])
        self.board.setFigure(self.board.figures[5], [0, -2])
        moves = self.whiteQueen.getMoves(self.board)
        toCoordsMoves = []
        for move in moves:
            toCoordsMoves += [move.to_coord]

        self.assertCountEqual(toCoordsMoves, [[1, -1], [1, -2]])

    def test_Queen2(self):
        queen = self.board.figures[0]
        self.board.doMove(Move(queen, [0, 1]))
        self.board.doMove(Move(self.board.figures[1], [0, 0]))

        moves = queen.getMoves(self.board)
        moveCoords = []
        for move in moves:
            moveCoords += [move.to_coord]

        self.assertCountEqual(moveCoords, [[-1, 1], [1, 0]])

    def test_Grasshoper(self):
        self.board.setFigure(self.board.figures[8], [0, -1])
        self.board.setFigure(self.board.figures[2], [0, 0])
        self.board.setFigure(self.board.figures[3], [-1, 0])
        self.board.setFigure(self.board.figures[4], [-1, -1])
        self.board.setFigure(self.board.figures[5], [0, -2])
        moves = self.board.figures[8].getMoves(self.board)
        toCoordsMoves = []
        for move in moves:
            toCoordsMoves += [move.to_coord]

        self.assertCountEqual(toCoordsMoves, [[0, 1], [-2, 1], [-2, -1], [0, -3]])

    def test_Grasshoper2(self):
        grasshoper = Grasshoper(Color.WHITE)
        self.board.setFigure(grasshoper, [0, -1])
        self.board.setFigure(self.board.figures[2], [0, 0])
        self.board.setFigure(self.board.figures[4], [0, 1])
        moves = grasshoper.getMoves(self.board)
        toCoordsMoves = []
        for move in moves:
            toCoordsMoves += [move.to_coord]

        self.assertCountEqual(toCoordsMoves, [[0, 2]])

    def test_Ant(self):
        ant = self.board.figures[2]
        self.board.setFigure(ant, [0, -1])
        self.board.setFigure(self.board.figures[1], [-1, 2])
        self.board.setFigure(self.board.figures[3], [-1, 1])
        self.board.setFigure(self.board.figures[4], [0, 0])
        self.board.setFigure(self.board.figures[5], [1, 0])
        self.board.setFigure(self.board.figures[6], [1, 1])
        moves = ant.getMoves(self.board)
        toCoordsMoves = []
        for move in moves:
            toCoordsMoves += [move.to_coord]

        self.assertCountEqual(toCoordsMoves, [[-1, 0], [-2, 1], [-2, 2], [-2, 3], [-1, 3], [0, 2], [1, 2], [2, 1], [2, 0], [2, -1], [1, -1]])

    def test_Spider(self):
        spider = self.board.figures[14]
        self.board.setFigure(spider, [0, -1])
        self.board.setFigure(self.board.figures[2], [0, 0])
        self.board.setFigure(self.board.figures[3], [1, 0])

        moves = spider.getMoves(self.board)
        toCoordsMoves = []
        for move in moves:
            toCoordsMoves += [move.to_coord]

        self.assertCountEqual(toCoordsMoves, [[0, 1], [2, 0]])

    def test_Spider2(self):
        spider = self.board.figures[14]
        self.board.setFigure(spider, [0, 1])
        self.board.setFigure(self.board.figures[2], [0, 0])
        self.board.setFigure(self.board.figures[3], [1, 0])

        moves = spider.getMoves(self.board)
        toCoordsMoves = []
        for move in moves:
            toCoordsMoves += [move.to_coord]

        self.assertCountEqual(toCoordsMoves, [[0, -1], [2, -1]])

    def test_Queen3(self):
        queen = self.board.figures[0]
        self.board.setFigure(queen, [0, -1])
        self.board.setFigure(self.board.figures[1], [0, 0])
        self.board.setFigure(self.board.figures[3], [1, -1])
        self.board.setFigure(self.board.figures[4], [1, -2])
        self.board.setFigure(self.board.figures[5], [0, -2])
        self.board.setFigure(self.board.figures[6], [-1, -1])
        self.assertFalse(queen.isSurrounded(self.board))

        self.board.setFigure(self.board.figures[7], [-1, 0])
        self.assertTrue(queen.isSurrounded(self.board))

    def test_Bug(self):
        bug1 = Bug(Color.WHITE)
        bug2 = Bug(Color.BLACK)
        self.board.setFigure(self.whiteQueen, [0, 0])
        self.board.setFigure(self.board.figures[4], [0, 1])

        moves = self.toMoveCoords(self.whiteQueen)
        self.assertCountEqual(moves, [[1, 0], [-1, 1]])

        self.board.setFigure(bug1, [0, 0])
        moves = self.toMoveCoords(self.whiteQueen)
        self.assertCountEqual(moves, [])

        self.board.setFigure(bug2, [0, -1])
        moves = self.toMoveCoords(bug1)
        self.assertCountEqual(moves, bug1.nearests())

        self.board.doMove(Move(bug2, [0, 0]))
        moves = self.toMoveCoords(bug1)
        self.assertCountEqual(moves, [])

        moves = self.toMoveCoords(bug2)
        self.assertCountEqual(moves, bug2.nearests())

    def toMoveCoords(self, figure):
        moves = figure.getMoves(self.board)
        toCoordsMoves = []
        for move in moves:
            toCoordsMoves += [move.to_coord]
        return toCoordsMoves

    def test_count(self):
        self.board.setFigure(self.board.figures[1], [0, 0])
        self.board.setFigure(self.board.figures[3], [1, -1])
        self.assertEqual(self.board.figuresOnBoard(), 2)
        self.assertEqual(self.board.figuresOnBoard(Color.WHITE), 1)
        self.assertEqual(self.board.figuresOnBoard(Color.BLACK), 1)

        self.board.setFigure(self.board.figures[4], [1, -2])
        self.board.setFigure(self.board.figures[5], [0, -2])
        self.board.setFigure(self.board.figures[6], [-1, -1])

    def test_Moves(self):
        color = Color.WHITE
        for i in range(100):
            color = Color.WHITE if color == Color.BLACK else color.BLACK
            moves = self.board.getAllMoves(color)
            if not moves:
                break
            randMove = moves[int(rand.random() * len(moves))]
            self.board.doMove(randMove)
            self.assertTrue(self.board.isSolid())
            # self.board.print()

    def test_countBugs(self):
        self.board.setFigure(self.board.figures[4], [1, -2])
        self.board.setFigure(self.board.figures[5], [0, -2])
        self.board.setFigure(self.board.figures[18], [0, -2])
        self.assertEqual(self.board.figuresOnBoard(), 3)
        self.assertTrue(self.board.isSolid())

    def test_countOfBlocks(self):
        whiteAnt = self.board.figures[4]
        blackBug = self.board.figures[20]
        whiteBug = self.board.figures[18]
        whiteGrass = self.board.figures[8]
        self.board.doMove(Move(whiteAnt, [0, 0]))
        self.board.doMove(Move(blackBug, [0, 1]))
        self.board.doMove(Move(whiteBug, [-1, 0]))
        self.board.doMove(Move(blackBug, [0, 0]))
        self.board.doMove(Move(whiteGrass, [0, 1]))
        move = Move(blackBug, [0, 1])
        self.board.doMove(move)
        self.board.undoMove(move)

        self.board.doMove(move)

        move = Move(whiteBug, [0, 0])
        self.board.doMove(move)
        self.board.undoMove(move)

        self.board.doMove(move)

        move = Move(blackBug, [0, 0])

        self.board.doMove(move)
        self.board.undoMove(move)

        self.board.doMove(move)

        move = Move(blackBug, [0, 1])

        self.board.doMove(move)
        self.board.undoMove(move)

        self.board.doMove(move)

        move = Move(whiteBug, [0, 1])

        self.board.doMove(move)
        self.board.undoMove(move)

        self.board.doMove(move)

        move = Move(whiteBug, [1, 0])

        self.board.doMove(move)
        self.board.undoMove(move)

        self.board.doMove(move)

        move = Move(blackBug, [1, 0])

        self.board.doMove(move)
        self.board.undoMove(move)

        self.board.doMove(move)

        blocked = countOfBlocked(self.board, Color.WHITE)
        self.board.print()
        # self.assertEqual(blocked, 2)

    def test_color(self):
        color = Color.WHITE
        self.assertEqual(color.value, 1)
        color = color.inverse()
        self.assertEqual(color.value, 0)

    if __name__ == '__main__':
        unittest.main()