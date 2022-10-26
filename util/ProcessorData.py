import numpy as np


def ReadData(fileName):
    f = open(fileName, 'r')
    lines = f.read().splitlines()
    f.close()

    items = []
    for i in range(len(lines)):
        itemFeatures = list(map(float, lines[i].split(",")))
        items.append(itemFeatures)
    items = np.array(items)
    return items


def ReadLabel(fileName):
    f = open(fileName, 'r')
    true_label = np.array(f.read().splitlines())
    f.close()
    return true_label


def assign_label(U):
    label = []

    for i in range(len(U)):
        maximum = max(U[i])
        max_index = np.where(U[i] == maximum)[0][0]
        label.append(max_index)
    label = np.array(label)
    return label
