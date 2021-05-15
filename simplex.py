# Jyoti Yadav's assignment
# Implementation of the Simplex algorithm with the below problem statement, made as project for the
# combinatorial and decision making course's second module taught by Vittorio Maniezzo

'''
A manufacturer company produces wooden tables and chairs ,they have only two resources wood(board feet) and labor
It takes 30bf of wood to make a table and 20 bf of wood to make a chair with the total consumption of wood as 300 bf
It takes 5 hours of labour to make a table and 10 hours of labour to make a chair with the total of 110 hours of labor availability
The unit profit for tables is $6 and for chair is $8
And the objective of the company is to get the maximum increase in profit
Here X1 and X2 are variables for tables and chairs

Maximize        6X1+8X2         (objective function)
Constraint      30X1+20X2<=300  (wood constraint: 300bf available)
                5X1+10X2<=110   (labor constraint:110 hours available)
                X1,X2>=0
'''

import numpy as np
from fractions import Fraction
import matplotlib.pyplot as plt

def printConsole():
    print("Bm \tCb \tSol \tX1 \tX2 \tX3 \tX4")
    for row in table:
        for i in row:
            print(Fraction(str(i)).limit_denominator(100), end ='\t')
        print()
    print()

def plot():
    x1 = np.linspace(0, 30, 1000)
    x2 = np.linspace(0, 30, 1000)
    # plot
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 8)
    # draw constraints
    plt.plot(x1, (300-(30*(x1)))/20, label=r'$30x1 + 20x2 \leq 300$') # constraint 1
    plt.plot(x1, (110 - (5*x1))/10, label=r'$5x1 + 10x2 \leq 110$') # constraint 2
    plt.axvline(0, color='g', label=r'$x1 \geq 0$') # constraint 3
    plt.axhline(0, color='r', label=r'$x2 \geq 0$') # constraint 4
    plt.xlim((0, 25))
    plt.ylim((0, 30))
    plt.xlabel(r'Number of Tables ($x1$)')
    plt.ylabel(r'Number of chairs ($x2$)')
    y=np.minimum((300-(30*(x1)))/20,(110 - (5*x1))/10)
    # fill in the fesaible region
    plt.fill_between(x1,y, where=x1 >= 0,color='green', alpha=0.25)
    plt.legend(bbox_to_anchor=(1, 1), loc=1, borderaxespad=0.)
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    x0 = [4]
    y0 = [9]
    plt.plot(x0, y0,marker='o',ms=10,mfc='r')
    plt.text(4,9,'   (4,9)')
    plt.show()


if __name__=="__main__":
    print("\n A simplex Tableau method : Production of wooden tables and chairs \n\n")

# Taking the number of inputs as coefficient
constraints=np.array([[30,20,1,0],[5,10,0,1]])
resources=np.array([300,110])
objectiveFunction=([6,8,0,0])
constraintBasic = np.array(objectiveFunction[3])
basicMix=np.array([[3],[4]])
print("basicMix",basicMix)
constraintBasic = np.vstack((constraintBasic, objectiveFunction[2]))
noOfResources = np.transpose([resources])
table=np.hstack((basicMix,constraintBasic))
table = np.hstack((table, noOfResources))
table = np.hstack((table, constraints))
table = np.array(table, dtype ='float')
print(table,"\n")


minimum=0
print("Table at iteration = 0")
printConsole()
# when optimality reached it will be made 1
reach = 0
itr = 1
unbound = 0
alt = 0

while reach == 0:
    print("Iteration: ", end =' ')
    print(itr)
    printConsole()

    # calculate Relative profits-> cj - zj for non-basics
    i = 0
    Improvement = []
    while i<len(constraints[0]):
        Improvement.append(objectiveFunction[i] - np.sum(table[:, 1]*table[:, 3 + i]))
        #print("rel_prof",rel_prof)
        i = i + 1

    print("Improvement in  profit: ", end =" ")
    for prof in Improvement:
        print(Fraction(str(prof)).limit_denominator(100), end =", ")
    print()
    i = 0

    b_var = table[:, 0]
    #print("b_var",b_var)
    # checking for alternate solution
    #print("constraints[0]",constraints[0])
    while i<len(constraints[0]):
        j = 0
        present = 0
        while j<len(b_var):
            if int(b_var[j]) == i:
                #print("b_var[j]",b_var[j])
                present = 1
                break;
            j+= 1
        if present == 0:
            if Improvement[i] == 0:
                #print("rel_prof[i]",rel_prof[i])
                alternate = 1
                print("Case of Alternate found")
                # print(i, end =" ")
        i+= 1
    print()
    flag = 0
    for profit in Improvement:
        if profit>0:
            flag = 1
            break
        # if all relative profits <= 0
    if flag == 0:
        print("All profits are <= 0, optimality reached")
        reach = 1
        break

    # kth var will enter the basis
    k = Improvement.index(max(Improvement))
    minimum = 99999
    i = 0;
    r = -1
    # exchange  ratio test (only positive values)
    while i<len(table):
        if (table[:, 2][i]>0 and table[:, 3 + k][i]>0):
            val = table[:, 2][i]/table[:, 3 + k][i]
            if val<minimum:
                minimum = val
                r = i     # leaving variable
        i+= 1

    # if no exchange ratio test was performed
    if r ==-1:
        unbound = 1
        print("Case of Unbounded")
        break
    print("pivot element index:", end =' ')
    print(np.array([r, 3 + k]))

    pivot = table[r][3 + k]
    print("pivot element: ", end =" ")
    print(Fraction(pivot).limit_denominator(100))

    # perform row operations
    # divide the pivot row with the pivot element
    table[r, 2:len(table[0])] = table[
            r, 2:len(table[0])] / pivot

    # do row operation on other rows
    i = 0
    while i<len(table):
        if i != r:
            table[i, 2:len(table[0])] = table[i,
                 2:len(table[0])] - table[i][3 + k] * table[r, 2:len(table[0])]
        i += 1


    # assign the new basic variable
    table[r][0] = k
    table[r][1] = objectiveFunction[k]

    print()
    print()
    itr+= 1
print()

if unbound == 1:
    print("UNBOUNDED Solution")
    exit()
if alt == 1:
    print("optimal table:")

printConsole()
print("Maximum Profit: ", end =" ")

basis = []
i = 0
sum = 0
while i<len(table):
    sum += objectiveFunction[int(table[i][0])]*table[i][2]
    temp = "x"+str(int(table[i][0])+1)
    basis.append(temp)
    i+= 1

if minimum == 1:
    print(-Fraction(str(sum)).limit_denominator(100),"\n")
else:
    print(Fraction(str(sum)).limit_denominator(100),"\n")

print("*********************Visualization*****************************")

plot()