import copy
from util.Calculator import calc_matrix_distance, calc_distance_item_to_cluster, end_condition, init_C
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
    for i in range(len(delta)):
        delta[i].sort()

    delta_star = []
    n = int(len(items) / number_clusters)
    # Calculate delta_star with formula
    for i in range(len(items)):
        dummy = 0
        for j in range(n):
            dummy += delta[i][j]
        delta_star.append(dummy)

    # Find min max range of delta_star
    min_delta_star = min(delta_star)
    max_delta_star = max(delta_star)

    fuzzification_coefficient = []
    # Calculate fuzzification coefficient
    for i in range(len(items)):
        dummy = ((delta_star[i] - min_delta_star) / (max_delta_star - min_delta_star)) ** alpha
        mi = mL + (mU - mL) * dummy
        fuzzification_coefficient.append(mi)
    return fuzzification_coefficient


def update_U(distance_matrix, fuzzification_coefficient):
    """Update membership value for each iteration"""

    U = []
    for i in range(len(distance_matrix)):
        current = []
        for j in range(len(distance_matrix[0])):
            dummy = 0
            for k in range(len(distance_matrix[0])):
                if distance_matrix[i][k] == 0:
                    current.append(0)
                    break
                dummy += (distance_matrix[i][j] / distance_matrix[i][k]) ** (2 / (fuzzification_coefficient[i] - 1))
            else:
                current.append(1 / dummy)
        U.append(current)
    return U


def update_V(items, U, fuzzification_coefficient):
    """ Update V after changing U """

    V = []

    for k in range(len(U[0])):
        current_cluster = []

        for j in range(len(items[0])):
            dummy_sum_ux = 0.0
            dummy_sum_u = 0.0
            for i in range(len(items)):
                dummy_sum_ux += (U[i][k] ** fuzzification_coefficient[i]) * items[i][j]
                dummy_sum_u += (U[i][k] ** fuzzification_coefficient[i])
            current_cluster.append(dummy_sum_ux / dummy_sum_u)
        V.append(current_cluster)

    return V


def MC_FCM(items):
    """Implement MC_FCM"""
    global number_clusters, Epsilon
    V = init_C(items, number_clusters)
    fuzzification_coefficient = init_fuzzification_coefficient(items)
    U = []
    for k in range(max_iter):
        distance_matrix = calc_distance_item_to_cluster(items, V)
        U = update_U(distance_matrix, fuzzification_coefficient)
        V_new = update_V(items, U, fuzzification_coefficient)
        if end_condition(V_new, V, Epsilon):
            break
        V = copy.deepcopy(V_new)

    return U, V

