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
		newspot = tri_in_direction(self.pos, self.dir, 3)	# Where is the bullet shooting?
		if self.tri.is_on_board(newspot):	# Is new spot off the board?
			self.pos = newspot	# On board. Update spot
			self.intense -= 0.05
			return True		# Still traveling
		else:
			return False	# Off board - kill
	
	def set_pos(self, pos):
		self.pos = pos

        		
class Gear(object):
	def __init__(self, trimodel, pos, color, size, turn):
		self.tri = trimodel
		self.size = size
		self.dir = 3
		self.turn = turn
		self.pos = pos
		self.colorchurn = randint(25,100)

	def draw_gear(self, color, clock):
		# Draw the center
		self.tri.set_cell(self.pos, wheel(color))
		
		# Draw the rest of the rings
		for r in range(self.size):
			col = (color + (r * self.colorchurn)) % maxColor
			self.tri.set_cells(get_ring(self.pos, r), wheel(col))
		
		# Draw the outside gear
		ring_cells = get_ring(self.pos, self.size)
		num_cells = len(ring_cells)
		for i in range(num_cells):
			col = (color + (self.size * self.colorchurn)) % maxColor
			if (i + clock) % 2 == 0:
				self.tri.set_cell(ring_cells[i], wheel(col))
	
	def move_gear(self):
		self.pos = tri_in_direction(self.pos, self.dir, 2)
		if self.turn == 1:
			self.dir = turn_right(self.dir)
		else:
			self.dir = turn_left(self.dir)
			
				
class Gears(object):
	def __init__(self, trimodel):
		self.name = "Gears"        
		self.tri = trimodel
		self.gears = []		# List that holds Gears objects
		self.bullets = []	# List that holds Bullet objects
		self.clock = 1000
		self.color = randColor()
		self.speed = 0.2
		          
	def next_frame(self):	
		
		for corner in all_corners():
			new_gear = Gear(self.tri, corner, 100, 2, 1)
			self.gears.append(new_gear)

		for center in all_centers():
			new_gear = Gear(self.tri, center, 100, 2, -1)
			self.gears.append(new_gear)
		
		self.tri.clear()

		while (True):
			
			# Set background to black
			self.tri.set_all_cells((0,0,0))

			# Add a bullet

			new_bullet = Bullet(self.tri, choice(all_centers()), randColor(), randDir())
			self.bullets.append(new_bullet)

			# Draw the Gears
				
			for g in self.gears:
				g.draw_gear(self.color, self.clock)
				g.move_gear()
			
			# Draw the Bullets
			
			for b in self.bullets:
				b.draw_bullet()
				if b.move_bullet() == False:
					self.bullets.remove(b)

			self.clock = (self.clock + 1) % 1000

			self.color = randColorRange(self.color, 30)

			yield self.speed