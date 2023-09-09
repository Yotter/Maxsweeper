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

        @return: dictionary of tile coordinates to True / False / None
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

    @staticmethod
    def config_mtrx(config_dict):
        """
        Create a more readable matrix from a config dictionary
        @param config_dict: dictionary of tile coordinates to True / False / None

        @return: 2d array of characters:
            - 'x': bomb
            - 'n': not a bomb
            - '?': unknown tile
            - ' ': not in config
        """
        config_mtrx = []
        width = max([x for x, y in config_dict.keys()]) + 1
        height = max([y for x, y in config_dict.keys()]) + 1
        for y in range(height):
            config_mtrx.append([' '] * width)

        for coords, value in config_dict.items():
            x, y = coords
            if value == True:
                config_mtrx[y][x] = 'x'
            elif value == False:
                config_mtrx[y][x] = 'n'
            elif value == None:
                config_mtrx[y][x] = '?'
        return config_mtrx

    @staticmethod
    def validate_config(board, config):
        """
        Ensure that config contains exactly the exposed tiles of the board.
        """
        exposed_tiles = board.get_exposed_tiles()
        assert len(exposed_tiles) == len(config)
        for tile in exposed_tiles:
            assert tile.coords in config

class ValidConfiguration(unittest.TestCase):
    """
    Tests for Board.is_valid_configuration()
    """

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
        TestingTools.validate_config(board, config)
        self.assertEqual(board.is_valid_configuration(config), False)

    def test_not_enough_bombs1(self):
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
        TestingTools.validate_config(board, config)
        self.assertEqual(board.is_valid_configuration(config), False)

    def test_not_enough_bombs2(self):
        board = Board.create_state(
            [
                ['x', 'r', 'r'],
                ['r', ' ', 'x'],
                ['r', 'x', 'x']
            ]
        )
        config = [
            ['x', ' ', ' '],
            [' ', '?', 'n'],
            [' ', 'n', ' ']
        ]
        config = TestingTools.config_dict(config)
        TestingTools.validate_config(board, config)
        self.assertEqual(board.is_valid_configuration(config), False)

    def test_more_than_number(self):
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
            [' ', 'x', ' ']
        ]
        config = TestingTools.config_dict(config)
        TestingTools.validate_config(board, config)
        self.assertEqual(board.is_valid_configuration(config), False)

    def test_less_than_number(self):
        board = Board.create_state(
            [
                ['x', 'r', 'r'],
                ['r', ' ', 'x'],
                ['r', 'x', ' ']
            ]
        )
        config = [
            ['x', ' ', ' '],
            [' ', 'n', 'x'],
            [' ', 'n', ' ']
        ]
        config = TestingTools.config_dict(config)
        TestingTools.validate_config(board, config)
        self.assertEqual(board.is_valid_configuration(config), False)

    def test_valid_config1(self):
        board = Board.create_state(
            [
                ['x', 'r', 'r'],
                ['r', ' ', 'x'],
                ['r', 'x', 'x']
            ]
        )
        config = [
            ['x', ' ', ' '],
            [' ', 'x', '?'],
            [' ', 'n', ' ']
        ]
        config = TestingTools.config_dict(config)
        TestingTools.validate_config(board, config)
        self.assertEqual(board.is_valid_configuration(config), True)

    def test_valid_config2(self):
        board = Board.create_state(
            [
                ['x', 'r', 'r'],
                ['r', ' ', 'x'],
                ['r', 'x', 'x']
            ]
        )
        config = [
            ['?', ' ', ' '],
            [' ', '?', '?'],
            [' ', '?', ' ']
        ]
        config = TestingTools.config_dict(config)
        TestingTools.validate_config(board, config)
        self.assertEqual(board.is_valid_configuration(config), True)

    def test_valid_config3(self):
        board = Board.create_state(
            [
                ['r', 'r', 'r'],
                ['r', 'x', 'r'],
                ['r', 'r', 'r']
            ]
        )
        config = [
            [' ', ' ', ' '],
            [' ', 'x', ' '],
            [' ', ' ', ' ']
        ]
        config = TestingTools.config_dict(config)
        TestingTools.validate_config(board, config)
        self.assertEqual(board.is_valid_configuration(config), True)

    def test_valid_config4(self):
        board = Board.create_state(
            [
                ['r', 'r', 'r'],
                ['r', 'x', 'r'],
                ['r', 'r', 'r']
            ]
        )
        config = [
            [' ', ' ', ' '],
            [' ', '?', ' '],
            [' ', ' ', ' ']
        ]
        config = TestingTools.config_dict(config)
        TestingTools.validate_config(board, config)
        self.assertEqual(board.is_valid_configuration(config), True)

class ConfigurationsGenerator(unittest.TestCase):
    """
    Tests for board.get_configurations_helper() and board.get_configurations()
    """

    def test_base_case(self):
        board = Board.create_state(
            [
                ['x', 'r', 'r'],
                ['r', ' ', 'x'],
                ['r', 'x', 'x']
            ]
        )
        config = [
            ['x', ' ', ' '],
            [' ', 'n', 'x'],
            [' ', 'x', ' ']
        ]
        config = TestingTools.config_dict(config)
        TestingTools.validate_config(board, config)
        self.assertEqual(board.get_configurations_helper(config), [config])

    def test_no_solutions(self):
        board = Board.create_state(
            [
                ['x', 'r', 'r'],
                ['r', ' ', 'x'],
                ['r', 'x', 'x']
            ]
        )
        config = [
            ['?', ' ', ' '],
            [' ', 'x', '?'],
            [' ', '?', ' ']
        ]
        config = TestingTools.config_dict(config)
        TestingTools.validate_config(board, config)
        self.assertEqual(board.get_configurations_helper(config), [])

    def test_one_solution1(self):
        board = Board.create_state(
            [
                ['x', 'r', 'r'],
                ['r', ' ', 'x'],
                ['r', 'x', 'x']
            ]
        )
        config = [
            ['?', ' ', ' '],
            [' ', '?', '?'],
            [' ', '?', ' ']
        ]
        config = TestingTools.config_dict(config)
        TestingTools.validate_config(board, config)
        configurations = board.get_configurations_helper(config)
        self.assertEqual(len(configurations), 1)
        self.assertEqual(configurations[0], TestingTools.config_dict(
            [
                ['x', ' ', ' '],
                [' ', 'n', 'x'],
                [' ', 'x', ' ']
            ]
        ))

    def test_one_solution2(self):
            board = Board.create_state(
                [
                    ['x', 'r', 'r'],
                    ['r', 'x', ' '],
                    ['r', ' ', ' ']
                ]
            )
            config = [
                ['?', ' ', ' '],
                [' ', '?', '?'],
                [' ', '?', ' ']
            ]
            config = TestingTools.config_dict(config)
            TestingTools.validate_config(board, config)
            configurations = board.get_configurations_helper(config)
            self.assertEqual(len(configurations), 1)
            self.assertEqual(configurations[0], TestingTools.config_dict(
                [
                    ['x', ' ', ' '],
                    [' ', 'x', 'n'],
                    [' ', 'n', ' ']
                ]
            ))

    def test_two_solutions(self):
        board = Board.create_state(
            [
                ['x', 'r', 'r'],
                ['r', 'x', ' '],
                ['r', ' ', 'x']
            ]
        )
        config = [
            ['?', ' ', ' '],
            [' ', '?', '?'],
            [' ', '?', ' ']
        ]
        config = TestingTools.config_dict(config)
        TestingTools.validate_config(board, config)
        configurations = board.get_configurations_helper(config)
        self.assertEqual(len(configurations), 2)
        self.assertIn(TestingTools.config_dict(
            [
                ['x', ' ', ' '],
                [' ', 'x', 'n'],
                [' ', 'n', ' ']
            ]
        ), configurations)
        self.assertIn(TestingTools.config_dict(
            [
                ['x', ' ', ' '],
                [' ', 'n', 'x'],
                [' ', 'x', ' ']
            ]
        ), configurations)

    def test_complex_board(self):
        board = Board.create_state(
            [
                ['r', 'r', 'x', 'r', 'r'],
                ['r', 'r', 'r', 'r', 'r'],
                ['r', 'r', 'r', 'r', 'r'],
                ['x', ' ', ' ', 'x', ' '],
                [' ', ' ', ' ', 'x', ' ']
            ]
        )
        config = [
            [' ', ' ', '?' ,' ', ' '],
            [' ', ' ', ' ' ,' ', ' '],
            [' ', ' ', ' ' ,' ', ' '],
            ['?', '?', '?' ,'?', '?'],
            [' ', ' ', ' ' ,' ', ' ']
        ]
        config = TestingTools.config_dict(config)
        TestingTools.validate_config(board, config)
        configurations = board.get_configurations_helper(config)
        self.assertEqual(len(configurations), 2)
        self.assertIn(TestingTools.config_dict(
            [
                [' ', ' ', 'x' ,' ', ' '],
                [' ', ' ', ' ' ,' ', ' '],
                [' ', ' ', ' ' ,' ', ' '],
                ['x', 'n', 'n' ,'x', 'n'],
                [' ', ' ', ' ' ,' ', ' ']
            ]
        ), configurations)
        self.assertIn(TestingTools.config_dict(
            [
                [' ', ' ', 'x' ,' ', ' '],
                [' ', ' ', ' ' ,' ', ' '],
                [' ', ' ', ' ' ,' ', ' '],
                ['n', 'x', 'n' ,'n', 'x'],
                [' ', ' ', ' ' ,' ', ' ']
            ]
        ), configurations)

    def test_get_configurations(self):
        board = Board.create_state(
            [
                ['r', 'r', 'x', 'r', 'r'],
                ['r', 'r', 'r', 'r', 'r'],
                ['r', 'r', 'r', 'r', 'r'],
                ['x', ' ', ' ', 'x', ' '],
                [' ', ' ', ' ', 'x', ' ']
            ]
        )
        configurations = board.get_configurations()
        self.assertEqual(len(configurations), 2)
        self.assertIn(TestingTools.config_dict(
            [
                [' ', ' ', 'x' ,' ', ' '],
                [' ', ' ', ' ' ,' ', ' '],
                [' ', ' ', ' ' ,' ', ' '],
                ['x', 'n', 'n' ,'x', 'n'],
                [' ', ' ', ' ' ,' ', ' ']
            ]
        ), configurations)
        self.assertIn(TestingTools.config_dict(
            [
                [' ', ' ', 'x' ,' ', ' '],
                [' ', ' ', ' ' ,' ', ' '],
                [' ', ' ', ' ' ,' ', ' '],
                ['n', 'x', 'n' ,'n', 'x'],
                [' ', ' ', ' ' ,' ', ' ']
            ]
        ), configurations)

if __name__ == '__main__':
    unittest.main()