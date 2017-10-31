#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
# Paxton main module

# Imports #################################################
import random
import sys
from optparse import OptionParser



# Init ####################################################
defaultStrategy = [10, 30, 60]



# Data structure ##########################################
class Memory:
    def __init__(self, strategy=defaultStrategy):
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
        size = dictChoice(fu, self.sizes)
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
        pass


    def restore(self, filename):
        pass



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

    parser.add_option("-n", "--number", type="int",  dest="number", default="1", help="Choose How many elements you want to generate.", metavar="number")
    parser.add_option("-g", "--global", type="int",  dest="globalStrategy", default=str(defaultStrategy[0]), help="Ponderation of the strategy that generates characters based on global stats of the characters.", metavar="globalStrategy")
    parser.add_option("-p", "--position", type="int",  dest="positionStrategy", default=str(defaultStrategy[1]), help="Ponderation of the strategy that generates characters based on the position.", metavar="positionStrategy")
    parser.add_option("-t", "--twochain", type="int",  dest="twochainStrategy", default=str(defaultStrategy[2]), help="Ponderation of the strategy that generates characters based on the previous character generated.", metavar="twochainStrategy")
    (options, args) = parser.parse_args()

    if len(sys.argv) < 2:
        print(usage)
    else:
        strategy = [options.globalStrategy, options.positionStrategy, options.twochainStrategy]
        mem = Memory(strategy)
        f = open(sys.argv[-1], 'r')
        data = f.read()
        mem.parse(data)

        for i in range(options.number):
            print(mem.produce())


if __name__ == "__main__":
    start()

