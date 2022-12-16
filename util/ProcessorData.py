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
