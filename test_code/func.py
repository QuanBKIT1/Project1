import config
import util.ProcessorData
from Cluster_Algorithm import MC_FCM, FCM
import calc_J
from sklearn import metrics
from util.ProcessorData import ReadData, ReadLabel

fileData = config.fileData
fileLabel = config.fileLabel

items = ReadData(fileData)
true_label = ReadLabel(fileLabel)


def calcJ():
    fu_co = MC_FCM.init_fuzzification_coefficient(items)
    U, V = MC_FCM.MC_FCM(items)
    D = MC_FCM.calc_distance_item_to_cluster(items, V)
    label = util.ProcessorData.assign_label(U)
    J = calc_J.calculate(U, D, fu_co)
    print(metrics.rand_score(true_label, label))
    print(J)
    return J


def run_FCM():
    U, V = FCM.FCM(items)
    label = util.ProcessorData.assign_label(U)
    print(U, V, true_label, label, sep='\n')
    print(metrics.rand_score(true_label, label))


def run_MC_FCM():
    U, V = MC_FCM.MC_FCM(items)
    label = util.ProcessorData.assign_label(U)
    print(U, V, true_label, label, sep='\n')
    print(metrics.rand_score(true_label, label))


def write_Result():
    pass
# f = open('FCM_iris_test.txt', 'a')
# for i in V:
#     print(i,sep=', ',file=f)
#
# print(metrics.rand_score(true_label,label),file=f)
# print('\n',file=f)
