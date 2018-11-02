from HelperFunctions import*
from triangle import*
        		
class Dendron(object):
	def __init__(self, trimodel, color, pos, dir, life):
		self.tri = trimodel
		self.color = color
		self.pos = pos
		self.dir = dir
		self.life = life

	def draw_dendron(self):
		intensity = 1.0 - (self.life / 50.0)
		self.tri.set_cells(self.tri.mirror_coords(self.pos), white_wheel(self.color, intensity))
							
		if oneIn(4):
			self.dir = turn_left_or_right(self.dir)  # Random chance that path changes
	
	def move_dendron(self):			
		newspot = tri_in_direction(self.pos, self.dir, 1)	# Where is the dendron going?
		if self.tri.is_on_board(newspot) and self.life < 50:	# Is new spot off the board?
			self.pos = newspot	# On board. Update spot
			self.life += 1
			return True
		return False	# Off board. Kill
	

class DendronsTwo(object):
	def __init__(self, trimodel):
		self.name = "DendronsTwo"
		self.tri = trimodel
		self.livedendrons = []	# List that holds Dendron objects
		self.speed = 0.01
		self.maincolor =  randColor()	# Main color of the show
		          
	def next_frame(self):
    	
		while (True):
			
			# Randomly add a center dendron
			if len(self.livedendrons) < 20 and oneIn(5):
				newdendron = Dendron(trimodel=self.tri,
									 color=randColorRange(self.maincolor, 50),
									 pos=choice(all_corners()),
									 dir=maxDir,
									 life=0)
				self.livedendrons.append(newdendron)
				
			for d in self.livedendrons:
				d.draw_dendron()
				
				# Chance for branching
				if oneIn(40):	# Create a fork
					newdir = turn_left_or_right(d.dir)
					newdendron = Dendron(self.tri, d.color, d.pos, newdir, d.life)
					self.livedendrons.append(newdendron)
					
				if not d.move_dendron():  # dendron has moved off the board
					self.livedendrons.remove(d) 	# kill the branch

			if oneIn(50):
				self.maincolor = randColorRange(self.maincolor, 200)
			
			yield self.speed