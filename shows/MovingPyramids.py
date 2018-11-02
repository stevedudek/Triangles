from HelperClasses import*
from triangle import*
from math import sin

class MovingPyramids(object):
	def __init__(self, trimodel):
		self.name = "MovingPyramids"
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
			x = self.get_offset(12, self.time*2)
			corner = tri_in_direction(corner, 0, x)

			for j, triangle in enumerate(inset_triangles(corner, 12-x)):
				color = self.color + (j * 80) + (i * 200)
				self.tri.set_cells(triangle, wheel(color))

		for i, corner in enumerate(all_center_corners()):
			x = self.get_offset(12, self.time*2)
			corner = self.push_down_one(tri_in_direction(corner, 3, x-2))

			for j, triangle in enumerate(inset_triangles(corner, x)):
				color = self.color + (j * 80) + (i * 200)
				self.tri.set_cells(triangle, wheel(color))

	def push_down_one(self, coord):
		x,y = coord
		return (x-1, y)

	def get_offset(self, width, time):
		x = time % (width * 2)
		if x > width:
			x = (width * 2) - x
		return x