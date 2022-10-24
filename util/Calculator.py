import random

from scipy.spatial import distance


def d(i,j):
    """Calculate Euclidean"""
    return distance.euclidean(i,j)


def calc_matrix_distance(items):
    """Calculate distance between two elements
    Return matrix distance of it"""
    dist = []
    for i in range(len(items)):
        current = []
        for j in range(len(items)):
            current.append(d(items[i], items[j]))
        dist.append(current)
    return dist


def calc_distance_item_to_cluster(items, V):
    """ Calculate distance matrix distance between item and cluster """
    distance_matrix = []
    for i in range(len(items)):
        current = []
        for j in range(len(V)):
            current.append(d(items[i], V[j]))
        distance_matrix.append(current)

    return distance_matrix


def end_condition(V_new, V, Epsilon):
    """ End condition """

    for i in range(len(V)):
        if d(V_new[i], V[i]) > Epsilon:
            return False
    return True

def init_C(items,number_clusters):
    """Initialize random clusters """
    C = []
    index = random.sample(range(len(items) - 1), number_clusters)
    for i in index:
        C.append(items[i])
    return C