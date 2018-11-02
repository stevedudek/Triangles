from HelperFunctions import*
from triangle import*

class Ball(object):
	def __init__(self, trimodel, maincolor):
		self.tri = trimodel
		self.color = randColorRange(maincolor, 100)
		self.pos = self.tri.get_rand_cell()
		self.size = randint(5,8)	# Random ball size
		self.dir = randDir()		# Direction of ball's travel
		self.life = randint(50,200)	# how long a ball is around
	
	def decrease_life(self):
		self.life -= 1

	def is_alive(self):
		return self.life > 0
	
	def draw_ball(self):
		for i in range(self.size - 3):
			color = gradient_wheel(self.color, (i+1) / (self.size - 3.0) )
			self.tri.set_cells(tri_shape(tri_in_direction(self.pos, 1, i * 2), self.size), color)
	
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


class Rings(object):
    def __init__(self, trimodel):
        self.name = "Rings"        
        self.tri = trimodel
        self.balls = []	# List that holds Balls objects
        self.speed = 0.1
        self.maincolor = randColor()
		          
    def next_frame(self):
    	
    	while (True):
			
			while len(self.balls) < 12:
				self.balls.append(Ball(self.tri, self.maincolor))
			
			self.tri.black_all_cells()
			
			for b in self.balls:
				b.draw_ball()
				b.move_ball()
				b.decrease_life()
				if not b.is_alive():
					self.balls.remove(b)

			yield self.speed
			
	
