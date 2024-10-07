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
    # TODO: delete this if it is still unused
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

    def generic_test(self, board_mtrx, config_mtrx, expected_result: bool):
        """
        Validate the config using the right tiles and perform test
        @param board_mtrx list[list] 2d array that represents a board and its current state:
            - 'x': bomb
			- 'r': revealed tile
			- (other): unrevealed tile

        @param config_mtrx list[list] 2d array that represents a config to validate:
            - 'x': bomb
            - 'n': not a bomb
            - '?': unknown tile
            - ' ': not in config

        @param expected_result bool expected output of is_valid_configuration()
        """
        board = Board.create_state(board_mtrx)
        config = TestingTools.config_dict(config_mtrx)
        TestingTools.validate_config(board, config)
        self.assertEqual(board.is_valid_configuration(config), expected_result)

    def test_too_many_bombs(self):
        self.generic_test(
            board_mtrx=[
                ['x', 'r', 'r'],
                ['r', 'x', ' '],
                ['r', ' ', ' ']
            ],
            config_mtrx=[
                ['x', ' ', ' '],
                [' ', 'n', 'x'],
                [' ', 'x', ' ']
            ],
            expected_result=False
        )

    def test_not_enough_bombs1(self):
        self.generic_test(
            board_mtrx=[
                ['x', 'r', 'r'],
                ['r', ' ', 'x'],
                ['r', 'x', 'x']
            ],
            config_mtrx=[
                ['x', ' ', ' '],
                [' ', 'x', 'n'],
                [' ', 'n', ' ']
            ],
            expected_result=False
        )

    def test_not_enough_bombs2(self):
        self.generic_test(
            board_mtrx=[
                ['x', 'r', 'r'],
                ['r', ' ', 'x'],
                ['r', 'x', 'x']
            ],
            config_mtrx=[
                ['x', ' ', ' '],
                [' ', '?', 'n'],
                [' ', 'n', ' ']
            ],
            expected_result=False
        )

    def test_more_than_number(self):
        self.generic_test(
            board_mtrx=[
                ['x', 'r', 'r'],
                ['r', ' ', 'x'],
                ['r', 'x', 'x']
            ],
            config_mtrx=[
                ['x', ' ', ' '],
                [' ', 'x', 'n'],
                [' ', 'x', ' ']
            ],
            expected_result=False
        )

    def test_less_than_number(self):
        self.generic_test(
            board_mtrx=[
                ['x', 'r', 'r'],
                ['r', ' ', 'x'],
                ['r', 'x', ' ']
            ],
            config_mtrx=[
                ['x', ' ', ' '],
                [' ', 'n', 'x'],
                [' ', 'n', ' ']
            ],
            expected_result=False
        )

    def test_valid_config1(self):
        self.generic_test(
            board_mtrx=[
                ['x', 'r', 'r'],
                ['r', ' ', 'x'],
                ['r', 'x', 'x']
            ],
            config_mtrx=[
                ['x', ' ', ' '],
                [' ', 'x', '?'],
                [' ', 'n', ' ']
            ],
            expected_result=True
        )

    def test_valid_config2(self):
        self.generic_test(
            board_mtrx=[
                ['x', 'r', 'r'],
                ['r', ' ', 'x'],
                ['r', 'x', 'x']
            ],
            config_mtrx=[
                ['?', ' ', ' '],
                [' ', '?', '?'],
                [' ', '?', ' ']
            ],
            expected_result=True
        )

    def test_valid_config3(self):
        self.generic_test(
            board_mtrx=[
                ['r', 'r', 'r'],
                ['r', 'x', 'r'],
                ['r', 'r', 'r']
            ],
            config_mtrx=[
                [' ', ' ', ' '],
                [' ', 'x', ' '],
                [' ', ' ', ' ']
            ],
            expected_result=True
        )

    def test_valid_config4(self):
        self.generic_test(
            board_mtrx=[
                ['r', 'r', 'r'],
                ['r', 'x', 'r'],
                ['r', 'r', 'r']
            ],
            config_mtrx=[
                [' ', ' ', ' '],
                [' ', '?', ' '],
                [' ', ' ', ' ']
            ],
            expected_result=True
        )

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

class SolveState(unittest.TestCase):
    """
    Tests for Board.solve_state()
    """
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
        self.assertTrue(board.solve_state())
        self.assertEqual(sum([1 if tile.is_revealed else 0 for tile in board.get_all_tiles()]), 15)
        self.assertTrue(board.tiles[3][2].is_revealed)

    def test_unexposed_reveal(self):
        board = Board.create_state(
            [
                ['r', 'r', 'x', 'r', 'r'],
                ['r', 'r', 'r', 'r', 'r'],
                ['r', 'r', 'r', 'r', 'r'],
                ['x', ' ', 'r', 'x', ' '],
                [' ', ' ', ' ', 'x', ' ']
            ]
        )
        self.assertTrue(board.solve_state())
        self.assertEqual(sum([1 if tile.is_revealed else 0 for tile in board.get_all_tiles()]), 17)
        self.assertTrue(board.tiles[4][0].is_revealed)
        self.assertTrue(board.tiles[4][4].is_revealed)

    def test_no_change(self):
        board = Board.create_state(
            [
                ['r', 'r', 'x', 'r', 'r'],
                ['r', 'r', 'r', 'r', 'r'],
                ['r', 'r', 'r', 'r', 'r'],
                ['x', ' ', 'r', 'x', ' '],
                ['r', 'r', 'r', 'x', 'r']
            ]
        )
        self.assertFalse(board.solve_state())
        self.assertEqual(sum([0 if tile.is_revealed else 1 for tile in board.get_all_tiles()]), 6)

class Solve(unittest.TestCase):
    """
    Tests for Board.is_solvable()
    """

    def test_simple_board1(self):
        board = Board.create_custom_board(
            [
                ['x', 'x', ' '],
                [' ', ' ', 'x'],
                [' ', ' ', 'x']
            ], (0, 2)
        )
        self.assertTrue(board.is_solvable())
        self.assertFalse(board.tiles[0][2].is_revealed)

    def test_simple_board2(self):
        board = Board.create_custom_board(
            [
                ['x', ' ', ' '],
                [' ', ' ', 'x'],
                [' ', ' ', 'x']
            ], (0, 2)
        )
        self.assertTrue(board.is_solvable())
        self.assertFalse(board.tiles[0][1].is_revealed)
        self.assertFalse(board.tiles[0][2].is_revealed)

    def test_complex_board1(self):
        board = Board.create_custom_board(
            [
                [' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' '],
                ['x', ' ', ' ', 'x', ' '],
                [' ', ' ', ' ', 'x', ' ']
            ], (0,0)
        )
        self.assertFalse(board.is_solvable())
        self.assertEqual(sum([1 if tile.is_revealed else 0 for tile in board.get_all_tiles()]), 10)

    def test_complex_board2(self):
        board = Board.create_custom_board(
            [
                [' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', 'x'],
                ['x', ' ', ' ', 'x', ' ', ' '],
                [' ', ' ', ' ', 'x', ' ', ' ']
            ], (0,0)
        )
        self.assertTrue(board.is_solvable())
        self.assertEqual(sum([1 if tile.is_revealed else 0 for tile in board.get_all_tiles()]), 10)

    def test_big_board1(self):
        board = Board.create_custom_board(
            [
                [' ', ' ', 'x', ' ', 'x', ' ', ' ', 'x', 'x', ' '] ,
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' '] ,
                [' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' '] ,
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '] ,
                ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '] ,
                [' ', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' '] ,
                [' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' '] ,
                [' ', ' ', ' ', 'x', ' ', ' ', 'x', 'x', ' ', ' '] ,
                [' ', ' ', ' ', ' ', 'x', ' ', 'x', 'x', ' ', ' '] ,
                ['x', 'x', ' ', ' ', 'x', ' ', ' ', 'x', ' ', ' '] ,
            ], (4,4)
        )
        self.assertTrue(board.is_solvable())

    def test_big_board2(self):
        board = Board.create_custom_board(
            [
                [' ', ' ', ' ', ' ', 'x', ' ', ' ', 'x', ' ', ' '] ,
                [' ', 'x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' '] ,
                [' ', 'x', ' ', ' ', ' ', ' ', ' ', 'x', ' ', 'x'] ,
                ['x', ' ', ' ', ' ', ' ', ' ', ' ', 'x', 'x', 'x'] ,
                [' ', ' ', ' ', ' ', ' ', 'x', 'x', ' ', ' ', 'x'] ,
                [' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' '] ,
                [' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', 'x', 'x'] ,
                [' ', 'x', ' ', 'x', ' ', ' ', ' ', 'x', 'x', 'x'] ,
                [' ', ' ', ' ', 'x', 'x', ' ', ' ', ' ', ' ', ' '] ,
                [' ', ' ', ' ', 'x', ' ', 'x', 'x', 'x', 'x', ' '] ,
            ], (2,4)
        )
        self.assertFalse(board.is_solvable())


if __name__ == '__main__':
    unittest.main()