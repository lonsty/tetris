import unittest

from tetris.const import TETROMINOS
from tetris.tetris import Board, Tetromino


class TestTetris(unittest.TestCase):
    def test_board_init(self):
        board = Board(20, 10)
        self.assertEqual(len(board.grid), 20)
        self.assertEqual(len(board.grid[0]), 10)

    def test_tetromino_coords(self):
        t = Tetromino(TETROMINOS[0], 0, 0)
        coords = t.get_coords()
        self.assertEqual(len(coords), 4)

    def test_collision(self):
        board = Board(4, 4)
        t = Tetromino([[1, 1], [1, 1]], 3, 3)
        self.assertTrue(board.check_collision(t))

    def test_remove_full_lines(self):
        board = Board(4, 4)
        board.grid[-1] = [1, 1, 1, 1]
        lines = board.remove_full_lines()
        self.assertEqual(lines, 1)


if __name__ == "__main__":
    unittest.main()
