import random
from random import randrange
from time import time
import copy
import sys


# ============================ GENETIC ALGORITHM =======================================
# Class to represent problems to be solved by means of a general
# genetic algorithm. It includes the following attributes:
# - genes: list of possible genes in a chromosome
# - individuals_length: length of each chromosome
# - decode: method that receives the genotype (chromosome) as input and returns
#    the phenotype (solution to the original problem represented by the chromosome)
# - fitness: method that returns the evaluation of a chromosome (acts over the
#    genotype)
# - mutation: function that implements a mutation over a chromosome
# - crossover: function that implements the crossover operator over two chromosomes
# ========================================================================================

class Individual(object):

    def __init__(self, genes, individuals_length, decode, fitness):
        self.genes = genes
        self.individuals_length = individuals_length
        self.decode = decode
        self.fitness = fitness

    def mutation(self, chromosome_aux):
        chromosome = chromosome_aux

        index1 = randrange(0, self.individuals_length)
        index2 = randrange(index1, self.individuals_length)

        chromosome_mid = chromosome[index1:index2]
        chromosome_mid.reverse()

        chromosome_result = chromosome[0:index1] + chromosome_mid + chromosome[index2:]

        return chromosome_result

    def crossover(self, parent1, parent2):
        pos = random.randrange(1, self.individuals_length - 1)
        child1 = parent1[:pos]
        child2 = parent2[:pos]
        parent1_copy = copy.deepcopy(parent1)
        parent2_copy = copy.deepcopy(parent2)
        for gen1 in parent1_copy:
            if child2.count(gen1) != parent1.count(gen1):
                child2.append(gen1)

        for gen2 in parent2_copy:
            if child1.count(gen2) != parent2.count(gen2):
                child1.append(gen2)

        return [child1, child2]


def decode_vrp(chromosome):
    ls = []
    truck = [cities.get(0)]
    for k in chromosome:
        truck.append(cities.get(k))
        if k == 0:
            ls.append(truck)
            truck = [cities.get(0)]
    return ls


def penalty_capacity(chromosome):
    actual = chromosome
    capacity_list = []
    index_cap = 0

    for i in range(0, num_truck):
        init = 0
        capacity_list.append(init)

    for k in actual:
        if k != 0:
            capacity_list[int(index_cap)] += 1
        else:
            index_cap += 1

    return max(capacity_list)


def fitness_vrp(chromosome):
    def distance_trip(index, city):
        w = distances.get(index)
        return w[city]

    penalty_cap = penalty_capacity(chromosome)

    actual_chromosome = [0] + chromosome + [0]
    fitness_value = []
    for i in range(0, num_truck + 1):
        init = 0
        fitness_value.append(init)
    count = 0
    for i in range(len(actual_chromosome) - 1):
        if actual_chromosome[i] == 0 and i != 0:
            count += 1
        fitness_value[int(count)] += distance_trip(actual_chromosome[i], actual_chromosome[i + 1]) \
                                     + (50 * penalty_cap) + capacity_customer[actual_chromosome[i]]
    min_value = sys.maxsize
    for value in fitness_value:
        if 0 < value < min_value:
            min_value = value
    return min_value


# =============================== FIRST PART: GENETIC OPERATORS======================================
# Here We defined the requierements functions that the GA needs to work
# The function receives as input:
# * problem_genetic: an instance of the class Problem_Genetic, with
#     the optimization problem that we want to solve.
# * k: number of participants on the selection tournaments.
# * opt: max or min, indicating if it is a maximization or a
#     minimization problem.
# * generation: number of generations (halting condition)
# * size: number of individuals for each generation
# * ratio_cross: portion of the population which will be obtained by
#     means of crossovers.
# * prob_mutate: probability that a gene mutation will take place.
# ====================================================================================================

class Population:
    def __init__(self, individual, tour_size=2, population_size=100, ratio_cross=0.8, prob_mutate=0.05):
        self.individual = individual
        self.tour_size = tour_size
        self.population_size = population_size
        n_parents = round(population_size * ratio_cross)
        self.n_parents = (n_parents if n_parents % 2 == 0 else n_parents - 1)
        self.n_directs = self.population_size - self.n_parents
        self.prob_mutate = prob_mutate

    def initial_population(self):
        def generate_chromosome(genes):
            chromosome = []
            for i in genes:
                chromosome.append(i)
            random.shuffle(chromosome)
            return chromosome

        return [generate_chromosome(self.individual.genes) for _ in range(self.population_size)]

    def tournament_selection(self, population, number_tour):
        winners = []
        for _ in range(number_tour):
            elements = random.sample(population, self.tour_size)
            winners.append(min(elements, key=self.individual.fitness))
        return winners

    def new_generation_t(self, population):
        def mutate(cross):
            for i in cross:
                if random.random() < self.prob_mutate:
                    self.individual.mutation(i)
            return cross

        def cross_over(parents):
            childs = []
            for i in range(0, len(parents), 2):
                childs.extend(self.individual.crossover(parents[i], parents[i + 1]))
            return childs

        directs = self.tournament_selection(population, self.n_directs)
        cross_parent = self.tournament_selection(population, self.n_parents)
        crosses = cross_over(cross_parent)
        mutations = mutate(crosses)
        new_generation = directs + mutations

        return new_generation


def genetic_algorithm_t(population, generation):
    individuals = population.initial_population()

    for _ in range(generation):
        individuals = population.new_generation_t(individuals)

    best_chromosome = min(individuals, key=population.individual.fitness)
    print("Chromosome: ", best_chromosome)
    genotype = population.individual.decode(best_chromosome)
    print("Solution: ", (genotype, population.individual.fitness(best_chromosome)))
    return genotype, population.individual.fitness(best_chromosome)

    # =================================THIRD PART: EXPERIMENTATION=================================================
    # Run over the same instances both the standard GA (from first part) as well as the modified version
    # (from second part).
    # Compare the quality of their results and their performance. Due to the inherent randomness of GA,
    # the experiments performed over each instance should be run several times.
    # =============================================================================================================

    # ----------------------------------------MAIN PROGRAMA PRINCIPAL--------------------------------


def first_part_ga(intances):
    genes = [0, 0, 0, 1, 2, 3, 4, 5, 6, 7]
    ind = Individual(genes, len(cities), lambda x: decode_vrp(x), lambda y: fitness_vrp(y))
    population = Population(ind, tour_size=2, population_size=100, ratio_cross=0.8, prob_mutate=0.05)
    cont = 0
    print(
        "-----------------------------Executing FIRST PART: VRP -------------------------------- \n")
    print("Office = ", cities.get(0))
    print("")
    tiempo_inicial_t2 = time()
    while cont <= intances:
        print("Intance 1: ")
        genetic_algorithm_t(population=population, generation=200)
        cont += 1
    tiempo_final_t2 = time()
    print("\n")
    print("Total time: ", (tiempo_final_t2 - tiempo_inicial_t2), " secs.\n")


# ---------------------------------------- AUXILIARY DATA FOR TESTING --------------------------------

# CONSTANTS

cities = {0: 'Office', 1: 'Cadiz', 2: 'Cordoba', 3: 'Granada', 4: 'Huelva', 5: 'Jaen', 6: 'Malaga', 7: 'Sevilla'}

# Distance between each pair of cities

w0 = [0, 454, 317, 165, 528, 222, 223, 410]
w1 = [453, 0, 253, 291, 210, 325, 234, 121]
w2 = [317, 252, 0, 202, 226, 108, 158, 140]
w3 = [165, 292, 201, 0, 344, 94, 124, 248]
w4 = [508, 210, 235, 346, 0, 336, 303, 94]
w5 = [222, 325, 116, 93, 340, 0, 182, 247]
w6 = [223, 235, 158, 125, 302, 185, 0, 206]
w7 = [410, 121, 141, 248, 93, 242, 199, 0]
distances = {0: w0, 1: w1, 2: w2, 3: w3, 4: w4, 5: w5, 6: w6, 7: w7}

capacity_customer = {0: 0, 1: 19, 2: 30, 3: 16, 4: 23, 5: 11, 6: 31, 7: 15, 8: 28}
num_truck = 4
if __name__ == "__main__":
    # Constant that is an instance object
    num_ga_intances = 10
    print("EXECUTING ", num_ga_intances, " INSTANCES ")
    first_part_ga(num_ga_intances)
    print(
        "--------------------------------------------------------------------------------------")
    # second_part_ga(num_ga_intances)
