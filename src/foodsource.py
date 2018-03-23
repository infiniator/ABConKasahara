from functools import cmp_to_key
from src.dataset import readData
from src.comparator import compare


class FoodSource:
    numTasks = 0  # number of input tasks
    numProcs = 0  # number of input processors
    initialized = False  # used to ensure readData() is called only once
    data = None  # data from the Kasahara dataset

    def __init__(self, file=0):
        if not FoodSource.initialized:
            FoodSource.initialized = True
            FoodSource.data = readData(file)
            FoodSource.numProcs = FoodSource.data['numProcs']
            FoodSource.numTasks = FoodSource.data['numTasks']
            del FoodSource.data['numProcs']
            del FoodSource.data['numTasks']
            FoodSource.data = list(FoodSource.data.values())
            # now, data is a list of task dictionaries sorted topologically
            # sort according to heights
            FoodSource.data.sort(key=cmp_to_key(compare))
            j = 0
            for i in FoodSource.data:  # save key for internal calculation later
                i['key'] = j
                j += 1
                # self.schedule = [[] for i in range(0, Chromosome.numProcs)]


# the fitness of a chromosome, currently, is its finishing time
def calculateNectar(foodsource):
    finishTime = [0] * FoodSource.numTasks
    for i in range(len(FoodSource.data)):  # for every task, do the following
        pre = []  # holds predecessors of i, including the forced predecessor
        p = foodsource[i]  # extract processor on which i is running
        j = True
        for _ in range(i):  # find if i is the first task to run
            if foodsource[_] == p:
                j = False
                break
        if not j:  # if i isn't first task, find task that runs just before i
            for k in range(i - 1, -1, -1):
                if p == foodsource[k]:  # forced predecessor
                    pre.append(FoodSource.data[k]['procID'])
        for k in FoodSource.data[i]:
            if 'pre' in k:
                pre.append(FoodSource.data[i][k])
        if len(pre) > 0:
            finishTime[FoodSource.data[i]['procID'] - 1] = max(
                [finishTime[j - 1] for j in pre]
            ) + FoodSource.data[i]['procTime']
        else:
            finishTime[FoodSource.data[i]['procID'] - 1] = FoodSource.data[i]['procTime']
    return max(finishTime),
