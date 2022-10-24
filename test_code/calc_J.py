def calculate(U,D,fuco):
    J = 0.0
    for k in range(len(D[0])):
        for i in range(len(D)):
           J += (U[i][k]**fuco[i])*D[i][k]

    return J