import pygame
import time
from copy import deepcopy

class GridWorld:

	def __init__(self, grid):

		pygame.init()
		pygame.font.init()

		# define colors
		self.BLACK = (100, 100, 100)
		self.WHITE = (255, 255, 255)
		self.GREEN = (0, 255, 0)
		self.RED = (255, 139, 139)
		self.BLUE = (175, 175, 255)
		self.ORANGE = (244, 164, 96)
		self.YELLOW = (255, 255, 0)
		self.HUMAN = (255, 0, 255)
		self.ROBOT = (0, 255, 255)

		# cell dimensions
		self.WIDTH = 45
		self.HEIGHT = 45
		self.MARGIN = 5
		self.color = self.WHITE

		# load grid
		self.grid = grid

		self.num_col = len(grid[0])
		self.num_row = len(grid)

		# set the width and height of the screen (width , height)		
		screen_width = (self.WIDTH + self.MARGIN) * self.num_col + self.MARGIN
		screen_height = (self.HEIGHT + self.MARGIN) * self.num_row + self.MARGIN
		self.size = (screen_width, screen_height)
		self.screen = pygame.display.set_mode(self.size)

		self.font = pygame.font.SysFont('arial', 20)

		pygame.display.set_caption("Grid world")

		self.clock = pygame.time.Clock()

		self.reset()

	def reset(self):
		self.screen.fill(self.BLACK)

		for row in range(self.num_row):
			for col in range(self.num_col):
				if self.grid[row][col] == 1:
					self.color = self.BLACK
				else:
					self.color = self.WHITE
				pygame.draw.rect(self.screen,
					self.color,
					[(self.MARGIN + self.WIDTH)*col+self.MARGIN,
					(self.MARGIN + self.HEIGHT)*row+self.MARGIN,
					self.WIDTH,
					self.HEIGHT])

	def is_wall(self, row, col):
		return (row < 0) or (row >= self.num_row) or (col < 0) or (col >= self.num_col) or (self.grid[row][col] == 1)

	def text_objects(self, text, font):
		textSurface = font.render(text, True, self.BLACK)
		return textSurface, textSurface.get_rect()

	def draw_human(self, center):
		origin = [0+1*self.MARGIN+22.5,0+1*self.MARGIN+22.5]
		col = self.MARGIN + self.WIDTH
		row = self.MARGIN + self.HEIGHT
		pygame.draw.circle(self.screen, self.HUMAN, (int(origin[1]+row*(center[1])), int(origin[0]+col*(center[0]))), 8)

	def draw_robot(self, center):
		origin = [0+1*self.MARGIN+22.5,0+1*self.MARGIN+22.5]
		col = self.MARGIN + self.WIDTH
		row = self.MARGIN + self.HEIGHT
		pygame.draw.circle(self.screen, self.ROBOT, (int(origin[1]+row*(center[1])), int(origin[0]+col*(center[0]))), 12, 2)

	def draw_cell(self, node, color):
		row = node[1][0]
		col = node[1][1]
		reward = node[0]
		pygame.draw.rect(self.screen,
				color,
				[(self.MARGIN + self.WIDTH)*col+self.MARGIN,
				(self.MARGIN + self.HEIGHT)*row+self.MARGIN,
				self.WIDTH,
				self.HEIGHT])
		TextSurf, TextRect = self.text_objects(str(reward), self.font)
		TextRect.center = ((self.MARGIN + self.WIDTH)*col + 4*self.MARGIN,
			(self.MARGIN + self.HEIGHT)*row + 4*self.MARGIN)
		self.screen.blit(TextSurf, TextRect)

	def draw_green_cell(self, node):
		self.draw_cell(node, self.GREEN)

	def draw_red_cell(self, node):
		self.draw_cell(node, self.RED)

	def draw_orange_cell(self, node):
		self.draw_cell(node, self.ORANGE)

	def draw_yellow_cell(self, node):
		self.draw_cell(node, self.YELLOW)

	def draw_rewards(self, rewards):
		for row in range(self.num_row):
			for col in range(self.num_col):
				if self.is_wall(row, col):
					continue

				reward = rewards[row][col]
				if reward > 0:
					self.draw_green_cell([reward, [row, col]])
				elif reward == 0:
					self.draw_cell([reward, [row, col]], self.WHITE)
				elif -5 < reward < 0:
					self.draw_cell([reward, [row, col]], self.YELLOW)
				elif -10 < reward <= -5:
					self.draw_cell([reward, [row, col]], self.ORANGE)
				elif reward <= -10:
					self.draw_red_cell([reward, [row, col]])

	def show(self, title=None):
		if title is not None:
			pygame.display.set_caption(title)
		pygame.display.flip()

	def loop(self):
		exit = False
		while exit == False:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit = True

			self.clock.tick(60)
			








