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

class Ball(object):
	def __init__(self, trimodel, pos, life):
		self.tri = trimodel
		self.pos = pos		
		self.life = life

	def draw_ball(self):
		
		return self.pos

	def move_ball(self, dir):
		
		while self.tri.is_on_board(tri_in_direction(self.pos, dir)) == False:	# Is new spot off the board?
			dir = (dir + 2) % maxDir

		self.pos = tri_in_direction(self.pos, dir)

		self.life -= 1
		if self.life > 0:
			return True
		else:
			return False

class SideToSide(object):
	def __init__(self, trimodel):
		self.name = "SideToSide"        
		self.tri = trimodel
		self.balls = []	# List that holds Ball objects
		self.sparkles = []	# List that holds Sparkle objects
		self.time = 0
		self.speed = 0.02
		self.fade = randint(10,50)
		self.dir = 0
		self.life = 30
		self.turning = 2
		self.color = randColor()

	def next_frame(self):

		while (True):
			
			# Periodically set up new balls
			if self.time % self.life == 0:

				for corner in all_left_corners():
					if point_up(corner):
						dir = 1
					else:
						dir = 5
				
					line = tri_in_line(corner, dir, 22)
					
					for i in range(0, len(line), 1):	
						new_ball = Ball(self.tri, line[i], self.life)
						self.balls.append(new_ball)

			# Set background to black
			self.tri.set_all_cells((0,0,0))

			# Move and draw the balls

			for b in self.balls:
				new_spot = b.draw_ball()
				new_sparkle = Sparkle(self.tri, self.color, new_spot, self.fade)
				self.sparkles.append(new_sparkle)

				if (b.move_ball(self.dir) == False):
					self.balls.remove(b)
			
			# Draw the sparkles
				
			for s in self.sparkles:
				s.draw_sparkle()
				if s.fade_sparkle() == False:
					self.sparkles.remove(s)

			if oneIn(50):
				self.fade = randint(10,50)
			
			if oneIn(10):
				self.dir = turn_left(self.dir)

			self.time += 1
			
			self.color = (self.color + 1) % maxColor					
			
			yield self.speed