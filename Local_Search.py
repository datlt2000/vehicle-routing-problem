from data import read_dataset
import math
import numpy as np
import time
dataSet = read_dataset('custom/c.vrp')
# for key in dataSet.keys():
#     print("{}: {}".format(key,dataSet[key]))
K = 4
N = len(dataSet.keys())-1
pointList = []

for i in range(N+1):
    temp = [0,0]
    temp[0] = dataSet[i+1]["x"]
    temp[1] = dataSet[i+1]["y"]
    pointList.append(temp)
# pointList[0][0] =int( sum([pointList[i][0] for i in range(1,N+1)])/N )
# pointList[0][1] =int( sum([pointList[i][1] for i in range(1,N+1)])/N )
def d(i,j):
    return math.sqrt(( pointList[i][0]-pointList[j][0] )**2 + ( pointList[i][1]-pointList[j][1] )**2)
t = [[int(d(i,j)) for i in range(N+1)] for j in range(N+1)]
d=[]
for i in range(N+1):
    d.append(dataSet[i+1]["d"])
import time
def genRandomState():
    R=[]
    y = [ np.random.randint(K) for i in range(N) ]
    for i in range(K):
        temp=[0]
        for j in range(N):
            if y[j]==i:
                temp.append(j+1)
        if len(temp) != 1:
                temp.append(0)
        R.append(temp)
    return R

def timework(route):
    if len(route)==1:
        return 0
    result = 0
    for j in range(1,len(route)):
        result += t[route[j-1]][route[j]]+d[route[j]]
    return result

def removeElement(route,ele_id):
    temp = route
    temp.remove(ele_id)
    if len(temp)==2:
        temp=[0]
    return temp
def addElement(route,ele_id):
    if len(route)==1:
        temp = route
        temp.append(ele_id)
        temp.append(0)
        return temp
    best = 100000
    miss = 0
    for i in range(1,len(route)-1):
        cur = t[route[i-1]][ele_id]+t[ele_id][route[i]]-t[route[i-1]][route[i]]
        if cur < best:
            best = cur
            miss = i
    if miss!=0:
        temp = route[0:miss]
        temp.append(ele_id)
        temp.extend(route[miss:-1])
        temp.append(0)
    return temp
def changeRoute(route,ele_id):
    temp = route
    if len(route)!=3:
        cur_index = temp.index(ele_id)
        best = 0
        miss = 0
        for i in range(1,len(route)-1):
            if i!=cur_index:
                cur = t[route[cur_index-1]][route[cur_index+1]] + t[route[i-1]][ele_id]+t[ele_id][route[i]] - t[route[i-1]][route[i]]-t[route[cur_index-1]][ele_id]-t[ele_id][route[cur_index]]
                if cur<best:
                    miss = i
                    best = cur
        if miss!=0:
            # print("change element {} from {} to {} with {}".format(ele_id,cur_index,miss,best))
            temp =[]
            for i in range(len(route)):
                if i==miss:
                    temp.append(ele_id)
                if i==cur_index:
                    continue
                temp.append(route[i])
    return temp
def findMax(R):
    max_index = 0
    max = timework(R[0])
    for i in range(1,K):
        cur = timework(R[i])
        if cur > max:
            max = cur
            max_index = i
    return max_index
def findMin(R):
    min_index = 0
    min = timework(R[0])
    for i in range(1,K):
        cur = timework(R[i])
        if cur < min:
            min = cur
            min_index = i
    return min_index
def findMaxEle(route):
    max = 0
    max_index=0
    for i in range(1,len(route)-1):
        cur = d[route[i]]+t[route[i-1]][route[i]]+t[route[i]][route[i+1]] - t[route[i-1]][route[i+1]]
        if cur > max:
            max = cur
            max_index = i
    return route[i]
def fitness(R):
    return max([timework(R[k]) for k in range(K)])
                
def moveElementBetween2Staff(R):
    result = R
    max_route = findMax(result)
    min_route = findMin(result)
    ele_id = findMaxEle(result[max_route])
    result[max_route] = removeElement(result[max_route], ele_id)
    result[min_route] = addElement(result[min_route], ele_id)
    return result
def moveElementInStaff(R):
    result = R
    max_route = findMax(result)
    ele_id = R[max_route][np.random.randint(1,len(result[max_route]))]
    result[max_route] = changeRoute(R[max_route],ele_id)
    return result
def swapElementBetween2Staff(R):
    result = R
    max_route = findMax(result)
    min_route = findMin(result)

    ele_id1 = findMaxEle(result[max_route])
    ele_id2 = findMaxEle(result[min_route])

    result[max_route] = removeElement(result[max_route], ele_id1)
    result[min_route] = removeElement(result[min_route], ele_id2)

    result[min_route] = addElement(result[min_route], ele_id1)
    result[max_route] = addElement(result[max_route], ele_id2)
    return result

def getNeighborhood(R):
    result = []
    result.append(moveElementBetween2Staff(R))
    result.append(moveElementInStaff(R))
    result.append(swapElementBetween2Staff(R))
    return result
def printAllRouter(R):
    for k in range(K):
        print("-- Staff {} : {} and work in {} min--".format(k,R[k],timework(R[k])))    
def copyRouter(R):
    result = R[:]
    return result

best_Routes = genRandomState()
best_fitness = fitness(best_Routes)

print(best_fitness)
printAllRouter(best_Routes)
loop_num = 1000
loop = 0
# startTime = time.time()
# while time.time() - startTime < 60:
while loop < loop_num:
    Neighborhoods = getNeighborhood(best_Routes)
    for Neighborhood in Neighborhoods:
        cur_fitness = fitness(Neighborhood)
        if cur_fitness < best_fitness:
            print("-------------------------------------------------------")
            # print("[True]")
            best_fitness = cur_fitness
            best_Routes = Neighborhood[:]
            printAllRouter(best_Routes)
        # print("-------------------------------------------------------")
        # printAllRouter(best_Routes)
        # print("\n")
        # printAllRouter(Neighborhood)
    loop+=1
print("-------------------------------------------------------")
print(best_fitness)
print("Solution")
printAllRouter(best_Routes)