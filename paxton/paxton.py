#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
# Paxton main module

# Imports #################################################
import random
import sys
from optparse import OptionParser
import json



# Init ####################################################
defaultStrategy = [10, 30, 60]



# Data structure ##########################################
class Memory:
    def __init__(self, strategy=defaultStrategy):
        # Strategy memory
        self.strategy = strategy
        self.strategyTotal = self.strategy[0] + self.strategy[1] + self.strategy[2]

        # Characters memory
        self.characters = dict()
        self.charactersTotal = 0

        # Sizes memory
        self.sizes = dict()
        self.sizesTotal = 0
        self.maxSize = 0

        # Positions memory
        # list of dict(), one for each position
        self.positions = []
        self.positionsTotal = []

        # Twochains memory
        # a dict of [total, dict()]
        self.twochains = dict()


    def setStrategy(self, part, strategyPart):
        self.strategyTotal += strategyPart - self.strategy[part]
        self.strategy[part] = strategyPart


    # Parsing =============================================
    def parse(self, data, separator="\n"):
        self.parseCharacters(data, separator)
        self.parseSizes(data, separator)
        self.parsePositions(data, self.maxSize, separator)
        self.parseTwochains(data, separator)
 

    def parseCharacters(self, data, separator="\n"):
        log("Beginning parsing characters.")

        self.charactersTotal = len(data)
        for i in range(len(data)):
            if data[i] == separator:
                self.charactersTotal -= 1
            else:
                if data[i] in self.characters.keys():
                    self.characters[data[i]] += 1
                else:
                    self.characters[data[i]] = 1

        log("Ending parsing characters.")


    def parseSizes(self, data, separator="\n"):
        log("Beginning parsing sizes.")

        datas = data.split(separator)
        self.maxSize = max(map(len, datas))
        self.sizesTotal = len(datas)
        for i in range(len(datas)):
            if len(datas[i]) in self.sizes.keys():
                self.sizes[len(datas[i])] += 1
            else:
                self.sizes[len(datas[i])] = 1

        log("Ending parsing sizes.")


    def parsePositions(self, data, maxSize, separator="\n"):
        log("Beginning parsing positions.")

        datas = data.split(separator)
        for i in range(maxSize):
            self.positions.append(dict())
            self.positionsTotal.append(0)

        for i in range(len(datas)):
            for j in range(len(datas[i])):
                if datas[i][j] in self.positions[j].keys():
                    self.positions[j][datas[i][j]] += 1
                else:
                    self.positions[j][datas[i][j]] = 1
                self.positionsTotal[j] += 1

        log("Ending parsing positions.")


    def parseTwochains(self, data, separator="\n"):
        log("Beginning parsing 2-chains.")

        # The very first character is assumed to have followed a separator.
        self.twochains[separator] = [1, dict()]
        self.twochains[separator][1][data[0]] = 1

        for i in range(1, len(data)):
            if not (data[i - 1] in self.twochains.keys()):
                self.twochains[data[i - 1]] = [0, dict()]

            if data[i] in self.twochains[data[i - 1]][1].keys():
                self.twochains[data[i - 1]][1][data[i]] += 1
            else:
                self.twochains[data[i - 1]][1][data[i]] = 1
            self.twochains[data[i - 1]][0] += 1
        
        # The very last character is assumed to be followed by a separator
        if separator in self.twochains[data[len(data) - 1]][1].keys():
            self.twochains[data[len(data) - 1]][1][separator] += 1
        else:
            self.twochains[data[len(data) - 1]][1][separator] = 1
        self.twochains[data[len(data) - 1]][0] += 1

        log("Ending parsing 2-chains.")


    # Production ==========================================
    def produce(self, separator="\n"):

        # Choose the size
        fu = random.randint(0, self.sizesTotal - 1)
        size = int(dictChoice(fu, self.sizes))
        assert(size >= 0)
        if size == 0:
            return ""

        # Choose the first element among all the classical first elements.
        fu = random.randint(0, self.positionsTotal[0] - 1)
        value = dictChoice(fu, self.positions[0])

        # Choose what remains
        for i in range(1, size - 1):
            fu = random.randint(0, self.strategyTotal - 1)
            strategy = listChoice(fu, self.strategy)

            # Strategy 0: among all characters
            if strategy == 0:
                fu = random.randint(0, self.charactersTotal - 1)
                value += dictChoice(fu, self.characters)

            # Strategy 1: according to the position
            elif strategy == 1:
                fu = random.randint(0, self.positionsTotal[i] - 1)
                value += dictChoice(fu, self.positions[i])

            # Strategy 2: according to the previoux character
            elif strategy == 2:
                fu = random.randint(0, self.twochains[value[-1]][0] - 1)
                char = dictChoice(fu, self.twochains[value[-1]][1])
                if char == separator:
                    # Use default strategy.
                    fu = random.randint(0, self.charactersTotal - 1)
                    value += dictChoice(fu, self.characters)
                else:
                    value += char

        return value

    # Save/restore ========================================
    def save(self, filename):
        """
            Save the object parameters in a json formatted file.
        """
        dataStructure = dict()
        dataStructure["strategy"] = self.strategy
        dataStructure["strategyTotal"] = self.strategyTotal
        dataStructure["characters"] = self.characters
        dataStructure["charactersTotal"] = self.charactersTotal
        dataStructure["sizes"] = self.sizes
        dataStructure["sizesTotal"] = self.sizesTotal
        dataStructure["maxSize"] = self.maxSize
        dataStructure["positions"] = self.positions
        dataStructure["positionsTotal"] = self.positionsTotal
        dataStructure["twochains"] = self.twochains

        with open(filename, 'w') as f:
            json.dump(dataStructure, f, indent=4)


    def restore(self, filename):
        """
            Restore the object parameters from a json formatted file.
        """
        dataStructure = dict()
        with open(filename, 'r') as f:
            dataStructure = json.load(f)

        self.strategy = dataStructure["strategy"]
        self.strategyTotal = dataStructure["strategyTotal"]
        self.characters = dataStructure["characters"]
        self.charactersTotal = dataStructure["charactersTotal"]
        self.sizes = dataStructure["sizes"]
        self.sizesTotal = dataStructure["sizesTotal"]
        self.maxSize = dataStructure["maxSize"]
        self.positions = dataStructure["positions"]
        self.positionsTotal = dataStructure["positionsTotal"]
        self.twochains = dataStructure["twochains"]



# Utility functions #######################################
def log(data):
    """
        Log the data given as input.
        Useful for a future change of the logger used.
    """
    print("*** " + data + " ***")


def dictChoice(invalue, dictionary):
    """
        Return the key of a dictionary designated by a given value, where the value is a ponderation to be consumed.
    """
    value = invalue
    for key in dictionary.keys():
        value -= dictionary[key]
        if value < 0:
            return key

    raise "Error: the value asked is out of the dictionary."

def listChoice(invalue, inlist):
    """
        Consume the inValue and returns the list element in which it ends.
    """
    value = invalue
    for i in range(len(inlist)):
        value -= inlist[i]
        if value < 0:
            return i

    raise "Error: the value asked is out of the list."


# Maint ###################################################
def start():
    usage = "Usage: {0} [options] <file>".format(sys.argv[0])
    parser = OptionParser(usage=usage)

    # Global options
    parser.add_option("-a", "--analyze", type="string",  dest="analyzedFile", default="", help="Analyze the given file.", metavar="analyzedFile")
    parser.add_option("-x", "--produce", type="int",  dest="producedNumber", default="0", help="Produce a given number of elements.", metavar="producedNumber")

    # Save/restore
    parser.add_option("-s", "--save", type="string",  dest="saveFile", default="", help="Save the object into the given file.", metavar="saveFile")
    parser.add_option("-r", "--restore", type="string",  dest="restoredFile", default="", help="Restore the results of a previous analysis from the given file.", metavar="restoredFile")

    # Tweaking
    parser.add_option("-g", "--global", type="int",  dest="globalStrategy", default=-1, help="Ponderation of the strategy that generates characters based on global stats of the characters.", metavar="globalStrategy")
    parser.add_option("-p", "--position", type="int",  dest="positionStrategy", default=-1, help="Ponderation of the strategy that generates characters based on the position.", metavar="positionStrategy")
    parser.add_option("-t", "--twochain", type="int",  dest="twochainStrategy", default=-1, help="Ponderation of the strategy that generates characters based on the previous character generated.", metavar="twochainStrategy")
    (options, args) = parser.parse_args()



    mem = Memory()
    if options.restoredFile != "":
        mem.restore(options.restoredFile)

    if options.analyzedFile != "":
        if options.restoredFile != "":
            log("A model has already been restored. It is now discarded in profit of the newly analyzed model.")
        with open(options.analyzedFile, 'r') as f:
            data = f.read()
            mem.parse(data)

    if options.saveFile != "":
        mem.save(options.saveFile)

    if options.restoredFile == "" and options.analyzedFile == "":
        log("No model has been loaded, aborting.")
        exit(1)

    # Set the strategy at the end in order to override the one given by the eventual restoration.
    if options.globalStrategy != -1:
        mem.setStrategy(0, options.globalStrategy)
    if options.positionStrategy != -1:
        mem.setStrategy(1, options.positionStrategy)
    if options.twochainStrategy != -1:
        mem.setStrategy(2, options.twochainStrategy)

    log("Generating with strategy [g:{0}, p:{1}, t:{2}]".format(mem.strategy[0], mem.strategy[1], mem.strategy[2]))
    for i in range(options.producedNumber):
        print(mem.produce())


if __name__ == "__main__":
    start()

