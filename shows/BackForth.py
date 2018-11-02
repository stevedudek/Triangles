from HelperClasses import*
from triangle import*

class Ball(object):
	def __init__(self, trimodel, pos, dir, color, life):
		self.tri = trimodel
		self.color = color
		self.pos = pos		
		self.dir = dir
		self.life = life
		self.faders = Faders(self.tri)

		self.faders.add_fader(color=self.color, pos=self.pos, change=(1.0 / self.life))

	def draw_ball(self):
		self.faders.cycle_faders(refresh=False)

	def move_ball(self):
		newspot = tri_in_direction(self.pos, self.dir)	# Where is the ball going?
		
		if not self.tri.is_on_board(newspot):	# Is new spot off the board?
			self.dir = (self.dir + 3) % 6	# turn around
			newspot = tri_in_direction(self.pos, self.dir)
			if not self.tri.is_on_board(newspot):	# Is new spot off the board?
				newspot = self.pos	# Stuck. Don't move

		self.pos = newspot
		self.faders.add_fader(color=self.color, pos=self.pos, change=(1.0 / self.life))

class BackForth(object):
	def __init__(self, trimodel):
		self.name = "BackForth"        
		self.tri = trimodel
		self.balls = []	# List that holds Ball objects
		self.time = 0
		self.speed = 0.02
		self.life = randint(5,25)
		self.color = randColor()

	def next_frame(self):

		# Set up the balls

		for corner in all_left_corners():
			dir = 1 if point_up(corner) else 5
			for cell in tri_in_line(corner, dir, 22):
				self.balls.append(Ball(self.tri, cell, 0, randColorRange(self.color, 100), self.life))

		while (True):
			
			self.tri.black_all_cells()

			for b in self.balls:
				b.move_ball()
				b.draw_ball()
			
			if oneIn(50):
				self.life = upORdown(self.life, 1, 5, 25)
				
			self.time += 1
			
			self.color = (self.color + 1) % maxColor					
			
			yield self.speed