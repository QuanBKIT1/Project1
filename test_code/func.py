import config
import util.ProcessorData
from Cluster_Algorithm import sSMC_FCM, MC_FCM, FCM
from util.ProcessorData import ReadData, ReadLabel
import util.Evaluation

fileData = config.fileData

items, true_label = ReadData(fileData)


def run_FCM():
    U, V = FCM.FCM(items)
    label = util.ProcessorData.assign_label(U)
    print("FCM :")
    # print(U, V, true_label, label, sep='\n')
    print("Rand Index Score: ", util.Evaluation.RI(true_label, label))
    print("DBI Score: ", util.Evaluation.DBI(items, label))
    print("PBM Score: ", util.Evaluation.PBM(items, label))
    print("ASWC Score: ", util.Evaluation.ASWC(items, label))  # khanh them
    # print("MA Score: ", util.Evaluation.MA(true_label, label))


def run_MC_FCM():
    U, V = MC_FCM.MC_FCM(items)
    label = util.ProcessorData.assign_label(U)
    print("MC_FCM:")
    # print(U, V, true_label, label, sep='\n')
    print("Rand Index Score: ", util.Evaluation.RI(true_label, label))
    print("DBI Score: ", util.Evaluation.DBI(items, label))
    print("PBM Score: ", util.Evaluation.PBM(items, label))
    print("ASWC Score: ", util.Evaluation.ASWC(items, label))  # khanh them
    # print("MA Score: ", util.Evaluation.MA(true_label, label))


def run_sSMC_FCM():
    U, V = sSMC_FCM.sSMC_FCM(items)
    label = util.ProcessorData.assign_label(U)
    print("sSMC_FCM:")
    # print(U, V, true_label, label, sep='\n')
    print("Rand Index Score: ", util.Evaluation.RI(true_label, label))
    print("DBI Score: ", util.Evaluation.DBI(items, label))
    print("PBM Score: ", util.Evaluation.PBM(items, label))
    print("ASWC Score: ", util.Evaluation.ASWC(items, label))  # khanh them
    # print("MA Score: ", util.Evaluation.MA(true_label, label))


def write_Result():
    pass
# f = open('FCM_iris_test.txt', 'a')
# for i in V:
#     print(i,sep=', ',file=f)
#
# print(metrics.rand_score(true_label,label),file=f)
# print('\n',file=f)
