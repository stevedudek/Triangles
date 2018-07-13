from HelperFunctions import*
from triangle import*
from math import sin
        		
class SwirlingCenter(object):
	def __init__(self, trimodel):
		self.name = "SwirlingCenter"        
		self.tri = trimodel
		self.time = 0
		self.speed = 0.05
		self.width = randint(1,8)
		self.color = randColor()

	def get_att(self, width, ring, time):
		return (sin(2 * 3.1415 * ((ring + time) % width) / width) + 1) * 0.5

	def next_frame(self):

		while (True):
			
			self.draw_nested_triangles()
			self.color = randColorRange(self.color, 50)
			self.time += 1

			if oneIn(20):
				self.width = upORdown(self.width, 1, 1, 8)
			yield self.speed

	def draw_nested_triangles(self):
		for k, corner in enumerate(all_left_corners()):
			for j, triangle in enumerate(nested_triangles(corner)):
				ring_size = len(triangle)
				for i, cell in enumerate(triangle):
					adj_color = self.color + (j * 40)
					color = gradient_wheel(adj_color, self.get_att(ring_size / (1 + ((k + self.width) % 7)) , i, self.time))
					self.tri.set_cell(cell, color)
