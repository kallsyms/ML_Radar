import numpy as np
import cv2

# BGR *not* RGB
REFLECTIVITY_MAP = [[255, 255, 170], [255, 160, 85], [255, 0, 29], [91, 229, 126], [67, 204, 78], [57, 178, 46], [61, 153, 30], [102, 255, 255], [102, 204, 255], [76, 136, 255], [25, 25, 255], [61, 61, 204], [49, 49, 165], [237, 0, 237], [205, 103, 137], [230, 240, 250]]
VELOCITY_MAP = [[243, 12, 25], [243, 12, 36], [245, 73, 56], [246, 156, 85], [179, 233, 111], [97, 201, 93], [40, 170, 80], [25, 164, 81], [29, 195, 115], [31, 220, 152], [0, 0, 0], [0, 0, 0], [41, 254, 249], [36, 222, 233], [33, 194, 227], [32, 161, 219], [26, 96, 202], [24, 49, 192], [23, 3, 189], [28, 0, 133], [63, 1, 73], [94, 4, 44]]


def colorize(src, color_map, color_start = 0, step = 5, under_color = [0,0,0], over_color = [0,0,0], missing_color = [0,0,0]):
	color_end = color_start + (step * len(color_map))
	
	# Create blank array with same width/height dimensions as raw data, but with a 3rd color dimension (of size 3 - BGR)
	d = np.zeros(src.shape + tuple([3]), np.uint8)
	
	# Apply missing color to anywhere the mask was present in the raw data
	d[src.mask] = missing_color
	
	d[src < color_start] = under_color
	d[src > color_end] = over_color
	
	# For each segment of the color mapping, apply the appropriate color
	for i in range(color_start, color_end-1, step):
		d[(src >= i) & (src < i+step)] = color_map[int((i-color_start)/step)]
	
	return d

def auto_colorize(src, field_name):
	if field_name == 'reflectivity':
		return colorize(src, REFLECTIVITY_MAP)
	elif field_name == 'velocity':
		return colorize(src, VELOCITY_MAP, color_start = -33, step = 3, over_color=[255, 255, 255])