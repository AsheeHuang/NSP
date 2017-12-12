import Chromosome
from random import sample,randint
class GA :
    chromosomes = []

    def __init__(self,dir,population) :
        self.population = population
        self.read_data(dir)
        for i in range(population) :
            self.chromosomes.append(Chromosome.Chromosome(self.nurse_num,self.day_num,self.shift_num,self.requirement,self.preference))

    def Run(self,total_count = 3000,select_pair = 4):
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
        count = 0
        #-------------Start Running--------------#
        while count < total_count :
            p1,p2 = Select()
            c_schedule = Crossover(self.chromosomes[p1].schedule,self.chromosomes[p2].schedule)

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


if __name__ =='__main__' :
    dir = './data/1.nsp'
    data = open(dir,'r')
    NSP = GA(dir,15)
    NSP.Run()
    end = True
