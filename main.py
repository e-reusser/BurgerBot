import time
import numpy
from PIL import ImageGrab
from directKeys import click
import cv2
import os
import yaml

# Frame coordinates, thresholds, and delays and their mappings
# Can be found in config.yml
with open('config.yml') as f:
    configMap = yaml.safe_load(f)
FRAME_COORDS = [configMap['frameCaptureCoordinates']['pos1'][0], configMap['frameCaptureCoordinates']['pos1'][1], configMap['frameCaptureCoordinates']['pos2'][0], configMap['frameCaptureCoordinates']['pos2'][1]]
ITEM_THRESHOLD = configMap['itemThreshold']
SIZE_THRESHOLD = configMap['sizeThreshold']
CHEESE_THRESHOLD = configMap['cheeseThreshold']
BUTTON_DELAY = configMap['buttonDelay']
FRAME_DELAY = configMap['frameDelay']

# Button locations and their mappings
with open('buttonLocations.yml') as f:
    buttonMap = yaml.safe_load(f)
imageToButton = {
    "Cheese.png": buttonMap['buttons']['ingredients']['cheese'],
    "Cheese1.png": buttonMap['buttons']['ingredients']['cheese'],
    "Cheese2.png": buttonMap['buttons']['ingredients']['cheese'],
    "Drink.png": buttonMap['buttons']['secondary']['top'],
    "Fry.png": buttonMap['buttons']['secondary']['top'],
    "Juice.png": buttonMap['buttons']['secondary']['middle'],
    "Lettuce.png": buttonMap['buttons']['ingredients']['lettuce'],
    "Onion.png": buttonMap['buttons']['ingredients']['onion'],
    "Patty.png": buttonMap['buttons']['ingredients']['patty'],
    "Ring.png": buttonMap['buttons']['secondary']['bottom'],
    "Sticks.png": buttonMap['buttons']['secondary']['middle'],
    "Tomato.png": buttonMap['buttons']['ingredients']['tomato'],
    "Veggie.png": buttonMap['buttons']['ingredients']['veggie'],
    "Shake.png": buttonMap['buttons']['secondary']['bottom'],
    "Small.png": buttonMap['buttons']['secondary']['small'],
    "Medium.png": buttonMap['buttons']['secondary']['medium'],
    "Large.png": buttonMap['buttons']['secondary']['large'],
    "Sides": buttonMap['buttons']['menu']['sides'],
    "Drink": buttonMap['buttons']['menu']['drink'],
    "Done": buttonMap['buttons']['menu']['done'],
    "bottomBun": buttonMap['buttons']['ingredients']['bottomBun'],
    "topBun": buttonMap['buttons']['ingredients']['topBun']
}

# Loading images for both menu items and sizes
images = []
menuFileNames = []
menuFileCount = 0
for filename in os.listdir('images'):
    f = os.path.join('images', filename)
    if os.path.isfile(f):
        images.append(cv2.imread(os.path.join('images', filename), cv2.IMREAD_GRAYSCALE))
        menuFileNames.append(filename)
        menuFileCount += 1
print("Loaded " + format(menuFileCount) + " menu items.")

sizeImages = []
sizeNames = []
sizeCount = 0
for filename in os.listdir('sizes'):
    f = os.path.join('sizes', filename)
    if os.path.isfile(f):
        sizeImages.append(cv2.imread(os.path.join('sizes', filename), cv2.IMREAD_GRAYSCALE))
        sizeNames.append(filename)
        sizeCount += 1
print("Loaded " + format(sizeCount) + " sizes.")

def checkRange(pt, sizePt):
    return ((0 <= (sizePt[0] - pt[0]) <= 80) and (0 <= (sizePt[1] - pt[1]) <= 80))

def findItems(screen, images, order, sizes):
    i = 0
    cheeseCheck = False
    for image in images:
        res = cv2.matchTemplate(screen, image, cv2.TM_CCOEFF_NORMED)
        if ("Cheese" in menuFileNames[i]):
            threshold = CHEESE_THRESHOLD
        else:
            threshold = ITEM_THRESHOLD
        loc = numpy.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            j = 0
            foundSize = "1x.jpg"
            for size in sizeImages:
                sizeRes = cv2.matchTemplate(screen, size, cv2.TM_CCOEFF_NORMED)
                sizeLoc = numpy.where(sizeRes >= SIZE_THRESHOLD)
                zipSizes = zip(*sizeLoc[::-1])
                for sizePt in zipSizes:
                    if (checkRange(pt, sizePt)):
                        foundSize = sizeNames[j]
                        break
                j += 1
            if (("Cheese" in menuFileNames[i]) and not(cheeseCheck)):
                cheeseCheck = True
                order.append([menuFileNames[i], foundSize])
            elif ("Cheese" not in menuFileNames[i]):
                order.append([menuFileNames[i], foundSize])
            break
        i += 1

def displayOrder(order, sizes):
    print("Full Order:")
    i = 0
    for item in order:
        try:
            print("Item: " + format(item[0]) + " Size: " + format(item[1]))
        except:
            print("No Item Found")
        i += 1

status = 0
while True:
    start = time.time()
    screen = numpy.array(ImageGrab.grab(bbox=FRAME_COORDS))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    order = []
    sizes = []
    findItems(screen, images, order, sizes)
    displayOrder(order, sizes)
    foundType = 0
    for item in order:
        if ("Patty.png" in item or "Veggie.png" in item):
            foundType = 1
        elif ("Ring.png" in item or "Sticks.png" in item or "Fry.png" in item):
            foundType = 2
        elif ("Drink.png" in item or "Juice.png" in item or "Shake.png" in item):
            foundType = 3
    if ((foundType == 1) and (status == 0)):
        bottomBun = imageToButton['bottomBun']
        topBun = imageToButton['topBun']
        sides = imageToButton['Sides']
        click(bottomBun['x'], bottomBun['y'])
        time.sleep(BUTTON_DELAY)
        for item in order:
            button = imageToButton[item[0]]
            try:
                if (item[1] == "x2.png"):
                    click(button['x'], button['y'], count=2)
                else:
                    click(button['x'], button['y'])
            except:
                # Default to 1
                click(button['x'], button['y'])
            time.sleep(BUTTON_DELAY)
        click(topBun['x'], topBun['y'])
        time.sleep(BUTTON_DELAY)
        click(sides['x'], sides['y'])
        status = 1
        drinkCheck = 0
    elif ((foundType == 2) and status == 1):
        button = imageToButton[order[0][0]]
        drink = imageToButton['Drink']
        click(button['x'], button['y'])
        time.sleep(BUTTON_DELAY)
        size = imageToButton[order[0][1]]
        click(size['x'], size['y'])
        time.sleep(BUTTON_DELAY)
        click(drink['x'], drink['y'])
        status = 2
    elif ((foundType == 3) and status == 2):
        button = imageToButton[order[0][0]]
        done = imageToButton['Done']
        click(button['x'], button['y'])
        time.sleep(BUTTON_DELAY)
        size = imageToButton[order[0][1]]
        click(size['x'], size['y'])
        time.sleep(BUTTON_DELAY)
        click(done['x'], done['y'])
        status = 0
    elif ((foundType == 0) and status == 2):
        drinkCheck += 1
        done = imageToButton['Done']
        if (drinkCheck > 2):
            click(done['x'], done['y'])
            status = 0
    time.sleep(FRAME_DELAY)