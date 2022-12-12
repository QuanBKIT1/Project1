import random
import math
from sklearn.cluster import kmeans_plusplus
from sklearn import preprocessing
from util.ProcessorData import *

def d(i, j):
    """Calculate Euclidean"""
    distance = math.sqrt(np.sum((i - j) ** 2))
    return distance


def calc_matrix_distance(items):
    """Calculate distance between two elements
    Return matrix distance of it"""
    return [[d(items[i], items[j]) for j in range(len(items))] for i in range(len(items))]


def calc_distance_item_to_cluster(items, V):
    """ Calculate distance matrix distance between item and cluster """
    return [[d(items[i], V[j]) for j in range(len(V))] for i in range(len(items))]


def end_condition(V_new, V, Epsilon):
    """ End condition """

    for i in range(len(V)):
        if d(V_new[i], V[i]) > Epsilon:
            return False
    return True


def init_C(items, number_clusters):
    """Initialize random clusters """
    C = np.zeros((number_clusters, len(items[0])))

    # Create difference clusters
    index = random.sample(range(len(items)), number_clusters)
    for i in range(len(index)):
        C[i] = items[index[i]]
    return C


def init_C_KMeans(items, number_clusters):
    data = np.array(items)
    C = kmeans_plusplus(data, number_clusters)[0]
    return C


def init_C_sSMC(items, true_label, number_clusters):
    """Initialize clusters for sSMC algorithm based on labeled data"""
    le = preprocessing.LabelEncoder()
    le.fit(true_label)
    label = le.transform(true_label)

    # Initialize clusters
    C = np.zeros((number_clusters,len(items[0])))
    for i in range(number_clusters):
        dummy = list()
        for j in range(len(items)):
            if label[j] == i:
                dummy.append(items[j])
        C[i] = np.mean(dummy, axis=0)

    return C
