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

    def __init__(self, instring):
        self._tokens = self._tokenize(instring)

    def hasnext(self):
        """Returns true if there is a next token."""
        return len(self._tokens) == 0

    def getnext(self):
        """Get the next token from the string and pops it from the list."""
        return self._tokens.pop(0)

    @property
    def xml(self):
        """Get the tokens as an multiline-string
        that encloses each token by its type in an xml tag."""
        xmlmap = {
            self.TTKEYWORD: "<keyword> {} </keyword>",
            self.TTSYMBOL: "<symbol> {} </symbol>",
            self.TTNUM: "<integerConstant> {} </integerConstant>",
            self.TTSTRING: "<stringConstant> {} </stringConstant>",
            self.TTID: "<identifier> {} </identifier>"
        }
        tokens = os.linesep.join(
            [xmlmap[t.ttype].format(t.value) for t in self._tokens])
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
