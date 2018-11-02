from HelperFunctions import*
from triangle import*
        		
class Branch(object):
	def __init__(self, trimodel, color, pos, dir, life):
		self.tri = trimodel
		self.color = color
		self.pos = pos
		self.dir = dir
		self.life = life	# How long the branch has been around

	def draw_branch(self, inversion):
		ratio = self.life / 10.0 if inversion else 1 - self.life / 40.0
		self.tri.set_cell(self.pos, gradient_wheel(self.color, ratio))
							
		# Random chance that path changes
		if oneIn(3):
			self.dir = turn_left_or_right(self.dir)
	
	def move_branch(self):			
		newspot = tri_in_direction(self.pos, self.dir, 1)	# Where is the branch going?
		if self.tri.is_on_board(newspot) and self.life < 40:# Is new spot off the board?
			self.pos = newspot	# On board. Update spot
			self.life += 1
			return True
		return False	# Off board. Pick a new direction
				
				
class CenterBranches(object):
	def __init__(self, trimodel):
		self.name = "Center Branches"        
		self.tri = trimodel
		self.livebranches = []	# List that holds Branch objects
		self.speed = 0.05
		self.maincolor =  randColor()	# Main color of the show
		self.inversion = randint(0,1)	# Toggle for effects
		          
	def next_frame(self):
    	
		while (True):
			
			# Add a center branch
			
			if len(self.livebranches) == 0 or oneIn(10):
				for center in all_centers():
					newbranch = Branch(trimodel=self.tri,
									   color=self.maincolor,
									   pos=center,
									   dir=randDir(),
									   life=0)
					self.livebranches.append(newbranch)
				self.maincolor = (self.maincolor + 50) % maxColor
				
			for b in self.livebranches:
				b.draw_branch(self.inversion)
				
				# Chance for branching
				if oneIn(20):	# Create a fork
					newdir = turn_left_or_right(b.dir)
					newbranch = Branch(self.tri, b.color, b.pos, newdir, b.life)
					self.livebranches.append(newbranch)
					
				if b.move_branch() == False:	# branch has moved off the board
					self.livebranches.remove(b)	# kill the branch
			
			yield self.speed