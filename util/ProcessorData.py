
def ReadData(fileName):
    f = open(fileName, 'r')
    lines = f.read().splitlines()
    f.close()

    items = []
    for i in range(len(lines)):
        line = lines[i].split(',')
        itemFeatures = []

        for j in range(len(line)):
            # Convert feature value to float
            v = float(line[j])
            # Add feature value to dict
            itemFeatures.append(v)

        items.append(itemFeatures)
    return items


def ReadLabel(fileName):
    f = open(fileName, 'r')
    lines = f.read().splitlines()
    f.close()

    true_label = []

    for i in range(len(lines)):
        true_label.append(lines[i])
    return true_label


def assign_label(U):
    label = []

    for i in range(len(U)):
        maximum = max(U[i])
        max_index = U[i].index(maximum)
        label.append(max_index)

    return label
