import copy

import numpy as np

import config
from util.Calculator import calc_distance_item_to_cluster, end_condition, init_C

m = config.m
Epsilon = config.Epsilon
number_clusters = config.number_clusters
max_iter = config.max_iter


def update_U(distance_matrix):
    """Update membership value for each iteration"""
    global m
    U = []
    for vector in distance_matrix:
        current = []
        for j in range(len(vector)):
            dummy = 0
            for l in range(len(vector)):
                if vector[l] == 0:
                    current.append(0)
                    break
                dummy += (vector[j] / vector[l]) ** (2 / (m - 1))
            else:
                current.append(1 / dummy)
        U.append(current)
    return U


def update_V(items, U):
    """ Update V after changing U """
    global m
    V = np.zeros((len(U[0]), len(items[0])))

    for k in range(len(V)):
        dummy_array = np.zeros(V.shape[1])
        dummy = 0
        for i in range(len(items)):
            dummy_array += (U[i][k] ** m) * items[i]
            dummy += U[i][k] ** m
        V[k] = dummy_array / dummy
    return V


def FCM(items):
    """Implement FCM"""
    global number_clusters, Epsilon
    V = init_C(items, number_clusters)
    U = []

    for k in range(max_iter):
        distance_matrix = calc_distance_item_to_cluster(items, V)
        U = update_U(distance_matrix)
        V_new = update_V(items, U)
        if end_condition(V_new, V, Epsilon):
            break
        V = copy.deepcopy(V_new)

    return U, V
