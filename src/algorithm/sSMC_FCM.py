from src.utils import ProcessorData, Evaluation
from src.utils.Calculator import *


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
        self.iterator = 0

    def run(self):
        """Implement sSMC_FCM"""
        self.fuzzification_coefficient = self.init_fuzzification_coefficient()
        for k in range(self.max_iter):
            item_to_cluster = calc_distance_item_to_cluster(self.items, self.V)
            self.update_U(item_to_cluster)
            V_new = self.update_V()
            self.iterator += 1
            if end_condition(V_new, self.V, self.Epsilon):
                break
            self.V = np.copy(V_new)

        self.label = ProcessorData.assign_label(self.U)
        self.label_map = ProcessorData.label_mapping(self.true_label, self.label, self.number_clusters)
        self.table_map = src.utils.ProcessorData.convert_to_table_map(self.label_map, self.label)
        self.eval()

    def eval(self):
        self.label = ProcessorData.assign_label(self.U)
        self.evalList = [Evaluation.RI(self.true_label, self.label),
                         Evaluation.DBI(self.items, self.label, self.number_clusters),
                         Evaluation.PBM(self.items, self.label, self.number_clusters),
                         Evaluation.ASWC(self.items, self.label, self.number_clusters),
                         Evaluation.MA(self.true_label, self.label, self.number_clusters)]
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
        item_to_cluster = calc_distance_item_to_cluster(self.items, self.V)
        # Do vế trái là 1 hàm nghịch biến nên ta cần tìm giá trị nhỏ nhất
        # của vế phải ứng với U'(ik). Vì nếu M' thỏa mãn với giá trị nhỏ
        # nhất đó thì nó cũng thỏa mãn với các trường hợp khác

        right_val_list = []
        U = 0
        for i in range(len(self.U)):
            if i in self.monitored_elements:
                # Calculate U for unsupervised components
                k = self.monitored_elements[i]
                if (item_to_cluster[i][k] != 0):
                    dummy = 0
                    for j in range(self.number_clusters):
                        dummy += (item_to_cluster[i][k] / item_to_cluster[i][j]) ** (2 / (self.M - 1))
                    else:
                        U = 1 / dummy
                        right_val = self.M * ((1 - self.alpha) / (1 / U - 1)) ** (self.M - 1)
                        right_val_list.append(right_val)
        min_right_value = min(right_val_list)
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
                if (0 in item_to_cluster[i]):
                    for k in range(self.number_clusters):
                        if (item_to_cluster[i][k] != 0):
                            self.U[i][k] = 0
                        else:
                            self.U[i][k] = 1
                    continue
                for k in range(self.number_clusters):
                    dummy = 0
                    for j in range(self.number_clusters):
                        dummy += (item_to_cluster[i][k] / item_to_cluster[i][j]) ** (2 / (self.M - 1))
                    else:
                        self.U[i][k] = 1 / dummy

    def update_V(self):
        """Update V after changing U"""
        V_new = np.zeros((self.number_clusters, len(self.items[0])))

        for k in range(len(V_new)):
            dummy_array = np.zeros(V_new.shape[1])
            dummy = 0
            for i in range(len(self.items)):
                tmp = self.U[i][k] ** self.fuzzification_coefficient[i][k]
                dummy_array += tmp * self.items[i]
                dummy += tmp
            V_new[k] = dummy_array / dummy
        return V_new

    def init_fuzzification_coefficient(self):
        """Calculate matrix of fuzzification coefficient correspond with each element"""
        m = np.full((len(self.items), self.number_clusters), self.M)

        for i in self.monitored_elements:
            m[i][self.monitored_elements[i]] = self.M1
        return m
