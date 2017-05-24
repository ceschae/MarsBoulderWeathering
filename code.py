# Mars boulder weathering simulation
# version: 0.9
# author: Caitlin Schaefer (ceschae@gmail.com)
# last updated: 24 May 2017
#
# weathers a NUMBER of basalt rocks in random locations from -WINDOW_SIZE
# to +WINDOW_SIZE in both x and y with random radii from MIN_RADIUS to 
# MAX_RADIUS (excluding overlapping boulders) for a given amount of TIME in days
# using aeolian weathering model, outputs before/after rock graph as a 
# result of weathering.
#
# to run on my machine:
# C:\Users\cesch\AppData\Local\Programs\Python\Python36-32\python.exe C:\Users\cesch\Documents\2016-2017\Research\MarsBoulderWeathering\code.py
# after running, can find image produced at in file as CFA.html and boulder_distribution.html

# TODO List:
#	- research: 
#		+ terrestrial alien rock weathering
#		+ not straightforward abrasion
#	- density plot
#	- save as PNG
#	- file import/export
#	- uniform distribution 
#	- movie of plot with changes?
#	- reformat title
#	- consider implementing own random distributions

import numpy as np
import math as math
# scipy may become important later

# import plotly for visualization
import plotly
import plotly.plotly as py 
import plotly.graph_objs as go

# csv for file processing
import csv

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
			# basic circle overlap comparison
			r = math.pow(math.pow(new_rock.x - rock.x, 2) + math.pow(new_rock.y - rock.y, 2), 0.5)
			if r - new_rock.radius - rock.radius < 0 is True:
				return True
		return False

file_rocks = []
file_radii = []
file_weathered_radii = []
file_lat = []
file_lon = []
with open('All_Lat_Diameter.csv') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		diameter = row[0]
		latitude = row[2]
		if diameter != "Radius" and diameter != "" and latitude != "" and latitude != "Lat":
			longitude = np.random.random_sample(1)[0] * WINDOW_SIZE * 2 - WINDOW_SIZE
			rock = BasaltRock(float(latitude), longitude, float(diameter), 0)
			file_rocks.append(rock)
			file_radii.append(rock.radius)
			file_lat.append(latitude)
			file_lon.append(longitude)
			rock.aeolian_weather(TIME)
			file_weathered_radii.append(rock.radius)
csvfile.close()

print("0% -> ", end='')
counter = 0
while len(BasaltRock.rocks) < NUMBER:
	x = np.random.random_sample(1)[0] * WINDOW_SIZE * 2 - WINDOW_SIZE
	y = np.random.random_sample(1)[0] * WINDOW_SIZE * 2 - WINDOW_SIZE
	radius = np.random.random_sample(1)[0] * (MAX_RADIUS - MIN_RADIUS) + MIN_RADIUS
	rock = BasaltRock(x, y, radius, 0)
	if BasaltRock.is_overlapping(rock) is False:
		BasaltRock.rocks.append(rock)
	if len(BasaltRock.rocks) // 50 > counter:
		print("*", end='')
		counter += 1
print(" -> 100%")

# for testing weathering products
for rock in BasaltRock.rocks:
	rock.aeolian_weather(TIME)
	BasaltRock.x.append(rock.x)
	BasaltRock.y.append(rock.y)
	BasaltRock.original_radii.append(rock.radius)
	BasaltRock.new_radii.append(rock.new_radius)

orig_r = [r * 5 for r in BasaltRock.original_radii]
new_r = [r * 5 for r in BasaltRock.new_radii]

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
		x=BasaltRock.x,
		y=BasaltRock.y,
		name='Original',
		mode='markers',
		hoverinfo='size',
		marker=dict(size = orig_r, color="rgb(0, 0, 0)")
	),
	go.Scatter(
		x=BasaltRock.x,
		y=BasaltRock.y,
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

# plotting position of file boulders
data = [
    go.Scatter(
		x=file_lat,
		y=file_lon,
		name='Original',
		mode='markers',
		hoverinfo='size',
		marker=dict(size = file_radii, color="rgb(0, 0, 0)")
	),
	go.Scatter(
		x=file_lat,
		y=file_lon,
		name='Post-Weathering',
		mode='markers',
		hoverinfo='size',
		marker=dict(size = file_weathered_radii, color="rgb(255, 255, 255")
	)
]

title = 'Time elapsed = ' + str(TIME)
layout = go.Layout(
	title = title,
	xaxis=dict(title='x position (m)'), 
	yaxis=dict(title='y position (m)')
)

figure = go.Figure(data=data, layout=layout)
plotly.offline.plot(figure, filename = 'file_boulder_position.html')
