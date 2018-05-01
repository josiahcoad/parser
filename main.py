"""Run this file to run project 8."""

import sys

from parser import Parser
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
        string = ifile.read()
    tokenizer = Tokenizer(string)
    parser = Parser(string)
    with open(f"{basename}T2.xml", "w") as ofile:
        ofile.write(tokenizer.xml)
    with open(f"{basename}2.xml", "w") as ofile:
        ofile.write(parser.xml)


def main():
    """Main program to run."""
    readwrite(getfilename_from_terminal())
    # readwrite("../Project_8_codes/Square/Square")


if __name__ == "__main__":
    main()
