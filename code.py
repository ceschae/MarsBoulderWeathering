# Mars boulder weathering simulation
# version: 0.1
# author: Caitlin Schaefer (ceschae@gmail.com)
# last updated: 11 April 2017
#
# weathers a NUMBER of basalt rocks for a given amount of TIME in days
# using aeolian weathering model 
#
# to run on my machine:
# C:\Users\cesch\Anaconda2\python.exe C:\Users\cesch\Documents\2016-2017\MarsWeathering\Code\code.py

# import numpy as np
# numpy may become important later, as may scipy

# import for Set usage
from sets import Set

NUMBER = 1000; # a thousand rocks
TIME = 10000000; # 10 million years

# defines basalt rock data container
# future plan is to make Rock generic, 
# store density as an attribute,
# define different weathering methods,
# have different definitions of those weathering methods for each type of rock
class BasaltRock: 

	# constructs a new spherical basalt rock with the given diameter at
	# the given location
	#
	# params:
	#	x_pos -    number to represent x geographic position in grid
	#	y_pos -    number to represent y geographic position in grid
	#	diameter - number to represent diameter of boulder in meters
	def __init__(self, x_pos, y_pos, diameter):
		self.x = x_pos
		self.y = y_pos
		self.radius = diameter / 2 

	# reduces radius of rock by 0.04 x 10^-9 m / year (Golombek & Bridges, 2000) 
	# (minimum listed) for years number of years; simulates aeolian weathering 
	# process
	#
	# params:
	# 	years - number of years to weather rock
	def aeolian_weather(self, years):
		self.radius -= years * 0.04 * 10**(-9)
		if self.y == 999: # printing one to make sure it's actually changing
			print(self.radius)

# rocks stores all rocks in grid
rocks = Set()

# adding many rocks to rocks
for i in range(NUMBER):
	rocks.add(BasaltRock(1,i,2))

# for testing weathering products
for rock in rocks:
	rock.aeolian_weather(TIME)