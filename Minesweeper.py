#Minesweeper!!
#V0.6
"""Changes: 
	Initial click no longer destroys bombs. yay!
	The user can now restart at any time. "R"
	Winning with the second condition (revealing all tiles except for the bombs) will now flag all unflagged bombs.
	Added timer!
	Added dark green flags when win.
	Appropriate colors for numbers.
"""
"""Todo:
	Visualize win (i.e. display "Yu win!" on screen... or something)
	UI
	No guess Minesweeper
"""
import pygame as pg
from time import sleep, time
from random import choice, randint

#Increase to make board bigger
relative_board_length = 950
#Increase to make margins bigger
relative_margin_length = 2

use_sample_board = False

sample = [[' ', ' ', ' ', ' ', ' ', ' '],
		  [' ', ' ', ' ', ' ', ' ', 'x'],
		  ['x', ' ', ' ', 'x', ' ', ' '],
		  [' ', ' ', ' ', 'x', ' ', ' ']]
first_tile = (0,0)

#Constants:
if use_sample_board:
	board_width = len(sample[0])
	board_height = len(sample)
else:
	board_width = 30
	board_height = 16
bomb_percentage = 20.75


#Colors:
white = (255,255,255)
black = (0,0,0)
grey = (128,128,128)
dark_grey = (50,50,50)

tile_1_color = (0,1,253)
tile_2_color = (1,126,0)
tile_3_color = (254,0,0)
tile_4_color = (1,1,128)
tile_5_color = (129,1,1)
tile_6_color = (0,128,128)
tile_7_color = black
tile_8_color = grey

tile_colors = {
	1: tile_1_color,
	2: tile_2_color,
	3: tile_3_color,
	4: tile_4_color,
	5: tile_5_color,
	6: tile_6_color,
	7: tile_7_color,
	8: tile_8_color
}

red = (255,0,0)
maroon = (128,0,0)
dark_green = (34,139,34)

#Calculated Constants:
tile_length = int(round(relative_board_length / max(board_width, board_height)))
margin_length = int(round(tile_length * relative_margin_length / 100, 0))
board_length_width = (tile_length * board_width) + (margin_length * (board_width + 1))
board_length_height = (tile_length * board_height) + (margin_length * (board_height + 1))
displayW, displayH = (board_length_width, board_length_height)


class Board:

	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.bomb_count = 0
		self.tiles = []
		self.nummed_tiles = [] # Tiles that appear as a number on the board (are surrounded by > 0 bombs and not a bomb themselves)
		self.win = False
		self.lose = False
		self.pre_reveal = True
		self.first_tile = None
		for row in range(height):
			self.tiles.append([])
			for col in range(width):
				c = Tile(self, (col,row))
				self.tiles[row].append(c)

	@staticmethod
	def create_custom_board(bomb_array, first_tile):
		"""Create a board from an array of either "x"s or "" with "x" 
		representing a bomb and "" representing... not a bomb AND a tile
		that represents the first place a user clicks. This tile will
		be revealed immediately"""

		# Create board
		board = Board(len(bomb_array[0]), len(bomb_array))
		board.first_tile = first_tile

		# Add bombs
		for row in range(len(bomb_array)):
			for col in range(len(bomb_array[row])):
				if bomb_array[row][col] == 'x':
					board.tiles[row][col].is_bomb = True
		board.bomb_count = sum([sum([1 for tile in row if tile.is_bomb]) for row in board.tiles])

		# Reveal first tile
		if __name__ == '__main__':
			timer.start()
		board.tiles[first_tile[1]][first_tile[0]].reveal()
		board.pre_reveal = False

		return board

	def create_state(matrix, first_tile=None):
		"""
		Create a board at a particular state given a matrix (2d array) of characters and a mandatory first tile.
		@param matrix: 2d array of characters:

			- 'x': bomb
			- 'r': revealed tile
			- (other): unrevealed tile

		@param first_tile (optional): tuple of coordinates of the first tile to be revealed, if None, the first tile is the first r tile found
		@return Board object
		"""
		if first_tile == None:
			for y, row in enumerate(matrix):
				if first_tile != None:
					break # revealed tile has been found
				for x, col in enumerate(row):
					if col == 'r':
						first_tile = (y, x)
						break
		if first_tile == None:
			raise ValueError('No first tile provided to function and no revealed tiles found in matrix')

		board = Board.create_custom_board(matrix, first_tile) # non 'x' characters are treated as non-bombs
		for tile in board.get_all_tiles():
			if matrix[tile.coords[1]][tile.coords[0]] == 'r':
				tile.reveal()
		return board

	def get_all_tiles(self):
		"""Return a list of all tiles on the board."""
		tiles = []
		for row in self.tiles:
			for tile in row:
				tiles.append(tile)
		return tiles

	def draw(self,draw_all=False):
		"""Draws the every tile in self.tiles and textto the board.
		Will also update to check for win or lose."""
		foundTiles = []
		revealedTiles = []
		flaggedTiles = []
		unrevealedTiles = []
		for row in self.tiles:
			for tile in row:
				if tile.is_flagged:
					flaggedTiles.append(tile)				
				if tile.is_found:
					foundTiles.append(tile)
				if tile.is_revealed:
					revealedTiles.append(tile)
				else:
					unrevealedTiles.append(tile)
				if draw_all or tile.needs_update:
					tile.draw()

		if __name__ == '__main__':
			pg.display.set_caption(f'Maxsweeper - Bombs left: {str(self.bomb_count - len(flaggedTiles))} - {str(round(timer.query()))} seconds')
		else:
			pg.display.set_caption(f'Maxsweeper - Bombs left: {str(self.bomb_count - len(flaggedTiles))}')

		if not self.pre_reveal and not self.lose:
			if len(foundTiles) == self.bomb_count and self.bomb_count - len(flaggedTiles) >= 0:
				self.win = True
				#Code below reveals all non-bomb tiles that have not been revealed.
				for tile in unrevealedTiles:
					if not tile.is_revealed:
						tile.reveal()
			elif len(revealedTiles) == self.width * self.height - self.bomb_count:
				self.win = True
				#Code below flags all bombs that have not been flagged.
				for tile in unrevealedTiles:
					tile.is_flagged = True

	def add_bombs(self, perc_bombs, mainSafeTile):
		"""Adds bombs to the board. takes perc_bombs% of the board
		will be bombs. Ex: let perc_bombs = 1, 1% of the board will have bombs.
		The mainSafeTile and it's 8 surrounding tiles will not have bombs."""
		self.first_tile = mainSafeTile.coords
		safeTiles = mainSafeTile.surrounding_bombs(mode=3)
		safeTiles.append(mainSafeTile)
		chance = perc_bombs / 100 
		bombs_num = int(self.width * self.height * chance)
		for tile in range(bombs_num):
			while True:
				r_coords = (randint(0, self.width - 1), randint(0, self.height - 1))
				if not self.tiles[r_coords[1]][r_coords[0]].is_bomb:
					for safeTile in safeTiles:
						if safeTile.coords == r_coords:
							break
					else:
						self.tiles[r_coords[1]][r_coords[0]].is_bomb = True
						break
		self.bomb_count = bombs_num

	def get_exposed_tiles(self):
		"""Return a list of all unrevealed tiles that are adjacent to revealed tiles."""
		exposed_tiles = []
		for row in self.tiles:
			for tile in row:
				if not tile.is_revealed:
					for neighbor_tile in tile.surrounding_bombs(mode=3):
						if neighbor_tile.is_revealed:
							if tile not in exposed_tiles:
								exposed_tiles.append(tile)
		return exposed_tiles

	def reset(self):
		"""
		Reset the board to its initial state (after the first tile is revealed)
		"""
		for tile in self.get_all_tiles():
			tile.is_flagged = False
			tile.is_revealed = False
			tile.is_found = False
			tile.needs_update = False
		self.nummed_tiles = []
		self.win = False
		self.lose = False
		self.pre_reveal = True
		self.tiles[first_tile[1]][first_tile[0]].reveal()
		self.pre_reveal = False


	def is_solvable(self):
		"""
		@return True if the board is could be solved, False if it is not solvable.
		"""
		# Solve each state
		while self.solve_state():
			pass

		# Check for win or stuck
		solved = False
		unrevealed_tile_count = sum([0 if tile.is_revealed else 1 for tile in self.get_all_tiles()])
		if unrevealed_tile_count == self.bomb_count:
			solved = True

		self.reset()
		return solved

	def solve_state(self):
		"""
		Uncover every tile that is definitely not a bomb given the current board state.
		@return True if the state changed, False otherwise.
		@changes self.tiles
		"""
		state_changed = False
		# Get all possible configurations of bombs on exposed tiles
		configurations = self.get_configurations()

		# Determine which tiles are ALWAYS bombs and which are ALWAYS not bombs
		master_configuration = configurations[0]
		all_bombs_in_exposed_tiles = True
		for configuration in configurations[1:]:
			if list(configuration.values()).count(True) != self.bomb_count:
				all_bombs_in_exposed_tiles = False
			for key in configuration:
				if configuration[key] != master_configuration[key]:
					master_configuration[key] = None

		# Uncover all tiles that are definitely not bombs
		for tile, is_bomb in master_configuration.items():
			x,y = tile
			if is_bomb == False:
				state_changed = True
				self.tiles[y][x].reveal()
		if all_bombs_in_exposed_tiles:
			# Uncover all unexposed tiles
			for tile in self.get_all_tiles():
				if tile.coords not in master_configuration and not tile.is_revealed: # every config. has exactly the exposed tile coords as keys
					state_changed = True
					tile.reveal()

		return state_changed


	def get_configurations(self):
		"""Returns a list of all the possible configurations for the exposed tiles as lists of bombs represented as True and non-bombs represented as False like so:
			[
				[
					(0,0) : True
					(0,1) : False
					(0,2) : False
					(1,0) : False
					(1,1) : False
					(1,2) : False
					(2,1) : False
					(2,2) : False
				],
				[
					(0,0) : False
					(0,1) : True
					(0,2) : False
					(1,0) : False
					(1,1) : False
					(1,2) : False
					(2,1) : False
					(2,2) : False
				],
				[
					(0,0) : False
					(0,1) : False
					(0,2) : True
					(1,0) : False
					(1,1) : False
					(1,2) : False
					(2,1) : False
					(2,2) : False
				]
			]
		As an example for a board  with 8 exposed tiles with 3 possible configurations.
		"""
		exposed_tiles = self.get_exposed_tiles()

		# Initialize blank_configuration
		blank_configuration = {}
		for tile in exposed_tiles:
			blank_configuration[tile.coords] = None

		# Call recursive helper function
		return self.get_configurations_helper(blank_configuration)

	def get_configurations_helper(self, configuration):
		"""Helper function for get_configurations that will be called recursively.
		@param configuration: A base configuration dictionary with the keys being the exposed tiles and the values being either True or False or None.
			- True: The tile is a bomb
			- False: The tile is not a bomb
			- None: The tile has not been assigned a value yet.
		@return a list of all *possible* configurations."""

		# Base case
		if None not in configuration.values():
			return [configuration]

		# Recursive case
		configurations = []
		
		# Find the first key with a value of None
		for key in configuration:
			if configuration[key] == None:
				break

		# Add a configuration with the key being True if it is a valid configuration
		configuration_copy_1 = configuration.copy()
		configuration_copy_1[key] = True
		if self.is_valid_configuration(configuration_copy_1):
			configurations += self.get_configurations_helper(configuration_copy_1)

		# Add a configuration with the key being False if it is a valid configuration
		configuration_copy_2 = configuration.copy()
		configuration_copy_2[key] = False
		if self.is_valid_configuration(configuration_copy_2):
			configurations += self.get_configurations_helper(configuration_copy_2)

		return configurations
	
	def is_valid_configuration(self, configuration):
		"""
		Return False if 'configuration' is illegal given the current board state.
		@param configuration: A dictionary with the keys being the exposed tiles and the values being either True or False or None:

			- True: The tile is supposed to be a bomb
			- False: The tile is supposed to not be a bomb
			- None: The tile has value has not been assigned yet
		@return bool True if the configuration is valid, False if it is not.
		"""

		# Check if there are more bombs than the board allows
		if list(configuration.values()).count(True) > self.bomb_count:
			# print('INVALID: Too many bombs')
			return False

		# Check if there are less hidden tiles than bombs left
		potential_bomb_tiles = 0
		for tile in self.get_all_tiles():
			if not tile.is_revealed:
				if tile.coords not in configuration:
					potential_bomb_tiles += 1
				elif configuration[tile.coords] == True:
					potential_bomb_tiles += 1
				elif configuration[tile.coords] == None:
					potential_bomb_tiles += 1
		if potential_bomb_tiles < self.bomb_count:
			# print('INVALID: Not enough hidden tiles')
			return False

		# Check all numbered tiles
		for tile in self.nummed_tiles:
			bombs_around_tile = 0
			unknowns_around_tile = 0
			surrounding_tiles = tile.surrounding_bombs(mode=3)
			for surrounding_tile in surrounding_tiles:
				if surrounding_tile.coords in configuration:
					if configuration[surrounding_tile.coords] == True:
						bombs_around_tile += 1
					elif configuration[surrounding_tile.coords] == None:
						unknowns_around_tile += 1

			# Check if any numbered tile has more bombs than its number
			if bombs_around_tile > tile.num:
				# print('INVALID: Too many bombs around a numbered tile: ' + str(tile.coords))
				return False

			# Check if any numbered tile has less (bombs + unknown tiles) around it than its number
			if bombs_around_tile + unknowns_around_tile < tile.num:
				# print('INVALID: Not enough bombs around a numbered tile: ' + str(tile.coords))
				return False

		return True


class Tile:

	def __init__(self,board,coords):
		self.board = board
		self.coords = coords
		self.is_bomb = False
		self.is_flagged = False
		self.is_revealed = False
		self.is_found = False
		self.needs_update = True
		self.x = coords[0]
		self.y = coords[1]

	def draw(self):
		"""Draws a tile to the screen."""
		x = (self.x + 1) * margin_length + tile_length * self.x
		y = (self.y + 1) * margin_length + tile_length * self.y
		#TEMPORARY
		if self.is_flagged:
			color = red
			if self.board.lose:
				if not self.is_bomb:
					color = maroon
			if self.board.win:
				color = dark_green
		elif self.is_revealed:
			color = white
			if self.is_bomb:
				color = dark_grey
		elif self.board.lose and self.is_bomb:
			color = black

		else:
			color = grey
		pg.draw.rect(screen, color, (x,y, tile_length, tile_length))
		if self.is_revealed and self.num != 0 or self.is_flagged and not self.is_bomb and self.board.lose:
			if self.is_flagged and not self.is_bomb and self.board.lose:
				msg = 'X'
				font_color = black
			else:
				msg = self.num
				font_color = tile_colors[self.num]
			font = pg.font.SysFont("Arial", int(7/6 * tile_length))
			text = font.render(str(msg), True, font_color)
			screen.blit(text,(int(x + 0.25*tile_length), int(y - 0.15*tile_length)))
		self.needs_update = False
		#/TEMPORARY

	def activate(self, button):	
		"""Will change or not change the atttributes of the tile based off of
		the button that the user presses and also the current attributes."""
		#If the tile has not been revealed and someone right clicks, toggle is_flagged
		self.needs_update = True
		if self.board.pre_reveal:
			if button == 1:
				self.first_reveal()
			else:
				return None
		else:
			if self.is_revealed:
				return None
			elif button == 3: # Right click
				self.is_flagged = not self.is_flagged
				if self.is_bomb:
					self.is_found = not self.is_found
			elif button == 1: # Left click
					self.reveal()
			elif button == 2: # Middle click
				if self.is_bomb:
					print(f'R {self.coords}')
				else:
					print(f'L {self.coords}')

	def reveal(self):
		"""What to do when someone reveals (left click) a 
		tile or the sytem reveals a tile."""
		if not self.is_flagged:
			self.needs_update = True
			self.is_revealed = True
			if self.is_bomb:
				self.board.lose = True
				self.num = 0
			else:
				self.num = self.surrounding_bombs(mode=1)
				if self.num == 0:
					self.surrounding_bombs(mode=2)
				else:
					self.board.nummed_tiles.append(self)

	def first_reveal(self):
		"""A function for when the user first reveals a tile.
		This makes sure that it opens something up right off the bat."""
		self.board.add_bombs(bomb_percentage, self)
		self.reveal()
		self.board.pre_reveal = False

		# DEV
		bomb_array = [["x" if self.board.tiles[y][x].is_bomb else ' ' for x in range(self.board.width)] for y in range(self.board.height)]
		print('First tile revealed at ' + str(self.coords))
		print("Bomb array: ")
		for row in bomb_array:
			print(row)
		# END DEV
		if __name__ == '__main__':
			timer.start()

	def surrounding_bombs(self,mode=1):
		"""A function with 3 modes so as to reuse a lot of the same code.
		Mode 1: Returns the number of bombs immediately surrounding the tile.
		Mode 2: Reveals the surrounding tiles.
		Mode 3: Return the surrounding tiles (a list of Tile-object instances)."""
		key = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
		bomb_count = 0
		tiles = []
		for relpos in key:
			newx = self.x + relpos[0]
			newy = self.y + relpos[1]
			#IF statment below for edge/corner case.
			if newx >= 0 and newx < self.board.width and newy >= 0 and newy < self.board.height:
				new_tile = self.board.tiles[newy][newx]
				if mode == 1:
					if new_tile.is_bomb:
						bomb_count += 1
				elif mode == 2:
					if not new_tile.is_revealed:
						new_tile.reveal()
				elif mode == 3:
					tiles.append(new_tile)
		if mode == 3:
			return tiles
		else:
			return bomb_count 


class Timer:

	def __init__(self):
		self.initial = None
		self.final  = None
		self.time = None

	def start(self):
		self.initial = time()

	def stop(self):
		self.final = time()
		self.time = self.final - self.initial
		return self.time

	def query(self):
		if self.initial == None:
			return 0
		if self.time == None:
			return time() - self.initial
		else:
			return self.time


def is_div(a,b):
	"""A simple function that will return True if a is divisible
	by b. and False if it is not."""
	return a % b == 0


def mouse_tile(pos):
	"""Returns which tile the user has clicked on based off of where
	they clicked on the screen."""
	x = pos[0]
	y = pos[1]
	tile_x = x // (margin_length + tile_length)
	tile_y = y // (margin_length + tile_length)
	#TEMPORARY
	if tile_x >= board_width:
		tile_x -= 1
	if tile_y >= board_height:
		tile_y -= 1
	return(tile_x,tile_y)
	#TEMPORARY

def win():
	"""A game loop for when the player wins."""
	if __name__ == '__main__':
		print(f'Yu win! (in {round(timer.time)} seconds!) Press ESC to quit. Press R to restart')
	else:
		print('Yu win! Press ESC to quit. Press R to restart')
	endgame()

def lose():
	"""A game loop for when the player loses."""
	
	print('boom! Press ESC to quit. Press R to restart')
	endgame()

def endgame():
	"""A game loop for when the player finishes a game (win or lose)"""
	board.draw(draw_all=True)
	pg.display.update()
	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
				pg.quit()
				quit()
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_r:
					main()

def main():
	global timer
	timer = Timer()

	global board
	if use_sample_board:
		board = Board.create_custom_board(sample, first_tile)
	else:
		board = Board(board_width, board_height)

	screen.fill(white)

	locked = True
	while locked:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				locked = False
			elif event.type == pg.MOUSEBUTTONDOWN:
				pressed_tile = mouse_tile(event.pos)
				board.tiles[pressed_tile[1]][pressed_tile[0]].activate(event.button)
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					locked = False
				elif event.key == pg.K_r:
					main()
				elif event.key == pg.K_f:
					# TEMPORARY
					exposed_tiles = board.get_exposed_tiles()
					for tile in exposed_tiles:
						tile.activate(button=3)
					print(Board.make_dict_with_null_values(exposed_tiles))
		board.draw()
		pg.display.update()
		if board.win:
			timer.stop()
			win()
			return None
		if board.lose:
			timer.stop()
			lose()
			return None
		clock.tick(60)

	pg.quit()
	quit()

if __name__ == '__main__':
	pg.init()
	pg.display.set_caption('Maxsweeper - Bombs left: N/A')
	clock = pg.time.Clock()
	screen = pg.display.set_mode((displayW, displayH))
	main()