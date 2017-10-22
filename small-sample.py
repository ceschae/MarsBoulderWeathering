from BasaltRock import *
import numpy as np
import math as math
import matplotlib.pyplot as plt

NUMBER = 10 # 10 rocks
TIME = 15000000 # 15 million years 
WINDOW_SIZE = 50 # 50 m x 50 m

small_sample_rocks = []
orig_x = []
orig_y = []
orig_radius = []

while (len(small_sample_rocks) < NUMBER):
	x = np.random.random_sample(1)[0] * WINDOW_SIZE * 2 - WINDOW_SIZE
	y = np.random.random_sample(1)[0] * WINDOW_SIZE * 2 - WINDOW_SIZE
	radius = np.random.random_sample(1)[0] * (MAX_RADIUS - MIN_RADIUS) + MIN_RADIUS
	rock = BasaltRock(x, y, radius, TEMP_HEIGHT, 0)
	if BasaltRock.is_overlapping(rock) is False:
		small_sample_rocks.append(rock)
		orig_x.append(x)
		orig_y.append(y)
		orig_radius.append(radius)
print(len(small_sample_rocks))

for year in range(TIME):
	for rock in small_sample_rocks:
		rock.time = rock.time + 1; # one hundrad thousand year has passed
		rock.aeolian_weather(1);
		crack_sample = np.random.normal(rock.time / CRACK_YEAR, CRACK_STDEV)
		#print('crack sample:', crack_sample)
		#print('rock.time / CRACK_YEAR: %6f' % (rock.time / CRACK_YEAR))
		if crack_sample >= 1:
			print('rock cracked:', rock.time)
			print('   old rock before:', rock)
			new_rock = rock.crack()
			print('   old rock after:', rock)
			print('   new rock:', new_rock)
			if rock.radius < MIN_RADIUS:
				small_sample_rocks.remove(rock)
			if new_rock.radius >= MIN_RADIUS:
				small_sample_rocks.append(new_rock)
	if (year % 100000 == 0):
		x = []
		y = []
		rad = []
		print(len(small_sample_rocks))
		for rock in small_sample_rocks:
			x.append(rock.x)
			y.append(rock.y)
			rad.append(rock.radius)
		plt.scatter(orig_x, orig_y, marker='s', s=orig_radius, color="#949494")
		plt.scatter(x, y, marker='s', s=rad, color="#8D0CE8")
		plt.title('boulder position at year ' + str(year / 100000) + ' x 10^5')
		plt.xlabel('x position')
		plt.ylabel('y position')
		plt.savefig('test/position-' + str(year / 100000) + '.png')
