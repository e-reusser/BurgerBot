import time
import numpy
from PIL import ImageGrab
from directKeys import click
import cv2
import os
import yaml

# Frame coordinates, thresholds, and delays
# These will typically vary based on machine
FRAME_COORDS = [530, 200, 1400, 450]
ITEM_THRESHOLD = .859
SIZE_THRESHOLD = .925
BUTTON_DELAY = 0.05
FRAME_DELAY = 0.5

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
        loc = numpy.where(res >= ITEM_THRESHOLD)
        for pt in zip(*loc[::-1]):
            j = 0
            for size in sizeImages:
                sizeRes = cv2.matchTemplate(screen, size, cv2.TM_CCOEFF_NORMED)
                sizeLoc = numpy.where(sizeRes >= SIZE_THRESHOLD)
                zipSizes = zip(*sizeLoc[::-1])
                for sizePt in zipSizes:
                    if (checkRange(pt, sizePt)):
                        sizes.append(sizeNames[j])
                        break
                j += 1
            if ((menuFileNames[i] == "Cheese.png" or menuFileNames[i] == "Cheese1.png" or menuFileNames[i] == "Cheese2.png") and not(cheeseCheck)):
                cheeseCheck = True
                order.append(menuFileNames[i])
            elif (not(menuFileNames[i] == "Cheese.png" or menuFileNames[i] == "Cheese1.png" or menuFileNames[i] == "Cheese2.png")):
                order.append(menuFileNames[i])
            break
        i += 1

def displayOrder(order, sizes):
    print("Full Order:")
    i = 0
    for item in order:
        try:
            print("Item: " + format(item) + " Size: " + format(sizes[i]))
        except:
            print("Item: " + format(item) + " Size: No Size")
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
    if (("Patty.png" in order or "Veggie.png" in order) and (status == 0)):
        bottomBun = imageToButton['bottomBun']
        topBun = imageToButton['topBun']
        sides = imageToButton['Sides']
        click(bottomBun['x'], bottomBun['y'])
        time.sleep(BUTTON_DELAY)
        i = 0
        for item in order:
            button = imageToButton[item]
            try:
                if (sizes[i] == "x2.png"):
                    click(button['x'], button['y'], count=2)
                else:
                    click(button['x'], button['y'])
            except:
                # Default to 1
                click(button['x'], button['y'])
            time.sleep(BUTTON_DELAY)
            i += 1
        click(topBun['x'], topBun['y'])
        time.sleep(BUTTON_DELAY)
        click(sides['x'], sides['y'])
        status = 1
        drinkCheck = 0
    elif (("Ring.png" in order or "Sticks.png" in order or "Fry.png" in order) and status == 1):
        button = imageToButton[order[0]]
        drink = imageToButton['Drink']
        click(button['x'], button['y'])
        time.sleep(BUTTON_DELAY)
        size = imageToButton[sizes[0]]
        click(size['x'], size['y'])
        time.sleep(BUTTON_DELAY)
        click(drink['x'], drink['y'])
        status = 2
    elif (("Drink.png" in order or "Juice.png" in order or "Shake.png" in order) and status == 2):
        button = imageToButton[order[0]]
        done = imageToButton['Done']
        click(button['x'], button['y'])
        time.sleep(BUTTON_DELAY)
        size = imageToButton[sizes[0]]
        click(size['x'], size['y'])
        time.sleep(BUTTON_DELAY)
        click(done['x'], done['y'])
        status = 0
    elif (not("Drink.png" in order or "Juice.png" in order or "Shake.png" in order) and status == 2):
        drinkCheck += 1
        done = imageToButton['Done']
        if (drinkCheck > 2):
            click(done['x'], done['y'])
            status = 0
    time.sleep(FRAME_DELAY)