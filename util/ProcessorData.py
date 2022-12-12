import numpy as np

def ReadData(fileName, colLabel):
    f = open(fileName, 'r')
    lines = f.read().splitlines()
    f.close()

    items = []
    trueLabel = []
    for i in range(len(lines)):
        itemFeatures = lines[i].split(",")
        trueLabel.append(itemFeatures.pop(colLabel))
        itemFeatures = list(map(float, itemFeatures))
        items.append(itemFeatures)
    items = np.array(items)
    trueLabel = np.array(trueLabel)
    return items, trueLabel


def assign_label(U):
    label = []

    for i in range(len(U)):
        maximum = max(U[i])
        max_index = np.where(U[i] == maximum)[0][0]
        label.append(max_index)
    label = np.array(label)
    return label
