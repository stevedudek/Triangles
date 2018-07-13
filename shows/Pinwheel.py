from HelperFunctions import*
from triangle import*
        		
class Pinwheel(object):
	def __init__(self, trimodel, color, pos, dir, life):
		self.tri = trimodel
		self.color = color
		self.pos = pos
		self.dir = dir
		self.life = life

	def draw_pinwheel(self):
		if self.tri.cell_exists(self.pos):
			color = gradient_wheel(self.color, 1 - self.life / 80.0)
			self.tri.set_cells(self.tri.mirror_coords(self.pos), color)
							
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
		self.name = "Pinwheels"
		self.tri = trimodel
		self.pinwheels = []	# List that holds Pinwheel objects
		self.speed = 0.1
		self.maincolor =  randColor()	# Main color of the show
		          
	def next_frame(self):
    	
		self.tri.clear()

		while (True):
			
			# Randomly add pinwheel
			while len(self.pinwheels) < 6 or oneIn(8):
				newpinwheel = Pinwheel(trimodel=self.tri,
									   color=self.maincolor,
									   pos=self.tri.get_rand_cell(),
									   dir=2,
									   life=0)
				self.pinwheels.append(newpinwheel)
				self.maincolor = randColorRange(self.maincolor, 100)
				
			for p in self.pinwheels:
				p.draw_pinwheel()
				
				# Chance for branching
				if oneIn(50):	# Create a fork
					newdir = turn_left(p.dir) # always fork left
					newpinwheel = Pinwheel(trimodel=self.tri, color=p.color, pos=p.pos, dir=newdir, life=p.life)
					self.pinwheels.append(newpinwheel)
					
				if not p.move_pinwheel():	# pinwheel has moved off the board
					self.pinwheels.remove(p)	# kill the branch
					
			yield self.speed  	# random time set in init function