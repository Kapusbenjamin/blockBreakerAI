import random

squares = [[10,5,5,5], [20,5,5,5]]


max_x = 30
max_y = 15

starting_xy = [0,0]

for _ in range(5):

    first_xy = [random.randint(-30, 30), random.randint(1, 5)]

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

        for cord in squares:
            if(vector[0] in range(cord[0], cord[0]+cord[2]) and vector[1] in range(cord[1], cord[1]+cord[3])):
                if((vector[0] == cord[0]) or vector[0] == cord[0]+cord[2]):
                    x_add = -x_add
                    print(vector, "x")
                if((vector[1] == cord[1]) or vector[1] == cord[1]+cord[3]):
                    y_add = -y_add
                    print(vector, "y")
        
        vector = [vector[0] + x_add, vector[1] + y_add]

    starting_xy = vector
    
    