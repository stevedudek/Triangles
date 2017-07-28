from HelperFunctions import*
from triangle import*
        		
class CenterColors(object):
	def __init__(self, trimodel):
		self.name = "CenterColors"        
		self.tri = trimodel
		self.time = 0
		self.speed = 0.01
		self.direction = 0
		self.color = randColor()

	def next_frame(self):

		while (True):
			
			# Set background to black
			#self.tri.set_all_cells((0,0,0))

			self.draw_nested_triangles()
			
			self.time += 1
			
			self.color = (self.color + 6) % maxColor					
			
			if oneIn(100):
				self.direction = (self.direction+1) % 2

			yield self.speed
	
	def draw_nested_triangles(self):
		for corner in all_left_corners():
			nested_cells = nested_triangles(corner)			

			for i in range(len(nested_cells)):
				if (i + self.direction) % 2:					
					self.tri.set_cell(nested_cells[i][self.time % len(nested_cells[i])],
						wheel(self.color))
				else:
					self.tri.set_cell(nested_cells[i][len(nested_cells[i])-1-(self.time % len(nested_cells[i]))],
						wheel(self.color))
