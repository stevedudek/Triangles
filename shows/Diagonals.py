from HelperFunctions import*
from triangle import*
        		
class Diagonals(object):
	def __init__(self, trimodel):
		self.name = "Diagonals"        
		self.tri = trimodel
		self.time = 0
		self.speed = 0.1
		self.width = 12
		self.color = randColor()
		self.background = randColor()

	def get_att(self, width, ring, time):
		saw = (1.0 / width) * (ring + (time % 1000))	# Linear sawtooth
		while saw >= 2:
			saw = saw - 2	# Cut into sawtooth periods
		if saw > 1:
			saw = 2 - saw	# Descending part of sawtooth
		return saw

	def next_frame(self):

		self.tri.set_all_cells(wheel(self.background))

		while (True):
			
			self.draw_triangles(self.color)
			
			self.time += 1
			
			self.color = (self.color + 5) % maxColor					
			
			yield self.speed
	
	# concentric triangles of decreasing intensities

	def draw_triangles(self, color):
		for i in range (12, 0, -2):  # total number of triangles
			intensity = self.get_att(self.width, i, self.time)
			for corner in all_left_corners():
				self.tri.set_cells(tri_shape(corner, i), gradient_wheel(color, intensity))
