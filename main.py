
import pyautogui
import time
import random
from PIL import ImageGrab
import pytesseract

def get_pixel_color(x, y):
    # Képernyőrészlet elkapása és a megadott pont színének lekérése
    screenshot = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))
    pixel_color = screenshot.getpixel((0, 0))
    return pixel_color

# Példa koordináták
# monitor_x, monitor_y = 280, 980
monitor_x, monitor_y = 513, 263
# pyautogui.moveTo(x=monitor_x, y=monitor_y, duration=1)

# Az első pont színének lekérése
color1 = (255,255,252)

while True:
    
    num = random.randint(5,555)
    pyautogui.click(x=num, y=865)
    
    # Várakozás egy kicsit
    time.sleep(1)

    # pytesseract.pytesseract.tesseract_cmd = r'D:\Alkalmazasok\Tesseract\tesseract.exe'

    # # Példa koordináták
    # square_x, square_y, square_width, square_height = 220, 180, 160, 30

    # # Képernyőrészlet elkapása a négyzet körül
    # screenshot = ImageGrab.grab(bbox=(square_x, square_y, square_x + square_width, square_y + square_height))

    # # Felismerés a Tesseract OCR használatával
    # recognized_text = pytesseract.image_to_string(screenshot, config='--psm 10 --oem 3 outputbase digits')

    # print(recognized_text)
    # A második pont színének lekérése
    color2 = get_pixel_color(monitor_x, monitor_y)

    # Feltétel: Ha két egymást követő szín különbözik, kilépés a ciklusból
    if color1 == color2:
        break

# A while ciklusból való kilépés utáni kód
print("A szín megváltozott.")




# pyautogui.moveTo(x=555, y=500, duration=1)

# for _ in range(20):
#     pyautogui.click(x=200, y=500)
#     time.sleep(2)