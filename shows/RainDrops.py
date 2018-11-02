from HelperFunctions import*
from triangle import*

class Drop(object):
	def __init__(self, trimodel, color):
		self.tri = trimodel
		self.color = color
		self.bands = randint(30,50)
		self.center = self.tri.get_rand_cell()
		self.size = randint(0,3)  # Random drop size
		self.currsize = 0
	
	def increase_size(self):
		self.currsize += 1

	def is_full(self):
		return self.currsize > self.size  # True if drop is fully drawn
	
	def draw_drop(self):
		color = (self.color + (self.currsize * self.bands)) % maxColor
		self.tri.set_cells(get_ring(self.center, self.currsize), wheel(color))

				
class Raindrops(object):
    def __init__(self, trimodel):
		self.name = "Raindrops"
		self.tri = trimodel
		self.drops = []	# List that holds Drop objects
		self.speed = 0.1
		self.color = randColor()
		          
    def next_frame(self):
    	
    	while (True):
			
			while len(self.drops) < 20:
				newdrop = Drop(self.tri, self.color)
				self.drops.append(newdrop)
				self.color = randColorRange(self.color, 100)
			
			for d in self.drops:
				d.draw_drop()  # Draw all the drops
				d.increase_size()  # Increase the size of each drop
				if d.is_full():  # Kill a drop if at full size
					self.drops.remove(d)
				
			yield self.speed  	# random time set in init function
			
	
