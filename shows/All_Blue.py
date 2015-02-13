from HelperFunctions import*
from triangle import*
        		
class AllBlue(object):
	def __init__(self, trimodel):
		self.name = "AllBlue"        
		self.tri = trimodel
		self.speed = 10
		self.color = (0,0,255)

	def next_frame(self):

		self.tri.set_all_cells(self.color)

		while (True):
			
			yield self.speed