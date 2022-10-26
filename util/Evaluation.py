from sklearn import metrics
import numpy as np

import config
from util.Calculator import d
number_clusters = config.number_clusters
def RI(labels_true, labels_pred):
    return metrics.rand_score(labels_true, labels_pred)


def DBI(X, labels):
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
    Dc = max([d(Xtb[j],Xtb[k]) for j in range(number_clusters) for k in range(number_clusters)])
    print(X_, El, Ec, Xtb, Dc, sep="\n")
    return ((Dc * El)/(Ec*number_clusters))**2