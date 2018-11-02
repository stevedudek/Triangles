from HelperFunctions import*
from triangle import*

class Gear(object):
	def __init__(self, trimodel, pos):
		self.tri = trimodel
		self.size = choice([1,2,3])
		self.dir = 3
		self.turn = self.size % 2
		self.pos = pos
		self.colorchurn = randint(25,100)

	def draw_gear(self, color, clock):
		color += (self.size * 100)
		self.tri.set_cell(self.pos, wheel(color))  # Draw the center
		
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
		self.dir = turn_right(self.dir) if self.turn == 1 else turn_left(self.dir)

				
class Gears(object):
	def __init__(self, trimodel):
		self.name = "Gears"        
		self.tri = trimodel
		self.gears = []		# List that holds Gears objects
		self.clock = 1000
		self.color = randColor()
		self.speed = 0.08
		          
	def next_frame(self):	

		self.gears.extend([Gear(trimodel=self.tri, pos=coord) for coord in all_corners() + all_centers()])

		self.tri.clear()

		while (True):
			
			self.tri.black_all_cells()

			for g in self.gears:
				g.draw_gear(self.color, self.clock)
				g.move_gear()
			
			self.clock += 1

			self.color = randColorRange(self.color, 30)

			yield self.speed