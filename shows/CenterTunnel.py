from HelperFunctions import*
from triangle import*
from math import sin
        		
class CenterTunnel(object):
	def __init__(self, trimodel):
		self.name = "CenterTunnel"        
		self.tri = trimodel
		self.time = 0
		self.speed = 0.05
		self.color = randColor()

	def get_att(self, width, ring, time):
		return (sin(2 * 3.1415 * ((ring + time) % width) / width) + 1) * 0.5

	def next_frame(self):

		while (True):
			
			self.draw_nested_triangles()
			
			self.time += 0.5
			
			self.color = (self.color + 5) % maxColor					
			
			yield self.speed

	def draw_nested_triangles(self):
		for j,corner in enumerate(all_left_corners()):
			nested_cells = nested_triangles(corner)
			num_nests = len(nested_cells)	# Total number of concentric triangles

			for i,cell in enumerate(nested_cells):
				self.tri.set_cells(cell,
					gradient_wheel(self.color, self.get_att(num_nests * 3, i, self.time)))
