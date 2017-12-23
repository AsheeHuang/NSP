from GA import *
import threading
from time import time
class MyThread(threading.Thread) :
    def __init__(self,threadID,name,island,generation,mutation_rate):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.island = island
        self.generation = generation
        self.mutation_rate = mutation_rate
    def run(self):
        print("Starting " + self.name)
        self.island.Run(generation=self.generation,mutation_rate=self.mutation_rate)
        print("Exiting " + self.name)

def migration(island1,island2,island3) :
    def find_best(island) :
        best_fitness = 0  #point to index
        for i in range(len(island.chromosomes)) :
            island.chromosomes[i].fitness = island.chromosomes[i].cal_fitness()
            if island.chromosomes[i].fitness < island.chromosomes[best_fitness].fitness :
                best_fitness = i
        return best_fitness

    def del_worst(island):
        while len(island.chromosomes) > island.population :
            max = 0
            for i in range(len(island.chromosomes)):
                island.chromosomes[i].fitness = island.chromosomes[i].cal_fitness()
                if island.chromosomes[i].fitness > island.chromosomes[max].fitness:
                    max = i
            # print("Worst :",island.chromosomes[max].fitness)
            island.chromosomes.pop(max)

    def find_max(island):
        max = 0
        for i in range(1, len(island.chromosomes)):
            if island.chromosomes[i].fitness > island.chromosomes[max].fitness:
                max = i
        return max

    """-------------Start--------------"""
    #
    # island1.chromosomes.append(island2.chromosomes[find_best(island2)])
    # island1.chromosomes.append(island3.chromosomes[find_best(island3)])
    #
    # island2.chromosomes.append(island1.chromosomes[find_best(island1)])
    # island2.chromosomes.append(island3.chromosomes[find_best(island3)])
    #
    # island3.chromosomes.append(island1.chromosomes[find_best(island1)])
    # island3.chromosomes.append(island2.chromosomes[find_best(island2)])
    #
    # del_worst(island1)
    # del_worst(island2)
    # del_worst(island3)
    island1.chromosomes[find_max(island1)] = island2.chromosomes[find_best(island2)]
    # island1.chromosomes[find_max(island1)] = island3.chromosomes[find_best(island3)]
    island2.chromosomes[find_max(island2)] = island1.chromosomes[find_best(island3)]
    # island2.chromosomes[find_max(island2)] = island3.chromosomes[find_best(island3)]
    island3.chromosomes[find_max(island3)] = island1.chromosomes[find_best(island1)]
    # island3.chromosomes[find_max(island3)] = island2.chromosomes[find_best(island2)]

    update(island1)
    update(island2)
    update(island3)

def update(island) :
    for i in range(island.population):
        if island.chromosomes[i].fitness < island.best:
            island.best = island.chromosomes[i].fitness
            island.best_sol = island.chromosomes[i].schedule
if __name__ == '__main__' :
    dir = './data/1.nsp'
    population = 15
    mutation_rate = 0.4
    generation = 100

    island1 = GA(dir, population)
    island2 = GA(dir, population)
    island3 = GA(dir, population)

    start_time = time()
    for i in range(100) :
        print('---------------------------',i,'--------------------------------')
        # island1.Run(100,mutation_rate=0.4)
        # island2.Run(100,mutation_rate=0.4)
        # island3.Run(100, mutation_rate=0.4)

        thread1 = MyThread(1, 'Thread 1',island1,generation=generation,mutation_rate = mutation_rate)
        thread2 = MyThread(2, 'Thread 2',island2,generation=generation,mutation_rate = mutation_rate)
        thread3 = MyThread(3, 'Thread 3',island3,generation=generation,mutation_rate = mutation_rate)

        thread1.start()
        thread2.start()
        thread3.start()

        thread1.join()
        thread2.join()
        thread3.join()

        migration(island1,island2,island3)

    min = 0
    for i in range(1, len(island1.chromosomes)):
        if island1.chromosomes[i].fitness < island1.chromosomes[min].fitness :
            min = i

    print("Best Fitness : " ,island1.chromosomes[min].fitness)
    trans = island1.transform(island1.chromosomes[min].schedule)
    for i in trans :
        print(i)

    end_time = time()
    print("Time : %.2f second" % float(end_time - start_time))

    end = True


