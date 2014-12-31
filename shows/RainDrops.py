from HelperFunctions import*
from triangle import*

class Drop(object):
	def __init__(self, trimodel, maincolor):
		self.tri = trimodel
		self.color = randColorRange(maincolor, 100)
		self.bands = randint(30,50)
		self.center = self.tri.get_rand_cell()
		self.size = randint(0,3)	# Random drop size
		self.currsize = 0
	
	def increase_size(self):
		self.currsize += 1
		return self.currsize > self.size	# True if drop is fully drawn
	
	def draw_drop(self):
		color = (self.color + (self.currsize * self.bands)) % maxColor
		self.tri.set_cells(get_ring(self.center, self.currsize), wheel(color))

				
class RainDrops(object):
    def __init__(self, trimodel):
		self.name = "rain drops"        
		self.tri = trimodel
		self.drops = []	# List that holds Drop objects
		self.speed = 0.1
		self.maincolor =  randColor()
		          
    def next_frame(self):
    	
    	while (True):
			
			while len(self.drops) < 20:
				newdrop = Drop(self.tri, self.maincolor)
				self.drops.append(newdrop)
			
			# Draw all the drops
			# Increase the size of each drop - kill a drop if at full size
			for d in self.drops:
				d.draw_drop()
				if d.increase_size() == True:
					self.drops.remove(d)
				
			yield self.speed  	# random time set in init function
			
	
