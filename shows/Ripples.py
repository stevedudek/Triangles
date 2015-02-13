from HelperFunctions import*
from triangle import*

class Ripples(object):
    def __init__(self, trimodel):
        self.name = "Ripples"        
        self.tri = trimodel
        self.center = self.tri.get_rand_cell()
        self.time = 0
        self.speed = 0.1 + (random() / 2)
        self.width = randint(8,20)      
        self.color = randColor()
    
    def get_att(self, width, ring, time):
		saw = (1.0 / width) * (ring + ((100000 - time) % 30))	# Linear sawtooth
		while saw >= 2: saw = saw - 2	# Cut into sawtooth periods
		if saw > 1: saw = 2 - saw	# Descending part of sawtooth
		return saw 
		          
    def next_frame(self):
    	
    	while (True):
			
			# Draw the rings
			for i in range (28): # total number of rings - can be bigger than display
				self.tri.set_cells(get_ring(self.center, i),
					gradient_wheel(self.color, self.get_att(self.width,i,self.time)))
			
			# Slowly change the colors
			self.color = (self.color + 5) % maxColor
			
			# Move the center of the ripple like a drunken mason
			if oneIn(5):
				newtri = choice(neighbors(self.center))
				if self.tri.is_on_board(newtri):
					self.center = newtri
				
			self.time = (self.time + 1) % 100000	# Advance the timer

			yield self.speed  	# random time set in init function