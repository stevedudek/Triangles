from HelperClasses import*

class Sparkles(object):
	def __init__(self, trimodel):
		self.name = "Sparkles"        
		self.tri = trimodel
		self.faders = Faders(self.tri)
		self.speed = 0.1
		self.color = randColor()
		self.spark_num = 400
		          
	def next_frame(self):
		
		for i in range (self.spark_num):
			self.add_new_sparkle()
					
		while (True):

			self.faders.cycle_faders(refresh=True)

			while self.faders.num_faders() < self.spark_num:
				self.add_new_sparkle()
			
			if oneIn(100):
				self.color = randColorRange(self.color, 30)
			
			yield self.speed  	# random time set in init function

	def add_new_sparkle(self):
		self.faders.add_fader(color=randColorRange(self.color, 30),
							  pos=self.tri.get_rand_cell(),
							  change=1.0 / randint(3,10),
							  intense=0,
							  growing=True)