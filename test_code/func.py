import config
import util.ProcessorData
from Cluster_Algorithm import MC_FCM, FCM
from util.ProcessorData import ReadData, ReadLabel
import util.Evaluation

fileData = config.fileData
fileLabel = config.fileLabel

items = ReadData(fileData)
true_label = ReadLabel(fileLabel)


def run_FCM():
    U, V = FCM.FCM(items)
    label = util.ProcessorData.assign_label(U)
    print("FCM :")
    # print(U, V, true_label, label, sep='\n')
    print("Rand Index Score: ", util.Evaluation.RI(true_label, label))
    print("DBI Score: ", util.Evaluation.DBI(items, V, label))
    print("PBM Score: ", util.Evaluation.PBM(items, V, label))


def run_MC_FCM():
    U, V = MC_FCM.MC_FCM(items)
    label = util.ProcessorData.assign_label(U)
    print("MC_FCM:")
    # print(U, V, true_label, label, sep='\n')
    print("Rand Index Score: ", util.Evaluation.RI(true_label, label))
    print("DBI Score: ", util.Evaluation.DBI(items, V, label))
    print("PBM Score: ", util.Evaluation.PBM(items, V, label))


def write_Result():
    pass
# f = open('FCM_iris_test.txt', 'a')
# for i in V:
#     print(i,sep=', ',file=f)
#
# print(metrics.rand_score(true_label,label),file=f)
# print('\n',file=f)
