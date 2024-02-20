from Agent import *
import numpy as np
import tkinter as tk
from PIL import ImageGrab
import pytesseract
import cv2
import pyautogui
import time

class Jatek:
    def __init__(self):
        #Maximumok
        self.max_x = 250
        self.max_y = 800
            
        # Játék ügynök létrehozása
        self.agent = Agent(state_size=2*self.max_x, action_size=self.max_x*self.max_y, max_x=self.max_x, max_y=self.max_y)
        
        self.ertekAdas()

    def ertekAdas(self):
        #Felismert sorok száma a kezdéshez (felül. pl.: line 26)
        self.rows = 0
        #Lépés a módtól függően. Ha classic akkor +1 egyébként -1
        self.step = -1
        try:
            self.rows = int(self.recognize_text(280, 155, 50, 35).strip())
        except:
            self.rows = 1
            self.step = 1
            
        #Kezdőpozíció
        self.starting_xy = np.array([0, 0])

        # Négyzetek és háromszögek tárolására szolgáló listák
        self.squares = []
        self.triangles = []

        #Négyzetek, h-szögek keresése
        self.get_squares_triangles()

        self.total_reward = 0
        
        self.done = False

    def jatekmenet(self):
        #1000 jatek
        for episode in range(10):
        
            #1 jatek
            while(not self.done):
                
                action = self.agent.choose_action([*self.starting_xy, *self.squares, *self.triangles])
                time.sleep(1)
                #kattintás x=[5,550] y=[5,400]
                pyautogui.click(x=255+action[0], y=455+action[1])
                time.sleep(1)
                
                remaining_rows_now = 999
                #Addig olvassa a számot, míg nem csökken a sorok száma
                while(self.rows+self.step != remaining_rows_now):
                    if self.step == -1:
                        remaining_rows_now = int(self.recognize_text(280, 155, 50, 35).strip())
                    else:
                        remaining_rows_now = int((self.recognize_text(230, 140, 245, 60, "classic")).strip())
                
                #Sorok számának felülírása    
                self.rows = remaining_rows_now
                
                self.done = self.check_game_over()  # Ellenőrizd, hogy a játék végetért-e
                
                # Jutalom és következő állapot számítása
                if self.done:
                    reward = 1000
                else:
                    reward = self.calculate_reward()
                self.total_reward += reward
                print(reward)
                time.sleep(1)
                
                # Ügynök tanulása és lépés a következő állapotba
                #next_state = bouncing(starting_xy)
                old_state = np.array([*self.starting_xy, *self.squares, *self.triangles], dtype=object)
                self.get_squares_triangles()
                
                #Labdák (kezdőpozíció) keresése
                if self.done:
                    self.starting_xy = np.array([0,0])
                else:
                    x, y = self.get_circle()
                    self.starting_xy = np.array([x,y])
                    print(f"Kör: x={x}, y={y}")
                time.sleep(1)
                
                self.agent.remember(old_state, action, reward, np.array([*self.starting_xy, *self.squares, *self.triangles], dtype=object), self.done)
                self.agent.replay(batch_size=32)

                if self.done:
                    print("Epizód: {}/{}, Jutalom: {}".format(episode, 1000, self.total_reward))
                    
                    # Főablak létrehozása
                    root = tk.Tk()
                    root.title("Folytatás")

                    # Gomb létrehozása
                    button = tk.Button(root, text="Indítás", command=lambda: self.ertekAdas())
                    button.pack(pady=20)

                    # Főablak megjelenítése
                    root.mainloop()
     
    def get_squares_triangles(self, old=False):
        self.squares = []
        self.triangles = []
        
        # Képernyőrészlet elkapása a négyzet körül
        square_x, square_y, square_width, square_height = 5, 270, 555, 570

        if old:
            square_x, square_y, square_width, square_height = 5, 340, 555, 500

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
                self.squares.append(approx)
            elif len(approx) == 3 and peri >= 45:
                square_x, square_y, square_width, square_height = square_x+approx[0][0][0], square_y+approx[1][0][1]-20, 45, 20
                # recognize_text(square_x, square_y, square_width, square_height)
                self.triangles.append(approx)
            
        # Eredeti képen való megjelenítés
        cv2.drawContours(image_np, self.squares, -1, (0, 255, 0), 2)
        cv2.drawContours(image_np, self.triangles, -1, (0, 0, 255), 2)

        # Képek megjelenítése
        cv2.imshow("Squares and Triangles", image_np)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()

    def get_circle(self):
        # Képernyőkép készítése
        screenshot = ImageGrab.grab(bbox=(5, 855, 550, 890))
        
        # Képet NumPy tömbbé konvertáljuk
        target = np.array(screenshot)

        # Kép konvertálása szürkeárnyalatosra
        gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

        # Kör detektálása
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=10, maxRadius=100)

        while circles is None:
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=10, maxRadius=100)
            # Éldetektálás
            edges = cv2.Canny(gray, 50, 150)

            # Kontúrkeresés
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                return 0,0
        
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center_x, center_y = int(i[0]+i[2]/2), i[1]
            return center_x, center_y

    def calculate_reward(self):
        #Előző állapot
        old_squares = self.squares
        old_triangles = self.triangles
        
        #Négyzetek, h-szögek keresése
        self.get_squares_triangles(old=True)

        if(len(self.squares)+len(self.triangles) < len(old_squares)+len(old_triangles)):
            reward = ((len(old_squares)+len(old_triangles))-(len(self.squares)+len(self.triangles)))*100
            return reward+1000
        else:
            return 1000

    def check_game_over(self):
        #Befejezés ha leértek a labdák és COUNTINUE megjelenik
        # pyautogui.moveTo(95, 675, 1)
        # pyautogui.moveTo(95+175, 675+45, 1)
        if self.step == -1:
            text = self.recognize_text(95, 675, 175, 45, "text").strip()
        else:
            text = self.recognize_text(95, 775, 175, 45, "text").strip()
        
        return text == "CONTINUE"

    def recognize_text(self, monitor_x, monitor_y, width, height, type = "num"):
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
        
        # time.sleep(1)

        # Kiíratás az eredményről
        print("Felismerés eredménye:", recognized_text)
        return(recognized_text)

jatek = Jatek()
jatek.jatekmenet()
