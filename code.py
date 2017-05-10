# Mars boulder weathering simulation
# version: 0.5
# author: Caitlin Schaefer (ceschae@gmail.com)
# last updated: 9 May 2017
#
# weathers a NUMBER of basalt rocks in random locations from -WINDOW_SIZE
# to +WINDOW_SIZE in both x and y with random radii from MIN_RADIUS to 
# MAX_RADIUS (excluding overlapping boulders) for a given amount of TIME in days
# using aeolian weathering model, outputs before/after rock graph as a 
# result of weathering.
#
# to run on my machine:
# C:\Users\cesch\AppData\Local\Programs\Python\Python36-32\python.exe C:\Users\cesch\Documents\2016-2017\Research\MarsBoulderWeathering\code.py
# after running, can find image produced at in file as temp-plot.html

# TODO List:
#	- movie of plot with changes?
#	- CFA plot
#	- reformat title
#	- size graphs
#	- consider implementing own random distributions

import numpy as np
import math as math
# scipy may become important later

# import plotly for visualization
import plotly
import plotly.plotly as py 
import plotly.graph_objs as go

NUMBER = 1000 # a thousand rocks
TIME = 15000000000 # 15 billion years
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

	def __repr__(self):
		return repr((self.x, self.y, self.radius))

	# reduces radius of rock by 0.04 x 10^-9 m / year (Golombek & Bridges, 2000) 
	# (minimum listed) for years number of years; simulates aeolian weathering 
	# process
	#
	# params:
	# 	years - number of years to weather rock
	def aeolian_weather(self, years):
		self.new_radius = self.radius - years * 0.04 * 10**(-9)

	def is_overlapping(new_rock):
		for rock in BasaltRock.rocks:
			# basic square overlap comparison
			if ((rock.x < new_rock.x) and (rock.x + rock.radius > new_rock.x - new_rock.radius)) \
					or ((rock.x > new_rock.x) and (new_rock.x + new_rock.radius > rock.x - rock.radius)) \
					or ((rock.y < new_rock.y) and (rock.y + rock.radius > new_rock.y - new_rock.radius)) \
					or ((rock.y > new_rock.y) and (new_rock.y + new_rock.radius > rock.y - rock.radius)):
				return True
		return False

x_small = np.random.random_sample(NUMBER) 
x = [n * WINDOW_SIZE * 2 - WINDOW_SIZE for n in x_small] # x ranges from -WINDOW_SIZE to +WINDOW_SIZE
y_small = np.random.random_sample(NUMBER) 
y = [n * WINDOW_SIZE * 2 - WINDOW_SIZE for n in y_small] # y ranges from -WINDOW_SIZE to +WINDOW_SIZE
radii_small = np.random.random_sample(NUMBER)
radii = [n * (MAX_RADIUS - MIN_RADIUS) + MIN_RADIUS for n in radii_small]	# radii ranges from 0 to MAX_RADIUS

# adding many rocks to rocks
for i in range(NUMBER):
	while radii_small[i] < MIN_RADIUS: # radii ranges from MIN_RADIUS to MAX_RADIUS
		radii_small[i] = np.random.random_sample(1)[0] * MAX_RADIUS
	radii.append(radii_small[i])
	rock = BasaltRock(x[i],y[i],radii[i],0)
	if BasaltRock.is_overlapping(rock) is False:
		BasaltRock.rocks.append(rock)

# for testing weathering products
for rock in BasaltRock.rocks:
	rock.aeolian_weather(TIME)
	BasaltRock.original_radii.append(rock.radius)
	BasaltRock.new_radii.append(rock.new_radius)

orig_r = [r * 20 for r in BasaltRock.original_radii]
new_r = [r * 20 for r in BasaltRock.new_radii]

total_area = WINDOW_SIZE * WINDOW_SIZE
cfa_x = []
cfa_y = []

cfa_sum = 0
sorted_rocks = sorted(BasaltRock.rocks, key=lambda rock: rock.radius, reverse=True)

for rock in sorted_rocks:
	diameter = rock.radius * 2
	area = math.pi * rock.radius * rock.radius 
	cfa_sum += area
	cfa_x.append(diameter)
	cfa_y.append(cfa_sum / total_area)

# plotting CFA
data = [
	go.Scatter(
		x=cfa_x,
		y=cfa_y,
		name='CFA',
		mode='markers'
	)
]

title = 'Cumulative Fractional Area (Random Boulders)'
layout = go.Layout(
	title = title,
	xaxis=dict(title='Diameter (m)'), 
	yaxis=dict(title='Cumulative Fractional Area')
)

figure = go.Figure(data=data, layout=layout)
plotly.offline.plot(figure, filename = 'CFA.html')

# plotting position of boulders
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
	title = title,
	xaxis=dict(title='x position (m)'), 
	yaxis=dict(title='y position (m)')
)

figure = go.Figure(data=data, layout=layout)
plotly.offline.plot(figure, filename = 'boulder_position.html')
