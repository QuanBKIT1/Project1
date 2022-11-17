from util.Calculator import *
import config

M = config.M
alpha = 0.6
Epsilon = config.Epsilon
max_iter = config.max_iter
number_clusters = config.number_clusters
rate = config.rate
M_ = config.M_


def init_monitored_elements(items, true_label):
    """initialize the monitored elements i of the cluster k"""
    dict1 = {}
    le = preprocessing.LabelEncoder()
    le.fit(true_label)
    number_monitored_item = math.floor(len(items) * rate / 100)
    monitored_index = random.sample(range(len(items)), number_monitored_item)
    monitored_label = [true_label[i] for i in monitored_index]
    monitored_label = le.transform(monitored_label)
    for i in range(number_monitored_item):
        dict1[monitored_index[i]] = monitored_label[i]

    return dict1


def g(x):
    return x * (alpha ** (x - 1))


def max_value(right_val):
    """Calculate the maximum value satisfying the inequality"""
    value = M
    while g(value) > right_val:
        value += 1
    return value


def calc_M1(items, monitored_elements):
    """Calculate value of M'"""
    global M

    distance_matrix = calc_matrix_distance(items)
    # Do vế trái là 1 hàm nghịch biến nên ta cần tìm giá trị nhỏ nhất
    # của vế phải ứng với U'(ik). Vì nếu M' thỏa mãn với giá trị nhỏ
    # nhất đó thì nó cũng thỏa mãn với các trường hợp khác

    min_right_value = 0

    for i in monitored_elements:
        # Calculate right-hand value
        U = 0
        for j in range(number_clusters):
            for k in range(number_clusters):
                if distance_matrix[i][k] == 0:
                    U = 1
                    break
                U += (distance_matrix[i][j] / distance_matrix[i][k]) ** (2 / (M - 1))
            else:
                U = 1 / U
        right_val = M * ((1 - alpha) / (1 / U - 1)) ** (M - 1)
        # M1_list.append(max_value(right_val))
        min_right_value = min(min_right_value, right_val)
    return max_value(min_right_value)


def init_fuzzification_coefficient(distance_matrix, monitored_elements, M1):
    """Calculate matrix of fuzzification coefficient correspond with each element"""
    global M, number_clusters
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

    while abs(f(x, a, b) - c) > Epsilon:
        if f(x + var_increase, a, b) <= c:
            x += var_increase
        else:
            var_increase /= 2
    return x


def update_U(distance_matrix, monitored_elements, M1):
    """Update membership value for each iteration"""
    global M
    U = np.zeros((len(distance_matrix), len(distance_matrix[0])))
    for i in range(len(U)):
        if i in monitored_elements:
            # Calculate U for monitored components
            dmin = np.min(distance_matrix[i])
            mu = distance_matrix[i] / dmin
            k = monitored_elements[i]
            a = 0
            for j in range(number_clusters):
                if j != k:
                    mu[j] = (M * mu[j] ** 2) ** (-1 / (M - 1))
                    a += mu[j]
            b = (M1 - M) / (M1 - 1)
            c = (M1 * mu[k] ** 2) ** (-1 / (M1 - 1))
            mu[k] = solution_of_equation(a, b, c)
            sumd = np.sum(mu)
            for j in range(number_clusters):
                U[i][j] = mu[j] / sumd
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

    V = np.zeros((number_clusters, len(items[0])))

    for k in range(len(V)):
        dummy_array = np.zeros(V.shape[1])
        dummy = 0
        for i in range(len(items)):
            dummy_array += (U[i][k] ** fuzzification_coefficient[i][k]) * items[i]
            dummy += U[i][k] ** fuzzification_coefficient[i][k]
        V[k] = dummy_array / dummy
    return V


def sSMC_FCM(items, true_label):
    """Implement sSMC_FCM"""
    global number_clusters, Epsilon, alpha, M, M_
    V = init_C_sSMC(items, true_label, number_clusters)
    monitored_elements = init_monitored_elements(items, true_label)
    # M1 = calc_M1(items, monitored_elements)

    m = init_fuzzification_coefficient(items, monitored_elements, M_)
    U = np.zeros((len(items), number_clusters))
    for k in range(max_iter):
        distance_matrix = calc_distance_item_to_cluster(items, V)
        U = update_U(distance_matrix, monitored_elements, M_)
        V_new = update_V(items, U, m)
        if end_condition(V_new, V, Epsilon):
            break
        V = np.copy(V_new)
    return U, V
