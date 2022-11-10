import numpy as np
import random
import math

from util.Calculator import calc_distance_item_to_cluster, end_condition, init_C
import config

M = config.M
alpha = config.alpha
Epsilon = config.Epsilon
max_iter = config.max_iter
number_clusters = config.number_clusters
rate = config.rate

def init_monitored_elements(distance_matrix):
    """initialize the monitored elements i of the cluster k"""
    dict1 = {}
    while (len(dict1) <= len(distance_matrix)*rate/100):
        dict1[random.randrange(len(distance_matrix))] = random.randrange(number_clusters)
    return dict1

def g(x,alpha):
    return x * (alpha ** (x-1))

def max_value(M, alpha, right_val):
    """Calculate the maximum value satisfying the inequality"""
    value = math.ceil(max(M, -1/ np.log(alpha)))
    while (g(value, alpha) <= right_val):
        value += 1
    return value

def calc_M1(M, distance_matrix, monitored_elements):
    """Calculate value of M'"""
    M1_list = []
    for i in monitored_elements:
        #Calculate right-hand value
        for j in range(number_clusters):
            dummy = 0
            for k in range(number_clusters):
                if distance_matrix[i][k] == 0:
                    Uik = 0
                    break
                dummy += (distance_matrix[i][j] / distance_matrix[i][k]) ** (2 / (M - 1))
            else:
                Uik = 1 / dummy
        right_val = M * ((1 - alpha)/ (1 / Uik - 1)) ** (M-1)
        M1_list.append(max_value(M, alpha, right_val))
        print(M1_list)
    print(1)
    return max(M1_list)


def init_fuzzification_coefficient(distance_matrix, monitored_elements):
    """Calculate matrix of fuzzification coefficient correspond with each element"""
    global M, M1, number_clusters
    m = np.full((len(distance_matrix), number_clusters), M)

    for i in monitored_elements:
        m[i][monitored_elements[i]] = M1
    return m

def f(x, a, b):
    """Calculate the left side of the equation"""
    return x / ((x + a) ** b)

def solution_of_equation(a, b, c):
    """Calculate solution of Equation"""
    x = 0
    var_increase = 1

    while (abs(f(x, a, b) - c) > Epsilon):
        if (f(x + var_increase, a, b) <= c):
            x += var_increase
        else:
            var_increase /= 2
    return x

def update_U(distance_matrix, monitored_elements):
    """Update membership value for each iteration"""
    global M
    U = np.zeros((len(distance_matrix), len(distance_matrix[0])))
    for i in range(len(U)):
        if i in monitored_elements:
            # Calculate U for monitored components
            dmin = np.min(distance_matrix[i])
            d = distance_matrix[i] / dmin
            k = monitored_elements[i]
            a = 0
            for j in range(number_clusters):
                if (j != k):
                    d[j] = (M * d[j] ** 2) ** (-1 / (M - 1))
                    a += d[j]
            b = (M1 - M)/(M1 - 1)
            c = (M1 * d[k] ** 2) ** (-1 / (M1 - 1))
            d[k] = solution_of_equation(a, b, c)
            sumd = np.sum(d)
            for j in range(number_clusters):
                U[i][j] = d[j]/ sumd
        else:
            # Calculate U for unsupervised components
            for j in range(number_clusters):
                dummy = 0
                for k in range(number_clusters):
                    if distance_matrix[i][k] == 0:
                        U[i][j] = 0
                        break
                    dummy += (distance_matrix[i][j] / distance_matrix[i][k]) ** (2 / (M - 1))
                else:
                    U[i][j] = 1 / dummy
    return U
def update_V(items, U, fuzzification_coefficient):
    """Update V after changing U"""

    V = np.zeros((number_clusters,len(items[0])))

    for k in range(len(V)):
        dummy_array = np.zeros(V.shape[1])
        dummy = 0
        for i in range(len(items)):
            dummy_array += (U[i][k]**fuzzification_coefficient[i][k])*items[i]
            dummy += U[i][k] ** fuzzification_coefficient[i]
        V[k] = dummy_array / dummy
    return V

def sSMC_FCM(items):
    """Implement sSMC_FCM"""
    global number_clusters, Epsilon, alpha, M, M1
    V = init_C(items, number_clusters)
    monitored_elements = init_monitored_elements(items)
    # M1 = calc_M1(M, items, monitored_elements)
    M1 = 4
    print(M1)
    m = init_fuzzification_coefficient(items, monitored_elements)
    U = np.zeros((len(items),number_clusters))
    for k in range(max_iter):
        distance_matrix = calc_distance_item_to_cluster(items, V)
        U = update_U(distance_matrix, monitored_elements)
        V_new = update_V(items, U, m)
        if end_condition(V_new, V, Epsilon):
            break
        V = np.copy(V_new)
    return U, V

