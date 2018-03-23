from deap import base
from deap import creator
from deap import tools

from src.artificial_bee_colony_algorithm import initialisation, rememberBEST
from src.foodsource import calculateNectar, FoodSource

import matplotlib.pyplot as plt
from copy import deepcopy
import numpy as np


def main(file):
    start = FoodSource(file)
    creator.create("NectarMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.NectarMin)

    EMPLOYED = 20
    ONLOOKER = 20
    SCOUT = 1
    NGEN = 100

    toolbox = base.Toolbox()
    toolbox.register("individual", initialisation, creator.Individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", calculateNectar)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)

    pop = toolbox.population(n=EMPLOYED)
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    myPlot = []
    evolution = [0] * EMPLOYED
    BEST = None
    for j in range(NGEN):
        # employed bee phase
        i = 0
        while i < EMPLOYED:
            temp = deepcopy(pop[i])

            toolbox.mutate(temp)
            temp_fitness = toolbox.evaluate(temp)
            if pop[i].fitness.values > temp_fitness:
                temp.fitness.values = temp_fitness
                delete_me = pop[i]
                pop[i] = temp
                del delete_me
                evolution[i] = 0
            else:
                evolution[i] = evolution[i] + 1
                if evolution[i] >= NGEN / 10 and BEST != pop[i]:
                    del evolution[i]
                    del pop[i]
                    SCOUT = SCOUT + 1
                    EMPLOYED = EMPLOYED - 1

            i = i + 1

        # onlooker bee phase
        totalFitness = 0
        onlooker_pop = []

        for i in pop:
            totalFitness = totalFitness + i.fitness.values[0]
        probability = [i.fitness.values[0] / totalFitness for i in pop]  # min.!
        for i in range(ONLOOKER):
            choice = np.random.choice(range(len(pop)), p=probability)
            onlooker_pop.append(pop[choice])

            temp = deepcopy(onlooker_pop[i])

            toolbox.mutate(temp)
            temp_fitness = toolbox.evaluate(temp)
            if onlooker_pop[i].fitness.values > temp_fitness:
                temp.fitness.values = temp_fitness
                delete_me = onlooker_pop[i]
                onlooker_pop[i] = temp
                del delete_me

        # scout bee phase
        if SCOUT > 0:
            newFS = toolbox.population(n=SCOUT)
            fitnesses = list(map(toolbox.evaluate, newFS))
            for ind, fit in zip(newFS, fitnesses):
                ind.fitness.values = fit
            pop = pop + newFS
            temp = [0] * len(newFS)
            evolution = evolution + temp
            EMPLOYED = EMPLOYED + SCOUT
            SCOUT = 0

        # remember BEST solution achieved so far
        BEST = rememberBEST(pop, BEST)
        BEST = rememberBEST(onlooker_pop, BEST)

        myPlot.append(BEST.fitness.values[0])

    # employed bees phase means
    # mutation

    # onlooker bees phase means
    # Choose probabilistically, a FS from the list
    # choose a neighbor, and apply greedy selection based on fitness
    # NOTE: This can actually be considered a selection phase (in a vague sense)

    # scout bees phase means
    # generate a random food source (use the initialization function)

    plt.plot(myPlot)
    plt.xlabel('Number of iterations')
    plt.ylabel('Fitness')
    plt.savefig('../Solutions/Solution ' + str(file) + '.svg', format='svg')
    plt.gcf().clear()
    print(BEST.fitness.values[0])
    FoodSource.initialized = False


for i in range(180):
    main(i)
