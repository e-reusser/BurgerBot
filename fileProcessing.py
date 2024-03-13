import yaml

def processConfig():
    with open('config.yml') as f:
        baseConfigMap = yaml.safe_load(f)
    configMap = {
        'FRAME_COORDS': [baseConfigMap['frameCaptureCoordinates']['pos1'][0], baseConfigMap['frameCaptureCoordinates']['pos1'][1], baseConfigMap['frameCaptureCoordinates']['pos2'][0], baseConfigMap['frameCaptureCoordinates']['pos2'][1]],
        'ITEM_THRESHOLD': baseConfigMap['itemThreshold'],
        'SIZE_THRESHOLD': baseConfigMap['sizeThreshold'],
        'CHEESE_THRESHOLD': baseConfigMap['cheeseThreshold'],
        'BUTTON_DELAY': baseConfigMap['buttonDelay'],
        'FRAME_DELAY': baseConfigMap['frameDelay']
    }
    return configMap

def processButtons():
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
    return imageToButton