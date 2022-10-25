import random

import numpy as np
import math
from sklearn.cluster import kmeans_plusplus


def d(i, j):
    """Calculate Euclidean"""
    distance = math.sqrt(np.sum((i - j) ** 2))
    return distance


def calc_matrix_distance(items):
    """Calculate distance between two elements
    Return matrix distance of it"""
    dist = np.zeros((len(items), len(items)))
    for i in range(len(items)):
        for j in range(len(items)):
            dist[i][j] = d(items[i], items[j])
    return dist


def calc_distance_item_to_cluster(items, V):
    """ Calculate distance matrix distance between item and cluster """
    distance_matrix = np.zeros((len(items), len(V)))
    for i in range(len(items)):
        for j in range(len(V)):
            distance_matrix[i][j] = d(items[i], V[j])

    return distance_matrix


def end_condition(V_new, V, Epsilon):
    """ End condition """

    for i in range(len(V)):
        if d(V_new[i], V[i]) > Epsilon:
            return False
    return True


def init_C(items, number_clusters):
    """Initialize random clusters """
    C = np.zeros((number_clusters,len(items[0])))
    index = random.sample(range(len(items) - 1), number_clusters)
    for i in range(len(index)):
        C[i] = items[index[i]]
    return C


def init_C_KMeans(items, number_clusters):
    data = np.array(items)
    C = kmeans_plusplus(data, number_clusters)[0]
    return C
