from data import read_dataset
import math 
import numpy as np
from ortools.sat.python import cp_model
import pandas as pd
from operator import itemgetter
dataSet = read_dataset('A/A-n32-k5.vrp')
K = 3
N = 20
pointList = [[0,0]]
for i in range(N):
    temp = [0,0]
    temp[0] = dataSet[i+1]["x"]
    temp[1] = dataSet[i+1]["y"]
    pointList.append(temp)

def d(i,j):
    return math.sqrt(( pointList[i][0]-pointList[j][0] )**2 + ( pointList[i][1]-pointList[j][1] )**2)
t = [[int(d(i,j)) for i in range(N+1)] for j in range(N+1)]
# for i in range(10):
#     print(t[i])
d = [0]+[np.random.randint(100) for i in range(N)]

def CP():
    model = cp_model.CpModel()
    x = {}
    for i in range(N+1):
        for j in range(N+1):
            for k in range(K):
               x[i,j,k] = model.NewIntVar(0, 1, 'x[{}][{}][{}]'.format(i, j, k))

    y = {}
    for i in range(1,N+1):
        for k in range(K):
            y[i,k] = model.NewIntVar(0, 1, 'y[{}][{}]'.format(i, k))

    u = {}
    for i in range(N+1):
        for k in range(K):
            u[i,k] =model.NewIntVar(1, N, 'u[{}][{}]'.format(i, k))
    maxT = model.NewIntVar(0, 100000000, 'maxTime')
    for k in range(K):
        model.Add(sum(x[0,i,k] for i in range(N+1)) == 1)
    for k in range(K):
        model.Add(sum(x[i,0,k] for i in range(N+1)) == 1)
    for i in range(1,N+1):
        for k in range(K):
            model.Add(sum(x[i,j,k] for j in range(N+1)) == y[i,k])
            model.Add(sum(x[j,i,k] for j in range(N+1)) == y[i,k])
    for i in range(1,N+1):
        model.Add( sum(y[i,k] for k in range(K))== 1 )
    for i in range(1, N+1):
        for j in range(1, N+1):
            if j != i:
                for k in range(K):
                    model.Add(u[i,k]-u[j,k]+N*x[i,j,k] <= N-1)
    for i in range(N+1):
        for k in range(K):
            model.Add(x[i,i,k] == 0)
    for k in range(K):
        model.Add(sum([(t[i][j]+d[j] )* x[i,j,k] for i in range(N+1) for j in range(N+1)]) <= maxT)
    model.Minimize(maxT)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        print('Solution:')
        print('Objective value =', solver.Value(maxT))
        for k in range(K):
            l = [0]
            start = 0
            workT = 0
            while True:
                for i in range(N+1):
                    if solver.Value(x[start,i,k])==1:
                        workT += t[start][i] + d[i]
                        l.append(i)
                        start = i
                        break
                if start == 0:
                    break    
            print("-- Staff {} : {} with work in {} min--".format(k,l,workT))
CP()