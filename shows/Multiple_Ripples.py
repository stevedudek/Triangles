from HelperFunctions import*
from triangle import*

class Rip(object):
	def __init__(self, trimodel):
		self.tri = trimodel
		self.center = self.tri.get_rand_cell()
		self.lifetime = randint(20,100)	# Time ripple lives
	
	def decrease_time(self):
		self.lifetime -= 1
		return self.lifetime	# True is still have life; False if life = 0
				
class Multiple_Ripples(object):
    def __init__(self, trimodel):
        self.name = "Multiple_Ripples"        
        self.tri = trimodel
        self.rips = []	# List that holds Rip objects
        
        self.time = 0
        self.speed = 0.01
        self.width = randint(8,20)      
        self.color = randColor() 
    
    def get_att(self, width, ring, time):
		saw = (1.0 / width) * (ring + ((100000 - time) % 30))	# Linear sawtooth
		while saw >= 2: saw = saw - 2	# Cut into sawtooth periods
		if saw > 1: saw = 2 - saw	# Descending part of sawtooth
		return saw 
		          
    def next_frame(self):
    	
    	self.tri.clear()

    	while (True):
			
			# Check how many rips are in play
			# If no rips, add one. If rips < 6 then add one more randomly
			while len(self.rips) < 4 or oneIn(20):
				newrip = Rip(self.tri)
				self.rips.append(newrip)
			
			# Draw the rings
			for i in range (8): # total number of rings - can be bigger than display
				for r in self.rips:
					self.tri.set_cells(get_ring(r.center, i),
						gradient_wheel(self.color, self.get_att(self.width,i,self.time)))
			
			# Slowly change the colors
			self.color = (self.color + 1) % maxColor
			
			# Decrease the life of each ripple - kill a ripple if life is zero
			for r in self.rips:
				if r.decrease_time == 0:
					self.rips.remove(r)
				
			self.time = (self.time + 1) % 100000	# Advance the timer
	
			yield self.speed  	# random time set in init function
			
			