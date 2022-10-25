from sklearn import metrics


def RI(labels_true, labels_pred):
    return metrics.rand_score(labels_true, labels_pred)


def DBI(X, labels):
    return metrics.davies_bouldin_score(X, labels)

