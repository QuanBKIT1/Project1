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
    U = np.zeros((len(distance_matrix), len(distance_matrix[0])))
    for i in range(len(U)):
        for j in range(number_clusters):
            dummy = 0
            for k in range(number_clusters):
                if distance_matrix[i][k] == 0:
                    U[i][j] = 0
                    break
                dummy += (distance_matrix[i][j] / distance_matrix[i][k]) ** (2 / (m - 1))
            else:
                U[i][j] = 1 / dummy
    return U


def update_V(items, U):
    """ Update V after changing U """
    global m
    V = np.zeros((number_clusters, len(items[0])))

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
