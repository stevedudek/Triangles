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
		if self.tri.is_on_board(newspot):	# Is new spot off the board?
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

	def is_alive(self):
		return self.intense > 0

        		
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
		self.life = randint(20, 300)
		
	def draw_planet(self):
		
		self.fade_trails()
		self.draw_add_trail(self.color, 1, self.pos)  # Draw the center
		
		# Draw an outer ring(s)
		for i in range(self.size):
			for c in get_ring(self.pos, i):
				self.draw_add_trail(self.color, 1, c)
	
	def move_planet(self):
		self.pos = tri_in_direction(self.pos, self.dir, 2)
		self.arc_count -= 1
		self.life -= 1
		if self.arc_count == 0:
			self.arc_count = self.arc
			self.dir = turn_left(self.dir) if self.rotation == 0 else turn_right(self.dir)

	def is_alive(self):
		return self.life > 0
		
	def draw_add_trail(self, color, intense, pos):
		self.tri.set_cell(pos, gradient_wheel(color, intense))
		new_trail = Trail(self.tri, color, intense, pos)
		self.trails.append(new_trail)
	
	def fade_trails(self):
		for t in reversed(self.trails):	# Plot last-in first
			t.draw_trail()
			t.fade_trail()
			if not t.is_alive():
				self.trails.remove(t)

	def kill_trails(self):
		for t in self.trails:
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
				new_planet = Planet(trimodel=self.tri,
									pos=choice(get_ring(choice(all_centers()), 3)),
									arc=randint(2,6),
									color=randColor(),
									size=choice([1,2,3])
									)
				self.planets.append(new_planet)
			
			self.tri.black_all_cells()
			
			for p in self.planets:
				p.draw_planet()
				p.move_planet()

				if not p.is_alive():
					for dir in range(maxDir):	# Cause explosion of bullets
						self.bullets.append(Bullet(trimodel=self.tri,
												   pos=p.pos,
												   color=randColorRange(p.color, 50),
												   dir=dir))
					p.kill_trails()
					self.planets.remove(p)	# Kill Planet
			
			for b in self.bullets:
				b.draw_bullet()
				if not b.move_bullet():
					self.bullets.remove(b)
					
			self.color = (self.color + 10) % maxColor
			
			yield self.speed