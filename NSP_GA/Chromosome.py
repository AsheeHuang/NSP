from random import sample,randint
class Chromosome:
    def __init__(self,nurse_num,day_num,shift_num,requirement,preference):
        Chromosome.preference = preference
        Chromosome.requirement = requirement
        self.create(nurse_num,day_num,shift_num,requirement) #create feasible chromosome

    def create(self,nurse_num,day_num,shift_num,requirement):
        # until this chromosome is feasible
        while True :
            self.schedule = [[0] * (day_num * shift_num) for i in range(nurse_num)]
            for i in range(day_num):
                #randomly select samples from 1 to nurse number
                select_list = sample([i for i in range(nurse_num)],sum(requirement[i]))
                # print(len(select_list),select_list)
                select= 0
                for j in range(shift_num) :
                    count = 0
                    while count < requirement[i][j] :
                        #check previous day
                        if j == 0 :
                            rand = select_list[select]
                            try:
                                while self.schedule[rand][(i-1)*4+2] == 1:
                                    while True:
                                        rand = randint(0, nurse_num-1 )
                                        if rand not in select_list:
                                            break
                            except IndexError:
                                pass
                            self.schedule[rand][i*4+j] = 1
                        #check next day
                        elif j == 2 :
                            rand = select_list[select]
                            try :
                                while self.schedule[rand][(i+1)*4] == 1 :
                                    while True :
                                        rand = randint(0,nurse_num-1)
                                        if rand not in select_list :
                                            break
                            except IndexError:
                                pass
                            self.schedule[rand][i*4+2] = 1
                        else :
                            self.schedule[select_list[select]][i*4+j] = 1
                        count += 1
                        select += 1


            for i in range(nurse_num):
                for j in range(day_num):
                    if self.schedule[i][j*4] == 0 and self.schedule[i][j*4+1] == 0 and self.schedule[i][j*4+2] == 0 :
                        self.schedule[i][j*4+3] = 1
            if self.isFeasible():
                break
        self.fitness = self.cal_fitness()
        # print(self.isFeasible())
        # trans_matrix = (self.transform(self.schedule))
        # for i in trans_matrix:
        #     print(i)
        # for i in self.schedule:
        #     print(i)
    def cal_fitness(self):
        preference_matrix = Chromosome.preference
        def preference_fitness(preference, schedule = self.schedule):
            sum_preference = 0
            for i in range(0, len(preference)):
                for j in range(0, len(preference[0])):
                    sum_preference += pow(preference[i][j], 2) * self.schedule[i][j]
            return sum_preference
        def fitness_OffDayOver3(schedule = self.schedule):
            sum_OffDayOver3 = 0
            OffDayCount = 0
            for i in range(0, len(schedule)):
                for j in range(0, len(schedule[0])):
                    if (j % 4 == 3):
                        if (schedule[i][j] == 1):
                            OffDayCount += 1
                            if (OffDayCount >= 3):
                                sum_OffDayOver3 += 1
                        else:
                            OffDayCount = 0

            return sum_OffDayOver3
        def fitness_OnDutyOver7(schedule = self.schedule):
            sum_OnDutyOver7 = 0
            OndutyCount = 0
            for i in range(0, len(schedule)):
                for j in range(0, len(schedule[0])):
                    if (j % 4 == 3):
                        if (schedule[i][j] != 1):
                            OndutyCount += 1
                            if (OndutyCount >= 7):
                                sum_OnDutyOver7 += 1
                        else:
                            sum_OnDutyOver7 = 0

            return sum_OnDutyOver7
        # ----------------------------------------------------------------#
        fitness = 0
        constraint = [0]*3
        penalty = [1,200,200]

        constraint[0] = preference_fitness(preference_matrix)
        constraint[1] = fitness_OffDayOver3()
        constraint[2] = fitness_OnDutyOver7()

        if len(constraint) == len(penalty):
            for i in range(len(constraint)) :
                fitness += constraint[i]*penalty[i]
        else :
            print('Calculate fitness error')

        print(constraint,fitness)
        return fitness
    def isFeasible(self):
        demand = Chromosome.requirement
        schedule = self.schedule
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
    def count_nurse(self,day,shift):
        count = 0
        for i in range(len(self.schedule)) :
            if self.schedule[i][day*4+shift] == 1 :
                count += 1
        return count
    def transform(self,schedule):
        # scheldule=[[0,1,0,0,0,0,1,0,1,0,0,0],[1,0,0,0,1,0,0,0,0,0,0,1]]
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
                        TSchedule[i][int(j / 4)] = 1
                        nurseCount = nurseCount + 1

                    elif (j % 4 == 1):
                        TSchedule[i][int(j / 4)] = 2
                        nurseCount = nurseCount + 1

                    elif (j % 4 == 2):
                        TSchedule[i][int(j / 4)] = 3
                        nurseCount = nurseCount + 1

                    elif (j % 4 == 3):
                        TSchedule[i][int(j / 4)] = 4
                        nurseCount = nurseCount + 1

                else:
                    zeroCount = zeroCount + 1

                if nurseCount > 1:
                    TSchedule = None
                    break;
        # print (TSchedule)
        return TSchedule;

        # transform(None)

