from HelperClasses import*
from triangle import*
from math import sin

class DarkSideMoon(object):
	def __init__(self, trimodel):
		self.name = "DarkSideMoon"
		self.tri = trimodel
		self.time = 0
		self.speed = 0.1

	def next_frame(self):

		self.tri.clear()

		while (True):

			self.draw_white_triange()
			self.draw_incoming_ray()
			self.draw_middle_ray()
			self.draw_exit_rays()
			self.time += 1

			yield self.speed

	def draw_white_triange(self):
		for i, corner in enumerate(all_left_corners()):
			corner = tri_in_direction(corner, 1, 4)
			corner = tri_in_direction(corner, 0, 4)

			cells = tri_shape(corner, 6)
			for j, cell in enumerate(cells):
				intense = 255 * (sin(2 * 3.1415 * ((i + j + self.time) % len(cells)) / len(cells)) + 1.5) * 0.5
				self.tri.set_cell(cell, (intense, intense, intense) )

	def draw_incoming_ray(self):
		white = (255, 255, 255)
		for corner in all_left_corners():
			start = tri_in_direction(corner, 1, 12)
			self.tri.set_cells(tri_in_line(start, 5, 3), white)

	def draw_middle_ray(self):
		white = (255, 255, 255)
		for corner in all_left_corners():
			start = tri_in_direction(corner, 1, 8)
			start = tri_in_direction(start, 0, 6)
			self.tri.set_cells(tri_in_line(start, 0, 2), white)

	def draw_exit_rays(self):
		num_rays = 4
		for corner in all_left_corners():
			start = tri_in_direction(corner, 1, 6)
			start = tri_in_direction(start, 0, 13)

			for i in range(num_rays):
				color = wheel((self.time * 20) + (i * maxColor / num_rays))
				self.tri.set_cells(tri_in_line(start, 1, 3), color)
				start = tri_in_direction(start, 2, 2)