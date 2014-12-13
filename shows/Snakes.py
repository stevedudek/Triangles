from HelperFunctions import*
from triangle import*

def create_snake_model(trimodel):
	sm = SnakeModel(trimodel)
	return sm

class SnakeModel(object):
	def __init__(self, trimodel):
		# similar to the tri Model
		# this model contains a dictionary of tri coordinates
		# coordinates are the keys
		# the values are the presence of a snake:
		# 0 = no snake
		# number = snake ID

		self.tri = trimodel
		self.snakemap = {}	# Dictionary of snake tri

		# Transfer regular trimodel to the snakemmap
		# And clear (set to 0) all of the snake tri

		for coord in self.tri.all_cells():
			self.snakemap[coord] = 0	# No snake

	def get_snake_value(self, coord, default=None):
		"Returns the snake value for a coordinate. Return 'default' if not found"
		return self.snakemap.get(coord, default)

	def put_snake_value(self, coord, snakeID):
		"Puts the snakeID in the snake tri"
		self.snakemap[coord] = snakeID

	def is_open_tri(self, coord):
		"Returns True if the tri is open. Also makes sure tri is on the board"
		if self.tri.cell_exists(coord) and self.get_snake_value(coord) == 0:
			return True
		else:
			return False

	def get_valid_directions(self, coord):
		valid = []	# List of valid directions
		for dir in range (0, maxDir):	# Check all six possible directions
			newspot = tri_in_direction(coord, dir, 1)
			if self.is_open_tri(newspot):
				valid.append(dir)
		return valid
	
	def get_open_spots(self, coord):
		valid = []
		for cell in neighbors(coord):	# Check all six possible directions
			if self.is_open_tri(cell):
				valid.append(cell)
		return valid

	def pick_open_tri(self):
		opentri = []
		for coord in self.snakemap.keys():
			if self.is_open_tri(coord):
				opentri.append(coord)
		if len(opentri) > 0:
			return choice(opentri)
		else:
			 return False	# No tri open!
	
	def remove_snake_path(self, snakeID):
		"In the snake map, changes all tri with snakeID back to 0. Kills the particular snake path"
		for coord in self.snakemap.keys():
			if self.get_snake_value(coord) == snakeID:
				self.put_snake_value(coord, 0)
				## Activate the line below for quite a different effect
				self.tri.set_cell(coord,[0,0,0]) # Turn path back to black

	def __repr__(self):
		return str(self.lifemap)
        
		
class Snake(object):
	def __init__(self, trimodel, maincolor, snakeID, startpos):
		self.tri = trimodel
		self.color = randColorRange(maincolor, 80)
		self.snakeID = snakeID		# Numeric ID
		self.pos = startpos  		# Starting position
		self.dir = randDir()
		self.pathlength = 0
		self.alive = True

	def draw_snake(self):
		self.tri.set_cell(self.pos, gradient_wheel(self.color, 1.0 - (self.pathlength/200.0)))
		self.pathlength += 1

				
class Snakes(object):
	def __init__(self, trimodel):
		self.name = "Snakes"        
		self.tri = trimodel
		self.snakemap = create_snake_model(trimodel)
		self.nextSnakeID = 0
		self.livesnakes = {}	# Dictionary that holds Snake objects. Key is snakeID.
		self.speed = 0.1
		self.maincolor =  randColor()
	
	def count_snakes(self):
		num = 0
		for id, s in self.livesnakes.iteritems():
			if s.alive:
				num += 1
		return num

	def next_frame(self):
    	
		self.tri.clear()

		while (True):
			
			# Check how many snakes are in play
			# If no snakes, add one. Otherwise if snakes < 4, add more snakes randomly
			while self.count_snakes() < 18:
				startpos = self.snakemap.pick_open_tri()
				if startpos:	# Found a valid starting position
					self.nextSnakeID += 1
					self.snakemap.put_snake_value(startpos, self.nextSnakeID)
					newsnake = Snake(self.tri, self.maincolor, self.nextSnakeID, startpos)
					self.livesnakes[self.nextSnakeID] = newsnake
				
			for id, s in self.livesnakes.iteritems():
				if s.alive:
					
					s.draw_snake()	# Draw the snake head
				
					# Try to move the snake
					nextpos = tri_in_direction(s.pos, s.dir, 1)	# Get the coord of where the snake will go
					if self.snakemap.is_open_tri(nextpos):	# Is the new spot open?
						s.pos = nextpos		# Yes, update snake position
						self.snakemap.put_snake_value(s.pos, s.snakeID)	# Put snake on the virtual snake map
					else:
						dirs = self.snakemap.get_valid_directions(s.pos)	# Blocked, check possible directions
						if len(self.snakemap.get_open_spots(s.pos)) > 0:	# Are there other places to go?
							s.dir = choice(dirs)	# Yes, pick a random new direction
							s.pos = tri_in_direction(s.pos, s.dir, 1)
							self.snakemap.put_snake_value(s.pos, s.snakeID)
						else:	# No directions available
							s.alive = False		# Kill the snake
							self.snakemap.remove_snake_path(s.snakeID)	# Snake is killed
				
			yield self.speed  	# random time set in init function