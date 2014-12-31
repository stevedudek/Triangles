from math import exp, sin, radians

from HelperFunctions import*
from triangle import*

class Pincushion(object):
	def __init__(self, trimodel):
		self.name = "Pin Cushion"        
		self.tri = trimodel
		self.pos = []	# List of pin centers
		self.spacing = randint(5,9)
		self.time = 0
		self.speed = 0.02
		self.width = randint(8,20)      
		self.color = randColor()
		self.a = 1	# -1 < a < 1 : sign and intensity of well
		self.c = 5	# Width of well

	def gauss(self, a, c, x):
		return a * exp(- 1 * x * x / (2.0 * c * c))
		
	def next_frame(self):
		
		self.tri.clear()
    	
		while (True):
			
			if self.time == 0:
				self.pos = self.get_pin_centers(self.spacing)
				self.c = randint(2,5)	# Width of well
				
			
			# Draw the rings
			for i in range (self.spacing, 0, -1): # total number of rings - can be bigger than display
				
				x = abs(self.gauss(self.a, self.c, i))
				
				for center in self.pos:
					self.tri.set_cells(get_ring(center, i), gradient_wheel(self.color, 1-x))		
			
			# Slowly change the colors
			
			if oneIn(8):
				self.color = (self.color + 10) % maxColor
							
			# Increase the timer
			
			self.time += 4
			if self.time > 720: self.time = 0
			
			self.a = sin(radians(self.time))

			yield self.speed  	# random time set in init function
			
	def get_pin_centers(self, spacing):
		center_array = []	# List of pin centers
		
		for center in all_centers():
			center_array.append(center)
			for dir in (1,4,5):
				center_array.append(tri_in_direction(center, dir, spacing))
		
		return center_array
