import string
import random

KEY: str = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit..."
KEY_LEN:int = len(KEY)
POPULATION_SIZE = 100
NO_GEN = 500
TOURNAMENT_SAMPLE_SIZE = 5
MUTATE_PROB = 0.01
ELITE_SIZE = 5
class Individual:
    def __init__ (self,genotype:str):
        self.genotype:str = genotype
        self.fitness_score = -1 #not evaluated yet
    def __str__(self):
        return f"{round(self.fitness_score,2)} - {self.genotype}"

def first_generation(population_arr:list, avaliable_genes:list):
    for _ in range(POPULATION_SIZE):
        new_invidual = Individual(''.join([avaliable_genes[random.randint(0,len(avaliable_genes)-1)] for _ in range(KEY_LEN)]))
        population_arr.append(new_invidual)
    return population_arr

def fitness_function(individual:Individual):
    correct_chars = 0
    for i in range (KEY_LEN):
        if(individual.genotype[i]==KEY[i]): correct_chars+=1

    char_score = correct_chars*100
    total_score = char_score
    individual.fitness_score = total_score

def evaluate_generation(population_arr:list):
    for individual in population_arr:
        fitness_function(individual)
    pass

def pick_parents(population):
    picked_arr = []
    while len(picked_arr)<TOURNAMENT_SAMPLE_SIZE:
        picked_randomly = random.choice(population)
        if picked_randomly not in picked_arr:
            picked_arr.append(picked_randomly)

    picked_arr.sort(key = lambda x:x.fitness_score, reverse=True)
    return picked_arr[0], picked_arr[1]

def mutate(genotype):
    genotype_arr = list(genotype)
    #mutate
    for i in range (len(genotype_arr)):
        if (random.random() <MUTATE_PROB):
            genotype_arr[i] = avaliable_genes[random.randint(0,len(avaliable_genes)-1)]

    return ''.join(genotype_arr)

def reproduction_function(population):
    # pick parents

    new_population = population[:ELITE_SIZE]
    while len(new_population)<POPULATION_SIZE:

        parent_1, parent_2 = pick_parents(population)
        # crossover
        middle_point = random.randint(1, KEY_LEN-1)

        child_genotype_1 = parent_1.genotype[:middle_point] + parent_2.genotype[middle_point:]
        child_genotype_2= parent_2.genotype[:middle_point] + parent_1.genotype[middle_point:]

        #mutation
        child_genotype_1 = mutate(child_genotype_1)
        child_genotype_2 = mutate(child_genotype_2)

        new_population.append(Individual(child_genotype_1))
        if len(new_population) < POPULATION_SIZE:
            new_population.append(Individual(child_genotype_2))

    return new_population

def print_top(population):
    pop_sorted = sorted(population, key=lambda x:x.fitness_score, reverse=True)
    for i in range(3):
        print(pop_sorted[i])

population_arr: list = []
avaliable_genes: list = list(string.ascii_letters )
avaliable_genes.append(" ")
avaliable_genes.append(".")
avaliable_genes.append(",")

first_generation(population_arr,avaliable_genes)
print_top(population_arr)
print("----------------------")
for i in range(NO_GEN):
    evaluate_generation(population_arr)

    if(i%5 ==0):
        print(f'GEN: {i}')
        print_top(population_arr)
        print("----------------------")

    population_arr = reproduction_function(population_arr)
