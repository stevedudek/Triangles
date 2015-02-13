from HelperFunctions import*
from triangle import*
        		
class Pinwheel(object):
	def __init__(self, trimodel, color, pos, dir, life):
		self.tri = trimodel
		self.color = color
		self.pos = pos
		self.dir = dir
		self.life = life	# How long the branch has been around

	def draw_pinwheel(self):
		if self.tri.cell_exists(self.pos):
			self.tri.set_cells(self.tri.mirror_coords(self.pos),
				gradient_wheel(self.color, 1 - self.life/80.0))
							
		# Random chance that path changes - spirals only in one direction
		if oneIn(2):
			self.dir = turn_left(self.dir)
	
	def move_pinwheel(self):			
		newspot = tri_in_direction(self.pos, self.dir, 1)	# Where is the pinwheel going?
		if self.tri.is_on_board(newspot) and self.life < 10:	# Is new spot off the board?
			self.pos = newspot	# On board. Update spot
			self.life += 1
			return True
		else:
			return False	# Off board. Kill.

				
class Pinwheels(object):
	def __init__(self, trimodel):
		self.name = "Pinwheel"        
		self.tri = trimodel
		self.livepinwheels = []	# List that holds Pinwheel objects
		self.speed = 0.1
		self.maincolor =  randColor()	# Main color of the show
		          
	def next_frame(self):
    	
		self.tri.clear()

		while (True):
			
			# Randomly add pinwheel
			
			while len(self.livepinwheels) < 6 or oneIn(8):
				newpinwheel = Pinwheel(self.tri,
						self.maincolor, 		
						self.tri.get_rand_cell(), 	# random placement
						2, 						# Always heading southeast
						0)						# Life = 0 (new pinwheel)
				self.livepinwheels.append(newpinwheel)
				
			for p in self.livepinwheels:
				p.draw_pinwheel()
				
				# Chance for branching
				if oneIn(50):	# Create a fork
					newdir = turn_left(p.dir) # always fork left
					newpinwheel = Pinwheel(self.tri, p.color, p.pos, newdir, p.life)
					self.livepinwheels.append(newpinwheel)
					
				if p.move_pinwheel() == False:	# pinwheel has moved off the board
					self.livepinwheels.remove(p)	# kill the branch
			
			self.maincolor = (self.maincolor + 3) % maxColor
					
			yield self.speed  	# random time set in init function