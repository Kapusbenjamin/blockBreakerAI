
import pyautogui
import time
import random
from PIL import ImageGrab
import pytesseract
import cv2
import numpy as np

# pytesseract.pytesseract.tesseract_cmd = r'D:\Alkalmazasok\Tesseract\tesseract.exe'

# # Példa koordináták
# square_x, square_y, square_width, square_height = 230, 140, 245, 60

# # pyautogui.moveTo(10, 845, 1)
# # pyautogui.moveTo(10+545, 845+35, 1)

# # Képernyőrészlet elkapása a négyzet körül
# screenshot = ImageGrab.grab(bbox=(square_x, square_y, square_x + square_width, square_y + square_height))

# # Felismerés a Tesseract OCR használatával
# recognized_text = pytesseract.image_to_string(screenshot, config='--psm 6 --oem 3 outputbase digits')

# # if recognized_text == "":
# #     # Példa koordináták
# #     square_x, square_y, square_width, square_height = 20, 290, 40, 30

# #     # Képernyőrészlet elkapása a négyzet körül
# #     screenshot = ImageGrab.grab(bbox=(square_x, square_y, square_x + square_width, square_y + square_height))

# #     # Felismerés a Tesseract OCR használatával
# #     recognized_text = pytesseract.image_to_string(screenshot, config='--psm 6 --oem 3 outputbase digits')
    

# # pyautogui.moveTo(x=25, y=290, duration=1)
# # time.sleep(1)
# # pyautogui.moveTo(x=50, y=320, duration=1)

# time.sleep(1)

# # Kiíratás az eredményről
# print("Felismerés eredménye:", recognized_text)
# #     # time.sleep(0.2)
# # pyautogui.click(x=130, y=500)
# # pyautogui.moveTo(x=280, y=980, duration=0)

def find_circle_center(target):
    # Általánosított Hough transzformáció használata kör detektálásához
    circles = cv2.HoughCircles(target, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=10, maxRadius=100)

    if circles is not None:
        # Az észlelt körök koordinátái
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center_x, center_y = int(i[0]+i[2]/2), i[1]
            return center_x, center_y

    return None

def capture_screen(region=(5, 855, 550, 890)):
    # Képernyőkép készítése a megadott régióban (x, y, width, height)
    screenshot = ImageGrab.grab(bbox=region)

    return screenshot

def main():
    # Képernyőkép készítése
    screenshot = capture_screen()

    # Képet NumPy tömbbé konvertáljuk
    target = np.array(screenshot)

    # Kép konvertálása szürkeárnyalatosra
    gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

    # Kör detektálása
    circle_center = find_circle_center(gray)

    if circle_center is not None:
        center_x, center_y = circle_center
        print(f'Kör középpontja: x={center_x}, y={center_y+855}')
        pyautogui.moveTo(x=center_x, y=center_y+855)
        
main()