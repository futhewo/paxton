from paxton.paxton import *
from nose.tools import *


def test_parseCharacters():
    data = "ABBCCCDDDDEEEEE"
    mem = Memory()
    mem.parseCharacters(data)

    assert_equals(mem.charactersTotal, 15)
    assert_equals(len(mem.characters.keys()), 5)
    assert_equals(mem.characters["A"], 1)
    assert_equals(mem.characters["B"], 2)
    assert_equals(mem.characters["C"], 3)
    assert_equals(mem.characters["D"], 4)
    assert_equals(mem.characters["E"], 5)
    

def test_parseSizes():
    data = "A BB C DDDD EEEEE"
    mem = Memory()
    mem.parseSizes(data, " ")

    assert_equals(mem.sizesTotal, 5)
    assert_equals(mem.maxSize, 5)
    assert_equals(len(mem.sizes.keys()), 4)
    assert_equals(mem.sizes[1], 2)
    assert_equals(mem.sizes[2], 1)
    assert_equals(mem.sizes[4], 1)
    assert_equals(mem.sizes[5], 1)
    

def test_parsePositions():
    data = "A BB C AAAA EEEEE"
    mem = Memory()
    mem.parsePositions(data, 5, " ")

    assert_equals(len(mem.positionsTotal), 5)
    assert_equals(mem.positionsTotal[0], 5)
    assert_equals(mem.positionsTotal[1], 3)
    assert_equals(mem.positionsTotal[2], 2)
    assert_equals(mem.positionsTotal[3], 2)
    assert_equals(mem.positionsTotal[4], 1)

    assert_equals(len(mem.positions), 5)
    assert_equals(len(mem.positions[0].keys()), 4)
    assert_equals(len(mem.positions[1].keys()), 3)
    assert_equals(len(mem.positions[2].keys()), 2)
    assert_equals(len(mem.positions[3].keys()), 2)
    assert_equals(len(mem.positions[4].keys()), 1)
    assert_equals(mem.positions[0]["A"], 2)
    assert_equals(mem.positions[0]["B"], 1)
    assert_equals(mem.positions[4]["E"], 1)


def test_parseTwoChains():
    data = "ABCABDABCABD"
    mem = Memory()
    mem.parseTwochains(data)

    assert_equals(len(mem.twochains.keys()), 5)
    assert_equals(mem.twochains["\n"][0], 1)
    assert_equals(len(mem.twochains["\n"][1].keys()), 1)
    assert_equals(mem.twochains["\n"][1]["A"], 1)

    assert_equals(mem.twochains["A"][0], 4)
    assert_equals(len(mem.twochains["A"][1].keys()), 1)
    assert_equals(mem.twochains["A"][1]["B"], 4)

    assert_equals(mem.twochains["B"][0], 4)
    assert_equals(len(mem.twochains["B"][1].keys()), 2)
    assert_equals(mem.twochains["B"][1]["C"], 2)
    assert_equals(mem.twochains["B"][1]["D"], 2)

    assert_equals(mem.twochains["D"][0], 2)
    assert_equals(len(mem.twochains["D"][1].keys()), 2)
    assert_equals(mem.twochains["D"][1]["A"], 1)
    assert_equals(mem.twochains["D"][1]["\n"], 1)
