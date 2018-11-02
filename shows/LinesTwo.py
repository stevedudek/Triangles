from HelperFunctions import*
from triangle import*
        		
class LinesTwo(object):
	def __init__(self, trimodel):
		self.name = "LinesTwo"
		self.tri = trimodel
		self.time = 1
		self.speed = 0.1
		self.width = 12
		self.color = randColor()
		self.background = randColor()
		self.color_grade = randint(30, 100)

		self.tri.set_all_cells((0, 0, 0))

	def next_frame(self):

		while (True):

			self.draw_lines()
			
			self.time += 1
			
			yield self.speed
	
	def draw_lines(self):
		i = self.time % 22
		if i > 11:
			i = 22 - i
		if i == 0:
			self.set_random_colors()

		for corner in all_left_corners():
			cell = tri_in_direction(corner, 1, i*2)
			for n, c in enumerate(tri_in_line(cell, 5, (i*2))):
				self.tri.set_cell(c, wheel(self.color + (n * self.color_grade)))

		for corner in all_center_corners():
			cell = tri_in_direction(corner, 5, i*2)
			for n, c in enumerate(tri_in_line(cell, 3, (i*2))):
				self.tri.set_cell(c, wheel(self.color + (n * self.color_grade)))

		for corner in all_right_corners():
			cell = tri_in_direction(corner, 3, i*2)
			for n, c in enumerate(tri_in_line(cell, 1, (i*2))):
				self.tri.set_cell(c, wheel(self.color + (n * self.color_grade)))

	def set_random_colors(self):
		self.color = randColor()
		self.background = randColor()
		self.color_grade = randint(30, 100)
