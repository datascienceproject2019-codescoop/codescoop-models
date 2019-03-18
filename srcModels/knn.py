import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_boston

bos = load_boston()
data = pd.DataFrame(bos.data)
data.columns = bos.feature_names

# normalize the columns
data = data.apply(lambda col: ((col-np.mean(col))/np.std(col)), axis=0)

# calculating distance between two instances
def distance(instance1, instance2):
    instance1 = np.array(instance1)
    instance2 = np.array(instance2)
    return np.linalg.norm(instance1 - instance2)

# add id variable
ids = range(1,len(data)+1)

# get_neighbors returns k nearest neighbours for an instance

def get_neighbors(k, instance, data, labels, distance=distance):
    distances = []
    for i in range(len(data)):
        dist = distance(instance, data.iloc[i])
        distances.append((dist, labels[i]))
    distances.sort(key=lambda x: x[0])
    neighbors = distances[1:k+1]
    return neighbors

# function returns distance and index of the neighbour)
nbrs = get_neighbors(5, data.iloc[1], data, ids)
nbrs
