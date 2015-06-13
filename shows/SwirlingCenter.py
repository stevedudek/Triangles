from HelperFunctions import*
from triangle import*
from math import sin
        		
class SwirlingCenter(object):
	def __init__(self, trimodel):
		self.name = "SwirlingCenter"        
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

			for i in range(len(nested_cells)):
				ring_size = len(nested_cells[i])
				for j in range(ring_size):
					self.tri.set_cell(nested_cells[i][j],
						gradient_wheel(self.color,
							self.get_att(ring_size/5,j,self.time)))
