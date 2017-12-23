from ortools.constraint_solver import pywrapcp
from IP import read_data
if __name__ == '__main__' :
    dir = './data/1.nsp'
    demand,preference = read_data(dir)
    data = open(dir, 'r').read().split('\n')[0].split('\t')
    nurse_num, day_num, shift_num = int(data[0]), int(data[1]), int(data[2])

    solver =pywrapcp.Solver('NSP')

    shift = [[] for i in range(nurse_num)]
    for i in range(nurse_num) :
        shift[i] = [solver.IntVar(0,shift_num-1,'x%i%i' %(i,j)) for j in range(day_num)]
    