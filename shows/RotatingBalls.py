from HelperClasses import*
from triangle import*

class RotatingBalls(object):
	def __init__(self, trimodel):
		self.name = "RotatingBalls"        
		self.tri = trimodel
		self.faders = Faders(self.tri)
		self.time = 0
		self.speed = 0.01
		self.life = randint(10,25)
		self.color = randColor()

	def next_frame(self):

		while (True):
			
			self.tri.black_all_cells()

			self.draw_nested_triangles()
			self.faders.cycle_faders()

			if oneIn(10):
				self.life = upORdown(self.life, 1, 10, 25)
				
			self.time += 1
			
			self.color = (self.color + 2) % maxColor					
			
			yield self.speed
	
	def draw_nested_triangles(self):
		for corner in all_left_corners():
			nested_cells = nested_triangles(corner)

			for i in range(len(nested_cells)):
				pos = nested_cells[i][self.time % len(nested_cells[i])]
				self.faders.add_fader(color=self.color, pos=pos, change=1.0 / self.life, intense=1.0, growing=False)
