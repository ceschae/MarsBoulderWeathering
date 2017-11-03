import numpy as np
import math as math
import matplotlib.pyplot as plt

MAX_RADIUS = 10 # 10 m
MIN_RADIUS = 0.25 # 0.25 m

TEMP_HEIGHT = 1 # 1 m
TIPPING_POINT = 0.25 # quarter of the rock

# boulder cracking variables
CRACK_YEAR = 1000000 # a million years
CRACK_STDEV = 0.033 # TODO: revisit
CRACK_X_MEAN = 0.5 # from 0-1 along diameter
CRACK_X_STDEV = 0.1 # TODO: revisit

# defines basalt rock data container
# future plan is to make Rock generic, 
# store density as an attribute,
# define different weathering methods,
# have different definitions of those weathering methods for each type of rock
class BasaltRock: 
	rocks = []
	x = []
	y = []
	original_radii = []
	new_radii = []

	# constructs a new spherical basalt rock with the given diameter at
	# the given location
	#
	# params:
	#	x_pos -    number to represent x geographic position in grid
	#	y_pos -    number to represent y geographic position in grid
	#	diameter - number to represent diameter of boulder in meters
	def __init__(self, x_pos, y_pos, diameter, height, generation):
		self.x = x_pos
		self.y = y_pos
		self.radius = diameter / 2 
		self.new_radius = diameter / 2
		self.gen = generation
		self.height = height
		self.time = 0

	def __repr__(self):
		return repr(self.x, self.y, self.radius)

	def toString(self):
		return str(self.x) + str(self.y) + str(self.radius)

	# reduces radius of rock by 0.04 x 10^-9 m / year (Golombek & Bridges, 2000) 
	# (minimum listed) for years number of years; simulates aeolian weathering 
	# process
	#
	# params:
	# 	years - number of years to weather rock
	def aeolian_weather(self, years):
		self.new_radius = self.radius - years * 0.04 * 10**(-9)

	def crack(self):
		crack_spot = self.radius * 2 * np.random.normal(CRACK_X_MEAN, CRACK_X_STDEV)
		# crack angle? for now assuming along longest axis (and projecting
		# longest axis along x axis)
		if crack_spot < self.radius * TIPPING_POINT:
			# new rock is the one that tipped over
			new_rock = BasaltRock(self.x - self.radius + crack_spot - (self.height / 2), self.y, self.height, crack_spot, self.gen + 1)
			# new_rock.x is probably correct? want to double-check
			self.x = self.x + (crack_spot / 2)
			self.radius = self.radius - (crack_spot / 2)
		elif crack_spot > self.radius * (1 - TIPPING_POINT):
			# new_rock is the one that tipped over
			new_rock = BasaltRock(self.x + self.radius - crack_spot + (self.height / 2), self.y, self.height, crack_spot, self.gen + 1)
			self.x = self.x - self.radius + (crack_spot / 2)
			self.radius = self.radius - (crack_spot / 2)
		else:
			new_rock = BasaltRock(self.x + (crack_spot / 2), self.y, self.radius * 2 - crack_spot, TEMP_HEIGHT, self.gen + 1)
			self.x = self.x - self.radius + (crack_spot / 2)
			self.radius = crack_spot / 2
		self.time = 0
		return new_rock


	def is_overlapping(new_rock):
		for rock in BasaltRock.rocks:
			# basic circle overlap comparison
			r = math.pow(math.pow(new_rock.x - rock.x, 2) + math.pow(new_rock.y - rock.y, 2), 0.5)
			if r - new_rock.radius - rock.radius < 0 is True:
				return True
		return False