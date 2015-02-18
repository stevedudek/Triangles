from HelperFunctions import*
from triangle import*
        		
class AllRed(object):
	def __init__(self, trimodel):
		self.name = "AllRed"        
		self.tri = trimodel
		self.speed = 1
		self.color = (255,0,0)	# Red

	def next_frame(self):

		while (True):
			self.tri.set_all_cells(self.color)	
			yield self.speed