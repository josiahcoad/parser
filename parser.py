"""Create a parse tree in xml.
    TODO: Make SYMBOL type the actual symbol
"""
from tokenizer import Tokenizer


class Parser:
    """Create a parse tree in xml."""
    INDENTAMOUNT = 4

    def __init__(self, string):
        self._tstream = Tokenizer(string)
        self._xml = []
        self._curindent = 0

    ###### Parser Methods ######
    def _class(self):
        # 'class' <className> '{' <classVarDec>* <subroutineDec>* '}'
        self._addopentag('class')
        self._tstream.addnext(Tokenizer.KEYWORD)  # class
        self._tstream.addnext(Tokenizer.ID)       # <classname>
        self._tstream.addnext(Tokenizer.SYMBOL)   # {
        while self._isclassvardec(self._tstream.peeknext()):
            self._vardec()
        while self._ismethodec(self._tstream.peeknext()):
            self._subroutinedec()
        self._tstream.addnext(Tokenizer.SYMBOL)  # }
        self._addclosetag('class')

    def _subroutinedec(self):
        #   ('constructor' | 'function' | 'method')
        #   ('void' | <type>) <subroutineName> '(' <parameterList> ')'
        #   <subroutineBody>
        self._addopentag('subroutineDec')
        self._tstream.addnext(Tokenizer.KEYWORD)
        self._tstream.addnext(Tokenizer.KEYWORD)
        self._tstream.addnext(Tokenizer.ID)
        self._tstream.addnext(Tokenizer.SYMBOL)
        # parameterList
        self._tstream.addnext(Tokenizer.SYMBOL)
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
        self._tstream.addnext(Tokenizer.KEYWORD)
        self._tstream.addnext(Tokenizer.ID)  # type
        self._tstream.addnext(Tokenizer.ID)  # varName
        while (self._tstream.peeknext() == ','):
            self._tstream.addnext(Tokenizer.SYMBOL)  # ,
            self._tstream.addnext(Tokenizer.ID)      # varName
        self._tstream.addnext(Tokenizer.SYMBOL)  # ;

    def _parameterlist(self):
        # (<type> <varName> (',' <type> <varName>)* )?
        self._addopentag('parameterList')
        self._tstream.addnext(Tokenizer.SYMBOL)  # (
        if self._tstream.peeknext() != ')':
            self._tstream.addnext(Tokenizer.ID)     # type
            self._tstream.addnext(Tokenizer.ID)     # varName
            while (self._tstream.peeknext() == ','):
                self._tstream.addnext(Tokenizer.SYMBOL)  # ,
                self._tstream.addnext(Tokenizer.ID)      # type
                self._tstream.addnext(Tokenizer.ID)      # varName
        self._tstream.addnext(Tokenizer.SYMBOL)          # )
        self._addclosetag('parameterList')

    def _subroutinebody(self):
        # '{' <varDec>* <statements> '}'
        self._addopentag('subroutineBody')
        self._tstream.addnext(Tokenizer.SYMBOL)  # {
        while self._tstream.peeknext() == 'var':
            self._vardec()
        while self._isstatement(self._tstream.peeknext()):
            self._statement()
        self._tstream.addnext(Tokenizer.SYMBOL)  # }
        self._addclosetag('subroutineBody')

    #~~~~~~ Statement Parser Methods ~~~~~~#
    def _statement(self):
        # <letStatement> | <ifStatement> | <whileStatement> |
        # <doStatement> | <returnStatement>
        methods = {
            'let': self._letstatement,
            'if': self._letstatement,
            'while': self._letstatement,
            'do': self._letstatement,
            'return': self._returnstatement,
        }
        methods[self._tstream.peeknext()]()

    def _letstatement(self):
        # 'let' <varName> ('[' <expression> ']')? '=' <expression> ';'
        self._addopentag("letStatement")
        self._tstream.addnext(Tokenizer.KEYWORD)
        self._tstream.addnext(Tokenizer.ID)
        self._tstream.addnext(Tokenizer.SYMBOL)
        if self._tstream.peeknext() == '[':
            self._tstream.addnext(Tokenizer.SYMBOL)
            self._expression()
            self._tstream.addnext(Tokenizer.SYMBOL)
        self._tstream.addnext(Tokenizer.SYMBOL)
        self._expression()
        self._tstream.addnext(Tokenizer.SYMBOL)
        self._addclosetag("letStatement")

    def _ifstatement(self):
        self._addopentag("ifStatement")
        # add
        self._addclosetag("ifStatement")

    def _whilestatement(self):
        # 'while' '(' <expression> ')' '{' statements> '}' ('else' '{' statements> '}')?
        self._addopentag("whileStatement")
        self._tstream.addnext(Tokenizer.KEYWORD)
        self._tstream.addnext(Tokenizer.SYMBOL)
        self._expression()
        self._tstream.addnext(Tokenizer.SYMBOL)
        self._tstream.addnext(Tokenizer.SYMBOL)
        self._statements()
        self._tstream.addnext(Tokenizer.SYMBOL)
        if self._tstream.peeknext() == 'else':
            self._tstream.addnext(Tokenizer.KEYWORD)
            self._tstream.addnext(Tokenizer.SYMBOL)
            self._statements()
            self._tstream.addnext(Tokenizer.SYMBOL)
        self._addclosetag("whileStatement")

    def _dostatement(self):
        # 'do' <subroutineCall> ';'
        self._tstream.addnext(Tokenizer.KEYWORD)
        self._subroutinecall()
        self._tstream.addnext(Tokenizer.SYMBOL)

    def _returnstatement(self):
        # 'return' <expression>? ';
        self._addopentag("returnStatement")
        self._tstream.addnext(Tokenizer.KEYWORD)
        if self._tstream.peeknext() != ';':
            self._expression()
        self._tstream.addnext(Tokenizer.SYMBOL)
        self._addclosetag("returnStatement")

    def _statements(self):
        # <statement>*
        self._addopentag("statements")
        while self._tstream.peeknext() != '{':
            self._statement()
        self._addclosetag("statements")

    def _expressionlist(self):
        # (<expression> (',' <expression>)* )?
        self._addopentag("expressionList")
        self._expression()
        while self._tstream.peeknext() == ',':
            self._expression()
        self._addclosetag("expressionList")

    def _expression(self):
        # <term> (<op> <term>)*
        self._addopentag("expression")
        while self._isbinaryop(self._tstream.peeknext()):
            self._addnext(Tokenizer.SYMBOL)
            self._term()
        self._addclosetag("expression")

    def _term(self):
        #   integerConstant | stringConstant | keywordConstant |
        #   <varName> | <varName> '[' <expression> ']' | <subroutineCall>
        #   | '(' <expression> ')' | unaryOp <term>
        self._addopentag("term")
        # integerConstant
        if self._tstream.peeknext().ttype == Tokenizer.INTLITERAL:
            self._tstream.addnext(Tokenizer.INTLITERAL)
        # stringConstant
        elif self._tstream.peeknext().ttype == Tokenizer.STRINGLITERAL:
            self._tstream.addnext(Tokenizer.STRINGLITERAL)
        # keywordConstant
        elif self._iskeywordconstant(self._tstream.peeknext()):
            self._tstream.addnext(Tokenizer.KEYWORD)
        # <varName> | <varName> '[' <expression> ']'
        elif self._tstream.peeknext().ttype == Tokenizer.IDENTIFIER:
            self._tstream.addnext(Tokenizer.IDENTIFIER)
            if self._tstream.peeknext() == '[':
                self._tstream.addnext(Tokenizer.SYMBOL)
                self._expression()
                self._tstream.addnext(Tokenizer.SYMBOL)
        # '(' <expression> ')'
        elif self._tstream.peeknext() == '(':
            self._tstream.addnext(Tokenizer.SYMBOL)
            self._expression()
            self._tstream.addnext(Tokenizer.SYMBOL)
        # unaryOp <term>
        elif self._isunaryop(self._tstream.peeknext()):
            self._tstream.addnext(Tokenizer.SYMBOL)
            self._term()
        # <subroutineCall>
        else:
            self._subroutinecall()
        self._addclosetag("term")

    def _subroutinecall(self):
        # <subroutineName> '(' <expressionList> ')' |
        # (<className>|<varName>) '.' <subroutineName> '(' <expressionList> ')'
        self._tstream.addnext(Tokenizer.IDENTIFIER)
        if self._tstream.peeknext() == '.':
            self._tstream.addnext(Tokenizer.SYMBOL)
            self._tstream.addnext(Tokenizer.IDENTIFIER)
        self._tstream.addnext(Tokenizer.SYMBOL)
        self._expressionlist()
        self._tstream.addnext(Tokenizer.SYMBOL)

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
        return token in ['+', '-', '*', '/', '&', ',', '<', '>', '=']

    def _iskeywordconstant(self, token):
        return token in ['true', 'false', 'null', 'this']

    ###### XML Output Methods ######

    def _addnext(self, ttype):
        self._addleveltoken(self._tstream.getnextoftype(ttype))

    def _addleveltoken(self, token):
        self._xml.append(self._tstream.getxml(token))

    def _addopentag(self, token):
        pass

    def _addclosetag(self, token):
        pass

    def _incindent(self):
        self._curindent += 1

    def _decindent(self):
        self._curindent -= 1

    def _getindent(self):
        return ' ' * self.INDENTAMOUNT * self._curindent

    # def tagwrap(tag):
    #     def decorated(f):
    #         def wrapper(*args, **kwargs):
    #             self._addopentag(tag)
    #             f(*args, **kwargs)
    #             self._addclosetag(tag)
    #         return wrapper
    #     return decorated


# class A:
#     def _addopentag(self, tag):
#         print("_addopentag " + tag)

#     def _addclosetag(self, tag):
#         print("_addclosetag " + tag)

#     def tagwrap(self, tag):
#         def decorated(f):
#             def wrapper(*args, **kwargs):
#                 self._addopentag(tag)
#                 f(*args, **kwargs)
#                 self._addclosetag(tag)
#             return wrapper
#         return decorated

#     @tagwrap("cool")
#     def printme():
#         print("me")