from HelperFunctions import*
from triangle import*
        		
class AllBlue(object):
	def __init__(self, trimodel):
		self.name = "AllBlue"        
		self.tri = trimodel
		self.speed = 1
		self.color = (0,0,255)	# Blue

	def next_frame(self):

		while (True):
			self.tri.set_all_cells(self.color)			
			yield self.speed