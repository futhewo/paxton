#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
# Paxton main module

# Imports #################################################
import random
import sys


# Data structure ##########################################
class Memory:
    def __init__(self):
        self.characters = dict()
        self.charactersTotal = 0

        self.sizes = dict()
        self.sizesTotal = 0
        self.maxSize = 0

        # list of dict(), one for each position
        self.positions = []
        self.positionsTotal = []

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
        random.seed(1)
        
        # Choose size
        fu = random.randint(0, self.sizesTotal - 1)
        size = dictChoice(fu, self.sizes)
        assert(size >= 0)
        if size == 0:
            return ""

        # Choose the first element
        fu = random.randint(0, self.positionsTotal[0] - 1)
        value = dictChoice(fu, self.positions[0])

        # Choose what remains
        for i in range(size - 1):
            fu = random.randint(0, self.charactersTotal - 1)
            value += dictChoice(fu, self.characters)

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


def start():
    usage = "Usage: {0} <file>".format(sys.argv[0])

    if len(sys.argv) != 2:
        print(usage)
    else:
        mem = Memory()
        f = open(sys.argv[1], 'r')
        data = f.read()
        mem.parse(data)
        print(mem.produce())

if __name__ == "__main__":
    start()

