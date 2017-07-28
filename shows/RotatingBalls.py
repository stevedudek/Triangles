from HelperFunctions import*
from triangle import*

class Sparkle(object):
	def __init__(self, trimodel, color, pos, life):
		self.tri = trimodel
		self.pos = pos
		self.color = color
		self.intense = 1.0
		self.life = life
	
	def draw_sparkle(self):
		self.tri.set_cell(self.pos, gradient_wheel(self.color, self.intense))
	
	def fade_sparkle(self):
		self.intense -= 1.0 / self.life
		if self.intense > 0:
			return True
		else:
			return False

class RotatingBalls(object):
	def __init__(self, trimodel):
		self.name = "RotatingBalls"        
		self.tri = trimodel
		self.sparkles = []	# List that holds Sparkle objects
		self.time = 0
		self.speed = 0.01
		self.life = randint(5,25)
		self.color = randColor()

	def next_frame(self):

		while (True):
			
			# Set background to black
			self.tri.set_all_cells((0,0,0))

			self.draw_nested_triangles()
			
			# Draw the sparkles
				
			for s in self.sparkles:
				s.draw_sparkle()
				if s.fade_sparkle() == False:
					self.sparkles.remove(s)

			if oneIn(200):
				self.life = randint(5,25)
				
			self.time += 1
			
			self.color = (self.color + 2) % maxColor					
			
			yield self.speed
	
	def draw_nested_triangles(self):
		for corner in all_left_corners():
			nested_cells = nested_triangles(corner)			

			for i in range(len(nested_cells)):

				pos = nested_cells[i][self.time % len(nested_cells[i])]
				new_sparkle = Sparkle(self.tri, self.color, pos, self.life)
				self.sparkles.append(new_sparkle)
