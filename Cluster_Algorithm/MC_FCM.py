import numpy as np

from util.Calculator import calc_matrix_distance, calc_distance_item_to_cluster, end_condition, init_C,init_C_KMeans
import config

mL = config.mL
mU = config.mU
alpha = config.alpha
Epsilon = config.Epsilon
number_clusters = config.number_clusters
max_iter = config.max_iter


def init_fuzzification_coefficient(items):
    """Calculate list of fuzzification coefficient correspond with each element"""

    global mL, mU, alpha, number_clusters
    delta = calc_matrix_distance(items)

    # Sort matrix distance by row
    delta = np.sort(delta)

    delta_star = np.zeros(len(delta))
    n = int(len(items) / number_clusters)
    # Calculate delta_star with formula
    for i in range(len(delta)):
        dummy = 0
        for j in range(n):
            dummy += delta[i][j]
        delta_star[i] = dummy

    # Find min max range of delta_star
    min_delta_star = min(delta_star)
    max_delta_star = max(delta_star)

    fuzzification_coefficient = np.zeros(len(items))
    # Calculate fuzzification coefficient
    for i in range(len(fuzzification_coefficient)):
        dummy = ((delta_star[i] - min_delta_star) / (max_delta_star - min_delta_star)) ** alpha
        mi = mL + (mU - mL) * dummy
        fuzzification_coefficient[i] = mi
    return fuzzification_coefficient


def update_U(distance_matrix, fuzzification_coefficient):
    """Update membership value for each iteration"""

    U = np.zeros((len(distance_matrix),number_clusters))
    for i in range(len(U)):
        for j in range(number_clusters):
            dummy = 0
            for k in range(number_clusters):
                if distance_matrix[i][k] == 0:
                    U[i][j] = 1
                    break
                dummy += (distance_matrix[i][j] / distance_matrix[i][k]) ** (2 / (fuzzification_coefficient[i] - 1))
            else:
                U[i][j] = 1/dummy
    return U


def update_V(items, U, fuzzification_coefficient):
    """ Update V after changing U """

    V = np.zeros((number_clusters,len(items[0])))

    for k in range(len(V)):
        dummy_array = np.zeros(V.shape[1])
        dummy = 0
        for i in range(len(items)):
            dummy_array += (U[i][k]**fuzzification_coefficient[i])*items[i]
            dummy += U[i][k]**fuzzification_coefficient[i]
        V[k] = dummy_array/dummy
    return V


def MC_FCM(items):
    """Implement MC_FCM"""
    global number_clusters, Epsilon
    V = init_C(items, number_clusters)
    fuzzification_coefficient = init_fuzzification_coefficient(items)
    U = np.zeros((len(items),number_clusters))
    for k in range(max_iter):
        distance_matrix = calc_distance_item_to_cluster(items, V)
        U = update_U(distance_matrix, fuzzification_coefficient)
        V_new = update_V(items, U, fuzzification_coefficient)
        if end_condition(V_new, V, Epsilon):
            break
        V = np.copy(V_new)

    return U, V

