from HelperFunctions import*
from triangle import*
        		
class DiagonalsSolidRed(object):
	def __init__(self, trimodel):
		self.name = "Diagonals"        
		self.tri = trimodel
		self.time = 0
		self.speed = 0.1
		self.width = 12
		self.color = 156
		self.background = 250 

	def get_att(self, width, ring, time):
		saw = (1.0 / width) * (ring + ((100000 - time) % 30))	# Linear sawtooth
		while saw >= 2: saw = saw - 2	# Cut into sawtooth periods
		if saw > 1: saw = 2 - saw	# Descending part of sawtooth
		return saw

	def next_frame(self):

		for i in range (12,0,-1): # total number of triangles
			for corner in all_left_corners():
				self.tri.set_cells(tri_shape(corner, i),
					(0,0,0))

		while (True):
			
			self.draw_background()
			
			self.time += 1
			
		#	self.color = (self.color + 5) % maxColor					
			yield self.speed
	
	# Draw the background - concentric triangles of decreasing intensities
	
	def draw_background(self):
		for i in range (10,0,-2): # total number of triangles
			for corner in all_left_corners():
				self.tri.set_cells(tri_shape(corner, i),(255,0,0))
			#		gradient_wheel(self.color, self.get_att(self.width,i,self.time)))
