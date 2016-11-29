'''	
Licence Info
'''

'''
	Author Info: <>
'''

from pprint import pprint
import numpy as np
import math

LIMIT = 1200
DIMENSIONS = []

def init(_raw_data):
	'''
		Function used to read the raw data for its headers and body and everything. Will return a matrix of image data.
		Will also update DIMENSIONS macro
	'''
	global DIMENSIONS

	#Parse the header for dimensions. 
	dimensions = _raw_data[1].split()
	dimensions = [int(x) for x in dimensions]
	DIMENSIONS = dimensions
	#dimensions = ['height','width']

	#Parse the body into a single file removing all the spaces and newlines
	image_data = ''.join(x.replace('\n','').replace(' ','') for x in _raw_data[2:])

	#Turn every element of the array into an integer. Convert that into a numpy array. And reshape that to a matrix of dimensions in the header
	image_data = np.array([int(x) for x in image_data]).reshape(dimensions[0], dimensions[1])

	return image_data

def distance(x1,y1,x2,y2):
	return math.sqrt( ((x2-x1)*(x2-x1)) + ((y2-y1)*(y2-y1)) )

def scan_distance_for_angle(_row,_col,_theta,_matrix):
	'''
		Being at the x and y location, and looking at _theta angle (absolute), find the first '1' and return the distance.
	'''
	global LIMIT, DIMENSIONS

	#Taking care of the fact that theta rounds off after 360
	_theta = _theta % 360

	#If theta is above 90 and under 270, x has to sample in negative direction, otherwise positive direction
	if _theta > 90 and _theta <= 270:
		direction_vector = -1
	else:
		direction_vector = 1

	angle_rad = _theta * math.pi / 180.0
	slope = math.tan(angle_rad)

	#Sampling x
	if direction_vector == 1:
		distance_x = [ 4 * (i-_row) for i in range(_row,DIMENSIONS[1]) ]
	else:
		distance_x = [ 4 * (i-_row) for i in range(0,_row) ]

	#Based on sampled x, find y
	distance_y = [ slope * x for x in distance_x ]

	#Now round off the absolute values in an index of the matrix taking care of the border conditions
	index_x_y = []
	for i in range(len(distance_x)):
		x = int(distance_x[i]/4) + _row
		y = _col - int(distance_y[i]/4)

		#Check for left border
		if x < 0:
			continue

		#Check for right border
		if x > DIMENSIONS[1]:
			continue

		#Check for the top border
		if y < 0:
			continue

		#Check for bottom border
		if y > DIMENSIONS[0]:
			continue

		index_x_y.append((x,y))

	# # index_w_b = [ matrix[i[0]][i[1]] for i in index_x_y]
	distance_color = [ (i, matrix[i[1]][i[0]], distance(_row,_col,i[0],i[1]) ) for i in index_x_y ]

	#Sort this list by the distances, ascending
	distance_color = sorted(distance_color, key=lambda tup: tup[2])

	for x in distance_color:
		if x[2] > LIMIT:
			return LIMIT

		if x[1] == 1:
			return x[2]

	#If neither a single '1' is met, nor we run out of 1200cm, simply return 
	return LIMIT

def run(_row,_col,_initial_angle, _matrix):
	if _initial_angle < 125:
		_initial_angle = _initial_angle + 360

	distances = [ scan_distance_for_angle(_row, _col, _initial_angle + x, _matrix) for x in range(-125,125,2)]

	return distances

if __name__ == "__main__":

	image_file = open('Assignment_04_Grid_Map.pbm','r')
	image_data_raw = image_file.read().split('\n')

	matrix = init(image_data_raw)

	x = 100
	y = 100
	initial_theta = 45
	print run(x,y,initial_theta,matrix)
