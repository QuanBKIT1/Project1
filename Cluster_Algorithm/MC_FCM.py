from util.Calculator import *
from util.ProcessorData import preprocessData, assign_label
from util.Evaluation import *
import numpy as np

class MC_FCM():
    def setFileData(self, fileData):
        self.fileData = fileData

    def processData(self, colLabel):
        self.items, self.true_label = preprocessData(self.fileData, colLabel)
    
    def MC_FCM(self, number_clusters, Epsilon, mL, mU, alpha, max_iter):
        """Implement MC_FCM"""
        self.V = init_C_KMeans(self.items, number_clusters)
        fuzzification_coefficient = self.init_fuzzification_coefficient(mL, mU, alpha, number_clusters)
        self.U = np.zeros((len(self.items), number_clusters))

        for k in range(max_iter):
            distance_matrix = calc_distance_item_to_cluster(self.items, self.V)
            self.U = self.update_U(distance_matrix, fuzzification_coefficient)
            V_new = self.update_V(self.items, self.U, fuzzification_coefficient)
            if end_condition(V_new, self.V, Epsilon):
                break
            self.V = np.copy(V_new)
        
    def printResult(self, numberCluster):
        label = assign_label(self.U)
        print("MC-FCM :")
        print("Rand Index Score: ", RI(self.true_label, label, numberCluster))
        print("DBI Score: ", DBI(self.items, label, numberCluster))
        print("PBM Score: ", PBM(self.items, label, numberCluster))
        print("ASWC Score: ", ASWC(self.items, label, numberCluster))
        print("MA Score: ", MA(self.true_label, label, numberCluster))

    def init_fuzzification_coefficient(self, mL, mU, alpha, number_clusters):
        """Calculate list of fuzzification coefficient correspond with each element"""
        delta = calc_matrix_distance(self.items)

        # Sort matrix distance by row
        delta = np.sort(delta)

        delta_star = np.zeros(len(delta))
        n = int(len(self.items) / number_clusters)
        # Calculate delta_star with formula
        for i in range(len(delta)):
            dummy = 0
            for j in range(n):
                dummy += delta[i][j]
            delta_star[i] = dummy

        # Find min max range of delta_star
        min_delta_star = min(delta_star)
        max_delta_star = max(delta_star)

        fuzzification_coefficient = np.zeros(len(self.items))
        # Calculate fuzzification coefficient
        for i in range(len(fuzzification_coefficient)):
            dummy = ((delta_star[i] - min_delta_star) / (max_delta_star - min_delta_star)) ** alpha
            mi = mL + (mU - mL) * dummy
            fuzzification_coefficient[i] = mi
        return fuzzification_coefficient


    def update_U(self, distance_matrix, fuzzification_coefficient):
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
                    dummy += (distance_matrix[i][k] / distance_matrix[i][j]) ** (2 / (fuzzification_coefficient[i] - 1))
                else:
                    U[i][k] = 1 / dummy
        return U


    def update_V(self, items, U, fuzzification_coefficient):
        """ Update V after changing U """

        V = np.zeros((len(U[0]),len(items[0])))

        for k in range(len(V)):
            dummy_array = np.zeros(V.shape[1])
            dummy = 0
            for i in range(len(items)):
                dummy_array += (U[i][k]**fuzzification_coefficient[i])*items[i]
                dummy += U[i][k]**fuzzification_coefficient[i]
            V[k] = dummy_array/dummy
        return V




