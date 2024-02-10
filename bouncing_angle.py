import random


max_x = 250
max_y = 800

starting_xy = [0,0]

for _ in range(10):

    first_xy = [random.randint(-250, 250), random.randint(1, 20)]

    vector = [first_xy[0]-starting_xy[0], first_xy[1]-starting_xy[1]]

    if(-max_x > vector[0]) or (vector[0] > max_x):
        continue
    
    x_add = 1
    y_add = 1
    if vector[0] < 0:
        x_add = -1

    while vector[1] > 0:

        if vector[0] == max_x or vector[0] == -max_x:
            x_add = -x_add

        if vector[1] == max_y:
            y_add = -y_add

        vector = [vector[0] + x_add, vector[1] + y_add]

    starting_xy = vector
    
    