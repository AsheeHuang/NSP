import GA
import Chromosome
from random import randint,sample


def fitness_OffDayOver3(schedule):
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
def fitness_OnDutyOver7(schedule):
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
def fitness_StayupOver3(schedule):
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

def local_search(individual):
    schedule = individual.schedule
    preference = individual.preference
    def find_maxColumn():
        day_fitness = []
        for k in range(int(len(schedule[0])/4)):
            day_sum = 0
            for i in range(len(schedule)) :
                for j in range(4) :
                    if schedule[i][k*4+j] == 1 :
                        day_sum += pow(preference[i][j],2)
            day_fitness.append(day_sum)

        max = 0
        for i in range(1,len(day_fitness)) :
            if day_fitness[i] > day_fitness[max] :
                max = i
        return max #return the max column sum
    def improve(day) :
        improve = [[],[],[],[]]
        #(improve[x])放的是 最多可以進步x的護士編號

        for i in range(len(schedule)) :
            curr_prefer = -1 #not found yet
            for j in range(4) :
                if schedule[i][day*4+j] == 1 : #found
                    curr_prefer = preference[i][day * 4 + j]
                    break
            max = -1
            for j in range(4) :
                diff = curr_prefer - preference[i][day * 4 + j]
                if   diff > 0 : #if improve
                    max = diff
            if max > 0 :
                improve[max].append(i)
        return improve
    def swap_shift(nurse,day):
        origin_shift = -1
        for i in range(4):
            if schedule[nurse][day*4+i] == 1 :
                prefer = preference[nurse][day*4+i]
                origin_shift = i
                break
        # print("origin_shift",origin_shift)
        max_diff = 0
        next_shift = -1
        for i in range(4) :
            diff = prefer - preference[nurse][day * 4 + i]
            # print(diff,"=",prefer,"-",preference[nurse][day * 4 + i])
            if  diff > max_diff:
                max_diff = diff
                next_shift = i
        # print("next shift",next_shift)
        #可以交換的護士
        candidate = []
        for i in range(len(schedule)) :
            if schedule[i][day*4+next_shift] == 1 :
                candidate.append(i)
        # print(candidate)
        #if candidate exist
        if len(candidate) > 0 and next_shift >= 0:
            change_shift(schedule,nurse,day,next_shift) #switch nurse from original shift to better shift
            # print("nurse :"+str(nurse)+"   day :"+str(day),"    =",origin_shift,"->",next_shift)
            if next_shift == 0 or 2 :
                fix(nurse,day,next_shift)
            sel_nurse = randint(0,len(candidate)-1)
            change_shift(schedule,candidate[sel_nurse],day,origin_shift)
            # print("nurse :" + str(candidate[sel_nurse]) + "   day :" + str(day), "    =", next_shift, "->", origin_shift)
            if origin_shift == 0 or 2 :
                fix(candidate[sel_nurse],day,origin_shift)
    def max_improve(nurse,day,shift)  : #return the shift improve most
        prefer = preference[nurse][day*4+shift]
        max = -10
        s = -1
        for i in range(4) :
            if i != shift :
                if prefer - preference[nurse][day*4+i] >= max :
                    max = prefer - preference[nurse][day * 4 + i]
                    s = i
        return s
    def change_shift(schedule, nurse, day, shift):
        schedule[nurse][4 * day] = 0
        schedule[nurse][4 * day + 1] = 0
        schedule[nurse][4 * day + 2] = 0
        schedule[nurse][4 * day + 3] = 0
        schedule[nurse][4 * day + shift] = 1
    def fix(nurse,day,next_shift) :
        if next_shift == 0  and schedule[nurse][(day-1)*4+2] == 1 :
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
                    shift = sample([0, 1, 3],1)[0]

            sel = randint(0, len(candidate) - 1)
            change_shift(schedule, nurse, day, shift)
            change_shift(schedule, candidate[sel], day, 2)


            fix(candidate[sel],day,2)

        elif next_shift == 2 and  day+1<int(len(schedule[0])/4)  and schedule[nurse][(day+1)*4] == 1 :
            day = day + 1
            shift = max_improve(nurse,day,0)

            candidate = []
            while True : #candidate can't be empty
                for i in range(len(schedule)) :
                    if schedule[i][day*4+shift] == 1 :
                        candidate.append(i)
                if len(candidate) > 0 :
                    break
                else :
                    shift = sample([1,2,3],1)[0]

            sel = randint(0,len(candidate)-1)
            change_shift(schedule,nurse,day,shift)
            change_shift(schedule,candidate[sel],day,0)

            fix(candidate[sel],day,0)


    """ --------------------start local search------------------------------- """
    # print("Local search")
    for repeat_time in range(10): #repeat time
        day = find_maxColumn()
        # print('day',day)
        better = improve(day)
        # print(improve)
        for i in [2,3] :
            for nurse_index in better[i] :
                # print(nurse_index,day)
                swap_shift(nurse_index,day)
        individual.schedule = schedule




if __name__ == "__main__" :
    dir = './data/1.nsp'
    data = open(dir,'r')
    schedule = [[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0],
                [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
                [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
                [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
                [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]]
    test = GA.GA(dir,1)

    test.chromosomes[0].schedule = schedule
    test.chromosomes[0].fitness = test.chromosomes[0].cal_fitness()
    print(test.chromosomes[0].isFeasible())
    print(test.chromosomes[0].fitness)
    trans = test.chromosomes[0].transform(schedule)
    for i in trans :
        print(i)

    local_search(test.chromosomes[0])


    test.chromosomes[0].fitness = test.chromosomes[0].cal_fitness()
    print(test.chromosomes[0].fitness)
    print(test.chromosomes[0].isFeasible())
    trans = test.chromosomes[0].transform(schedule)
    for i in trans:
        print(i)