import random


MAX_X = 250
MAX_Y = 800

starting_xy = [0,0]

for _ in range(10):

    first_xy = [random.randint(-250, 250), random.randint(0, 800)]

    vector = [first_xy[0]-starting_xy[0], first_xy[1]-starting_xy[1]]

    x_add = 1
    y_add = 1

    if vector[0] >= 0 : x_add = 1 
    else: x_add = -1

    while vector[1] > 0:
        if vector[0] == MAX_X or vector[0] == -MAX_X:
            x_add = -x_add
            print(vector)
            print(x_add)
        if vector[1] == MAX_Y or vector[1] == -MAX_Y:
            y_add = -y_add
            print(vector)
            print(y_add)

        vector = [vector[0]+x_add, vector[1]+y_add]

    starting_xy = vector
    print(starting_xy)