
import pyautogui
import time
import random
from PIL import ImageGrab
import pytesseract
import cv2
import numpy as np

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

    starting_xy = vector
    
def get_squares_triangles():
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

#Maximumok
max_x = 250
max_y = 800

# Négyzetek és háromszögek tárolására szolgáló listák
squares = []
triangles = []

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
    
#Kezdőpozíció
starting_xy = [0,0]

while(text != "CONTINUE"):
    
    #Minden kör után legyen üres
    squares = []
    triangles = []
    
    #Négyzetek, h-szögek keresése
    get_squares_triangles()
    
    num = random.randint(5,555)
    pyautogui.click(x=num, y=865)
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
    
    #Befejezés ha leértek a labdák és COUNTINUE megjelenik
    # pyautogui.moveTo(95, 675, 1)
    # pyautogui.moveTo(95+175, 675+45, 1)
    if step == -1:
        text = recognize_text(95, 675, 175, 45, "text").strip()
    else:
        text = recognize_text(95, 775, 175, 45, "text").strip()
    