import random
def Crossover(fParent,sParent):

    child = [[fParent[i][j] for j in range (0,len(fParent[0]))]for i in range(0,len(fParent))]
    x = random.randint(1,int(len(fParent[0])/4)-1)
    #print (x)
    for i in range(0,len(sParent)):
        for j in range(x*4, len(sParent[0])):
            child[i][j] = sParent[i][j]

    #print (child)
    return child

#Crossover(None,None)