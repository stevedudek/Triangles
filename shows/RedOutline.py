from HelperFunctions import*
from triangle import*
        		
class RedOutline(object):
	def __init__(self, trimodel):
		self.name = "RedOutline"        
		self.tri = trimodel
		self.speed = 1
		self.color = (255,0,0)

	def next_frame(self):

		self.tri.clear()

		while (True):
			for corner in all_left_corners():
				self.tri.set_cells(tri_shape(corner, 10), self.color)

			yield self.speed