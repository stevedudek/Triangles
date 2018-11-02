from HelperFunctions import*
from triangle import*
from math import sin
        		
class Spinner(object):
	def __init__(self, trimodel, pos):
		self.tri = trimodel
		self.pos = pos
		self.expand = 0	# -1: contracting, 0: nothing, 1: expanding
		self.size = 2
	
	def explode_spinner(self):
		self.expand = 1
	
	def is_resting(self):
		return self.expand == 0

	def draw_spinner(self, spincolor, explodecolor, time):
		color = spincolor if self.expand == 0 else explodecolor

		self.tri.set_cell(self.pos, wheel(color))  # Draw the center
		
		# Draw the spinning bits
		for i in range(0, self.size + 1):
			ringcells = get_ring(self.pos, i)
			num = len(ringcells)
			if num > 0:
				for j in range(num):
					intensity = (sin(2 * 3.1415 * ((j + time) % num) / num) + 1) * 0.5
					self.tri.set_cell(ringcells[j], gradient_wheel(color, intensity))
	
	def move_spinner(self):
		self.size += self.expand
		if self.size > 12:
			self.expand = -1  # Contract!
		if self.size <= 0:
			self.expand = 0	 # Done
		
			
				
class ExplodingSpinners(object):
	def __init__(self, trimodel):
		self.name = "Exploding spinners"        
		self.tri = trimodel
		self.spinners = []	# List that holds Spinner objects
		self.speed = 0.05
		self.explodecolor = randColor()  # Color for exploding spinner
		self.spincolor =  randColor()  # Spinner color
		self.time = 0
		          
	def next_frame(self):

		self.set_up_spinners()

		while (True):
	
			# Draw the spinners - draw exploding spinners last
				
			for s in self.spinners:
				s.draw_spinner(self.spincolor, self.explodecolor, self.time)
				if not s.is_resting():
					s.move_spinner()
			
			self.time += 1
			
			if self.all_resting() and oneIn(20):
				choice(self.spinners).explode_spinner()  # Explode a spinner
			
			# Change the colors
			
			self.explodecolor = (self.explodecolor + 10) % maxColor					
			
			self.spincolor = (maxColor + self.spincolor - 2) % maxColor
			
			yield self.speed
	
	def all_resting(self):
		return all([s.is_resting() for s in self.spinners])

	def set_up_spinners(self):
		self.spinners.extend([Spinner(self.tri, coord) for coord in all_centers() + all_corners()])