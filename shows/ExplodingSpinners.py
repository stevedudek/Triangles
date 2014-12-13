from HelperFunctions import*
from triangle import*
        		
class Spinner(object):
	def __init__(self, trimodel, pos):
		self.tri = trimodel
		self.pos = pos
		self.expand = 0	# -1: contracting, 0: nothing, 1: expanding
		self.size = 1
	
	def explode_spinner(self):
		self.expand = 1
	
	def is_resting(self):
		if self.expand == 0:
			return True
		else:
			return False

	def draw_spinner(self, spincolor, explodecolor, time):
		if self.expand == 0:
			color = spincolor
		else:
			color = explodecolor
			
		# Draw the center
		self.tri.set_cell(self.pos, wheel(color))
		
		# Draw the spinning bits
		for i in range(0, self.size + 1):
			ringcells = get_ring(self.pos, i)
			num = len(ringcells)
			if num > 0:
				for j in range(num):
					gradient = 1 - (abs(j - (time % num)) / (num - 0.0) )
					self.tri.set_cell(ringcells[j], gradient_wheel(color, gradient))
	
	def move_spinner(self):
		newspot = tri_in_direction(self.pos, randDir(), 2)
		if self.tri.cell_exists(newspot):
			self.pos = newspot
			
		if self.expand == 1:
			self.size += 1
			if self.size > 12:
				self.expand = -1	# Contract!
		elif self.expand == -1:
			self.size -= 1
			if self.size <= 1:
				self.expand = 0	# Done
		
			
				
class ExplodingSpinners(object):
	def __init__(self, trimodel):
		self.name = "Exploding spinners"        
		self.tri = trimodel
		self.spinners = []	# List that holds Spinner objects
		self.speed = 0.05
		self.explodecolor = randColor()	# Color for exploding spinner
		self.spincolor =  randColor()	# Spinner color
		self.time = 0
		          
	def next_frame(self):

		self.set_up_spinners()

		while (True):
	
			# Draw the spinners - draw exploding spinners last
				
			for s in self.spinners:
				if s.is_resting():
					s.draw_spinner(self.spincolor, self.explodecolor, self.time)
				
			for s in self.spinners:
				if s.is_resting() == False:
					s.draw_spinner(self.spincolor, self.explodecolor, self.time)
					s.move_spinner()
			
			self.time += 1
			
			# Explode a spinner
			
			if self.all_resting() == True and oneIn(20):
				choice(self.spinners).explode_spinner()
			
			# Change the colors
			
			self.explodecolor = (self.explodecolor + 10) % maxColor					
			
			self.spincolor = (maxColor + self.spincolor - 2) % maxColor
			
			yield self.speed  	# random time set in init function
	
	# all_resting

	def all_resting(self):
		for s in self.spinners:
			if s.is_resting() == False:
				return False
		return True

	# Initialize the spinners

	def set_up_spinners(self):
		for center in all_centers():
			newspinner = Spinner(self.tri, center)
			self.spinners.append(newspinner)

		for corner in all_corners():
			newspinner = Spinner(self.tri, corner)
			self.spinners.append(newspinner)