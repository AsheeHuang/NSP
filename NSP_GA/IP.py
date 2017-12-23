from gurobipy import *

def read_data(dir):
    data = open(dir, 'r')
    data = data.read().split('\n')
    data = list(filter(lambda a: a != '', data))

    for i in range(len(data)):
        data[i] = data[i].split('\t')
        data[i] = list(filter(lambda a: a != '', data[i]))
        data[i] = list(map(int, data[i]))
    # set (I,K,S)
    nurse_num = int(data[0][0])
    day_num = int(data[0][1])
    shift_num = int(data[0][2])

    # read requirement matrix
    requirement = []
    for i in range(day_num):
        requirement.append(data[1 + i])
    # set preference matrix
    preference = []
    for i in range(nurse_num):
        preference.append(data[1 +day_num + i])

    return requirement,preference

if __name__ == "__main__" :
    dir = './data/60.nsp'
    demand,preference = read_data(dir)
    data = open(dir,'r').read().split('\n')[0].split('\t')
    nurse_num,day_num,shift_num = int(data[0]),int(data[1]),int(data[2])
    try :
        m = Model()

        M = nurse_num*10 #bigM
        penalty = [10,20]

        #set Variable
        """Decision Variable"""
        x = m.addVars(nurse_num,day_num,shift_num,vtype = GRB.BINARY,name = 'x')
        """Artificial Variable"""
        y = m.addVars(nurse_num,day_num-2,vtype= GRB.BINARY,name = 'y')
        z = m.addVars(nurse_num,day_num-6,vtype=GRB.BINARY,name = 'z')


        #setObjective
        expr1 = LinExpr()
        expr2 = LinExpr()
        expr3 = LinExpr()
        for i in range(nurse_num):
            for j in range(day_num):
                for k in range(shift_num):
                    expr1.add(x[i,j,k],pow(preference[i][j*shift_num+k],2))

        for i in range(nurse_num) :
            for j in range(day_num-2):
                expr2.add(y[i,j],1)

        for i in range(nurse_num) :
            for j in range(day_num-6):
                expr3.add(z[i,j],1)

        m.setObjective(expr1 + expr2 * penalty[0] + expr3 * penalty[1] ,GRB.MINIMIZE)

        #set Constraints
        """Hard Constraint"""
        for i in range(nurse_num) :
            for j in range(day_num) :
                expr = LinExpr()
                for k in range(shift_num) :
                    expr.add(x[i,j,k],1)
                m.addConstr(expr,GRB.EQUAL,1,'c0')
        for j in range(day_num) :
            for k in range(shift_num) :
                expr = LinExpr()
                for i in range(nurse_num) :
                    expr.add(x[i,j,k],1)
                m.addConstr(expr >= demand[j][k],'c1')
        for i in range(nurse_num) :
            for j in range(day_num-1) :
                m.addConstr(x[i,j,2]+x[i,j+1,0]<=1,'c2')


        """Soft Constraint"""

        #Continuously not work for three days
        for i in range(nurse_num) :
            for j in range(day_num-2) :
                m.addConstr(x[i,j,3]+x[i,j+1,3]+x[i,j+2,3]-2 <= y[i,j]*M)

        #Continuously work for 7 days
        for i in range(nurse_num) :
            for j in range(day_num-6):
                m.addConstr(x[i,j,3]+x[i,j+1,3]+x[i,j+2,3]+x[i,j+3,3]+x[i,j+4,3]+x[i,j+5,3]+x[i,j+6,3]-1 >= z[i,j]*(-M))

        for i in range(nurse_num) :
            for j in range(day_num-2) :
                m.addConstr(x[i,j,2]+x[i, j+1, 2] + x[i, j+2, 2] <= 2, 'c5')



        # for i in range(nurse_num):
        #     for j in range(day_num - 2):
        #         m.addConstr(x[i, j, 3] + x[i, j + 1, 3] + x[i, j + 2, 3] <= 2, 'c3')
        # for i in range(nurse_num) :
        #     for j in range(day_num-6) :
        #         m.addConstr(x[i,j,3]+x[i,j+1,3]+x[i,j+2,3]+x[i,j+3,3]+x[i,j+4,3]+x[i,j+5,3]+x[i,j+6,3] >= 1,'c4')
        #
        # for i in range(nurse_num) :
        #     for j in range(day_num-2) :
        #         m.addConstr(x[i, j, 2] + x[i, j+1, 2] + x[i, j+2, 2] <= 2, 'c5')
        #
        for j in range(day_num) :
            for k in range(shift_num-1) :
                expr = LinExpr()
                for i in range(nurse_num):
                    expr.add(x[i, j, k], 1)
                m.addConstr(expr, GRB.EQUAL, demand[j][k], 'c6')

        m.optimize()

        sol = [[-1]*day_num]*nurse_num

        for i in range(nurse_num) :
            print('[', end='')
            for j in range(day_num) :
                for k in range(shift_num) :
                    if x[i,j,k].getAttr('X') == 1 :
                        print(k,end = ', ')
            print(']')
        y_sum,z_sum = 0,0
        for i in range(nurse_num) :
            for j in range(day_num-2) :
                if y[i,j].getAttr('X') == 1 :
                    y_sum += 1
        for i in range(nurse_num) :
            for j in range(day_num-6) :
                if z[i,j].getAttr('X') == 1 :
                    z_sum += 1

        print(y_sum,z_sum)

    except GurobiError as e :
        print(e)
