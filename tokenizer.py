"""
Tokenizer takes an string and provides an API to access the tokens
of the string in order they are in the string. A token is an
object with a type and value.
"""
import re
import itertools
import os


class Token:
    """A token is an object with a type and value."""

    def __init__(self, ttype, value):
        self.ttype = ttype
        self.value = value

    def __str__(self):
        return str((self.ttype, self.value))

    def __repr__(self):
        return f"Token({self.ttype}, '{self.value}')"

    def __eq__(self, string):
        return self.value == string

    def __ne__(self, string):
        return self.value != string

class Tokenizer:
    """Takes an inputstring and provides an API to access the
    tokens of the string in order they are in the string.
    """
    TTKEYWORD = 'KEYWORD'
    TTSYMBOL = 'SYMBOL'
    TTNUM = 'NUMBER'
    TTSTRING = 'STRING'
    TTID = 'IDENTIFIER'
    TTYPES = [TTKEYWORD, TTSYMBOL, TTNUM, TTSTRING, TTID]

    KEYWORD = ('(class|constructor|function|method|field|static|var|int|'
               'char|boolean|void|true|false|null|this|let|do|if|else|while|return)')
    SYMBOL = r'([{}()[\].,;+\-*/&|<>=~])'
    INTLITERAL = r'(\d+)'  # should we make this catch floating points?
    STRINGLITERAL = r'\"([^\n]*)\"'
    IDENTIFIER = r'([A-Za-z_]\w*)'
    TOKEN = f'{KEYWORD}|{SYMBOL}|{INTLITERAL}|{STRINGLITERAL}|{IDENTIFIER}'
    @staticmethod
    def getxml(token):
        """Get a token enclosed by its type in an xml tag."""
        xmlmap = {
            Tokenizer.TTKEYWORD: "<keyword> {} </keyword>",
            Tokenizer.TTSYMBOL: "<symbol> {} </symbol>",
            Tokenizer.TTNUM: "<integerConstant> {} </integerConstant>",
            Tokenizer.TTSTRING: "<stringConstant> {} </stringConstant>",
            Tokenizer.TTID: "<identifier> {} </identifier>"
        }
        return xmlmap[token.ttype].format(token.value)

    def __init__(self, instring):
        self._tokens = self._tokenize(instring)

    def hasnext(self):
        """Returns true if there is a next token."""
        return bool(self._tokens)

    def getnext(self):
        """Get the next token and remove it from the stream."""
        return self._tokens.pop(0)

    def peeknext(self, index=0):
        """Get the next token and without removing it from the stream."""
        if self._tokens:
            return self._tokens[index]
        raise IndexError("peek from empty list")

    def getnextoftype(self, ttype):
        """Get the next token if it matches 'type' and remove it from the stream.
        If next token doesn't match type, then raise Exception."""
        typechecker = {
            self.TTKEYWORD: self.nextiskeyword,
            self.TTSYMBOL: self.nextissymbol,
            self.TTNUM: self.nextisconstant,
            self.TTSTRING: self.nextisconstant,
            self.TTID: self.nextisid
        }
        if typechecker[ttype]():
            return self.getnext()
        raise Exception(f"Next token not of type {ttype}.")

    ####### Type Checkers #######
    def nextissymbol(self):
        """Returns true if there is a next token and if it is a symbol."""
        return self._tokens and self._tokens[0].ttype == self.TTSYMBOL

    def nextisconstant(self):
        """Returns true if there is a next token and if it is a num or string."""
        return self._tokens and self._tokens[0].ttype in [self.TTSTRING, self.TTNUM]

    def nextisid(self):
        """Returns true if there is a next token and if it is a id."""
        return self._tokens and self._tokens[0].ttype == self.TTID

    def nextiskeyword(self):
        """Returns true if there is a next token and if it is a keyword."""
        return self._tokens and self._tokens[0].ttype == self.TTKEYWORD

    @property
    def xml(self):
        """Get the tokens as an multiline-string
        that encloses each token by its type in an xml tag."""
        tokens = os.linesep.join([self.getxml(t) for t in self._tokens])
        return f"<tokens>\n{tokens}\n</tokens>\n"


    def _tokenize(self, string):
        string = self._removecomments(string)
        match_groups = re.findall(self.TOKEN, string)
        ttypes = [self.TTYPES[next(index for index, group in enumerate(match) if group)]
                  for match in match_groups]
        tokens = [token for token in itertools.chain(*match_groups) if token]
        return [Token(ttype, match) for ttype, match in zip(ttypes, tokens)]

    def _removecomments(self, string):
        string = re.sub(r'//.*', '', string)
        return re.sub(r'/\*.*?\*/', '', string, flags=re.S)

    def __str__(self):
        return str([str(t) for t in self._tokens])
