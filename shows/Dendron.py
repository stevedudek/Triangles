from HelperFunctions import*
from triangle import*
        		
class Dendron(object):
	def __init__(self, trimodel, color, pos, dir, life):
		self.tri = trimodel
		self.color = color
		self.pos = pos
		self.dir = dir
		self.life = life	# How long the branch has been around

	def draw_dendron(self, inversion):
		if inversion:
			ratio = self.life/100.0 # dark center
		else:
			ratio = 1 - self.life/100.0 # light center
			
		# color the 3 mirrored coordinates
		self.tri.set_cells(self.tri.mirror_coords(self.pos),
			gradient_wheel(self.color, ratio))
							
		# Random chance that path changes
		if oneIn(4):
			self.dir = turn_left_or_right(self.dir)
	
	def move_dendron(self):			
		newspot = tri_in_direction(self.pos, self.dir, 1)	# Where is the dendron going?
		if self.tri.cell_exists(newspot) and self.life < 50:	# Is new spot off the board?
			self.pos = newspot	# On board. Update spot
			self.life += 1
			return True
		return False	# Off board. Kill.
	

				
class Dendrons(object):
	def __init__(self, trimodel):
		self.name = "Dendrons"        
		self.tri = trimodel
		self.livedendrons = []	# List that holds Dendron objects
		self.speed = 0.02
		self.maincolor =  randColor()	# Main color of the show
		self.inversion = randint(0,1)	# Toggle for effects
		          
	def next_frame(self):
    	
		while (True):
			
			# Randomly add a center dendron
			
			if len(self.livedendrons) < 20 and oneIn(5):
				newdendron = Dendron(self.tri,
						randColorRange(self.maincolor, 50), 	# color
						choice(all_centers()), 	# center
						maxDir,
						0)					# Life = 0 (new branch)
				self.livedendrons.append(newdendron)
				
			for d in self.livedendrons:
				d.draw_dendron(self.inversion)
				
				# Chance for branching
				if oneIn(20):	# Create a fork
					newdir = turn_left_or_right(d.dir)
					newdendron = Dendron(self.tri, d.color, d.pos, newdir, d.life)
					self.livedendrons.append(newdendron)
					
				if d.move_dendron() == False:	# dendron has moved off the board
					self.livedendrons.remove(d)	# kill the branch

			# Randomly change the main color
			if oneIn(20):
				self.maincolor = randColorRange(self.maincolor, 100)				
			
			yield self.speed