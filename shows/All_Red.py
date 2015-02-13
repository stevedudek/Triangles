from HelperFunctions import*
from triangle import*
        		
class AllRed(object):
	def __init__(self, trimodel):
		self.name = "AllRed"        
		self.tri = trimodel
		self.speed = 10
		self.color = (255,0,0)

	def next_frame(self):

		self.tri.set_all_cells(self.color)

		while (True):
			
			yield self.speed