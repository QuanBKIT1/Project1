import copy
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
    for i in range(len(distance_matrix)):
        current = []
        for j in range(len(distance_matrix[0])):
            dummy = 0
            for k in range(len(distance_matrix[0])):
                if distance_matrix[i][k] == 0:
                    current.append(0)
                    break
                dummy += (distance_matrix[i][j] / distance_matrix[i][k]) ** (2 / (m - 1))
            else:
                current.append(1 / dummy)
        U.append(current)
    return U


def update_V(items, U):
    """ Update V after changing U """
    global m
    V = []

    for k in range(len(U[0])):
        current_cluster = []

        for j in range(len(items[0])):
            dummy_sum_ux = 0.0
            dummy_sum_u = 0.0
            for i in range(len(items)):
                dummy_sum_ux += (U[i][k] ** m) * items[i][j]
                dummy_sum_u += (U[i][k] ** m)
            current_cluster.append(dummy_sum_ux / dummy_sum_u)
        V.append(current_cluster)
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
