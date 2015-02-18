from HelperFunctions import*
from triangle import*

class Ball(object):
	def __init__(self, trimodel, maincolor):
		self.tri = trimodel
		self.color = randColorRange(maincolor, 200)
		self.pos = self.tri.get_rand_cell()
		self.size = randint(1,5)	# Random ball size
		self.dir = randDir()		# Direction of ball's travel
		self.life = randint(50,200)	# how long a ball is around

	def decrease_life(self):
		if self.life > 0:
			self.life -= 1
			return True
		else:
			return False
	
	def draw_ball(self):
		self.tri.set_cell(self.pos, wheel(self.color))	# Draw the center
		for i in range (self.size):
			self.tri.set_cells(get_ring(self.pos, i),
				gradient_wheel(self.color, 1-(0.15*(i+1))))
	
	def move_ball(self):
		tries = 20
		while (tries > 0):
			newspot = tri_in_direction(self.pos, self.dir, 2)	# Where is the ball going?
			if self.tri.cell_exists(newspot):	# Is new spot off the board?
				self.pos = newspot	# On board. Update spot
				return
			else:
				tries -= 1
				self.dir = randDir()	# Off board. Pick a new direction
		self.life = 0	# Ball is stuck - kill it
		return
			
				
class Balls(object):
    def __init__(self, trimodel):
        self.name = "bouncing balls"        
        self.tri = trimodel
        self.balls = []	# List that holds Balls objects
        self.speed = 0.1
        self.maincolor = randColor()	# Main color of the show
		          
    def next_frame(self):
    	
    	while (True):
			
			# Check how many balls are in play
			# If no balls, add one. Otherwise if balls < 8, add more balls randomly
			while len(self.balls) < 8:
				newball = Ball(self.tri, self.maincolor)
				self.balls.append(newball)
			
			# Black the screen
			self.tri.set_all_cells([0,0,0])

			# Draw all the balls
			# Move balls. Kill ball if out of life
			for b in self.balls:
				b.draw_ball()
				b.move_ball()
				if b.decrease_life() == False:
					self.balls.remove(b)
			
			yield self.speed  	# random time set in init function
			