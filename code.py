# Mars boulder weathering simulation
# version: 0.2
# author: Caitlin Schaefer (ceschae@gmail.com)
# last updated: 26 April 2017
#
# weathers a NUMBER of basalt rocks for a given amount of TIME in days
# using aeolian weathering model, outputs before/after rock graph as a 
# result of weathering. random input x, y, radius data set 
#
# to run on my machine:
# C:\Users\cesch\Anaconda2\python.exe C:\Users\cesch\Documents\2016-2017\MarsWeathering\Code\code.py
# after running, can find image produced at https://plot.ly/~ceschae (most recent will be first result)

import numpy as np
# numpy may become important later, as may scipy

# import for Set usage
from sets import Set

# import plotly for visualization
import plotly.plotly as ply 
import plotly.graph_objs as go

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

# rocks stores all rocks in grid
rocks = []
x = np.random.randn(NUMBER)
y = np.random.randn(NUMBER)
radii = np.random.random_sample(NUMBER)

# adding many rocks to rocks
for i in range(NUMBER):
	rocks.append(BasaltRock(x[i],y[i],radii[i]))

new_radii = []
# for testing weathering products
for rock in rocks:
	rock.aeolian_weather(TIME)
	new_radii.append(rock.radius)

trace1 = go.Scatter(
	x=x,
	y=y,
	name='Original',
	mode='markers',
	marker = dict(
		size = radii * 20
	)
)
trace2 = go.Scatter(
	x=x,
	y=y,
	name='Post-Weathering',
	mode='markers',
	marker = dict(
		size = new_radii * 20
	)
)
data = [trace1,trace2]
ply.iplot(data)
