from HelperFunctions import*
from triangle import*
        		
class Spinner(object):
	def __init__(self, trimodel, pos):
		self.tri = trimodel
		self.pos = pos
		self.start = pos
		self.time = 0

	def move_spinner(self):
		newspot = tri_in_direction(self.pos, randDir(), 2)
		if self.tri.is_on_board(newspot):
			self.pos = newspot
		if self.time > 100:
			self.time = 0
			self.pos = self.start

	def draw_spinner(self, color):
		self.time += 1
		for size in range(4):
			ring_cells = get_ring(self.pos, size)
			num_cells = len(ring_cells)
			for i, cell in enumerate(ring_cells):
				if self.tri.is_on_board(cell):
					gradient = 0.8 - (abs(i - (self.time % num_cells)) / float(num_cells))
					adj_color = color + (size * 20) + (i * 5)
					#self.tri.set_cell(ring_cells[c],gradient_wheel(color, gradient))
					self.tri.set_cells(self.tri.mirror_coords(cell), gradient_wheel(adj_color, gradient))
				
class Spinners(object):
	def __init__(self, trimodel):
		self.name = "Spinners"        
		self.tri = trimodel
		self.spinners = []	# List that holds Spinner objects
		self.speed = 0.1
		self.background = randColor()
		self.spincolor = randColor()
		          
	def next_frame(self):

		self.spinners.extend([Spinner(self.tri, center) for center in all_centers()])

		while (True):

			self.tri.set_all_cells(wheel(self.background))
			
			for s in self.spinners:
				s.draw_spinner(self.spincolor)
				if oneIn(5):
					s.move_spinner()
			
			self.background = (self.background + 5) % maxColor
			self.spincolor = randColorRange(self.spincolor, 40)
			
			yield self.speed
