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
	def __init__(self, trimodel, pos, dir, color, life):
		self.tri = trimodel
		self.color = color
		self.pos = pos		
		self.dir = dir
		self.life = life
		self.sparkles = []	# List that holds Sparkle objects

		new_sparkle = Sparkle(self.tri, self.color, self.pos, self.life)
		self.sparkles.append(new_sparkle)

	def draw_ball(self):
		
		# Draw the sparkles
				
		for s in self.sparkles:
			s.draw_sparkle()
			if s.fade_sparkle() == False:
				self.sparkles.remove(s)

	def move_ball(self):
		
		newspot = tri_in_direction(self.pos, self.dir)	# Where is the ball going?
		
		if self.tri.is_on_board(newspot) == False:	# Is new spot off the board?
			self.dir = (self.dir + 3) % 6	# turn around
			newspot = tri_in_direction(self.pos, self.dir)
			if self.tri.is_on_board(newspot) == False:	# Is new spot off the board?
				newspot = self.pos	# Stuck. Don't move

		self.pos = newspot
		new_sparkle = Sparkle(self.tri, self.color, self.pos, self.life)
		self.sparkles.append(new_sparkle)

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
			if point_up(corner):
				dir = 1
			else:
				dir = 5
			
			line = tri_in_line(corner, dir, 22)
			
			for i in range(0, len(line), 1):	
				new_ball = Ball(self.tri, line[i], 0, self.color, self.life)
				self.balls.append(new_ball)

		while (True):
			
			# Set background to black
			self.tri.set_all_cells((0,0,0))

			# Move and draw the balls

			for b in self.balls:
				b.move_ball()
				b.draw_ball()
			
			if oneIn(50):
				self.life = (self.life + 1) % 20
				
			self.time += 1
			
			self.color = (self.color + 1) % maxColor					
			
			yield self.speed