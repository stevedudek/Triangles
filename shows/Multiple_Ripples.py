from HelperFunctions import*
from triangle import*
from math import sin, pi

class Rip(object):
	def __init__(self, trimodel, color):
		self.tri = trimodel
		self.center = self.tri.get_rand_cell()
		self.lifetime = randint(20, 100)	# Time ripple lives
		self.color = color
		self.width = randint(8, 20)

	def draw(self):
		for i in range(8):  # total number of rings - can be bigger than display
			color = gradient_wheel(self.color, self.get_att(self.width, i, self.lifetime))
			self.tri.set_cells(get_ring(self.center, i), color)

	def decrease_time(self):
		self.lifetime -= 1

	def is_alive(self):
		return self.lifetime > 0

	def get_att(self, width, ring, time):
		gradient = (ring + time) % width
		attenuation = (sin(2 * pi * gradient / width) + 1) * 0.5
		return attenuation


class Multiple_Ripples(object):
	def __init__(self, trimodel):
		self.name = "Multiple_Ripples"
		self.tri = trimodel
		self.rips = []	# List that holds Rip objects
		self.time = 0
		self.speed = 0.1
		self.color = randColor()

	def next_frame(self):

		self.tri.clear()

		while (True):

			# Check how many rips are in play
			# If no rips, add one. If rips < 6 then add one more randomly
			while len(self.rips) < 4 or oneIn(20):
				newrip = Rip(self.tri, randColorRange(self.color, 200))
				self.rips.append(newrip)
			
			# Decrease the life of each ripple - kill a ripple if life is zero
			for r in self.rips:
				r.draw()
				r.decrease_time()
				if r.is_alive() == 0:
					self.rips.remove(r)

			self.color = (self.color + 1) % maxColor  # Slowly change the colors

			self.time += 1
	
			yield self.speed  	# random time set in init function
			
			