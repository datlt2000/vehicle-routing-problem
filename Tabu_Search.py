# coding=<encoding name>
# This Python file uses the following encoding: utf-8
import time
import copy
import math
import sys
import copy
import matplotlib.pyplot as plt


class CVRP(object):
    def __init__(self, problem, graph, attempts=1000):
        self.problem = problem
        self.tabu_list = []
        self.tabu_list_size = 1000
        self.number_attempts = attempts  # stop search if cannot improve solution after number_of_attempts times
        self.graph = graph
        self.problem_solver()
        #self.data = []
    

    def problem_solver(self):  # state 1 trạng thái
        current_state, current_fitness = self.problem.initial_state() # khởi tạo ra currentstate= 0 0 .. 0 123.., currentfitness được khởi tjao ra từ currentstate
        best_state, best_fitness = current_state, current_fitness
        attempts = 0
        self.tabu_list.append(current_state)
        while attempts < self.number_attempts:

            attempts += 1
            neighbors = self.problem.find_neighbors(current_state) # tập hàng xóm đuọc tạo
            next_state, next_fitness = self.chose_neighbor(neighbors, current_state, current_fitness)
            if next_state is None:
                break
            if best_fitness > next_fitness:  #nếu gtri tốt nhất lớn hơn giá trị tiếp theo 
                best_state = next_state   #trạng thái tốt nhất là trạng thái tiếp theo
                best_fitness = next_fitness # gtrị tốt nhất là giá trị tiếp theo
            current_state = next_state
            current_fitness = next_fitness
        print("Last state: " + str(best_state))
        print("Best fitness: " + str(best_fitness))
        
        data= []
        count = 0
        for i in range(len(best_state)):
            if(best_state[i] == 0):
                data.append([0] + best_state[count:i] + [0])
                count = i + 1
            elif i == (len(best_state)-1):
                data.append([0] + best_state[count:(i+1)] + [0])
        print(len(best_state))    
        print(data)
        visualize(data, self.graph)

        
    
    # chọn hàng xóm
    def chose_neighbor(self, neighbors, current_state, current_fitness):
        if len(neighbors) == 0:
            return None, None
        chosen_neighbor = None
        chosen_fitness = sys.maxsize
        for neighbor in neighbors:  # duyệt trong tập neighbors
            if neighbor not in self.tabu_list and self.problem.fitness(neighbor) < chosen_fitness:
                chosen_neighbor = neighbor
                chosen_fitness = self.problem.fitness(neighbor)
        if len(self.tabu_list) > self.tabu_list_size:
            self.tabu_list.pop(0)
        self.tabu_list.append(chosen_neighbor)
        return chosen_neighbor, chosen_fitness

def visualize(data, distances): 
        for i in data:
            x = []
            y = []
            for j in i:
                x.append(distances[j + 1]['x'])
                y.append(distances[j + 1]['y'])
            plt.plot(x, y)
        plt.show()

def distince(f, t):
    return math.sqrt(math.pow(f['x'] - t['x'], 2) + math.pow(f['y'] - t['y'], 2))  # tính khoảng cách 2 đeimer


class Problem(object):
    def __init__(self, graph, number_of_truck):  # truyền vào graph = data, number_of_truck = 4
        self.graph = graph
        self.number_of_truck = number_of_truck  # 0 .. 0 1 2 3.. n-1
        self.node_set = [0] * (number_of_truck - 2) + [i for i in range(len(graph))] # n khách + k-1 nhân viên, nối thành 1 mảng
      
    def initial_state(self): # khởi tạo state và fitness ban đầu
        state = copy.deepcopy(self.node_set)
      
        return state, self.fitness(state)

    def fitness(self, state):
        def distance_trip(fr, to):
            w = self.graph[fr + 1]
            q = self.graph[to + 1]
            #return math.sqrt(math.pow((w['x'] - q['x']), 2) + math.pow((w['y'] - q['y']), 2))
            return distince(w,q)
        # penalty_cap = penalty_capacity(chromosome)
    
        actual_chromosome = [0] + state + [0]
        fitness_value = []
        for i in range(0, num_truck + 1):
            init = 0
            fitness_value.append(init)
            count = 0
        for i in range(len(actual_chromosome) - 1):
            if actual_chromosome[i] == 0 and i != 0:
                count += 1
            fitness_value[int(count)] += distance_trip(actual_chromosome[i], actual_chromosome[i + 1]) \
                                     + self.graph[actual_chromosome[i] + 1]['w']
        max_value = 0
        for value in fitness_value:
            if value > max_value:
                max_value = value
        return max_value

    def find_neighbors(self, current_state): # tjao ra tập neighbors
        neighbors = []  # tập hàng xóm
        num_node = len(current_state)  # 
        for i in range(num_node):
            for j in range(num_node - 1):
                if i != j:
                    temp = current_state[:i] + current_state[i + 1:]
                    neighbor = temp[:j] + [current_state[i]] + temp[j:]
                   
                    neighbors.append(neighbor) #thêm vào tập neighbors các trường hợp
  
        return neighbors


def trim(s):
    # replace multi space, tab and new line by space
    # return string
    new_str = s.replace("\n", " ").replace("\r\n", " ")#thay ki tu xuong dong bang dau cach
    new_str = ' '.join(new_str.split()) 
    new_str = new_str.strip()#xoa cac ptu space dau va cuoi
    return new_str


def convert_data(raw_data):
    # convert list data string to dict of int
    # return dict
    dataset = dict()
    for d in raw_data:
        ds = d.split()
        if len(ds) == 3:
            if ds[0].isnumeric() and ds[1].isnumeric() and ds[2].isnumeric():
                a = dict()
                a['x'] = int(ds[1])
                a['y'] = int(ds[2])
                dataset[int(ds[0])] = a
        if len(ds) == 2:
            if ds[0].isnumeric() and ds[1].isnumeric():
                dataset[int(ds[0])]['w'] = int(ds[1])
    return dataset


def read_dataset(filename):
    # read file and convert data to dict
    # return data as dict
    with open(filename, 'r') as f:
        lines = f.readlines()
    raw_data = []
    for line in lines:
        trimed = trim(line)
        raw_data.append(trimed)#them new_str vao rawdata
    dataset = convert_data(raw_data)
    return dataset



if __name__ == '__main__':
    data = read_dataset('/Users/apple/vehicle-routing-problem/data/custom/a.vrp')
    print(data)
    num_truck = int(input("nhap num_truck : "))
    start_time = time.time()
    p = Problem(data, num_truck)
    hc = CVRP(p,data, 1000)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

    #visualize
    
