"""Run this file to run project 8."""

import sys

# from .parser import Parser
from tokenizer import Tokenizer


def getfilename_from_terminal():
    """Validate the users input and return vm filename to parse."""

    if len(sys.argv) != 2:
        raise Exception("You must pass only one arg, namely input filename")
    fullfilename = sys.argv[1].strip()
    filenameparts = fullfilename.split(".")
    if len(filenameparts) != 2 or filenameparts[1] != "jack":
        raise Exception("Argument must be filename like prog.hack")
    return filenameparts[0]


def readwrite(basename):
    """Read in a hack file, translate it to an xml code.
    Write out the tokens in xml and
    also write out the parse tree in xml."""

    with open(f"{basename}.jack") as ifile:
        tokenizer = Tokenizer(ifile.read())
    with open(f"{basename}TT.xml", "w") as ofile:
        ofile.write(tokenizer.xml)


def main():
    """Main program to run."""
    readwrite(getfilename_from_terminal())


if __name__ == "__main__":
    main()
