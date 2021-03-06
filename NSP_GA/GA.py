from Chromosome import *
from time import time
from random import sample,randint,random
import Local_search
class GA :
    chromosomes = []
    best = 100000000000
    best_sol = []
    def __init__(self,dir,population) :
        self.chromosomes = []
        self.population = population
        self.read_data(dir)
        for i in range(population) :
            self.chromosomes.append(Chromosome(self.nurse_num,self.day_num,self.shift_num,self.requirement,self.preference))
    def Run(self,generation = 10000,mutation_rate = 0.4,select_pair = 4):
        def Select():
            p_pool = []
            for i in range(select_pair):
                pair = sample([i for i in range(self.population)], 2)

                if self.chromosomes[pair[0]].fitness < self.chromosomes[pair[1]].fitness:
                    p_pool.append(pair[0])
                else:
                    p_pool.append(pair[1])
            select = sample(p_pool,2)
            p1,p2 = select[0],select[1]
            return p1,p2
        def Crossover(fParent, sParent):

            child = [[fParent[i][j] for j in range(0, len(fParent[0]))] for i in range(0, len(fParent))]
            x = randint(1, int(len(fParent[0]) / 4) - 1)
            # print (x)
            for i in range(0, len(sParent)):
                for j in range(x * 4, len(sParent[0])):
                    child[i][j] = sParent[i][j]

            return child
        def del_worst():
            while len(self.chromosomes) > self.population:
                min = 0
                for i in range(1,len(self.chromosomes)):
                    if self.chromosomes[i].fitness > self.chromosomes[min].fitness :
                        min = i
                self.chromosomes.pop(min)
        def find_max():
            max = 0
            for i in range(1,len(self.chromosomes)) :
                if self.chromosomes[i].fitness > self.chromosomes[max].fitness :
                    max = i
            return max

        count = 0
        #-------------Start Running--------------#
        while count <= generation :
            while True :
                p1,p2 = Select()
                c_schedule = Crossover(self.chromosomes[p1].schedule,self.chromosomes[p2].schedule)
                if self.isFeasible(c_schedule) == True or False  :
                    break
            new = find_max()
            self.chromosomes[new].schedule = c_schedule
            # self.chromosomes[new].fitness = self.chromosomes[new].cal_fitness()
            # newC = Chromosome.Chromosome(requirement=self.requirement,preference = self.preference,schedule = c_schedule)
            # if feasible

            if random() <  mutation_rate:
                # repeat = randint(1,2)
                # for i in range(repeat):
                self.chromosomes[new].mutation()

            self.chromosomes[new].fitness = self.chromosomes[new].cal_fitness()
            if self.chromosomes[new].fitness < self.best :
                # origin_schedule = self.chromosomes[new].schedule
                # print("Before :",self.chromosomes[new].violate)
                # Local_search.local_search(self.chromosomes[new])

                # new_fitness = self.chromosomes[new].cal_fitness()
                # # print("After :", self.chromosomes[new].violate)
                # # print("After local search:",new_fitness,"before :",self.chromosomes[new].fitness)
                #
                # if(new_fitness < self.chromosomes[new].fitness) :
                #     self.chromosomes[new].fitness = new_fitness
                #     self.best = self.chromosomes[new].fitness
                #     self.best_sol = self.chromosomes[new].schedule
                # else:
                #     self.best = self.chromosomes[new].fitness
                #     self.best_sol = origin_schedule
                self.best = self.chromosomes[new].fitness
                self.best_sol = self.chromosomes[new].schedule


            if count % 1000 == 0 :
                print("Generation : " ,count)
                fitness_sum = 0
                for i in self.chromosomes :
                    fitness_sum += i.fitness

                print(self.chromosomes[new].violate)
                print("Avg. Fitness = %.2f" % float(fitness_sum/self.population))

            # if convergent ,then all mutation
            if count % 100 == 0 :
                for i in range(1,len(self.chromosomes)) :
                    if self.chromosomes[i-1].fitness != self.chromosomes[i].fitness :
                        break
                    if(i == len(self.chromosomes)-1) :
                        # print('same')
                        for i in range(len(self.chromosomes)):
                            self.chromosomes[i].mutation()

            count += 1

    def read_data(self,dir):
        data = open(dir,'r')
        data = data.read().split('\n')
        data = list(filter(lambda a : a != '',data))

        for i in range(len(data)):
            data[i] = data[i].split('\t')
            data[i] = list(filter(lambda a: a != '', data[i]))
            data[i] = list(map(int,data[i]))
        # set (I,K,S)
        self.nurse_num = int(data[0][0])
        self.day_num = int(data[0][1])
        self.shift_num = int(data[0][2])

        # read requirement matrix
        self.requirement = []
        for i in range(self.day_num) :
            self.requirement.append(data[1+i])
        # set preference matrix
        self.preference = []
        for i in range(self.nurse_num) :
            self.preference.append(data[1+self.day_num+i])
        # for i in self.requirement:
        #     print(i)
        # print(self.preference)
    def transform(self,schedule):
        # schedule=[[0,1,0,0,0,0,1,0,1,0,0,0],[1,0,0,0,1,0,0,0,0,0,0,1]]
        TSchedule = [[0 for j in range(0, int(len(schedule[0]) / 4))] for i in range(0, int(len(schedule)))]
        nurseCount = 0;
        zeroCount = 0;
        for i in range(0, len(schedule)):
            if TSchedule == None:
                break

            for j in range(0, len(schedule[i])):
                if zeroCount == 4:
                    TSchedule = None
                    break;

                if j % 4 == 0:
                    nurseCount = 0
                    zeroCount = 0

                if (schedule[i][j] == 1):
                    if (j % 4 == 0):
                        TSchedule[i][int(j / 4)] = 0
                        nurseCount = nurseCount + 1

                    elif (j % 4 == 1):
                        TSchedule[i][int(j / 4)] = 1
                        nurseCount = nurseCount + 1

                    elif (j % 4 == 2):
                        TSchedule[i][int(j / 4)] = 2
                        nurseCount = nurseCount + 1

                    elif (j % 4 == 3):
                        TSchedule[i][int(j / 4)] = 3
                        nurseCount = nurseCount + 1

                else:
                    zeroCount = zeroCount + 1

                if nurseCount > 1:
                    TSchedule = None
                    break;
        # print (TSchedule)
        return TSchedule;
    def isFeasible(self,schedule):
        demand = self.requirement
        supply = [[demand[i][j] for j in range(0, len(demand[0]))] for i in range(len(demand))]
        shiftCount = 0
        TF = True
        for i in range(0, len(schedule)):
            if (TF == False):
                break
            for j in range(0, len(schedule[i])):
                if (schedule[i][j] == 1):

                    if (shiftCount >= 1):  # more than 1 shift a day
                        TF = False
                        # print('more than 1 s', i, j)
                        break

                    if (j % 4 == 2 and j <= len(
                            schedule[i]) - 4):  # when shife3 is assigned, shift 1 of the next day is infeasible
                        if (schedule[i][j + 2] == 1):
                            TF = False
                            # print('s3 than s1', i, j)
                            break

                    supply[int(j / 4)][int(j % 4)] -= 1
                    shiftCount += 1

                if (int(j % 4) == 3):

                    if (shiftCount == 0):  # ALL ZERO
                        TF = False
                        # print('all zero', i, j)
                        break

                    shiftCount = 0

        for i in range(0, len(supply)):  # supply enough?
            if (TF == False):
                break

            for j in range(0, len(supply[i])):
                if (supply[i][j] > 0):
                    TF = False
                    # print('supply not enough', i, j)
                    break
        # print (TF)
        return TF
if __name__ =='__main__' :
    dir = './data/1.nsp'

    for i in range(1) :
        start_time = time()
        population = 15
        mutation_rate = 0.4
        print('\n-----------Population = %d Mutation rate = %.2f---------------' % (population,mutation_rate))
        NSP = GA(dir,population)
        NSP.Run(generation=10000,mutation_rate = mutation_rate)

        print(NSP.best)
        trans = NSP.transform(NSP.best_sol)
        for i in trans:
            print(i)
        # print(NSP.chromosomes[0].schedule)
        end_time = time()
        print("Time : %.2f second" % float(end_time - start_time))

    end = True