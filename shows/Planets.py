from HelperFunctions import*
from triangle import*

class Bullet(object):
	def __init__(self, trimodel, pos, color, dir):
		self.tri = trimodel
		self.color = color
		self.dir = dir
		self.pos = pos
		self.intense = 1
			
	def draw_bullet(self):
		self.tri.set_cell(self.pos, gradient_wheel(self.color, self.intense))
	
	def move_bullet(self):
		newspot = tri_in_direction(self.pos, self.dir, 1)	# Where is the bullet shooting?
		if self.tri.cell_exists(newspot):	# Is new spot off the board?
			self.pos = newspot	# On board. Update spot
			self.intense -= 0.05
			return True		# Still traveling
		else:
			return False	# Off board - kill


class Trail(object):
	def __init__(self, trimodel, color, intense, pos):
		self.tri = trimodel
		self.pos = pos
		self.color = color
		self.intense = intense
	
	def draw_trail(self):
		self.tri.set_cell(self.pos, gradient_wheel(self.color, self.intense))
	
	def fade_trail(self):
		self.intense -= 0.15
		if self.intense > 0: return True
		else: return False

        		
class Planet(object):
	def __init__(self, trimodel, pos, arc, color, size):
		self.tri = trimodel
		self.pos = pos
		self.color = color
		self.rotation = randint(0,1)
		self.dir = randDir()
		self.arc = arc
		self.arc_count = arc
		self.size = size
		self.trails = []	# List that holds trails
		self.life = randint(20,300)
		
	def draw_planet(self):
		
		self.fade_trails()
			
		# Draw the center
		self.draw_add_trail(self.color, 1, self.pos)
		
		# Draw an outer ring(s)
		for i in range(self.size):
			for c in get_ring(self.pos, i):
				self.draw_add_trail(self.color, 1, c)
	
	
	def move_planet(self):
		self.pos = tri_in_direction(self.pos, self.dir, 2)
		self.arc_count -= 1
		if self.arc_count == 0:
			self.arc_count = self.arc
			if self.rotation == 0:
				self.dir = turn_left(self.dir)
			else:
				self.dir = turn_right(self.dir)
		
		self.life -= 1
		if self.life > 0:
			return True
		else:
			return False
		
	def draw_add_trail(self, color, intense, pos):
		self.tri.set_cell(pos, gradient_wheel(color, intense))
		new_trail = Trail(self.tri, color, intense, pos)
		self.trails.append(new_trail)
	
	def fade_trails(self):
		for t in reversed(self.trails):	# Plot last-in first
			t.draw_trail()
			if t.fade_trail() == False:
				self.trails.remove(t)
						
class Planets(object):
	def __init__(self, trimodel):
		self.name = "Planets"        
		self.tri = trimodel
		self.planets = []	# List that holds Planet objects
		self.bullets = []	# List that holds Bullet objects
		self.speed = 0.05
		self.color = randColor()
		          
	def next_frame(self):
		
		self.tri.clear()

		while (True):
			
			if len(self.planets) < 10:
				new_center = choice(all_centers())
				new_planet = Planet(self.tri,
					choice(get_ring(new_center, 3)),
					randint(2,6),
					randColor(), 2)
				self.planets.append(new_planet)
			
			# Set background to black
			self.tri.set_all_cells((0,0,0))
			
			# Draw the Planets
				
			for p in self.planets:
				p.draw_planet()
				if p.move_planet() == False:
					
					for dir in range(maxDir):	# Cause explosion of bullets
						bull_color = randColorRange(p.color, 50)
						new_bullet = Bullet(self.tri, p.pos, bull_color, dir)
						self.bullets.append(new_bullet)
						
					self.planets.remove(p)	# Kill Planet
			
			# Draw the Bullets
			
			for b in self.bullets:
				b.draw_bullet()
				if b.move_bullet() == False:
					self.bullets.remove(b)
					
			# Change the colors
			
			self.color = (self.color + 10) % maxColor
			
			yield self.speed