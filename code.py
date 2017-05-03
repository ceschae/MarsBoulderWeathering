# Mars boulder weathering simulation
# version: 0.4
# author: Caitlin Schaefer (ceschae@gmail.com)
# last updated: 3 May 2017
#
# weathers a NUMBER of basalt rocks for a given amount of TIME in days
# using aeolian weathering model, outputs before/after rock graph as a 
# result of weathering. random input x, y, radius data set 
#
# to run on my machine:
# C:\Users\cesch\AppData\Local\Programs\Python\Python36-32\python.exe C:\Users\cesch\Documents\2016-2017\MarsBoulderWeathering\code.py
# after running, can find image produced at in file as temp-plot.html

# TODO List:
#	- get rid of overlapping rocks
#	- movie of plot with changes?
#	- CFA plot
#	- reformat title
#	- size graphs
#	- implement overlap search
#	- consider implementing own random distributions


import numpy as np
# numpy may become important later, as may scipy

# import plotly for visualization
import plotly
import plotly.plotly as py 
import plotly.graph_objs as go

NUMBER = 1000 # a thousand rocks
TIME = 2000000000 # 2 billion years
WINDOW_SIZE = 100 # 100 m x 100 m
MAX_RADIUS = 10 # 10 m
MIN_RADIUS = 0.25 # 0.25 m

# defines basalt rock data container
# future plan is to make Rock generic, 
# store density as an attribute,
# define different weathering methods,
# have different definitions of those weathering methods for each type of rock
class BasaltRock: 
	rocks = []
	original_radii = []
	new_radii = []

	# constructs a new spherical basalt rock with the given diameter at
	# the given location
	#
	# params:
	#	x_pos -    number to represent x geographic position in grid
	#	y_pos -    number to represent y geographic position in grid
	#	diameter - number to represent diameter of boulder in meters
	def __init__(self, x_pos, y_pos, diameter, generation):
		self.x = x_pos
		self.y = y_pos
		self.radius = diameter / 2 
		self.new_radius = diameter / 2
		self.gen = generation

	# reduces radius of rock by 0.04 x 10^-9 m / year (Golombek & Bridges, 2000) 
	# (minimum listed) for years number of years; simulates aeolian weathering 
	# process
	#
	# params:
	# 	years - number of years to weather rock
	def aeolian_weather(self, years):
		self.new_radius = self.radius - years * 0.04 * 10**(-9)

	def is_overlapping(new_rock):
		return True

x_small = np.random.random_sample(NUMBER) 
x = [n * WINDOW_SIZE * 2 - WINDOW_SIZE for n in x_small] # x ranges from -WINDOW_SIZE to +WINDOW_SIZE
y_small = np.random.random_sample(NUMBER) 
y = [n * WINDOW_SIZE * 2 - WINDOW_SIZE for n in y_small] # y ranges from -WINDOW_SIZE to +WINDOW_SIZE
radii_small = np.random.random_sample(NUMBER)
radii = [n * MAX_RADIUS for n in radii_small]	# radii ranges from 0 to MAX_RADIUS

# adding many rocks to rocks
for i in range(NUMBER):
	while radii_small[i] < MIN_RADIUS: # radii ranges from MIN_RADIUS to MAX_RADIUS
		radii_small[i] = np.random.random_sample(1)[0] * MAX_RADIUS
	radii.append(radii_small[i])
	rock = BasaltRock(x[i],y[i],radii[i],0)
	if BasalTRock.is_overlapping(rock) is False:
		BasaltRock.rocks.append(rock)

# for testing weathering products
for rock in rocks:
	rock.aeolian_weather(TIME)
	BasaltRock.original_radii.append(rock.radius)
	BasaltRock.new_radii.append(rock.new_radius)

orig_r = [r * 20 for r in BasaltRock.original_radii]
new_r = [r * 20 for r in BasaltRock.new_radii]
print(orig_r[0])
print(new_r[0])
data = [
    go.Scatter(
		x=x,
		y=y,
		name='Original',
		mode='markers',
		hoverinfo='size',
		marker=dict(size = orig_r, color="rgb(0, 0, 0)")
	),
	go.Scatter(
		x=x,
		y=y,
		name='Post-Weathering',
		mode='markers',
		hoverinfo='size',
		marker=dict(size = new_r, color="rgb(255, 255, 255")
	)
]

title = 'Time elapsed = ' + str(TIME)
layout = go.Layout(
	title = title
)

figure = go.Figure(data=data, layout=layout)
plotly.offline.plot(figure)