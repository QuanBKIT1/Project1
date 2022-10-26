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


def sklearn_dbi(X, labels):
    return metrics.davies_bouldin_score(X, labels)


def PBM(X, V, labels):
    X_ = [np.average([X[i][j] for i in range(len(X))]) for j in range(len(X[0]))]
    El = sum([d(X[i], X_) for i in range(len(X))])
    Ec = 0
    Xtb = []
    for k in range(number_clusters):
        item = []
        for i in range(len(X)):
            if labels[i] == k:
                item.append(X[i])
        Xtb.append([np.average([item[i][j] for i in range(len(item))]) for j in range(len(X[0]))])
    Xtb = np.array(Xtb)

    for k in range(number_clusters):
        for i in range(len(X)):
            if labels[i] == k:
                Ec += d(X[i], Xtb[k])
    Dc = max([d(Xtb[j], Xtb[k]) for j in range(number_clusters) for k in range(number_clusters)])
    # print(X_, El, Ec, Xtb, Dc, sep="\n")
    return ((Dc * El) / (Ec * number_clusters)) ** 2
