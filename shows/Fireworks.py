from HelperClasses import*
from triangle import*

class Firework(object):
	def __init__(self, trimodel, coord, color, dirs, max_life=10):
		self.tri = trimodel
		self.coord = coord
		self.color = color
		self.dirs = dirs
		self.max_life = max_life
		self.life = 0

	def draw(self):
		if self.tri.cell_exists(self.coord):
			self.tri.set_cell(self.coord, wheel(self.color))

	def get_coord(self):
		return self.coord

	def get_color(self):
		return self.color

	def move(self):
		self.coord = tri_nextdoor(self.coord, choice(self.dirs))
		self.life += 1

	def get_life(self):
		return self.life

	def is_alive(self):
		return self.life <= self.max_life


class Fireworks(object):
	def __init__(self, trimodel):
		self.name = "Fireworks"
		self.tri = trimodel
		self.speed = 0.1
		self.fireworks = []  # list that holds Firework objects
		self.bangs = []  # list that holds Firework explosions
		self.faders = Faders(self.tri)
		self.possible_starts = self.get_possible_starts()
		self.freq = randint(1,5)

	def next_frame(self):

		while (True):

			self.tri.black_all_cells()

			for r in range(self.freq):  # just a repeat loop to generate a lot of fireworks
				f = Firework(self.tri, choice(self.possible_starts), randColor(), [1,2], 10)  # 1,2 is up left + right
				self.fireworks.append(f)

			if oneIn(100):
				self.freq = upORdown(self.freq, 1, 1, 5)

			for f in self.fireworks:
				self.faders.add_fader(f.get_color(), f.get_coord())

			for f in self.fireworks:
				if not f.is_alive() and oneIn(10):
					# Kill the firework; turn dead firework into six bangs
					life = randint(3,8)
					for d in range(6):
						bang = Firework(self.tri, f.get_coord(), f.get_color(), [d], life)
						self.bangs.append(bang)
					self.fireworks.remove(f)  # remove the firework
				else:
					f.move()

			self.faders.cycle_faders(refresh=False)

			for bang in self.bangs:
				if not bang.is_alive():
					self.bangs.remove(bang)
				else:
					bang.move()
					bang.draw()

			yield self.speed

	def get_possible_starts(self):
		min_row, max_row = min_max_row()
		possible_starts = self.tri.get_row(min_row)
		return possible_starts

