import cv2
import numpy as np
from PIL import ImageGrab
import pytesseract
import pyautogui

# Kép beolvasása
# Példa koordináták
square_x, square_y, square_width, square_height = 5, 270, 555, 570

def findOne():
    pytesseract.pytesseract.tesseract_cmd = r'D:\Alkalmazasok\Tesseract\tesseract.exe'
    
    # pyautogui.moveTo(x=square_x, y=square_y, duration=0.2)
    # pyautogui.moveTo(x=square_x+square_width, y=square_y+square_height, duration=0.2)

    # Képernyőrészlet elkapása a négyzet körül
    screenshot = ImageGrab.grab(bbox=(square_x, square_y, square_x + square_width, square_y + square_height))

    # Felismerés a Tesseract OCR használatával
    recognized_text = pytesseract.image_to_string(screenshot, config='--psm 6 --oem 3 outputbase digits')

    print(recognized_text)
    
# Képernyőrészlet elkapása a négyzet körül
screenshot = ImageGrab.grab(bbox=(square_x, square_y, square_x + square_width, square_y + square_height))

image_np = np.array(screenshot)

# Szürkeárnyalat konverzió
gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

# Éldetektálás
edges = cv2.Canny(gray, 50, 150)

# Kontúrkeresés
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Négyzetek és háromszögek tárolására szolgáló listák
squares = []
triangles = []

# Kontúrok ellenőrzése
for contour in contours:
    # Kontúr hosszúságának meghatározása
    peri = cv2.arcLength(contour, True)

    # Kontúr közelítése egy sokszöggel
    approx = cv2.approxPolyDP(contour, 0.04 * peri, True)

    square_x, square_y, square_width, square_height = 5, 270, 555, 570
    
    # Közelített alakzat vizsgálata
    if len(approx) == 4 and peri >= 60:
        square_x, square_y, square_width, square_height = square_x+approx[0][0][0]+5, square_y+approx[0][0][1]+10, 45, 35
        findOne()
        squares.append(approx)
    elif len(approx) == 3 and peri >= 35:
        square_x, square_y, square_width, square_height = square_x+approx[0][0][0], square_y+approx[1][0][1]-20, 45, 20
        findOne()
        triangles.append(approx)
        
print(triangles)
    
# Eredeti képen való megjelenítés
cv2.drawContours(image_np, squares, -1, (0, 255, 0), 2)
cv2.drawContours(image_np, triangles, -1, (0, 0, 255), 2)

# Képek megjelenítése
cv2.imshow("Squares and Triangles", image_np)
cv2.waitKey(0)
cv2.destroyAllWindows()
