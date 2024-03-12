import time
import numpy
from PIL import ImageGrab
from directKeys import click
import cv2
import os

# Frame coordinates and thresholds
frame_coords = [530, 200, 1400, 450]
itemThreshold = .859 #.859 or .812
sizeThreshold = .925
buttonDelay = 0.05
frameDelay = 0.5

# Coordinates of ingredients
bottomBun = [1674, 741]
lettuce = [1674, 676]
tomato = [1674, 602]
patty = [1627, 535]
veggie = [1713, 531]
cheese = [1674, 472]
onion = [1674, 402]
topBun = [1674, 331]

# Menu buttons
sides = [1871, 477]
drink = [1871, 599]
done = [1865, 705]

# Side / Drink buttons
top = [1602, 415]
middle = [1602, 538]
bottom = [1602, 660]
small = [1738, 414]
medium = [1738, 541]
large = [1738, 660]

imageToButton = {
    "Cheese.png": cheese,
    "Cheese1.png": cheese,
    "Cheese2.png": cheese,
    "Drink.png": top,
    "Fry.png": top,
    "Juice.png": middle,
    "Lettuce.png": lettuce,
    "Onion.png": onion,
    "Patty.png": patty,
    "Ring.png": bottom,
    "Sticks.png": middle,
    "Tomato.png": tomato,
    "Veggie.png": veggie,
    "Shake.png": bottom,
    "Small.png": small,
    "Medium.png": medium,
    "Large.png": large
}

directory = 'images'
images = []
menuFileNames = []
menuFileCount = 0
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        images.append(cv2.imread(os.path.join(directory, filename), cv2.IMREAD_GRAYSCALE))
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
        loc = numpy.where(res >= itemThreshold)
        for pt in zip(*loc[::-1]):
            j = 0
            for size in sizeImages:
                sizeRes = cv2.matchTemplate(screen, size, cv2.TM_CCOEFF_NORMED)
                sizeLoc = numpy.where(sizeRes >= sizeThreshold)
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
    screen = numpy.array(ImageGrab.grab(bbox=frame_coords))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    order = []
    sizes = []
    findItems(screen, images, order, sizes)
    displayOrder(order, sizes)
    if (("Patty.png" in order or "Veggie.png" in order) and (status == 0)):
        click(bottomBun[0], bottomBun[1])
        time.sleep(buttonDelay)
        i = 0
        for item in order:
            button = imageToButton[item]
            try:
                if (sizes[i] == "x2.png"):
                    click(button[0], button[1], count=2)
                else:
                    click(button[0], button[1])
            except:
                # Default to 1
                click(button[0], button[1])
            time.sleep(buttonDelay)
            i += 1
        click(topBun[0], topBun[1])
        time.sleep(buttonDelay)
        click(sides[0], sides[1])
        status = 1
        drinkCheck = 0
    elif (("Ring.png" in order or "Sticks.png" in order or "Fry.png" in order) and status == 1):
        button = imageToButton[order[0]]
        click(button[0], button[1])
        time.sleep(buttonDelay)
        size = imageToButton[sizes[0]]
        click(size[0], size[1])
        time.sleep(buttonDelay)
        click(drink[0], drink[1])
        status = 2
    elif (("Drink.png" in order or "Juice.png" in order or "Shake.png" in order) and status == 2):
        button = imageToButton[order[0]]
        click(button[0], button[1])
        time.sleep(buttonDelay)
        size = imageToButton[sizes[0]]
        click(size[0], size[1])
        time.sleep(buttonDelay)
        click(done[0], done[1])
        status = 0
    elif (not("Drink.png" in order or "Juice.png" in order or "Shake.png" in order) and status == 2):
        drinkCheck += 1
        if (drinkCheck > 2):
            click(done[0], done[1])
            status = 0
    time.sleep(frameDelay)