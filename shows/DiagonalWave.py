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
		saw = (1.0 / width) * (ring + (time % 1000))	# Linear sawtooth
		while saw >= 2:
			saw = saw - 2	# Cut into sawtooth periods
		if saw > 1:
			saw = 2 - saw	# Descending part of sawtooth
		return saw

	def next_frame(self):

		while (True):
			
			self.draw_background()

			self.draw_bar()
			
			self.time += 1
			
			self.color = (self.color + 5) % maxColor					
			
			yield self.speed
	
	def draw_background(self):
		for i in range (48, 0, -1): # total number of triangles
			intensity = self.get_att(self.width, 46-i, self.time)
			for strip in [0, 3]:
				self.tri.set_cells(tri_shape(left_corner(strip), i), gradient_wheel(self.background, intensity))
	
	def draw_bar(self):
		i = self.time % 48
		if i > 24:
			i = 48 - i
		intensity = self.get_att(self.width, i, self.time)
		for strip in [0,3]:
			self.tri.set_cells(tri_shape(left_corner(strip), i), gradient_wheel(self.color, intensity))
