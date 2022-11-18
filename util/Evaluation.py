from sklearn import metrics
import numpy as np
import util
import config
from util.Calculator import d


number_clusters = config.number_clusters


def RI(labels_true, labels_pred):
    return metrics.rand_score(labels_true, labels_pred)


def DBI(X, labels):
    global number_clusters

    index_cluster = [[] for i in range(number_clusters)]
    for i in range(len(labels)):
        index_cluster[labels[i]].append(i)

    # Calculate X_
    X_ = np.zeros((number_clusters,len(X[0])))
    for i in range(len(X_)):
        for j in range(len(X_[0])):
            dummy = 0
            for k in range(len(index_cluster[i])):
                dummy += X[index_cluster[i][k]][j]
            X_[i][j] = dummy/len(index_cluster[i])
    # Calculate di
    intra_dispersion = np.zeros(number_clusters)

    for i in range(number_clusters):
        dummy = 0
        for j in range(len(index_cluster[i])):
            dummy += util.Calculator.d(X[index_cluster[i][j]], X_[i])
        intra_dispersion[i] = 1 / len(index_cluster[i]) * dummy

    # Calculate dij
    separation_measure = util.Calculator.calc_matrix_distance(X_)

    # Calculate Dij
    similarity = np.zeros((number_clusters, number_clusters))
    for i in range(number_clusters):
        for j in range(number_clusters):
            if i != j:
                similarity[i][j] = (intra_dispersion[i] + intra_dispersion[j]) / separation_measure[i][j]
            else:
                similarity[i][j] = 0

    # Calculate Di
    D = np.max(similarity, axis=0)
    # Calculate dbi
    score = np.mean(D)
    return score


def PBM(X, labels):
    # Calculate X_
# Ngoc Huy begin:
    X_ = np.mean(X, axis=0)

    # Calculate El
    El = sum([d(X[i], X_) for i in range(len(X))])

    # Calculate list X_
    Xtb = []
    for k in range(number_clusters):
        item = []
        for i in range(len(X)):
            if labels[i] == k:
                item.append(X[i])
        Xtb.append(np.mean(item, axis=0))
    Xtb = np.array(Xtb)

    # Calculate Ec
    Ec = sum([d(X[i], Xtb[labels[i]]) for i in range(len(X))])

    # Calculate Dc
    Dc = max([d(Xtb[j], Xtb[k]) for j in range(number_clusters) for k in range(number_clusters)])
    return (1/number_clusters * El/Ec * Dc)**2

# Ngoc Huy End:

# khanh begin:
def ASWC(items,label):
    cum = []
    for j in range(number_clusters):
        clus = []
        for i in range(len(label)):
            if label[i] == j:
                clus.append(items[i])
        cum.append(clus)
    sum1 = 0
    sum2 = 0
    dem1 = 0
    dem2 = 0
    apj = []
    # dqj=[]
    bpj = []
    sxj = []
    ee = 0.00001
    tong = 0
    for j in range(len(label)):
        dqj = []
        for i in range(number_clusters):
            if i != label[j]:  # nếu khác cụm
                for ob in cum[i]:
                    sum2 = sum2 + d(ob, items[j])
                    dem2 = dem2 + 1
                dqj.append(sum2 / dem2)  # dqi = trung bình khoảng cách từ item[j] đến cụm q !=
            if i == label[j]:  # nếu cùng cụm
                for ob in cum[i]:
                    sum1 = sum1 + d(ob, items[j])
                    dem1 = dem1 + 1
        bpj.append(min(dqj))
        apj.append(sum1 / (dem1 - 1))  # khoảng cách tb từ item[j] đến đối tượng cùng cụm
        sxj.append(bpj[j] / (apj[j] + ee))
        # sxj.append((-apj[j]+bpj[j])/max(bpj[j],apj[j]))           # đây là SWC
        dem1 = 0
        dem2 = 0
        sum1 = 0
        sum2 = 0

    for i in sxj:
        tong += i
    return tong / len(sxj)
#khanh end

#the huy begin

def MA(true_label, label):

    trueL = set(true_label)

    list_trueL = [[la,0] for la in trueL]

    ''' count the number of each label in true_label'''

    for i in true_label:
        for j in list_trueL:
            if i == j[0]:
                j[1]+=1

    list_trueL.sort(key = lambda ns:ns[1])

    '''count the number of Xi in cluster after clustering'''

    list_L = [[i,0] for i in range(len(trueL))]

    for i in label:
        for j in list_L:
            if i == j[0]:
                j[1] +=1

    list_L.sort(key = lambda ns:ns[1])
    
    return min([list_L[i][1]/list_trueL[i][1] for i in range(len(trueL))])

# the huy end
