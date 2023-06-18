#Minesweeper!!
#V0.6
"""Changes: 
	Initial click no longer destroys bombs. yay!
	The user can now restart at any time. "R"
	Winning with the second condition (revealing all tiles except for the bombs) will now flag all unflagged bombs.
	Added timer!
	Added dark green flags when win.
"""
"""Todo:
	Add a middle click currency system
	Make middle click user friendly
	Visualize win (i.e. display "Yu win!" on screen... or something)
	Make marathon minesweeper
	Color numbers
	UI
"""
#sample = [['x', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', 'x', ''], ['', '', '', '', '']]
import pygame as pg
from time import sleep, time
from random import choice, randint
pg.init()
pg.display.set_caption('Maxsweeper - Bombs left: N/A')

#Constants:
board_width = 30
board_height = 16
bomb_percentage = 20.75

#Increase to make board bigger
relative_board_length = 1500
#Increase to make margins bigger
relative_margin_length = 2


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

clock = pg.time.Clock()
screen = pg.display.set_mode((displayW, displayH))


class Board:

	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.bomb_count = 0
		self.tiles = []
		self.win = False
		self.lose = False
		self.pre_reveal = True
		for row in range(height):
			self.tiles.append([])
			for col in range(width):
				c = Tile(self, (col,row))
				self.tiles[row].append(c)

	def add_bombs_custom(self, array):
		"""A method for testing purposes only. Lets you submit an array
		with either "x"s or "" with "x" representing a bomb and "" representing...
		not a bomb. (WARNING THIS WON"T ENSURE A SAFE FIRST CLICK)"""
		bomb_count = 0
		for b, row in enumerate(array):
			for bb, item in enumerate(row):
				if item == 'x':
					bomb_count += 1
					board.tiles[b][bb].is_bomb = True
		self.bomb_count = bomb_count

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

		pg.display.set_caption(f'Maxsweeper - Bombs left: {str(self.bomb_count - len(flaggedTiles))} - {str(round(timer.query()))} seconds')

		if not self.pre_reveal:
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
		safeTiles = mainSafeTile.surrounding_bombs(mode=3)
		safeTiles.append(mainSafeTile)
		chance = perc_bombs / 100 
		bombs_num = int(self.width * self.height * chance)
		for tile in range(bombs_num):
			while True:
				r_coords = (randint(0, board_width - 1), randint(0,board_height - 1))
				if not self.tiles[r_coords[1]][r_coords[0]].is_bomb:
					for safeTile in safeTiles:
						if safeTile.coords == r_coords:
							break
					else:
						self.tiles[r_coords[1]][r_coords[0]].is_bomb = True
						break
		self.bomb_count = bombs_num


class Tile:

	def __init__(self,board,coords):
		self.board = board
		self.coords = coords
		self.is_bomb = False
		self.is_flagged = False
		self.is_revealed = False
		self.is_found = False
		self.is_winning = False
		self.needs_update = True
		self.x = coords[0]
		self.y = coords[1]

	def draw(self):
		"""Draws a tile to the screen."""
		x = (self.x + 1) * margin_length + tile_length * self.x
		y = (self.y + 1) * margin_length + tile_length * self.y
		#TEMPORARY
		if self.is_flagged:
			color = black
			if self.board.lose:
				if not self.is_bomb:
					color = dark_grey
			if self.board.win:
				color = dark_green
		elif self.is_revealed:
			color = white
			if self.is_bomb:
				color = maroon
		elif self.board.lose and self.is_bomb:
			color = red

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
			elif button == 3:
				self.is_flagged = not self.is_flagged
				if self.is_bomb:
					self.is_found = not self.is_found
			elif button == 1:
					self.reveal()
			elif button == 2:
				if self.is_bomb:
					print(f'R {self.coords}')
				else:
					print(f'L {self.coords}')

	def reveal(self, clear=False):
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

	def first_reveal(self):
		"""A function for when the user first reveals a tile.
		This makes sure that it opens something up right off the bat."""
		self.board.add_bombs(bomb_percentage, self)                     
		#self.board.add_bombs_custom(sample) #For testing with a custom board
		self.reveal()
		self.board.pre_reveal = False
		timer.start()

	def surrounding_bombs(self,mode=1):
		"""A function with 2 modes so as to reuse a lot of the same code.
		Mode 1: Returns the number of bombs immediately surrounding the tile.
		Mode 2: Reveals the surrounding tiles.
		Mode 3: Return the surrounding tiles (a list of Tile-object instances)."""
		key = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
		bomb_count = 0
		total_cleared = 0
		tiles = []
		for relpos in key:
			newx = self.x + relpos[0]
			newy = self.y + relpos[1]
			#IF statment below for edge/corner case.
			if newx >= 0 and newx < board_width and newy >= 0 and newy < board_height:
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


def display_message(text, size):
	"""WIP"""
	font = pg.font.SysFont("Arial", size)
	text_surface = font.render(text, True)
	screen.blit(text_surface,( int(displayW/2 - size/2), int(displayH/2 - size/2)))
	pg.display.update()


def win(marathon=False):
	"""A game loop for when the player wins."""
	if marathon:
		print('Yu win! Press ESC to quit. Press ENTER to move on to the next stage.')
	else:
		print(f'Yu win! (in {round(timer.time)} seconds!) Press ESC to quit. Press R to restart')
	endgame()

def lose():
	"""A game loop for when the player loses."""
	
	print('boom! Press ESC to quit. Press R to restart')
	endgame()

def endgame(marathon=False):
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

def intro():
	"""work in progress."""
	screen.fill(white)

def main(marathon=False):
	global board
	global timer
	board = Board(board_width, board_height)
	timer = Timer()
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

main()