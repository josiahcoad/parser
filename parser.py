"""Create a parse tree in xml.
    TODO: Make SYMBOL type the actual symbol
"""
import os
from tokenizer import Tokenizer


class Parser:
    """Create a parse tree in xml."""
    INDENTAMOUNT = 2

    def __init__(self, string):
        self._tstream = Tokenizer(string)
        self._xml = []
        self._curindent = 0
        self._class()

    @property
    def xml(self):
        """Get the parse tree xml as a formatted string."""
        return os.linesep.join(self._xml) + os.linesep

    ###### Parser Methods ######
    def _class(self):
        # 'class' <className> '{' <classVarDec>* <subroutineDec>* '}'
        self._addopentag('class')
        self._addnext(Tokenizer.TTKEYWORD)  # class
        self._addnext(Tokenizer.TTID)       # <classname>
        self._addnext(Tokenizer.TTSYMBOL)   # {
        while self._isclassvardec(self._tstream.peeknext()):
            self._classvardec()
        while self._ismethodec(self._tstream.peeknext()):
            self._subroutinedec()
        self._addnext(Tokenizer.TTSYMBOL)  # }
        self._addclosetag('class')

    def _subroutinedec(self):
        #   ('constructor' | 'function' | 'method')
        #   ('void' | <type>) <subroutineName> '(' <parameterList> ')'
        #   <subroutineBody>
        self._addopentag('subroutineDec')
        self._addnext(Tokenizer.TTKEYWORD)
        # type as a user defined type
        if self._tstream.peeknext().ttype == Tokenizer.TTID:
            self._addnext(Tokenizer.TTID)
        # type as a primitive type
        else:
            self._addnext(Tokenizer.TTKEYWORD)
        self._addnext(Tokenizer.TTID)
        self._addnext(Tokenizer.TTSYMBOL)
        self._parameterlist()
        self._addnext(Tokenizer.TTSYMBOL)
        self._subroutinebody()
        self._addclosetag('subroutineDec')

    def _vardec(self):
        # 'var' <type> <varName> (',' <varName>)* ';'
        self._addopentag('varDec')
        self._commonvardec()
        self._addclosetag('varDec')

    def _classvardec(self):
        # '(' ('static' | 'field') <type> <varName> (',' <varName>)* ';'
        self._addopentag('classVarDec')
        self._commonvardec()
        self._addclosetag('classVarDec')

    def _commonvardec(self):
        # only meant to be called by _classvardec or _vardec!
        self._addnext(Tokenizer.TTKEYWORD)
        # type as a user defined type
        if self._tstream.peeknext().ttype == Tokenizer.TTID:
            self._addnext(Tokenizer.TTID)
        # type as a primitive type
        else:
            self._addnext(Tokenizer.TTKEYWORD)
        self._addnext(Tokenizer.TTID)  # varName
        while self._tstream.peeknext() == ',':
            self._addnext(Tokenizer.TTSYMBOL)  # ,
            self._addnext(Tokenizer.TTID)      # varName
        self._addnext(Tokenizer.TTSYMBOL)  # ;

    def _parameterlist(self):
        # (<type> <varName> (',' <type> <varName>)* )?
        self._addopentag('parameterList')
        if self._tstream.peeknext() != ')':
            # type as a user defined type
            if self._tstream.peeknext().ttype == Tokenizer.TTID:
                self._addnext(Tokenizer.TTID)
            # type as a primitive type
            else:
                self._addnext(Tokenizer.TTKEYWORD)
            self._addnext(Tokenizer.TTID)     # varName
            while self._tstream.peeknext() == ',':
                self._addnext(Tokenizer.TTSYMBOL)  # ,
                # type as a user defined type
                if self._tstream.peeknext().ttype == Tokenizer.TTID:
                    self._addnext(Tokenizer.TTID)
                # type as a primitive type
                else:
                    self._addnext(Tokenizer.TTKEYWORD)
                self._addnext(Tokenizer.TTID)      # varName
        self._addclosetag('parameterList')

    def _subroutinebody(self):
        # '{' <varDec>* <statements> '}'
        self._addopentag('subroutineBody')
        self._addnext(Tokenizer.TTSYMBOL)  # {
        while self._tstream.peeknext() == 'var':
            self._vardec()
        self._statements()
        self._addnext(Tokenizer.TTSYMBOL)  # }
        self._addclosetag('subroutineBody')

    #~~~~~~ Statement Parser Methods ~~~~~~#
    def _statement(self):
        # <letStatement> | <ifStatement> | <whileStatement> |
        # <doStatement> | <returnStatement>
        methods = {
            'let': self._letstatement,
            'if': self._ifstatement,
            'while': self._whilestatement,
            'do': self._dostatement,
            'return': self._returnstatement,
        }
        methods[self._tstream.peeknext().value]()

    def _letstatement(self):
        # 'let' <varName> ('[' <expression> ']')? '=' <expression> ';'
        self._addopentag("letStatement")
        self._addnext(Tokenizer.TTKEYWORD)
        self._addnext(Tokenizer.TTID)
        if self._tstream.peeknext() == '[':
            self._addnext(Tokenizer.TTSYMBOL)
            self._expression()
            self._addnext(Tokenizer.TTSYMBOL)
        self._addnext(Tokenizer.TTSYMBOL)
        self._expression()
        self._addnext(Tokenizer.TTSYMBOL)
        self._addclosetag("letStatement")

    def _ifstatement(self):
        # 'if' '(' <expression> ')' '{' statements> '}'
        # ('else' '{' statements> '}')?
        self._addopentag("ifStatement")
        self._addnext(Tokenizer.TTKEYWORD)
        self._addnext(Tokenizer.TTSYMBOL)
        self._expression()
        self._addnext(Tokenizer.TTSYMBOL)
        self._addnext(Tokenizer.TTSYMBOL)
        self._statements()
        self._addnext(Tokenizer.TTSYMBOL)
        if self._tstream.peeknext() == 'else':
            self._addnext(Tokenizer.TTKEYWORD)
            self._addnext(Tokenizer.TTSYMBOL)
            self._statements()
            self._addnext(Tokenizer.TTSYMBOL)
        self._addclosetag("ifStatement")

    def _whilestatement(self):
        # 'while' '(' <expression> ')' '{' <statements> '}' ('else' '{' statements> '}')?
        self._addopentag("whileStatement")
        self._addnext(Tokenizer.TTKEYWORD)
        self._addnext(Tokenizer.TTSYMBOL)
        self._expression()
        self._addnext(Tokenizer.TTSYMBOL)
        self._addnext(Tokenizer.TTSYMBOL)
        self._statements()
        self._addnext(Tokenizer.TTSYMBOL)
        if self._tstream.peeknext() == 'else':
            self._addnext(Tokenizer.TTKEYWORD)
            self._addnext(Tokenizer.TTSYMBOL)
            self._statements()
            self._addnext(Tokenizer.TTSYMBOL)
        self._addclosetag("whileStatement")

    def _dostatement(self):
        # 'do' <subroutineCall> ';'
        self._addopentag("doStatement")
        self._addnext(Tokenizer.TTKEYWORD)
        self._subroutinecall()
        self._addnext(Tokenizer.TTSYMBOL)
        self._addclosetag("doStatement")

    def _returnstatement(self):
        # 'return' <expression>? ';
        self._addopentag("returnStatement")
        self._addnext(Tokenizer.TTKEYWORD)
        if self._tstream.peeknext() != ';':
            self._expression()
        self._addnext(Tokenizer.TTSYMBOL)
        self._addclosetag("returnStatement")

    def _statements(self):
        # <statement>*
        self._addopentag("statements")
        while self._isstatement(self._tstream.peeknext()):
            self._statement()
        self._addclosetag("statements")

    def _expressionlist(self):
        # (<expression> (',' <expression>)* )?
        self._addopentag("expressionList")
        if self._tstream.peeknext() != ')':
            self._expression()
        while self._tstream.peeknext() == ',':
            self._addnext(Tokenizer.TTSYMBOL)
            self._expression()
        self._addclosetag("expressionList")

    def _expression(self):
        # <term> (<op> <term>)*
        self._addopentag("expression")
        self._term()
        while self._isbinaryop(self._tstream.peeknext()):
            self._addnext(Tokenizer.TTSYMBOL)
            self._term()
        self._addclosetag("expression")

    def _term(self):
        #   integerConstant | stringConstant | keywordConstant |
        #   <varName> | <varName> '[' <expression> ']' | <subroutineCall>
        #   | '(' <expression> ')' | unaryOp <term>
        self._addopentag("term")
        # integerConstant
        if self._tstream.peeknext().ttype == Tokenizer.TTNUM:
            self._addnext(Tokenizer.TTNUM)
        # stringConstant
        elif self._tstream.peeknext().ttype == Tokenizer.TTSTRING:
            self._addnext(Tokenizer.TTSTRING)
        # keywordConstant
        elif self._iskeywordconstant(self._tstream.peeknext()):
            self._addnext(Tokenizer.TTKEYWORD)
        # <varName> | <varName> '[' <expression> ']' | <subroutineCall>
        elif self._tstream.peeknext().ttype == Tokenizer.TTID:
            # <subroutineCall>
            if self._tstream.peeknext(1) in ['(', '.']:
                self._subroutinecall()
            # <varName> | <varName> '[' <expression> ']'
            else:
                self._addnext(Tokenizer.TTID)
                # '[' <expression> ']'
                if self._tstream.peeknext() == '[':
                    self._addnext(Tokenizer.TTSYMBOL)
                    self._expression()
                    self._addnext(Tokenizer.TTSYMBOL)
        # '(' <expression> ')'
        elif self._tstream.peeknext() == '(':
            self._addnext(Tokenizer.TTSYMBOL)
            self._expression()
            self._addnext(Tokenizer.TTSYMBOL)
        # unaryOp <term>
        elif self._isunaryop(self._tstream.peeknext()):
            self._addnext(Tokenizer.TTSYMBOL)
            self._term()
        self._addclosetag("term")

    def _subroutinecall(self):
        # <subroutineName> '(' <expressionList> ')' |
        # (<className>|<varName>) '.' <subroutineName> '(' <expressionList> ')'
        self._addnext(Tokenizer.TTID)
        if self._tstream.peeknext() == '.':
            self._addnext(Tokenizer.TTSYMBOL)
            self._addnext(Tokenizer.TTID)
        self._addnext(Tokenizer.TTSYMBOL)
        self._expressionlist()
        self._addnext(Tokenizer.TTSYMBOL)

    ###### Type Checkers ######

    def _isclassvardec(self, token):
        return token in ['field', 'static']

    def _ismethodec(self, token):
        return token in ['constructor', 'function', 'method']

    def _isstatement(self, token):
        return token in ['while', 'if', 'let', 'do', 'return']

    def _isunaryop(self, token):
        return token in ['-', '~']

    def _isbinaryop(self, token):
        return token in ['+', '-', '*', '/', '&', '<', '>', '=', '|']

    def _iskeywordconstant(self, token):
        return token in ['true', 'false', 'null', 'this']

    ###### XML Output Methods ######

    def _addnext(self, ttype):
        self._addleveltoken(self._tstream.getnextoftype(ttype))

    def _addleveltoken(self, token):
        # only to be called by _addnext
        self._xml.append(self._getindent() + self._tstream.getxml(token))

    def _addopentag(self, tag):
        self._xml.append(self._getindent() + "<" + tag + ">")
        self._incindent()

    def _addclosetag(self, tag):
        self._decindent()
        self._xml.append(self._getindent() + "</" + tag + ">")

    def _incindent(self):
        self._curindent += 1

    def _decindent(self):
        self._curindent -= 1

    def _getindent(self):
        return ' ' * self.INDENTAMOUNT * self._curindent
