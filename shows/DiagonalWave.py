from HelperFunctions import*
from triangle import*
        		
class DiagonalWave(object):
	def __init__(self, trimodel):
		self.name = "DiagonalWave"        
		self.tri = trimodel
		self.time = 0
		self.speed = 0.1
		self.width = 12
		self.color = randColor()
		self.background = randColor()

	def get_att(self, width, ring, time):
		saw = (1.0 / width) * (ring + ((100000 - time) % 30))	# Linear sawtooth
		while saw >= 2: saw = saw - 2	# Cut into sawtooth periods
		if saw > 1: saw = 2 - saw	# Descending part of sawtooth
		return saw

	def next_frame(self):

		while (True):
			
			self.draw_background()

			self.draw_bar()
			
			self.time += 1
			
			self.color = (self.color + 5) % maxColor					
			
			yield self.speed
	
	def draw_background(self):
		for i in range (10,0,-1): # total number of triangles
			for corner in all_left_corners():
				self.tri.set_cells(tri_shape(corner, i),
					gradient_wheel(self.background, self.get_att(self.width,10-i,self.time)))
	
	def draw_bar(self):
		i = self.time % 21
		if i > 10:
			i = 20 - i
		for corner in all_left_corners():
			self.tri.set_cells(tri_shape(corner, i),
				gradient_wheel(self.color, self.get_att(self.width, i, self.time)))
