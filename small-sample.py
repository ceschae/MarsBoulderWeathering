# TODO
# - Why is it that some boulders seem to shrink and other don't 
# 		(they should be shrinking with every time step right? so 
#		they should be noticeably smaller in each plot but it seems 
#		they shrink in big chunks)
# - Mass doesn't seem to be conserved with the cracking
# - At some point we will have to consider that they can crack in 
#		other direction other than the x-axis
# - They seem to be disappearing rather quickly (also I suggest 
#		stopping plotting once length(small_sample_rocks) = 0)
#   + fixed issue of continuing to plot
# - Not sure if my generation coloring scheme is working properly 
#		(I think we should keep original rocks as gen 0 when gen 
#		resets it goes to 1 maybe? so we can identify original rocks 
#		vs. newest rocks). 

from BasaltRock import *
import numpy as np
import math as math
import matplotlib.pyplot as plt
import pylab

NUMBER = 10 # 10 rocks
TIME = 15000000 # 15 million years 
WINDOW_SIZE = 50 # 50 m x 50 m

small_sample_rocks = []
orig_x = []
orig_y = []
orig_radius = []

def my_square_scatter(axes, x_array, y_array, size_array, gen_array, **kwargs):
	c = ['b', 'r', 'g', 'k', 'm', 'c', 'y']
	for x, y, r, g in zip(x_array, y_array, size_array, gen_array):
		ii = g % 7
		square = pylab.Rectangle((x-r,y-r), r*2, r*2, color=c[ii], **kwargs)
		axes.add_patch(square)
	return True

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

text_file = open("test2/output.txt", "w")
for year in range(TIME):
	for rock in small_sample_rocks:
		rock.time = rock.time + 1; # one hundrad thousand year has passed
		rock.aeolian_weather(1);
		crack_sample = np.random.normal(rock.time / CRACK_YEAR, CRACK_STDEV)
		#print('crack sample:', crack_sample)
		#print('rock.time / CRACK_YEAR: %6f' % (rock.time / CRACK_YEAR))
		if crack_sample >= 1:
			text_file.write('rock cracked:' + str(rock.time))
			text_file.write('   old rock before:' + rock.toString())
			new_rock = rock.crack()
			text_file.write('   old rock after:' + rock.toString())
			text_file.write('   new rock:' + new_rock.toString())
			if rock.radius < MIN_RADIUS:
				small_sample_rocks.remove(rock)
			if new_rock.radius >= MIN_RADIUS:
				small_sample_rocks.append(new_rock)
	if (year % 100000 == 0 and len(small_sample_rocks) != 0):
		x = []
		y = []
		rad = []
		gen = []
		text_file.write("# of rocks at year " + str(year) + ": " + str(len(small_sample_rocks)))
		i = 0
		for rock in small_sample_rocks:
			x.append(rock.x)
			y.append(rock.y)
			rad.append(rock.radius)
			gen.append(rock.gen)
			text_file.write("   rock #" + str(i) + " gen:" + str(rock.gen))
			i += 1
		
		axes = pylab.axes()
		my_square_scatter(axes, x, y, rad, gen)
		pylab.axis('scaled')
		pylab.axis([-WINDOW_SIZE,WINDOW_SIZE,-WINDOW_SIZE,WINDOW_SIZE])
		pylab.savefig('test2/position-' + str(year / 100000) + '.png')
		pylab.close()
text_file.close()