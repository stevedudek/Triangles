from math import exp, sin, radians

from HelperFunctions import*
from triangle import*

class Well(object):
	def __init__(self, trimodel):
		self.name = "Well"        
		self.tri = trimodel
		self.dir = randDir()
		self.time = 0
		self.speed = 0.05
		self.color = randColor()
		self.a = 1.0	# -1 < a < 1 : sign and intensity of well
		self.c = randint(2,6)	# Width of well

	def gauss(self, a, c, x):
		return a * exp(- 1 * x * x / (2.0 * c * c))
		  
	def next_frame(self):
    	
		while (True):
				
			# Draw the rings
			for i in range (8,0,-1): # total number of rings - can be bigger than display
				
				x = abs(self.gauss(self.a, self.c, i))
		
				for center in all_centers():
					self.tri.set_cells(get_ring(center, i),gradient_wheel(self.color, 1-x))
			
			# Increase the timer
			
			self.time += 4

			if self.time > 720:
				self.time = 0
				self.color = randColorRange(self.color, 50)
				self.c = randint(2,6)	# Width of well
			
			self.a = sin(radians(self.time))

			yield self.speed
			