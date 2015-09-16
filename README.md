# ML_Radar

----

Testing how machine learning can be used in the analysis of level 2 RADAR data for tornado detection (and prediction).

There are 2 programs: selector.py and predict.py

## selector.py

Used to view and select storms from level 2 RADAR data. Run as

    python selector.py path/to/level2/file

After the radar data has been projected onto a grid, you can mark storms as tornadic (left-click) or non-tornadic (right-click). When done, ESC exits and saves.

Included is (non-)tornadic.gz which can be used as a base set (must be ungzipped). These include samples from 3 major EF5 tornadoes (El Reno 2013, Joplin 2011, and Moore 2013)

## predict.py

Reads tornadic and non-tornadic data files and does basic learning and predicting on the data. Currently this only predicts from data already in the datasets (i.e. not new data), but the ability to predict new data will be coming soon.
