import sys
import pyart
import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy import ndimage
import pickle
import os

import radar_color

EXPORT_FIELDS = ['reflectivity', 'velocity', 'spectrum_width']
DISPLAY_FIELDS = ['reflectivity', 'velocity']

print "Reading NEXRAD data..."

rad = pyart.io.read(sys.argv[1])

print "Mapping to grid..."

grid = pyart.map.grid_from_radars(
    (rad,),
    grid_shape=(1,512,512),
    grid_limits=((2000, 2000), (-300000.0, 300000.0), (-300000.0, 300000.0)))

print "Have {} gridded fields ({})".format(len(grid.fields.keys()), str(grid.fields.keys()))


displays = dict()

for field in DISPLAY_FIELDS:
	displays[field] = radar_color.auto_colorize(grid.fields[field]['data'][0][::-1], field)


current_field = 0

MARGIN = 100

tornadic = []
non_tornadic = []

def handleClick(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONUP:
		tornadic.append([y-MARGIN, y+MARGIN, x-MARGIN, x+MARGIN])
		cv2.putText(displays[DISPLAY_FIELDS[current_field]], 'T', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))
		cv2.imshow("RADAR", displays[DISPLAY_FIELDS[current_field]])
	elif event == cv2.EVENT_RBUTTONUP:
		non_tornadic.append([y-MARGIN, y+MARGIN, x-MARGIN, x+MARGIN])
		cv2.putText(displays[DISPLAY_FIELDS[current_field]], 'S', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0))
		cv2.imshow("RADAR", displays[DISPLAY_FIELDS[current_field]])

cv2.imshow("RADAR", displays[DISPLAY_FIELDS[current_field]])
cv2.setMouseCallback("RADAR", handleClick)

while True:
	k = cv2.waitKey()
	if k == 27:
		break
	elif k == ord('t'):
		current_field += 1
		if current_field >= len(DISPLAY_FIELDS):
			current_field = 0
		cv2.imshow("RADAR", displays[DISPLAY_FIELDS[current_field]])

print "Exporting gridded data ({} tornado(es), {} storm(s))".format(len(tornadic), len(non_tornadic))

def saveStorms(cells, filename):
	out = []
	if os.path.exists(filename):
		out = pickle.load(open(filename, 'r'))
	
	with open(filename,'w') as f:
		for storm in cells:
			data = {}
			for field_name in EXPORT_FIELDS:
				field = grid.fields[field_name]['data'][0]
				data[field_name] = field[storm[0]:storm[1],storm[2]:storm[3]]
			out.append(data)
		pickle.dump(out, f)

saveStorms(tornadic, 'tornadic')
saveStorms(non_tornadic, 'non-tornadic')

cv2.destroyAllWindows()