import os
import json
from hashlib import md5

def loadJSON(filename):
    filename = os.path.normpath(filename)
    with open(filename) as f:
        loadedJSON = json.load(f)
    return loadedJSON

def saveJSON(filename, JSONToSave):
    filename = os.path.normpath(filename)
    with open(filename, "w") as f:
        f.write(json.dumps(JSONToSave, indent = 4))

def SAO_RGBToHex(colorRGB):
    return ("#%02x%02x%02x" % colorRGB).upper()

def SAO_StringToMD5(string):
    string = string.encode("UTF-8")
    md5Instance = md5()
    md5Instance.update(string)
    return md5Instance.hexdigest()

def convertRebaneToSAO(inputJSON):
    returnJSON = inputJSON[:51] # remove 1.13+ since 2b2t will never update
    returnJSON = {str(value[2]): value for value in returnJSON} # turn into dict with key
    for key in returnJSON:
        returnJSON[key] = {
            "tones": returnJSON[key][0],
            "blocks": returnJSON[key][1]
        }
        returnJSON[key]["tones"] = {
            "dark": SAO_RGBToHex(tuple(returnJSON[key]["tones"][0])),
            "normal": SAO_RGBToHex(tuple(returnJSON[key]["tones"][1])),
            "light": SAO_RGBToHex(tuple(returnJSON[key]["tones"][2]))
        }
        returnJSON[key]["blocks"] = {str(blockNumber): {
            "blockName": (blockName := block[2].title().replace("Tnt", "TNT")),
            "filename": (filename := "{}.png".format((block[4] if block[4] else block[0]))),
            "blockNameTonesHash": {
                "dark": SAO_StringToMD5("{}dark".format(blockName)),
                "normal": SAO_StringToMD5("{}normal".format(blockName)),
                "light": SAO_StringToMD5("{}light".format(blockName))
            }
            } for blockNumber, block in enumerate(returnJSON[key]["blocks"])}
    return returnJSON

def findMinimumTruncationLengthForUniqueHashes(inputJSON):
    endLength = 0
    def inner():
        # easier to Return from inner function than break a tonne of for loops
        nonlocal endLength
        endLength += 1
        hashesSoFar = []
        for colourSet in inputJSON.values():
            for block in colourSet["blocks"].values():
                for tone, blockNameTonesHash in block["blockNameTonesHash"].items():
                    hashLastNChars = blockNameTonesHash[-endLength:]
                    if not (alreadyUsedList := [t for t in hashesSoFar if t["hashLastNChars"] == hashLastNChars]):
                        hashesSoFar.append(
                            {
                                "blockName": block["blockName"],
                                "tone": tone,
                                "hashLastNChars": hashLastNChars
                            }
                        )
                    else:
                        alreadyUsedItem = alreadyUsedList[0]
                        print("Hash ending with {} already exists for {}:{}, cannot reuse for {}:{}".format(hashLastNChars, alreadyUsedItem["blockName"], alreadyUsedItem["tone"], block["blockName"], tone))
                        return False
    while inner() is False:
        # this looks so silly lol
        pass
    print("All unique for length {}".format(endLength))
    return endLength

def createColourIdLookupJSON(inputJSON, hashLength):
    lookupTable = {}
    for colourSetNumber, colourSet in inputJSON.items():
        for blockNumber, block in colourSet["blocks"].items():
            for tone, blockNameTonesHash in block["blockNameTonesHash"].items():
                numberFromHash = str(int(blockNameTonesHash[-hashLength:], 16))
                assert numberFromHash not in lookupTable
                lookupTable[numberFromHash] = {
                    "colourSetNumber": colourSetNumber,
                    "blockNumber": blockNumber,
                    "tone": tone
                }
    return lookupTable

def swapHashesForColourId(inputJSON, hashLength):
    for key in inputJSON:
        for blockKey in inputJSON[key]["blocks"]:
            inputJSON[key]["blocks"][blockKey]["blockId"] = {}
            for tone in inputJSON[key]["blocks"][blockKey]["blockNameTonesHash"]:
                inputJSON[key]["blocks"][blockKey]["blockId"][tone] = str(int(inputJSON[key]["blocks"][blockKey]["blockNameTonesHash"][tone][-hashLength:], 16))
            del inputJSON[key]["blocks"][blockKey]["blockNameTonesHash"]
    return inputJSON

def createColourHexLookupJSON(inputJSON):
    lookupTable = {}
    for colourSetNumber, colourSet in inputJSON.items():
        for toneName, toneColour in colourSet["tones"].items():
            assert not toneColour in lookupTable
            lookupTable[toneColour] = {
                "colourSetNumber": colourSetNumber,
                "tone": toneName
            }
    return lookupTable

def create_colours_naturalJSON(inputJSON):
    """I have manually chosen what is natual and what is not per colourSet"""
    allowedColourSets = {
        "0": ["0"],
        "1": ["0"], # maybe not 1 sandstone
        "2": ["0"],
        "3": ["1"],
        "4": ["0"],
        "5": ["2"],
        "6": ["0"], # leaves, may have to consider biome
        "7": ["0"],
        "8": ["3"],
        "9": ["1"], # maybe enable 7 gravel
        "10": ["0"], # water
        "11": ["0"],
        "12": ["1"],
        "13": ["7"],
        "14": ["9", "11"],
        "15": ["6"],
        "17": ["6"],
        "18": ["6"],
        "22": ["6"],
        "23": ["6"],
        "25": ["6"],
        "27": ["6"],
        "28": ["7"],
        "30": ["1"],
        "33": ["5"], # set to podzol, could be horizontal log
        "34": ["0"],
        "35": ["0"], # terracotta starts
        "36": ["0"],
        "37": ["0"],
        "38": ["0"],
        "39": ["0"],
        "40": ["0"],
        "41": ["0"],
        "42": ["0"],
        "43": ["0"],
        "44": ["0"],
        "45": ["0"],
        "46": ["0"],
        "47": ["0"],
        "48": ["0"],
        "49": ["0"],
        "50": ["0"]  # terracotta finishes
    }
    returnJSON = {}
    for allowedColourSet_key, allowedColourSet_value in allowedColourSets.items():
        returnJSON[allowedColourSet_key] = inputJSON[allowedColourSet_key]
        returnJSON[allowedColourSet_key]["blocks"] = {k: v for (k, v) in returnJSON[allowedColourSet_key]["blocks"].items() if k in allowedColourSet_value}
    return returnJSON

if __name__ == "__main__":
    loadedJSON = loadJSON("./rebaneColours.json")
    modifiedJSON = convertRebaneToSAO(loadedJSON)

    # hashLength = findMinimumTruncationLengthForUniqueHashes(modifiedJSON)
    hashLength = 6 # hashLength turns out to be 5, so we can safely use 6. Also keep <= 8 for int32

    lookupTable = createColourIdLookupJSON(modifiedJSON, hashLength)
    saveJSON("./colourIdLookup.json", lookupTable)

    modifiedJSON = swapHashesForColourId(modifiedJSON, hashLength)
    saveJSON("./colours.json", modifiedJSON)

    lookupTable = createColourHexLookupJSON(modifiedJSON)
    saveJSON("./colourHexLookup.json", lookupTable)

    colours_natural = create_colours_naturalJSON(modifiedJSON)
    saveJSON("./colours_natural.json", colours_natural)
