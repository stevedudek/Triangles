from HelperClasses import*
from triangle import*
from math import sin

class Pyramids(object):
	def __init__(self, trimodel):
		self.name = "Pyramids"
		self.tri = trimodel
		self.time = 0
		self.speed = 0.1
		self.color = randColor()

	def next_frame(self):

		while (True):
			
			self.tri.black_all_cells()

			self.draw_inset_triangles()

			self.time += 1
			
			self.color = (self.color + 2) % maxColor					
			
			yield self.speed
	
	def draw_inset_triangles(self):
		for i, corner in enumerate(all_left_corners()):
			for j, triangle in enumerate(inset_triangles(corner)):
				num_cells = len(triangle)
				for k, cell in enumerate(triangle):
					color = self.color + (j * 80)
					l = num_cells - k - 1 if j % 2 else k
					intensity = self.get_att(num_cells, l, self.time)
					self.tri.set_cell(cell, gradient_wheel(color, intensity))

	def get_att(self, width, ring, time):
		return (sin(2 * 3.1415 * ((ring + time) % width) / width) + 2) * 0.5