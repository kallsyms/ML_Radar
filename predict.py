import pickle
import numpy as np

ATTRIBUTES = ['reflectivity', 'velocity', 'spectrum_width']

# Function to create a filled, flat representation of the storm suitable for ML
def storm_representation(s):
    repr = []
    for attr in ATTRIBUTES:
        repr.extend(s[attr].filled().flatten())
    
    return np.array(repr)


tornadic = pickle.load(open('tornadic', 'r'))
non_tornadic = pickle.load(open('non-tornadic', 'r'))

print "Loaded {} tornadic storms and {} non-tornadic storms".format(len(tornadic), len(non_tornadic))

num_storms = len(tornadic) + len(non_tornadic)

# len(storm_representation({any storm})) should be 120,000 = 200*200*3 = w*h*num_images
storm_repr_size = 120000

data = np.zeros(storm_repr_size)
target = []

for storm in tornadic:
    r = storm_representation(storm)
    if len(r) == storm_repr_size:
        data = np.vstack((data, r))
        target.append(1)

for storm in non_tornadic:
    r = storm_representation(storm)
    if len(r) == storm_repr_size:
        data = np.vstack((data, r))
        target.append(0)

data = data[1:] # Remove leading set of zeroes. TODO: better way to stack all of these?
target = np.array(target)

# Pick the training samples - train with 70% of the data, test with the other 30%. These percentages are completely arbitrary.
test_indexes = np.random.uniform(0, 1, len(data)) <= 0.3

train_data = data[test_indexes == False]
train_target = target[test_indexes == False]
test_data = data[test_indexes == True]
test_target = target[test_indexes == True]

# Training
from sklearn.neighbors import KNeighborsClassifier

classifier = KNeighborsClassifier()
classifier.fit(train_data, train_target)

print "After training, predicting:"
print classifier.predict(test_data)
print "In reality:"
print test_target