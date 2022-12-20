import copy
from util import Evaluation, ProcessorData
from util.Calculator import *


class FCM:
    def __init__(self, items, true_label, number_clusters, m, Epsilon, max_iter):
        self.items = items
        self.true_label = true_label
        self.number_clusters = number_clusters
        self.Epsilon = Epsilon
        self.m = m
        self.max_iter = max_iter
        self.U = []
        self.V = init_C_KMeans(self.items, self.number_clusters)

    def run(self):
        """
        Implement FCM
        """
        for k in range(self.max_iter):
            distance_matrix = calc_distance_item_to_cluster(self.items, self.V)
            self.U = self.update_U(distance_matrix)
            V_new = self.update_V(self.items, self.U, self.m)
            if end_condition(V_new, self.V, self.Epsilon):
                break
            self.V = copy.deepcopy(V_new)

        self.eval()

    def eval(self):

        label = ProcessorData.assign_label(self.U)
        self.evalList = [Evaluation.RI(self.true_label, label), Evaluation.DBI(self.items, label, self.number_clusters),
                    Evaluation.PBM(self.items, label, self.number_clusters),
                    Evaluation.ASWC(self.items, label, self.number_clusters),
                    Evaluation.MA(self.true_label, label, self.number_clusters)]
        self.evalList = np.array(self.evalList)
        self.evalList = self.evalList.reshape(len(self.evalList),1)

    def update_U(self, distance_matrix):
        """Update membership value for each iteration"""
        U = np.zeros((len(distance_matrix), len(distance_matrix[0])))
        for i in range(len(U)):
            if 0 in distance_matrix[i]:
                for k in range(len(U[0])):
                    if distance_matrix[i][k] != 0:
                        U[i][k] = 0
                    else:
                        U[i][k] = 1
                continue
            for k in range(len(U[0])):
                dummy = 0
                for j in range(len(U[0])):
                    dummy += (distance_matrix[i][k] / distance_matrix[i][j]) ** (2 / (self.m - 1))
                else:
                    U[i][k] = 1 / dummy
        return U

    def update_V(self, items, U, m):
        """ Update V after changing U """
        V = np.zeros((len(U[0]), len(items[0])))

        for k in range(len(V)):
            dummy_array = np.zeros(V.shape[1])
            dummy = 0
            for i in range(len(items)):
                dummy_array += (U[i][k] ** m) * items[i]
                dummy += U[i][k] ** m
            V[k] = dummy_array / dummy
        return V

# data_table = readData("../dataset/wdbc.data")
# i1, i2 = preprocessData(data_table, 1, [0])
# fcm = FCM(i1, i2, 2, 2, 0.000001, 300)
# fcm.run()
# print(fcm.U)