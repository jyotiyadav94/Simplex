# Jyoti Yadav assignment
# Implementation of the Simplex algorithm with the below problem statement, made as project for the
# combinatorial and decision making course's second module taught by Vittorio Maniezzo

'''
A manufacturer company produces wooden tables and chairs ,they have only two resources wood(board feet) and labor
It takes 30bf of wood to make a table and 20 bf of wood to make a chair with the total consumption of wood as 300 bf
It takes 5 hours of labour to make a table and 10 hours of about to make a chair with the total of 110 hours of labor availability
The unit profit for tables is $6 and for chair is $8
And the objective of the comp   any is to get the maximum increase in profit
Here X1 and X2 variables are tables and chairs

Maximize        Z=6X1+8X2       (objective function)
Constraint      30X1+20X2<= 300 (wood constraint: 300bf available)
                5X1+10X2<=110   (labor constraint:110 hours available)
                X1,X2>=0
'''

import numpy as np
from fractions import Fraction
import matplotlib.pyplot as plt

print("\n A simplex Tableau method : Production of wooden tables and chairs \n\n")

# Taking the inputs

#It stores all the coefficients of the constraints and the slack variables
constraints=np.array([[30,20,1,0],[5,10,0,1]])

#It stores all the coefficients of the resources
resources=np.array([300,110])

#It stores all the coefficients of the objective function
objective_function=([6,8,0,0])

# It will contain the basic variables that make identity matrix
constraint_basic = np.array(objective_function[3])
basic=np.array([[3],[2]])

inital_basic=np.array([[0],[0]])
constraint_basic = np.vstack((constraint_basic, objective_function[2]))

no_of_resources = np.transpose([resources])

table=np.hstack((inital_basic,constraint_basic))

table = np.hstack((table, no_of_resources))

table = np.hstack((table, constraints))

table = np.array(table, dtype ='float')
print(table,"\n")

min=0

print("Table at iteration = 0")
print("Bm \tCb \tSol \tX1 \tX2 \tSw \tSl")
for row in table:
    for el in row:
                # limit the denominator under 100
        print(Fraction(str(el)).limit_denominator(100), end ='\t')
    print()
print()
print(" ***************************************************************")

# when optimality reached it will be made 1
reached = 0
itr = 1
unbounded = 0
alternate = 0

while reached == 0:
    print("reached value =",reached)

    print("Iteration: ", end =' ')
    print(itr)
    print("Bm \tCb \tSol \tX1 \tX2 \tSw \tSl")
    for row in table:
        for el in row:
            print(Fraction(str(el)).limit_denominator(100), end ='\t')
        print()

    # calculate Relative profits-> cj - zj for non-basics
    i = 0
    rel_prof = []
    while i<len(constraints[0]):
        rel_prof.append(objective_function[i] - np.sum(table[:, 1]*table[:, 3 + i]))
        #print("rel_prof",rel_prof)
        i = i + 1

    print("rel profit: ", end =" ")
    for profit in rel_prof:
        print(Fraction(str(profit)).limit_denominator(100), end =", ")
    print()
    i = 0

    b_var = table[:, 0]
    #print("b_var",b_var)
    # checking for alternate solution
    print("constraints[0]",constraints[0])
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
            if rel_prof[i] == 0:
                #print("rel_prof[i]",rel_prof[i])
                alternate = 1
                #print("Case of Alternate found")
                # print(i, end =" ")
        i+= 1
    print()
    flag = 0
    for profit in rel_prof:
        if profit>0:
            flag = 1
            break
        # if all relative profits <= 0
    if flag == 0:
        print("All profits are <= 0, optimality reached")
        reached = 1
        break

    # kth var will enter the basis
    k = rel_prof.index(max(rel_prof))
    min = 99999
    i = 0;
    r = -1
    # min ratio test (only positive values)
    while i<len(table):
        if (table[:, 2][i]>0 and table[:, 3 + k][i]>0):
            val = table[:, 2][i]/table[:, 3 + k][i]
            if val<min:
                min = val
                r = i     # leaving variable
        i+= 1

        # if no min ratio test was performed
    if r ==-1:
        unbounded = 1
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
    table[r][1] = objective_function[k]

    print()
    print()
    itr+= 1


print()

print("***************************************************************")
if unbounded == 1:
    print("UNBOUNDED LPP")
    exit()
if alternate == 1:
    print("ALTERNATE Solution")

print("optimal table:")
print("Bm \tCb \tSol \tX1 \tX2 \tSw \tSl")
for row in table:
    for el in row:
        print(Fraction(str(el)).limit_denominator(100), end ='\t')
    print()
print()
print("value of Z at optimality: ", end =" ")

basis = []
i = 0
sum = 0
while i<len(table):
    sum += objective_function[int(table[i][0])]*table[i][2]
    temp = "x"+str(int(table[i][0])+1)
    basis.append(temp)
    i+= 1

if min == 1:
    print(-Fraction(str(sum)).limit_denominator(100))
else:
    print(Fraction(str(sum)).limit_denominator(100))
print("\n")


x_1 = np.linspace(0, 30, 1000)
x_2 = np.linspace(0, 30, 1000)

# plot
fig, ax = plt.subplots()
fig.set_size_inches(12, 8)

# draw constraints
plt.axvline(0, color='g', label=r'$x_1 \geq 0$') # constraint 1
plt.axhline(0, color='r', label=r'$x_2 \geq 0$') # constraint 2
plt.plot(x_1, (300-(30*(x_1)))/20, label=r'$30x_1 + 20x_2 \leq 300$') # constraint 3
plt.plot(x_1, (110 - (5*x_1))/10, label=r'$5x_1 + 10x_2 \leq 110$') # constraint 4


plt.xlim((0, 25))
plt.ylim((0, 30))
plt.xlabel(r'Number of Tables ($x_1$)')
plt.ylabel(r'Number of chairs ($x_2$)')

y=np.minimum((300-(30*(x_1)))/20,(110 - (5*x_1))/10)
# fill in the fesaible region
plt.fill_between(x_1,y, where=x_1 >= 0,color='green', alpha=0.25)
plt.legend(bbox_to_anchor=(1, 1), loc=1, borderaxespad=0.)

# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.show()