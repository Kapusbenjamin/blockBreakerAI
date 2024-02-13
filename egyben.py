
import pyautogui
import time
import random
from PIL import ImageGrab
import pytesseract
import cv2
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

class DeepQNetwork:
    def __init__(self, state_size, action_size):
        self.model = self.build_model(state_size, action_size)

    def build_model(self, state_size, action_size):
        model = Sequential()
        model.add(Dense(24, input_dim=state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=0.001))
        return model

class Agent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.gamma = 0.95  # discount factor
        self.epsilon = 1.0  # exploration rate
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.model = DeepQNetwork(state_size, action_size)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return 
        q_values = self.model.model.predict(state)
        return np.argmax(q_values[0])

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = np.random.choice(self.memory, batch_size, replace=False)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.model.predict(next_state)[0]))
            target_f = self.model.model.predict(state)
            target_f[0][action] = target
            self.model.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


def recognize_text(monitor_x, monitor_y, width, height, type="num"):
    pytesseract.pytesseract.tesseract_cmd = r'D:\Alkalmazasok\Tesseract\tesseract.exe'

    # Képernyőrészlet elkapása a négyzet körül
    screenshot = ImageGrab.grab(bbox=(monitor_x, monitor_y, monitor_x + width, monitor_y + height))

    recognized_text = ""
    # Felismerés a Tesseract OCR használatával
    if type == "text":
        recognized_text = pytesseract.image_to_string(screenshot, config='--psm 6 --oem 3')
    elif type == "num":
        recognized_text = pytesseract.image_to_string(screenshot, config='--psm 1 --oem 3 outputbase digits')
    elif type == "classic":
        recognized_text = pytesseract.image_to_string(screenshot, config='--psm 6 --oem 3 outputbase digits')
    
    time.sleep(1)

    # Kiíratás az eredményről
    print("Felismerés eredménye:", recognized_text)
    return(recognized_text)

def bouncing():
    first_xy, vector
    
    while(-max_x <= vector[0]) and (vector[0] <= max_x):
        first_xy = [random.randint(-max_x, max_x), random.randint(5, 20)]

        vector = [first_xy[0]-starting_xy[0], first_xy[1]-starting_xy[1]]

    x_add = 1
    y_add = 1
    if vector[0] < 0:
        x_add = -1

    while vector[1] > 0:
        if vector[0] == max_x or vector[0] == -max_x:
            x_add = -x_add

        if vector[1] == max_y:
            y_add = -y_add

        for sq in squares:
            x = [cords[0] for cords in sq]
            y = [cords[1] for cords in sq]
            if(vector[0] in range(min(x), max(x)) and vector[1] in range(min(y), max(y))):
                if((vector[0] in range(min(x),max(x)))):
                    x_add = -x_add
                    print(vector, "x")
                if((vector[1] in range(min(y), max(y)))):
                    y_add = -y_add
                    print(vector, "y")
        
        vector = [vector[0] + x_add, vector[1] + y_add]

    return np.array(vector)
    
def get_squares_triangles():
    squares = []
    triangles = []
    
    # Képernyőrészlet elkapása a négyzet körül
    square_x, square_y, square_width, square_height = 5, 270, 555, 570
    screenshot = ImageGrab.grab(bbox=(square_x, square_y, square_x + square_width, square_y + square_height))

    image_np = np.array(screenshot)

    # Szürkeárnyalat konverzió
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

    # Éldetektálás
    edges = cv2.Canny(gray, 50, 150)

    # Kontúrkeresés
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Kontúrok ellenőrzése
    for contour in contours:
        # Kontúr hosszúságának meghatározása
        peri = cv2.arcLength(contour, True)

        # Kontúr közelítése egy sokszöggel
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        square_x, square_y, square_width, square_height = 5, 270, 555, 570
        
        # Közelített alakzat vizsgálata
        if len(approx) == 4 and peri >= 70:
            square_x, square_y, square_width, square_height = square_x+approx[0][0][0]+5, square_y+approx[0][0][1]+10, 45, 35
            # recognize_text(square_x, square_y, square_width, square_height)
            squares.append(approx)
        elif len(approx) == 3 and peri >= 45:
            square_x, square_y, square_width, square_height = square_x+approx[0][0][0], square_y+approx[1][0][1]-20, 45, 20
            # recognize_text(square_x, square_y, square_width, square_height)
            triangles.append(approx)
          
    # Eredeti képen való megjelenítés
    cv2.drawContours(image_np, squares, -1, (0, 255, 0), 2)
    cv2.drawContours(image_np, triangles, -1, (0, 0, 255), 2)

    # Képek megjelenítése
    cv2.imshow("Squares and Triangles", image_np)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
    
    return squares, triangles

def calculate_reward():
    #Négyzetek, h-szögek keresése
    new_squares, new_triangles = get_squares_triangles()

    if(len(squares)+len(triangles) > len(new_squares)+len(new_triangles)):
        reward = ((len(squares)+len(triangles))-(len(new_squares)+len(new_triangles)))*100
        squares = new_squares
        triangles = new_triangles
        return reward-100
    else:
        squares = new_squares
        triangles = new_triangles
        return -100

def check_game_over():
    #Befejezés ha leértek a labdák és COUNTINUE megjelenik
    # pyautogui.moveTo(95, 675, 1)
    # pyautogui.moveTo(95+175, 675+45, 1)
    if step == -1:
        text = recognize_text(95, 675, 175, 45, "text").strip()
    else:
        text = recognize_text(95, 775, 175, 45, "text").strip()
    
    return text == "CONTINUE"

#Maximumok
max_x = 250
max_y = 800

#Felismert szöveg a befejezéshez
text = ""

#Felismert sorok száma a kezdéshez (felül. pl.: line 26)
rows = 0
#Lépésa módtól függően. Ha classic akkor +1 egyébként -1
step = -1
try:
    rows = int(recognize_text(280, 155, 50, 35).strip())
except:
    rows = 1
    step = 1
    
# Játék ügynök létrehozása
agent = Agent(state_size=2, action_size=1)

#Kezdőpozíció
starting_xy = np.array([[0, 0]])

# Négyzetek és háromszögek tárolására szolgáló listák
squares = []
triangles = []

#Négyzetek, h-szögek keresése
squares, triangles = get_squares_triangles()

total_reward = 0

for episode in range(1000):
    
    x_num = random.randint(5,555)
    y_num = random.randint(5,800)
    action = np.array(x_num, y_num)
    pyautogui.click(x=x_num, y=y_num)
    pyautogui.moveTo(250,500)

    remaining_rows_now = 999
    #Addig olvassa a számot, míg nem csökken a sorok száma
    while(rows+step != remaining_rows_now):
        if step == -1:
            remaining_rows_now = int(recognize_text(280, 155, 50, 35).strip())
        else:
            remaining_rows_now = int(recognize_text(230, 140, 245, 60, "classic").strip())
    
    #Sorok számának felülírása    
    rows = remaining_rows_now
    
     # Jutalom és következő állapot számítása
    reward = calculate_reward()
    total_reward += reward
    done = check_game_over()  # Ellenőrizd, hogy a játék végetért-e

    # Ügynök tanulása és lépés a következő állapotba
    next_state = bouncing()
    agent.remember(starting_xy, action, reward, next_state, done)
    agent.replay(batch_size=32)

    if done:
        print("Epizód: {}/{}, Jutalom: {}".format(episode, 1000, total_reward))
        break
