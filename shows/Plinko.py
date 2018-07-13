from HelperFunctions import*
from triangle import*

class Plink(object):
	def __init__(self, trimodel, coord, color, dirs):
		self.tri = trimodel
		self.coord = coord
		self.color = color
		self.dirs = dirs

	def draw(self):
		self.tri.set_cell(self.coord, wheel(self.color))

	def move(self):
		self.coord = tri_nextdoor(self.coord, choice(self.dirs))

	def is_on_board(self):
		return self.tri.is_on_board(self.coord)


class Plinko(object):
	def __init__(self, trimodel):
		self.name = "Plinko"
		self.tri = trimodel
		self.speed = 0.02
		self.plinks = []  # list that holds Plink objects
		self.starts = [  (all_left_corners, [0,1], 0),
					   (all_center_corners, [4,5], 500),
					    (all_right_corners, [2,3], 1000)]
		self.corner = randint(0,2)

	def next_frame(self):

		while (True):

			self.tri.black_all_cells()

			for i in range(4):
				start_corners, dirs, color = self.starts[self.corner]
				start_corner = choice(start_corners())
				p = Plink(self.tri, start_corner, randColorRange(color, 200) , dirs)
				self.plinks.append(p)

			for p in self.plinks:
				p.move()
			for p in self.plinks:
				if p.is_on_board():
					p.draw()
				else:
					self.plinks.remove(p)

			if oneIn(20):
				self.corner = randint(0, 2)

			yield self.speed

