import os
import json
import random
from PIL import Image

"""For turning a Minecraft map into a JSON compatible with the colours JSONs in this repo"""

# coords start top left

def loadJSON(filename):
    filename = os.path.normpath(filename)
    with open(filename) as f:
        loadedJSON = json.load(f)
    return loadedJSON

def saveJSON(filename, JSONToSave):
    filename = os.path.normpath(filename)
    with open(filename, "w") as f:
        f.write(json.dumps(JSONToSave, indent = 4))

def SAO_RGBAToHexNoAlpha(colorRGB):
    return ("#%02x%02x%02x%02x" % colorRGB).upper()[:7]

def pixelToColourId(pixel):
    """Returns randomly chosen natural terrain blocks colourId for given input pixel"""
    pixelHex = SAO_RGBAToHexNoAlpha(pixel)
    colourDict = colourHexLookup[pixelHex]
    colourSet = colours_natural[colourDict["colourSetNumber"]]
    randomBlockChoiceNumber = random.randint(0, len(colourSet["blocks"]) - 1)
    randomBlockChoice = list(colourSet["blocks"].values())[randomBlockChoiceNumber]
    colourId = randomBlockChoice["blockId"][colourDict["tone"]]
    return colourId

def pixelsToColourIdJSON(im_size, pixels):
    size_x, size_y = im_size
    colourIdJSON = []
    for y in range(size_y):
        for x in range(size_x):
            pixel = pixels[x, y]
            colourId = pixelToColourId(pixel)
            colourIdJSON.append(
                {
                    "x": x,
                    "y": y,
                    "colourId": colourId
                }
            )
    return colourIdJSON

colours_natural = loadJSON("./colours_natural.json")
colourHexLookup = loadJSON("./colourHexLookup.json")

if __name__ == "__main__":
    im = Image.open("./map_24360.png")
    pixels = im.load()
    colourIdJSON = pixelsToColourIdJSON(im.size, pixels)
    saveJSON("./map_JSON.json", colourIdJSON)
