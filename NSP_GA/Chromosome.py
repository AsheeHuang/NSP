from random import sample,randint
import Local_search

class Chromosome:
    def __init__(self,nurse_num=0,day_num=0,shift_num=0,requirement=0,preference=0):
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

        def fitness_preference(preference, schedule=self.schedule):
            sum_preference = 0
            for i in range(0, len(preference)):
                for j in range(0, len(preference[0])):
                    sum_preference += pow(preference[i][j], 2) * self.schedule[i][j]
            return sum_preference

        def fitness_OffDayOver3(schedule=self.schedule):
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

        def fitness_OnDutyOver7(schedule=self.schedule):
            sum_OnDutyOver7 = 0
            OndutyCount = 0
            for i in range(0, len(schedule)):
                for j in range(0, len(schedule[0])):
                    if (j % 4 == 3):
                        if (schedule[i][j] != 1):
                            OndutyCount += 1
                            if (OndutyCount >= 6):
                                sum_OnDutyOver7 += 1
                        else:
                            OndutyCount = 0

            return sum_OnDutyOver7

        def fitness_StayupOver3(schedule=self.schedule):
            sum_StayupOver3 = 0
            StayupDays_Count = 0
            for i in range(0, len(schedule)):
                for j in range(0, len(schedule[0])):
                    if (j % 4 == 2 and schedule[i][j] == 1):
                        StayupDays_Count += 1
                        # print("Stayup at {0} {1}".format(i, j))
                        if (StayupDays_Count >= 3):
                            sum_StayupOver3 += 1
                    elif (j % 4 == 2 and schedule[i][j] == 0):
                        StayupDays_Count = 0

            return sum_StayupOver3

        def fitness_overStaffing(schedule=self.schedule):
            violate = 0
            for i in range(int(len(schedule[0]) / 4)):
                for j in range(3):
                    if Chromosome.requirement[i][j] < self.count_nurse(i, j):
                        # print('violate at',i,j)
                        violate += 1
            return violate

        # ----------------------------------------------------------------#
        fitness = 0
        constraint = [0] * 5
        penalty = [1, 10, 20, 10, 50]

        constraint[0] = fitness_preference(preference_matrix)
        constraint[1] = fitness_OffDayOver3()
        constraint[2] = fitness_OnDutyOver7()
        constraint[3] = fitness_StayupOver3()
        constraint[4] = fitness_overStaffing()

        if len(constraint) == len(penalty):
            for i in range(len(constraint)):
                fitness += constraint[i] * penalty[i]
        else:
            print('Calculate fitness error')
        if self.isFeasible() == False:
            fitness += 1000
            # tran = self.transform(self.schedule)
            # for i in tran :
            #     print(i)
            # print()
            # print('infeasible')
        self.violate = constraint
        # print(constraint, fitness)
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

                    if (j % 4 == 2 and j <= len(schedule[i]) - 4):  # when shife3 is assigned, shift 1 of the next day is infeasible
                        if (schedule[i][j + 2] == 1):
                            TF = False
                            # print('s3 than s1', i, (j-2)/4)
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

        # transform(None)
    def mutation(self):
        origin_schedule = self.schedule

        def max_improve(nurse, day, shift):  # return the shift improve most
            preference = Chromosome.preference
            prefer = preference[nurse][day * 4 + shift]
            max = -10
            s = -1
            for i in range(4):
                if i != shift:
                    if prefer - preference[nurse][day * 4 + i] >= max:
                        max = prefer - preference[nurse][day * 4 + i]
                        s = i
            return s
        def fix(nurse, day, next_shift):
            schedule = self.schedule
            if next_shift == 0 and schedule[nurse][(day - 1) * 4 + 2] == 1:
                day = day - 1
                shift = max_improve(nurse, day, 0)

                candidate = []
                while True:  # candidate can't be empty
                    for i in range(len(schedule)):
                        if schedule[i][day * 4 + shift] == 1:
                            candidate.append(i)
                    if len(candidate) > 0:
                        break
                    else:
                        shift = sample([0, 1, 3], 1)[0]

                sel = randint(0, len(candidate) - 1)
                self.change_shift(nurse, day, shift)
                self.change_shift(candidate[sel], day, 2)

                fix(candidate[sel], day, 2)

            if next_shift == 2 and day+1<int(len(schedule[0])/4) and  schedule[nurse][(day + 1) * 4] == 1:
                day = day + 1
                shift = max_improve(nurse, day, 0)

                candidate = []
                while True:  # candidate can't be empty
                    for i in range(len(schedule)):
                        if schedule[i][day * 4 + shift] == 1:
                            candidate.append(i)
                    if len(candidate) > 0:
                        break
                    else:
                        shift = sample([1, 2, 3], 1)[0]

                sel = randint(0, len(candidate) - 1)
                self.change_shift(nurse, day, shift)
                self.change_shift(candidate[sel], day, 0)

                fix(candidate[sel], day, 0)

        n = randint(0,len(self.schedule)-1)
        d = randint(0,len(self.schedule[0])/4-1)
        # print(self.schedule[n][d*4:d*4+4])

        for i in range(4):
            if self.schedule[n][d*4+i] == 1 :
                shift_num = randint(1,3)
                self.schedule[n][d*4+i] = 0
                next_shift = (i+shift_num)%4
                origin_shift = i
                self.schedule[n][d*4+next_shift] = 1

                fix(n,d,next_shift)

                while True :
                    candidate = []
                    for i in range(len(self.schedule)):
                        if self.schedule[i][d * 4 + next_shift] == 1:
                            candidate.append(i)
                    # print(candidate)
                    # if candidate exist
                    if len(candidate) > 0 :
                        break
                    else :
                        next_shift = sample([0,1,2,3].remove(i))
                        self.change_shift(n,d,next_shift)

                self.change_shift(n, d, next_shift)  # switch nurse from original shift to better shift
                # print("nurse :" + str(n) + "   day :" + str(d), "    =", origin_shift, "->", next_shift)
                sel_nurse = randint(0, len(candidate) - 1)
                self.change_shift(candidate[sel_nurse], d, origin_shift)
                # print("nurse :" + str(candidate[sel_nurse]) + "   day :" + str(d), "    =", next_shift, "->",origin_shift)

                fix(candidate[sel_nurse], d, origin_shift)
                if self.isFeasible() is False :
                    self.schedule=origin_schedule

                break
        # print(self.schedule[n][d * 4:d * 4 + 4])
    def change_shift(self,nurse,day,shift):
        self.schedule[nurse][4 * day] = 0
        self.schedule[nurse][4 * day +1] = 0
        self.schedule[nurse][4 * day +2] = 0
        self.schedule[nurse][4 * day +3] = 0
        self.schedule[nurse][4 * day + shift] = 1