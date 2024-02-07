
import pyautogui
import time
import random
from PIL import ImageGrab
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'D:\Alkalmazasok\Tesseract\tesseract.exe'

# Példa koordináták
square_x, square_y, square_width, square_height = 20, 290, 40, 30

# Képernyőrészlet elkapása a négyzet körül
screenshot = ImageGrab.grab(bbox=(square_x, square_y, square_x + square_width, square_y + square_height))

# Felismerés a Tesseract OCR használatával
recognized_text = pytesseract.image_to_string(screenshot, config='--psm 6 --oem 3 outputbase digits')

if recognized_text == "":
    # Példa koordináták
    square_x, square_y, square_width, square_height = 20, 290, 40, 30

    # Képernyőrészlet elkapása a négyzet körül
    screenshot = ImageGrab.grab(bbox=(square_x, square_y, square_x + square_width, square_y + square_height))

    # Felismerés a Tesseract OCR használatával
    recognized_text = pytesseract.image_to_string(screenshot, config='--psm 6 --oem 3 outputbase digits')
    

# pyautogui.moveTo(x=25, y=290, duration=1)
# time.sleep(1)
# pyautogui.moveTo(x=50, y=320, duration=1)

time.sleep(1)

# Kiíratás az eredményről
print("Felismerés eredménye:", recognized_text)
#     # time.sleep(0.2)
# pyautogui.click(x=130, y=500)
# pyautogui.moveTo(x=280, y=980, duration=0)

