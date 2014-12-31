from HelperFunctions import*
from triangle import*
        		
class Bullet(object):
	def __init__(self, trimodel, color, pos, dir):
		self.tri = trimodel
		self.color = color
		self.pos = pos
		self.dir = dir

	def draw_bullet(self):
		self.tri.set_cell(self.pos, wheel(self.color))
	
	def move_bullet(self):			
		newspot = tri_in_direction(self.pos, self.dir, 1)	# Where is the bullet going?
		if self.tri.cell_exists(newspot):	# Is new spot off the board?
			self.pos = newspot	# On board. Update spot
			self.draw_bullet()
			return True
		else:
			return False	# Off board. Kill.
			
class Spinner(object):
	def __init__(self, trimodel, pos):
		self.tri = trimodel
		self.pos = pos
		self.start = pos
		self.time = 0

	def move_spinner(self):
		newspot = tri_in_direction(self.pos, randDir(), 2)
		if self.tri.cell_exists(newspot):
			self.pos = newspot
		if self.time > 100:
			self.time = 0
			self.pos = self.start

	def draw_spinner(self, color):
		self.time += 1
		for size in range(4):
			ring_cells = get_ring(self.pos, size)
			num_cells = len(ring_cells)
			for c in range(num_cells):
				if self.tri.cell_exists(ring_cells[c]):
					gradient = 1 - (abs(c - (self.time % num_cells))/(float)(num_cells-1))
					#self.tri.set_cell(ring_cells[c],gradient_wheel(color, gradient))
					self.tri.set_cells(self.tri.mirror_coords(ring_cells[c]),
						gradient_wheel(color, gradient))
				
class Spinners(object):
	def __init__(self, trimodel):
		self.name = "Spinners"        
		self.tri = trimodel
		self.spinners = []	# List that holds Spinner objects
		self.bullets = []	# List that holds Bullets objects
		self.speed = 0.05
		self.background = randColor()
		self.spincolor = randColor()
		          
	def next_frame(self):

		for center in all_centers():
			newspinner = Spinner(self.tri, center)
			self.spinners.append(newspinner)

		while (True):
			
			# Randomly fire a bullet
			
			self.draw_background()
			
			# Draw the bullets
				
			for b in self.bullets:
				if b.move_bullet() == False:	# bullet has moved off the board
					self.bullets.remove(b)	# kill the bullet
			
			# Random move the spin centers
			
			for s in self.spinners:
				s.draw_spinner(self.spincolor)
				if oneIn(5):
					s.move_spinner()
				if oneIn(5):
					newbullet = Bullet(self.tri, self.spincolor, s.pos, randDir())
					self.bullets.append(newbullet)
			
			# Change the colors
			
			self.background = (self.background + 5) % maxColor					
			
			self.spincolor = (maxColor + self.spincolor - 10) % maxColor
			
			yield self.speed
	
	# Draw the background - concentric triangles of decreasing intensities
	
	def draw_background(self):
		for i in range (12,0,-1): # total number of triangles
			for corner in all_left_corners():
				self.tri.set_cells(tri_shape(corner, i),
							gradient_wheel(self.background, 1-(i/12.0)))
