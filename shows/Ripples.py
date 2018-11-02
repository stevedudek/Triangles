from HelperFunctions import*
from triangle import*
from math import sin, pi

class Ripples(object):
	def __init__(self, trimodel):
		self.name = "Ripples"
		self.tri = trimodel
		self.center = self.tri.get_rand_cell()
		self.time = 0
		self.speed = 0.1
		self.width = randint(8,20)
		self.color = randColor()
		self.dir = randDir()

	def get_att(self, width, ring, time):
		gradient = (ring + time) % width
		attenuation = (sin(2 * pi * gradient / width) + 1) * 0.5
		return attenuation

	def next_frame(self):

		while (True):

			# Draw the rings
			for i in range (50): # total number of rings - can be bigger than display
				color = gradient_wheel(self.color + (i * 10), self.get_att(self.width, i, self.time))
				self.tri.set_cells(get_ring(self.center, i), color)

			# Move the center of the ripple like a drunken mason
			newtri = tri_in_direction(self.center, self.dir, 2)
			if self.tri.is_on_board(newtri) and not oneIn(5):
				self.center = newtri
			else:
				self.dir = randDir()

			if oneIn(20):
				self.width = upORdown(self.width, 1, 8, 20)

			self.color = (self.color + 5) % maxColor

			self.time += 1

			yield self.speed