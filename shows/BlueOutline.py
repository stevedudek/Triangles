from HelperFunctions import*
from triangle import*
        		
class BlueOutline(object):
	def __init__(self, trimodel):
		self.name = "BlueOutline"        
		self.tri = trimodel
		self.speed = 10
		self.color = (0,0,255)

	def next_frame(self):

		self.tri.clear()

		for corner in all_left_corners():
				self.tri.set_cells(tri_shape(corner, 10), self.color)

		while (True):
			
			yield self.speed