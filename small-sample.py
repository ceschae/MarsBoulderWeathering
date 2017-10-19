from BasaltRock import *
import numpy as np
import math as math
import matplotlib.pyplot as plt

NUMBER = 10 # 10 rocks
TIME = 2000000 # 2 million years 
WINDOW_SIZE = 50 # 50 m x 50 m

small_sample_rocks = []
orig_x = []
orig_y = []

while (len(small_sample_rocks) < NUMBER):
	x = np.random.random_sample(1)[0] * WINDOW_SIZE * 2 - WINDOW_SIZE
	y = np.random.random_sample(1)[0] * WINDOW_SIZE * 2 - WINDOW_SIZE
	radius = np.random.random_sample(1)[0] * (MAX_RADIUS - MIN_RADIUS) + MIN_RADIUS
	rock = BasaltRock(x, y, radius, TEMP_HEIGHT, 0)
	if BasaltRock.is_overlapping(rock) is False:
		small_sample_rocks.append(rock)
		orig_x.append(x)
		orig_y.append(y)

for year in range(TIME):
	for rock in small_sample_rocks:
		rock.time = rock.time + 100000; # one hundrad thousand year has passed
		rock.aeolian_weather(1);
		crack_sample = np.random.normal(rock.time / CRACK_YEAR, CRACK_STDEV)
		print('crack sample:', crack_sample)
		print('rock.time / CRACK_YEAR: %6f' % (rock.time / CRACK_YEAR))
		if crack_sample >= 1:
			print('rock cracked:', rock.time)
			new_rock = rock.crack();
			if rock.radius < MIN_RADIUS:
				small_sample_rocks.remove(rock)
			if new_rock.radius >= MIN_RADIUS:
				small_sample_rocks.append(new_rock)
	if (year % 100000 == 0):
		x = []
		y = []
		for rock in small_sample_rocks:
			x.append(rock.x)
			y.append(rock.y)
		plt.plot(x, y, 'o')
		plt.title('boulder position at year ' + str(year))
		plt.xlabel('x position')
		plt.ylabel('y position')
		plt.savefig('test4/position-' + str(year) + '.png')
