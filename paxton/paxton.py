#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
# Paxton main module

# Imports #################################################
import random
import sys
from optparse import OptionParser
import json



# Init ####################################################

# Combination modes:
CM_NONE   = 0
CM_SIMPLE = 1

# Default values:
defaultStrategy = [2, 20, 100]
defaultMode     = CM_SIMPLE



# Data structure ##########################################
class Memory:
    """
        Contains all the information infers from the input file.
    """

    def __init__(self, strategy=defaultStrategy):
        """
            Set the strategy to the given value and init all structures.
        """
        # Strategy memory: a list of 3 ([global, position, twochain]) ponderating each one of these elements.
        self.strategy = strategy
        self.strategyTotal = self.strategy[0] + self.strategy[1] + self.strategy[2]

        # The strategy combination mode. It can be:
        # CM_NONE : no combination, choose a random strategy for each new character
        # CM_SIMPLE : combine all strategies (conserving ponderations) to make a new dict and chose the new character in this dict.
        self.combinationMode = defaultMode

        # Characters memory: count the occurences of any character in the whole file.
        self.characters = dict()
        self.charactersTotal = 0

        # Sizes memory: count the occurrences of any size in the whole file.
        self.sizes = dict()
        self.sizesTotal = 0
        self.maxSize = 0

        # Positions memory: count the occurences of any character at any given position.
        # list of dict(), one dict() of characters for each position.
        self.positions = []
        self.positionsTotal = []

        # Twochains memory: count the occurences of any character after any other character.
        # a dict of [total, dict()], keys of the first dict are (n-1) characters, total is the sum of characters counted after (n-1) ; dict() contains occurences of n characters.
        self.twochains = dict()


    def setStrategyPart(self, part, strategyPart):
        """
            Set one of the strategy, identified as part with the value strategyPart.
        """
        self.strategyTotal += strategyPart - self.strategy[part]
        self.strategy[part] = strategyPart


    # Parsing =============================================
    def parse(self, data, separator="\n"):
        """
            Launch all parsers on the data.
        """
        self.parseCharacters(data, separator)
        self.parseSizes(data, separator)
        self.parsePositions(data, self.maxSize, separator)
        self.parseTwochains(data, separator)
 

    def parseCharacters(self, data, separator="\n"):
        """
            Count the occurences of all characters.
        """
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
        """
            Count the occurences of all sizes of all subelements. The separator is used in order to split the input into subelements.
        """
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
        """
            Count the occurences of all characters at any position in a subelement. The separator is used to split the input into subelements.
        """
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
        """
            Count the occurences of one character after another one.
        """
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
        """
            Produce an output from the model and following the strategy.
        """
        # Choose the size
        fu = random.randint(0, self.sizesTotal - 1)
        size = int(dictChoice(fu, self.sizes))
        assert(size >= 0)
        if size == 0:
            return ""

        if self.combinationMode == CM_NONE:
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

        elif self.combinationMode == CM_SIMPLE:
            # Create a dict of possibilities for the next character.
            value = ""

            for i in range(size - 1):
                nextCharDict = dict()
                nextCharTotal = 0

                # Characters
                for key in self.characters.keys():
                    # Copy the value and keep the ponderation.
                    nextCharDict[key] = self.characters[key] * self.strategy[0]
                nextCharTotal += self.charactersTotal * self.strategy[0]

                # Positions
                for key in self.positions[i].keys():
                    if key in nextCharDict.keys():
                        nextCharDict[key] += self.positions[i][key] * self.strategy[1]
                    else:
                        nextCharDict[key] = self.positions[i][key] * self.strategy[1]
                nextCharTotal += self.positionsTotal[i] * self.strategy[1]

                # Twochains
                previousChar = ""
                if i == 0:
                    previousChar = separator
                else:
                    previousChar = value[-1]
                nextCharTotal += self.twochains[previousChar][0] * self.strategy[2]

                for key in self.twochains[previousChar][1].keys():
                    if key == separator:
                        nextCharTotal -= self.twochains[previousChar][1][key] * self.strategy[2]
                        continue

                    if key in nextCharDict.keys():
                        nextCharDict[key] += self.twochains[previousChar][1][key] * self.strategy[2]
                    else:
                        nextCharDict[key] = self.twochains[previousChar][1][key] * self.strategy[2]

                # Generation
                fu = random.randint(0, nextCharTotal - 1)
                value += dictChoice(fu, nextCharDict)

            return value

        else:
            raise Exception("Wrong combination mode chosen.")



    # Save/restore ========================================
    def save(self, filename):
        """
            Save the object parameters in a json formatted file.
        """
        dataStructure = dict()
        dataStructure["strategy"] = self.strategy
        dataStructure["strategyTotal"] = self.strategyTotal
        dataStructure["combinationMode"] = self.combinationMode
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
            log("Model saved.")


    def restore(self, filename):
        """
            Restore the object parameters from a json formatted file.
        """
        dataStructure = dict()
        with open(filename, 'r') as f:
            dataStructure = json.load(f)

            self.strategy = dataStructure["strategy"]
            self.strategyTotal = dataStructure["strategyTotal"]
            self.combinationMode = dataStructure["combinationMode"]
            self.characters = dataStructure["characters"]
            self.charactersTotal = dataStructure["charactersTotal"]
            self.sizes = dataStructure["sizes"]
            self.sizesTotal = dataStructure["sizesTotal"]
            self.maxSize = dataStructure["maxSize"]
            self.positions = dataStructure["positions"]
            self.positionsTotal = dataStructure["positionsTotal"]
            self.twochains = dataStructure["twochains"]
            log("Model loaded.")



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

    raise Exception("The value asked is out of the dictionary.")

def listChoice(invalue, inlist):
    """
        Consume the inValue and returns the list element in which it ends.
    """
    value = invalue
    for i in range(len(inlist)):
        value -= inlist[i]
        if value < 0:
            return i

    raise Exception("The value asked is out of the list.")


# Maint ###################################################
def start():
    usage = "Usage: {0} [options]".format(sys.argv[0])
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
    parser.add_option("-m", "--mode", type="int",  dest="combinationMode", default=-1, help="The combination mode (0: no combination, 1: simple mode), determines how the different strategy are combined.", metavar="combinationMode")
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
        mem.setStrategyPart(0, options.globalStrategy)
    if options.positionStrategy != -1:
        mem.setStrategyPart(1, options.positionStrategy)
    if options.twochainStrategy != -1:
        mem.setStrategyPart(2, options.twochainStrategy)
    if options.combinationMode != -1:
        mem.combinationMode = options.combinationMode

    log("Generating {0} outputs with strategy [g:{1}, p:{2}, t:{3}] and mode {4}.".format(options.producedNumber, mem.strategy[0], mem.strategy[1], mem.strategy[2], mem.combinationMode))
    for i in range(options.producedNumber):
        print(mem.produce())


if __name__ == "__main__":
    start()

