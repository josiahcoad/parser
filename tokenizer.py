# pylint: disable=missing-docstring
"""
Tokenizer takes an string and provides an API to access the tokens
of the string in order they are in the string. A token is an
object with a type and value.
"""
import re
import itertools


class Token:
    """A token is an object with a type and value."""
    def __init__(self, ttype, value):
        self.ttype = ttype
        self.value = value

    def __str__(self):
        return str((self.ttype, self.value))


class Tokenizer():
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

    def __init__(self, instring):
        """
        @param string: tokenize this string
        """
        self.tokens = self._tokenize(instring)

    def hasnext(self):
        """Returns true if there is a next token."""
        return len(self.tokens) == 0

    def getnext(self):
        """Get the next token from the string and pops it from the list."""
        return self.tokens.pop(0)

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
        return str([str(t) for t in self.tokens])
