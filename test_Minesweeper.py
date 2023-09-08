import unittest

from Minesweeper import *

class TestingTools:
    """
    Some functions for helping with the testing
    """
    @staticmethod
    def config_dict(config_mtrx):
        """
        Create a properly formatted config dictionary from a more readable matrix
        @param config_mtrx: 2d array of characters:
            - 'x': bomb
            - 'n': not a bomb
            - '?': unknown tile
            - ' ': not in config
        """
        config = {}
        for y in range(len(config_mtrx)):
            for x in range(len(config_mtrx[y])):
                if config_mtrx[y][x] == 'x':
                    config[(x, y)] = True
                elif config_mtrx[y][x] == 'n':
                    config[(x, y)] = False
                elif config_mtrx[y][x] == '?':
                    config[(x, y)] = None
        return config

class ValidConfiguration(unittest.TestCase):
    """
    Tests for Board.is_valid_configuration()
    """

    def validate_config(self, board, config):
        """
        Ensure that config contains exactly the exposed tiles of the board.
        """
        exposed_tiles = board.get_exposed_tiles()
        self.assertEqual(len(exposed_tiles), len(config))
        for tile in exposed_tiles:
            self.assertIn(tile.coords, config)

    def test_too_many_bombs(self):
        board = Board.create_state(
            [
                ['x', 'r', 'r'],
                ['r', 'x', ' '],
                ['r', ' ', ' ']
            ]
        )
        config = [
            ['x', ' ', ' '],
            [' ', 'n', 'x'],
            [' ', 'x', ' ']
        ]
        config = TestingTools.config_dict(config)
        self.validate_config(board, config)
        self.assertEqual(board.is_valid_configuration(config), False)

    def test_not_enough_bombs(self):
        board = Board.create_state(
            [
                ['x', 'r', 'r'],
                ['r', ' ', 'x'],
                ['r', 'x', 'x']
            ]
        )
        config = [
            ['x', ' ', ' '],
            [' ', 'x', 'n'],
            [' ', 'n', ' ']
        ]
        config = TestingTools.config_dict(config)
        self.validate_config(board, config)
        self.assertEqual(board.is_valid_configuration(config), False)

if __name__ == '__main__':
    unittest.main()