from ortools.sat.python import cp_model
import numpy as np
import pandas as pd
from operator import itemgetter


K=3
N=4
t= [[ 0, 72, 53, 65, 19],
    [72,  0, 78, 90, 96],
    [53, 78,  0, 71, 26],
    [65, 90, 71,  0, 11],
    [19, 96, 26, 11,  0]]
d=  [0 ,9 ,6 ,2 ,4]

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
# Constraints
# 1: Each vehicle must start from 0 and end at 0
for k in range(K):
  model.Add(sum(x[0,i,k] for i in range(N+1)) == 1)
for k in range(K):
  model.Add(sum(x[i,0,k] for i in range(N+1)) == 1)

# 2: If point i is served by vehicle k, we have the followings:
for i in range(1,N+1):
  for k in range(K):
    model.Add(sum(x[i,j,k] for j in range(N+1)) == y[i,k])
    model.Add(sum(x[j,i,k] for j in range(N+1)) == y[i,k])

# 3: Each point must be served by at least one vehicle
for i in range(1,N+1):
      model.Add( sum(y[i,k] for k in range(K))== 1 )

# 4: MLZ      
for i in range(1, N+1):
  for j in range(1, N+1):
    if j != i:
      for k in range(K):
        model.Add(u[i,k]-u[j,k]+N*x[i,j,k] <= N-1)

# 5: Ban loop
for i in range(N+1):
  for k in range(K):
    model.Add(x[i,i,k] == 0)

for k in range(K):
    model.Add(sum([(t[i][j]+d[j] )* x[i,j,k] for i in range(N+1) for j in range(N+1)]) <= maxT)
model.Minimize(maxT)

solver = cp_model.CpSolver()
printSolution(solver)
def printSolution(solver)
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