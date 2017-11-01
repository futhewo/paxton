# paxton

## Introduction

Paxton is a command line tool used to produce a set of data that *looks like* another set of data. To do so, it first takes and analyzes an input, yields some statistics on it. Then, he used these statistics to produce an output that look like what he understood of the input.

## Strategies

Several strategies are defined to generate look-a-like outputs:
* global (-g): produce a character based on its occurences inside the whole input.
* position (-p): produce a character based on its occurences at this very position.
* twochain (-t): produce a character based on the previous character.
Each time paxton has to produce a new character, he will choose randomly one of these strategies, then use it. The ponderations of these strategies can be changed with command line arguments.

## Combination modes

The previous strategies can be combined, according to a chosen combination mode:
* none (-m0): no combination betwenn strategies, one strategy is selected according to the ponderation for each new character.
* simple (-m1): combine the strategies and their ponderation before choosing a new character.

## Help

Now, this is the help of paxton:
```
Usage: paxton/paxton.py [options]

Options:
  -h, --help            show this help message and exit
  -a analyzedFile, --analyze=analyzedFile
                        Analyze the given file.
  -x producedNumber, --produce=producedNumber
                        Produce a given number of elements.
  -s saveFile, --save=saveFile
                        Save the object into the given file.
  -r restoredFile, --restore=restoredFile
                        Restore the results of a previous analysis from the
                        given file.
  -g globalStrategy, --global=globalStrategy
                        Ponderation of the strategy that generates characters
                        based on global stats of the characters.
  -p positionStrategy, --position=positionStrategy
                        Ponderation of the strategy that generates characters
                        based on the position.
  -t twochainStrategy, --twochain=twochainStrategy
                        Ponderation of the strategy that generates characters
                        based on the previous character generated.
  -m combinationMode, --mode=combinationMode
                        The combination mode (0: no combination, 1: simple
                        mode), determines how the different strategy are
                        combined.
```

## Example

You will find examples of input and modelization (json formatted) in the exampled directory.
To analyze an input and directly produce 10 outputs:

```
python3 paxton/paxton.py -x10 -a examples/englishNames/englishNames.list
```

Same, but we restore a previous model:
```
python3 paxton/paxton.py -x10 -r examples/englishNames/englishNames.json
```

To analyze a file, set a fancy strategy and save the model:
```
python3 paxton/paxton.py -g50 -p300 -t2000 -m1 -a examples/englishNames/englishNames.list -s /tmp/myModel.json
```



