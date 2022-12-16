from util import ProcessorData, Evaluation
from util.Evaluation import *
import numpy as np


def f(x, a, b):
    """Calculate the left side of the equation"""
    return x / ((x + a) ** b)


class sSMC_FCM:

    def __init__(self, items, true_label, number_clusters, M, M1, alpha, rate, Epsilon, max_iter):
        self.items = items
        self.true_label = true_label
        self.number_clusters = number_clusters
        self.Epsilon = Epsilon
        self.M = M
        self.M1 = M1
        self.alpha = alpha
        self.rate = rate
        self.max_iter = max_iter
        self.V = init_C_sSMC(self.items, self.true_label, self.number_clusters)
        self.U = np.zeros((len(self.items), self.number_clusters))
        self.monitored_elements = self.init_monitored_elements()

    def run(self):
        """Implement sSMC_FCM"""
        for k in range(self.max_iter):
            item_to_cluster = calc_distance_item_to_cluster(self.items, self.V)
            self.update_U(item_to_cluster)
            V_new = self.update_V(self.items)
            if end_condition(V_new, self.V, self.Epsilon):
                break
            self.V = np.copy(V_new)
        self.eval()

    def eval(self):

        label = ProcessorData.assign_label(self.U)
        self.evalList = [Evaluation.RI(self.true_label, label), Evaluation.DBI(self.items, label, self.number_clusters),
                         Evaluation.PBM(self.items, label, self.number_clusters),
                         Evaluation.ASWC(self.items, label, self.number_clusters),
                         Evaluation.MA(self.true_label, label, self.number_clusters)]
        self.evalList = np.array(self.evalList)
        self.evalList = self.evalList.reshape(len(self.evalList), 1)

    def init_monitored_elements(self):
        """initialize the monitored elements i of the cluster k"""
        dict1 = {}
        le = preprocessing.LabelEncoder()
        le.fit(self.true_label)
        number_monitored_item = math.floor(len(self.items) * self.rate / 100)
        monitored_index = random.sample(range(len(self.items)), number_monitored_item)
        monitored_label = [self.true_label[i] for i in monitored_index]
        monitored_label = le.transform(monitored_label)
        for i in range(number_monitored_item):
            dict1[monitored_index[i]] = monitored_label[i]

        return dict1

    def g(self, x):
        return x * (self.alpha ** (x - 1))

    def max_value(self, right_val):
        """Calculate the maximum value satisfying the inequality"""
        value = self.M
        while self.g(value) > right_val:
            value += 1
        return value

    def calc_M1(self):
        """Calculate value of M'"""
        distance_matrix = calc_matrix_distance(self.items)
        # Do vế trái là 1 hàm nghịch biến nên ta cần tìm giá trị nhỏ nhất
        # của vế phải ứng với U'(ik). Vì nếu M' thỏa mãn với giá trị nhỏ
        # nhất đó thì nó cũng thỏa mãn với các trường hợp khác

        min_right_value = 0

        for i in self.monitored_elements:
            # Calculate right-hand value
            U = 0
            for j in range(self.number_clusters):
                for k in range(self.number_clusters):
                    if distance_matrix[i][k] == 0:
                        U = 1
                        break
                    U += (distance_matrix[i][j] / distance_matrix[i][k]) ** (2 / (self.M - 1))
                else:
                    U = 1 / U
            right_val = self.M * ((1 - self.alpha) / (1 / U - 1)) ** (self.M - 1)
            # M1_list.append(max_value(right_val))
            min_right_value = min(min_right_value, right_val)
        return self.max_value(min_right_value)

    def solution_of_equation(self, a, b, c):
        """Calculate solution of Equation"""
        x = 0
        var_increase = 1

        while abs(f(x, a, b) - c) > self.Epsilon:
            if f(x + var_increase, a, b) <= c:
                x += var_increase
            else:
                var_increase /= 2
        return x

    def update_U(self, item_to_cluster):
        """Update membership value for each iteration"""
        for i in range(len(self.U)):
            if i in self.monitored_elements:
                # Calculate U for monitored components
                dmin = np.min(item_to_cluster[i])
                dij = item_to_cluster[i] / dmin
                k = self.monitored_elements[i]
                a = 0
                for j in range(self.number_clusters):
                    if j != k:
                        dij[j] = (self.M * dij[j] ** 2) ** (-1 / (self.M - 1))
                        a += dij[j]
                b = (self.M1 - self.M) / (self.M1 - 1)
                c = (self.M1 * dij[k] ** 2) ** (-1 / (self.M1 - 1))
                dij[k] = self.solution_of_equation(a, b, c)
                sumd = np.sum(dij)
                for j in range(self.number_clusters):
                    self.U[i][j] = dij[j] / sumd
            else:
                # Calculate U for unsupervised components
                for j in range(self.number_clusters):
                    dummy = 0
                    for k in range(self.number_clusters):
                        if item_to_cluster[i][k] == 0:
                            self.U[i][j] = 0
                            break
                        dummy += (item_to_cluster[i][j] / item_to_cluster[i][k]) ** (2 / (self.M - 1))
                    else:
                        self.U[i][j] = 1 / dummy

    def update_V(self, fuzzification_coefficient):
        """Update V after changing U"""

        V_new = np.zeros((self.number_clusters, len(self.items[0])))

        for k in range(len(V_new)):
            dummy_array = np.zeros(V_new.shape[1])
            dummy = 0
            for i in range(len(self.items)):
                dummy_array += (self.U[i][k] ** fuzzification_coefficient[i][k]) * self.items[i]
                dummy += self.U[i][k] ** fuzzification_coefficient[i][k]
            V_new[k] = dummy_array / dummy
        return V_new

    # def printResult(self):
    #     label = assign_label(self.U)
    #     print("sSMC-FCM :")
    #     print("Rand Index Score: ", RI(self.true_label, label))
    #     print("DBI Score: ", DBI(self.items, label, self.number_clusters))
    #     print("PBM Score: ", PBM(self.items, label, self.number_clusters))
    #     print("ASWC Score: ", ASWC(self.items, label, self.number_clusters))
    #     print("MA Score: ", MA(self.true_label, label, self.number_clusters))

# if __name__ == "__main__":
#     data_table = readData("../dataset/wine.data")
#     i1, i2 = preprocessData(data_table, 0, [])
#     ssmc = sSMC_FCM(i1, i2, 3, 2, 6, 0.6, 20, 0.000001, 300)
#     ssmc.run()
#     ssmc.printResult()
