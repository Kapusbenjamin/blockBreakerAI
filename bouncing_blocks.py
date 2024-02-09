import random

squares = [[10,5], [20,5]]


MAX_X = 30
MAX_Y = 15

starting_xy = [0,0]

for _ in range(1):

    first_xy = [random.randint(-30, 30), random.randint(0, 15)]

    vector = [first_xy[0]-starting_xy[0], first_xy[1]-starting_xy[1]]

    x_add = 1
    y_add = 1

    while vector[1] > 0:
        if vector[0] == MAX_X or vector[0] == -MAX_X:
            x_add = -x_add
            print("pálya", vector)
        if vector[1] == MAX_Y or vector[1] == -MAX_Y:
            y_add = -y_add
            print("pálya", vector)

        for cord in squares:
            if vector == cord:
                if vector[0] == cord[0]:
                    x_add = -x_add
                    print(vector)
                if vector[1] == cord[1]:
                    y_add = -y_add
                    print(vector)
            


        vector = [vector[0]+x_add, vector[1]+y_add]

    starting_xy = vector
    print(starting_xy)