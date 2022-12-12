from util.Calculator import *
from util.ProcessorData import ReadData, assign_label
from util.Evaluation import *
import numpy as np
class sSMC_FCM():
    def setFileData(self, fileData):
        self.fileData = fileData

    def processData(self, colLabel):
        self.items, self.true_label = ReadData(self.fileData, colLabel)

    def sSMC_FCM(self, number_clusters, Epsilon, M, M_, rate, alpha, max_iter):
        """Implement sSMC_FCM"""
        self.V = init_C_sSMC(self.items, self.true_label, number_clusters)
        monitored_elements = self.init_monitored_elements(self.items, self.true_label, rate)
        # M1 = calc_M1(items, monitored_elements)
        m = self.init_fuzzification_coefficient(self.items, monitored_elements, M, M_)
        self.U = np.zeros((len(self.items), number_clusters))
        for k in range(max_iter):
            distance_matrix = calc_distance_item_to_cluster(self.items, self.V)
            self.U = self.update_U(distance_matrix, monitored_elements, M, M_, Epsilon)
            V_new = self.update_V(self.items, self.U, m)
            if end_condition(V_new, self.V, Epsilon):
                break
            self.V = np.copy(V_new)

    def update_U(self, distance_matrix, monitored_elements, M, M1, Epsilon):
        """Update membership value for each iteration"""
        U = np.zeros((len(distance_matrix), len(distance_matrix[0])))
        for i in range(len(U)):
            if i in monitored_elements:
                # Calculate U for monitored components
                dmin = np.min(distance_matrix[i])
                mu = distance_matrix[i] / dmin
                k = monitored_elements[i]
                a = 0
                for j in range(len(U[0])):
                    if j != k:
                        mu[j] = (M * mu[j] ** 2) ** (-1 / (M - 1))
                        a += mu[j]
                b = (M1 - M) / (M1 - 1)
                c = (M1 * mu[k] ** 2) ** (-1 / (M1 - 1))
                mu[k] = self.solution_of_equation(a, b, c, Epsilon)
                sumd = np.sum(mu)
                for j in range(len(U[0])):
                    U[i][j] = mu[j] / sumd
            else:
                # Calculate U for unsupervised components
                if (0 in distance_matrix[i]):
                    for k in range(len(U[0])):
                        if (distance_matrix[i][k] != 0):
                            U[i][k] = 0
                        else:
                            U[i][k] = 1
                    continue
                for k in range(len(U[0])):
                    dummy = 0
                    for j in range(len(U[0])):
                        dummy += (distance_matrix[i][k] / distance_matrix[i][j]) ** (2 / (M - 1))
                    else:
                        U[i][k] = 1 / dummy
        return U

    def printResult(self):
        label = assign_label(self.U)
        print("sSMC-FCM :")
        print("Rand Index Score: ", RI(self.true_label, label))
        print("DBI Score: ", DBI(self.items, label))
        print("PBM Score: ", PBM(self.items, label))
        print("ASWC Score: ", ASWC(self.items, label))
        print("MA Score: ", MA(self.true_label, label))

    def update_V(self, items, U, fuzzification_coefficient):
        """Update V after changing U"""

        V = np.zeros((len(U[0]), len(items[0])))

        for k in range(len(V)):
            dummy_array = np.zeros(V.shape[1])
            dummy = 0
            for i in range(len(items)):
                dummy_array += (U[i][k] ** fuzzification_coefficient[i][k]) * items[i]
                dummy += U[i][k] ** fuzzification_coefficient[i][k]
            V[k] = dummy_array / dummy
        return V

    def init_monitored_elements(self, items, true_label, rate):
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

    def g(self, x, alpha):
        return x * (alpha ** (x - 1))
    
    def f(self, x, a, b):
        """Calculate the left side of the equation"""
        return x / ((x + a) ** b)

    def calc_M1(self, items, alpha, monitored_elements):
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
            for j in range(len(distance_matrix[0])):
                for k in range(len(distance_matrix[0])):
                    if distance_matrix[i][k] == 0:
                        U = 1
                        break
                    U += (distance_matrix[i][j] / distance_matrix[i][k]) ** (2 / (M - 1))
                else:
                    U = 1 / U
            right_val = M * ((1 - alpha) / (1 / U - 1)) ** (M - 1)
            # M1_list.append(max_value(right_val))
            min_right_value = min(min_right_value, right_val)
        return self.max_value(min_right_value)


    def max_value(self, right_val):
        """Calculate the maximum value satisfying the inequality"""
        value = M
        while self.g(value) > right_val:
            value += 1
        return value

    def init_fuzzification_coefficient(self, distance_matrix, monitored_elements, M, M1):
        """Calculate matrix of fuzzification coefficient correspond with each element"""
        m = np.full((len(distance_matrix), len(distance_matrix[0])), M)

        for i in monitored_elements:
            m[i][monitored_elements[i]] = M1
        return m

    def solution_of_equation(self, a, b, c, Epsilon):
        """Calculate solution of Equation"""
        x = 0
        var_increase = 1

        while abs(self.f(x, a, b) - c) > Epsilon:
            if self.f(x + var_increase, a, b) <= c:
                x += var_increase
            else:
                var_increase /= 2
        return x