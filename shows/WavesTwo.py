from math import sin, cos
from HelperFunctions import*
from triangle import*
        		
class WavesTwo(object):
	def __init__(self, trimodel):
		self.name = "WavesTwo"
		self.tri = trimodel
		self.time = 0
		self.speed = 0.05
		self.color = randColor()
		self.min_x, self.max_x = min_max_column()
		self.min_y, self.max_y = min_max_row()
		self.fract = randint(5,20)
		self.hue_fract = randint(5,20)

	def next_frame(self):

		while (True):
			
			for x_coord in range(self.min_x, self.max_x):
				for y_coord in range(self.min_y, self.max_y + 1):
					att = self.calc_sin(x_coord - self.min_x + self.time, self.fract)
					hue = int(maxColor * self.calc_sin(y_coord - self.min_y + self.time, self.hue_fract * 10))
					self.tri.set_cell((x_coord, y_coord), gradient_wheel(hue, att))

			self.time += 1
			
			self.color = (self.color + 5) % maxColor

			yield self.speed

	def calc_sin(self, value, max_value):
		"""Returns 0-1.0"""
		sin_value = (sin(2 * 3.1415 * (value % max_value) / max_value) + 1) * 0.5
		return sin_value

