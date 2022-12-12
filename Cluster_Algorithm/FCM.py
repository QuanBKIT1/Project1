import copy
import util
from util.Calculator import *

class FCM():
    def setFileData(self, fileData):
        self.fileData = fileData
        
    def setColLabel(self, colLabel):
        self.colLabel = colLabel

    def processData(self, colLabel):
        self.items, self.true_label = ReadData(self.fileData, colLabel)
        
    def FCM(self, number_clusters, Epsilon, m, max_iter):
        """Implement FCM"""
        self.V = init_C_KMeans(self.items, number_clusters)
        self.U = []

        for k in range(max_iter):
            distance_matrix = calc_distance_item_to_cluster(self.items, self.V)
            self.U = self.update_U(distance_matrix, m)
            V_new = self.update_V(self.items, self.U, m)
            if end_condition(V_new, self.V, Epsilon):
                break
            self.V = copy.deepcopy(V_new)
            
    def printResult(self):
        label = util.ProcessorData.assign_label(self.U)
        print("FCM :")
        print("Rand Index Score: ", util.Evaluation.RI(self.true_label, label))
        print("DBI Score: ", util.Evaluation.DBI(self.items, label))
        print("PBM Score: ", util.Evaluation.PBM(self.items, label))
        print("ASWC Score: ", util.Evaluation.ASWC(self.items, label))
        print("MA Score: ", util.Evaluation.MA(self.true_label, label))
        
    def update_U(self, distance_matrix, m):
        """Update membership value for each iteration"""
        U = np.zeros((len(distance_matrix), len(distance_matrix[0])))
        for i in range(len(U)):
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
                    dummy += (distance_matrix[i][k] / distance_matrix[i][j]) ** (2 / (m - 1))
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