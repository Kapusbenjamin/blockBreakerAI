
import pyautogui
import time
import random
from PIL import ImageGrab
import pytesseract

def recognize_text():
    pytesseract.pytesseract.tesseract_cmd = r'D:\Alkalmazasok\Tesseract\tesseract.exe'

    # Példa koordináták
    monitor_x, monitor_y, width, height = 95, 675, 175, 45

    # Képernyőrészlet elkapása a négyzet körül
    screenshot = ImageGrab.grab(bbox=(monitor_x, monitor_y, monitor_x + width, monitor_y + height))

    # Felismerés a Tesseract OCR használatával
    recognized_text = pytesseract.image_to_string(screenshot, config='--psm 6 --oem 3')

    pyautogui.moveTo(x=monitor_x, y=monitor_y, duration=1)
    pyautogui.moveTo(x=monitor_x+width, y=monitor_y+height, duration=1)

    time.sleep(1)

    # Kiíratás az eredményről
    print("Felismerés eredménye:", recognized_text)
    return(recognized_text)


# Példa koordináták
monitor_x, monitor_y, width, height = 95, 675, 175, 45
text = ""

while(text != "CONTINUE"):
    
    num = random.randint(5,555)
    pyautogui.click(x=num, y=865)
    
    # Várakozás egy kicsit
    time.sleep(1)
    
    text = recognize_text().strip()

