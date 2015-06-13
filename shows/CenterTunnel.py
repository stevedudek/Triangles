from HelperFunctions import*
from triangle import*
        		
class CenterTunnel(object):
	def __init__(self, trimodel):
		self.name = "CenterTunnel"        
		self.tri = trimodel
		self.time = 0
		self.speed = 0.2
		self.width = 12
		self.color = randColor()

	def get_att(self, width, ring, time):
		saw = (1.0 / width) * (ring + (time % 1000))	# Linear sawtooth
		while saw >= 2: saw = saw - 2	# Cut into sawtooth periods
		if saw > 1: saw = 2 - saw	# Descending part of sawtooth
		return saw

	def next_frame(self):

		while (True):
			
			self.draw_nested_triangles()
			
			self.time += 1
			
			self.color = (self.color + 5) % maxColor					
			
			yield self.speed

		
	
	def draw_nested_triangles(self):
		for corner in all_left_corners():
			nested_cells = nested_triangles(corner)
			num_nests = len(nested_cells)	# Total number of concentric triangles

			for i in range(num_nests):
				self.tri.set_cells(nested_cells[i],
					gradient_wheel(self.color, self.get_att(num_nests*1.5,i,self.time)))
