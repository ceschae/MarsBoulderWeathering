# Mars boulder weathering simulation
# version: 0.10
# author: Caitlin Schaefer (ceschae@gmail.com)
# last updated: 4 October 2017
#
# weathers a NUMBER of basalt rocks in random locations from -WINDOW_SIZE
# to +WINDOW_SIZE in both x and y with random radii from MIN_RADIUS to 
# MAX_RADIUS (excluding overlapping boulders) for a given amount of TIME in days
# using aeolian weathering model, outputs before/after rock graph as a 
# result of weathering.
#
# to run on my machine:
# C:\Users\cesch\AppData\Local\Programs\Python\Python36-32\python.exe C:\Users\cesch\Documents\2016-2017\Research\MarsBoulderWeathering\code.py
# after running, can find image produced at in file as CFA.html, boulder_distribution.html, and file_boulder_position.html

# TODO List:
#	- research: 
#		+ terrestrial alien rock weathering
#		+ not straightforward abrasion
#	- density plot
#	- uniform distribution 
#	- movie of plot with changes?
#	- reformat title
#
#boulder cracking 
#	- "3D" boulders
#	- where it's going to crack:
#		+ mass breaks unevenly along diameter
#		+ figuring out where to put the boulders after is tricky
#			-> sometimes it falls over and sometimes it doesn't
#			-> bigger piece stays where it is (with its center adjusted)
#			-> smaller piece falls over (with its center adjusted, and its diameter is the "crack length" along the old diameter axis)
#			-> "left" piece x, y: center must shift right
#			-> "smaller" piece x, y: center will be (x + radius, y)
#		+ ideally we'd store information about height?
#	- we'll have to deal with the "multiple cracks" thing at some point
#
#aeolian
#	- probably ok that it's linear erosion
#	- gaussian distribution
#		+ mean
#		+ stdev
#		+ every year picks something in that distribution as the "amount eroded"
#	- too small, turn into rubble pile
#		+ if boulder size is < detection limit (maybe 0.25 m), remove from model
#
#long term
#	- variables get optimized and solved for based on before/after sample data
	
import numpy as np
import math as math
import matplotlib.pyplot as plt
# scipy may become important later

# csv for file processing
import csv

NUMBER = 1000 # a thousand rocks
TIME = 1500000 # 1.5 million years
WINDOW_SIZE = 100000 # 100000 m x 100000 m
MAX_RADIUS = 10 # 10 m
MIN_RADIUS = 0.25 # 0.25 m

# boulder cracking variables
CRACK_YEAR = 1000000 # a million years
CRACK_STDEV = 0.001 # TODO: revisit
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
	def __init__(self, x_pos, y_pos, diameter, generation):
		self.x = x_pos
		self.y = y_pos
		self.radius = diameter / 2 
		self.new_radius = diameter / 2
		self.gen = generation
		self.time = 0;
		#self.height = ??

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

	def crack(self):
		crack_spot = self.radius * 2 * np.random.normal(CRACK_X_MEAN, CRACK_X_STDEV)
		new_rock = BasaltRock(self.x, self.y, self.radius * 2 - crack_spot, self.gen + 1)
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

# arrays to help with graphing
file_rocks = []
file_radii = []
file_weathered_radii = []
file_lat = []
file_lon = []

max_lat = 0;
min_lat = 0;
max_lon = 0;
min_lon = 0;
# file input
with open('Lat_Long_ESP_011779_2050.csv') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		diameter = row[0]
		latitude = row[1]
		longitude = row[2]
		if diameter != "Certain_Boulder_Line.SHAPE_Length" and diameter != "" \
					and latitude != "" and latitude != "Certain_Boulder_Points.LAT" \
					and longitude != "" and longitude != "Certain_Boulder_Points.LON" \
					and float(diameter) / 2 >= MIN_RADIUS:
			rock = BasaltRock(float(latitude), float(longitude), float(diameter), 0)
			file_rocks.append(rock)
			file_radii.append(rock.radius)
			file_lat.append(float(latitude))
			file_lon.append(float(longitude))
			if float(latitude) > max_lat:
				max_lat = float(latitude)
			elif float(latitude) < min_lat:
				min_lat = float(latitude)
			if float(longitude) > max_lon:
				max_lon = float(longitude)
			elif float(longitude) < min_lon:
				min_lon = float(longitude)
			# rock.aeolian_weather(TIME)
csvfile.close()

# weathering code
for year in range(TIME):
	for rock in file_rocks:
		rock.time = rock.time + 1; # one year has passed
		rock.aeolian_weather(1);
		crack_sample = np.random.normal(rock.time / CRACK_YEAR, CRACK_STDEV)
		if crack_sample >= 1:
			new_rock = rock.crack();
			if rock.radius < MIN_RADIUS:
				file_rocks.remove(rock)
			else:
				file_rocks.append(new_rock)
				file_radii.append(new_rock.radius)
				file_lat.append(new_rock.x)
				file_lon.append(new_rock.y)


# file output
with open('011779_2050_weathered.csv', 'w', newline='') as csvfile:
    rockwriter = csv.writer(csvfile, delimiter=',')
    rockwriter.writerow(['lat_orig', 'lon_orig', 'diam_orig', 'lat_new', 'lon_new', 'diam_new', 'generation'])
    for i in range(len(file_rocks)):
    	file_weathered_radii.append(file_rocks[i].radius)
    	rockwriter.writerow([str(file_lat[i]), str(file_lon[i]), str(file_radii[i] * 2), \
    		str(file_lat[i]), str(file_lon[i]), str(file_weathered_radii[i] * 2), str(file_rocks[i].gen)])

# random distribution generation
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

# aeolian weathering on random distribtuion 
for rock in BasaltRock.rocks:
	rock.aeolian_weather(TIME)
	BasaltRock.x.append(rock.x)
	BasaltRock.y.append(rock.y)
	BasaltRock.original_radii.append(rock.radius)
	BasaltRock.new_radii.append(rock.new_radius)

# structures for CFA plot
total_area = WINDOW_SIZE * WINDOW_SIZE
cfa_x = []
cfa_y = []

#generating CFA data
cfa_sum = 0
sorted_rocks = sorted(BasaltRock.rocks, key=lambda rock: rock.radius, reverse=True)
for rock in sorted_rocks:
	diameter = rock.radius * 2
	area = math.pi * rock.radius * rock.radius 
	cfa_sum += area
	cfa_x.append(diameter)
	cfa_y.append(cfa_sum / total_area)

# plotting CFA of randomly generated boulders
plt.plot(cfa_x, cfa_y, 'o')
plt.title('cumulative fractional area (cfa)')
plt.xlabel('diameter of boulder (m)')
plt.ylabel('cumulative fractional area (m^2 / m^2)')
plt.show()

# plotting position of randomly generated boulders
plt.plot(BasaltRock.x, BasaltRock.y, 'o')
plt.title('boulder position (randomly generated)')
plt.xlabel('x position')
plt.ylabel('y position')
plt.show()

#generating CFA data
file_cfa_sum = 0
file_sorted_rocks = sorted(file_rocks, key=lambda rock: rock.radius, reverse=True)
# structures for CFA plot
file_total_area = (max_lat - min_lat) * 59000 * (max_lon - min_lon) * 59000 # degress to m
file_cfa_x = []
file_cfa_y = []
for rock in file_sorted_rocks:
	diameter = rock.radius * 2
	area = math.pi * rock.radius * rock.radius 
	file_cfa_sum += area
	file_cfa_x.append(diameter)
	file_cfa_y.append(cfa_sum / total_area)

# plotting position of file boulders
plt.plot(file_cfa_x, file_cfa_y, 'o')
plt.title('cumulative fractional area (cfa)')
plt.xlabel('diameter of boulder (m)')
plt.ylabel('cumulative fractional area (m^2 / m^2)')
plt.show()