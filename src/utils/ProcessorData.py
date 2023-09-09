import numpy as np
import pandas as pd


def readData(fileName):
    """
    Read a file and return data
    :param fileName: Path to file
    :return: array of data
    """
    data = pd.read_csv(fileName, header=None, sep="\s+|,", engine='python')
    data_table = np.array(data)
    return data_table


def preprocessData(data_table, colLabel, colRedundant):
    """
    :param data_table: location of dataset in computer (.data, .csv, ...)
    :param colLabel: column containing label of dataset
    :param colRedundant: column containing redundant data
    :return: 2 numpy array: standard data and true label
    """

    items = []
    trueLabel = []

    # Read column label
    for i in range(len(data_table)):
        trueLabel.append(data_table[i][colLabel])

    # Read column data
    colData = [i for i in range(len(data_table[0]))]
    colData.remove(colLabel)
    if colRedundant is not None:
        for i in colRedundant:
            colData.remove(i)

    for i in range(len(data_table)):
        item = []
        for j in colData:
            item.append(data_table[i][j])
        items.append(item)

    items = np.array(items)
    trueLabel = np.array(trueLabel)

    # Minimax Scaler
    # scaler = MinMaxScaler()
    # scaler.fit(items)
    # items = scaler.transform(items)

    return items, trueLabel


def readColumn(data_table, col):
    return [data_table[i][col] for i in range(len(data_table))]


def assign_label(U):
    label = []

    for i in range(len(U)):
        maximum = max(U[i])
        max_index = np.where(U[i] == maximum)[0][0]
        label.append(max_index)
    label = np.array(label)
    return label


def label_mapping(true_label, label, number_clusters):
    trueL = list(set(true_label))
    indexL = [i for i in range(number_clusters)]
    dict0 = {}

    for i in trueL:
        dummy = 0
        for j in range(len(true_label)):
            if true_label[j] == i:
                dummy = dummy + 1
        dict0[i] = dummy

    # print(dict0)
    dict1 = {}
    while indexL:
        i = indexL.pop()
        l = [0, 0, 0]
        for j in trueL:
            dummy = 0
            for k in range(len(label)):
                if label[k] == i and true_label[k] == j:
                    dummy = dummy + 1
            if dummy >= l[2]:
                l = [i, j, dummy]
        # print(l)
        dict1[l[0]] = [l[1], l[2], dict0[l[1]]]

        trueL.remove(l[1])
    return dict1


def convert_to_table_map(dict1, label):
    table_map = []
    for i in label:
        table_map.append([i, dict1[i][0]])
    return table_map
