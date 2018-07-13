from HelperFunctions import*
from triangle import*
        		
class VerticalWave(object):
	def __init__(self, trimodel):
		self.name = "DiagonalWave"        
		self.tri = trimodel
		self.time = 0
		self.speed = 0.1
		self.width = 12
		self.color = randColor()
		self.background = randColor()
		self.min_row, self.max_row = min_max_row()
		self.max_row

	def get_att(self, width, ring, time):
		saw = (1.0 / width) * (ring + ((100000 - time) % 30))	# Linear sawtooth
		while saw >= 2:
			saw = saw - 2	# Cut into sawtooth periods
		if saw > 1:
			saw = 2 - saw	# Descending part of sawtooth
		return saw

	def next_frame(self):

		while (True):
			
			self.draw_background()
			self.time += 5
			self.color = (self.color + 5) % maxColor
			
			yield self.speed
	
	def draw_background(self):
		for i in range (self.max_row, self.min_row-1, -1):
			color = wheel((self.background + (i * 20) + self.time) % maxColor)
			self.tri.set_cells(self.tri.get_row(i), color)

