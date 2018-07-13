from HelperFunctions import*
from triangle import*
        		
class Swirl(object):
	def __init__(self, trimodel, color, pos, dir, sym, life):
		self.tri = trimodel
		self.color = color
		self.pos = pos
		self.dir = dir
		self.sym = sym	# 0, 1, 2, 3 = 1x, 2x, 3x, 6x symmetric
		self.life = life	# How long the branch has been around

	def draw_swirl(self):
		color = gradient_wheel(self.color, 1 - self.life / 50.0)
		if self.tri.cell_exists(self.pos):
			self.tri.set_cells(self.multi_mirror_tri(self.pos, self.sym), color)
							
		# Random chance that path changes - spirals only in one direction
		if oneIn(2):
			self.dir = turn_left(self.dir)
	
	def move_swirl(self):			
		newspot = tri_in_direction(self.pos, self.dir, 1)	# Where is the swirl going?
		if self.tri.is_on_board(newspot) and self.life < 30:	# Is new spot off the board?
			self.pos = newspot	# On board. Update spot
			self.life += 1
			return True
		return False	# Off board. Kill.

	# Find the other mirrored tri for a given tri
	# Symmetry is variable: 0, 1, 2, 3 = 1, 2, 2, or 3 mirrors
	def multi_mirror_tri(self, coord, sym):
		if sym == 0:
			return coord
		elif sym == 1:
			return list([coord, self.tri.rotate_right(coord)])
		elif sym == 2:
			return self.tri.mirror_coords(coord)
		else:
			return self.tri.six_mirror(coord)
	
				
class Swirls(object):
	def __init__(self, trimodel):
		self.name = "Swirls"        
		self.tri = trimodel
		self.liveswirls = []	# List that holds Swirl objects
		self.speed = 0.1
		self.maincolor = randColor()
		          
	def next_frame(self):
    	
		while (True):
			
			if not self.liveswirls or oneIn(20):
				for center in all_centers():
					self.liveswirls.append(Swirl(trimodel=self.tri,
												 color=self.maincolor,
												 pos=center,
												 dir=randDir(),
												 sym=randint(0,3),
												 life=0))
					self.maincolor = (self.maincolor + 20) % maxColor
				
			for s in self.liveswirls:
				s.draw_swirl()
				
				# Chance for branching
				if oneIn(15):	# Create a fork
					newdir = turn_left(s.dir) # always fork left
					newswirl = Swirl(self.tri, s.color, s.pos, newdir, s.sym, s.life)
					self.liveswirls.append(newswirl)
					
				if not s.move_swirl():	# Swirl has moved off the board
					self.liveswirls.remove(s)	# kill the branch
			
			yield self.speed