from random import randrange
from src.foodsource import FoodSource


def initialisation(food):  # done
    newBee = food()
    for i in range(FoodSource.numTasks):
        newBee.append(0)
    for j in range(len(FoodSource.data)):
        k = randrange(0, FoodSource.numProcs)
        newBee[j] = k
    return newBee


def rememberBEST(pop, currBEST):
    maxFitness = 0
    for i in range(len(pop)):
        if pop[maxFitness].fitness.values > pop[i].fitness.values:
            maxFitness = i
    if currBEST is None or currBEST.fitness.values > pop[maxFitness].fitness.values:
        currBEST = pop[maxFitness]
    return currBEST
