from HelperFunctions import*
from triangle import*

class Trail(object):
	def __init__(self, trimodel, color, intense, pos, center):
		self.tri = trimodel
		self.pos = pos
		self.color = color
		self.intense = intense
		self.center = center
	
	def draw_trail(self):
		self.tri.set_cell(self.pos, gradient_wheel(self.color, self.intense))
	
	def fade_trail(self):
		
		self.pos = near_neighbor(self.pos, self.center)
		self.intense *= 0.9
		if self.intense > 0.05:
			return True
		else:
			return False		
       		
class Planet(object):
	def __init__(self, trimodel, pos, color, dir, center):
		self.tri = trimodel
		self.pos = pos
		self.color = color
		self.rotation = randint(0,1)
		self.dir = dir
		self.arc = randint(3,6)
		self.arc_count = self.arc
		self.size = 2
		self.center = center
		self.trails = []	# List that holds trails
		
	def draw_planet(self):
		
		self.fade_trails()
		
		for i in range(2):
			for c in get_ring(self.pos, i):	
				self.draw_add_trail(self.color, 1-(0.07*i), c, self.center)
	
	def move_planet(self):
		self.pos = tri_in_direction(self.pos, self.dir, 2)
		self.arc_count -= 1
		if self.arc_count == 0:
			self.arc_count = self.arc
			if self.rotation == 0:
				self.dir = turn_left(self.dir)
			else:
				self.dir = turn_right(self.dir)
		
	def draw_add_trail(self, color, intense, pos, center):
		if self.tri.cell_exists(pos):
			self.tri.set_cell(pos, gradient_wheel(color, intense))
			new_trail = Trail(self.tri, color, intense, pos, center)
			self.trails.append(new_trail)
	
	def fade_trails(self):
		for t in reversed(self.trails):	# Plot last-in first
			t.draw_trail()
			if t.fade_trail() == False:
				self.trails.remove(t)
			
				
class Circling(object):
	def __init__(self, trimodel):
		self.name = "Circling"        
		self.tri = trimodel
		self.planets = []	# List that holds Planet objects
		self.speed = 0.05
		self.dir = 0
		self.color = randColor()
		          
	def next_frame(self):
		
		self.tri.clear()

		for strip in range(6):
			for corner in corners(strip):
				new_planet = Planet(self.tri, corner, self.color, self.dir, center(strip))
				self.planets.append(new_planet)
				self.color = (self.color + 40) % maxColor
				self.dir = turn_left(self.dir)

			
		while (True):
			
			# Set background to black
			self.tri.set_all_cells((0,0,0))
			
			for p in self.planets:
				p.draw_planet()
				p.move_planet()
			
			yield self.speed  	# random time set in init function