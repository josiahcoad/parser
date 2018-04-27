#pylint: skip-file
from tokenizer import Tokenizer


class Parser:
    INDENTAMOUNT = 4

    def __init__(self, string):
        self.tokens = Tokenizer(string)

    ###### Parser Methods ######

    def _ifstatement():
        pass

    def _returnstatement():
        pass

    def _statement():
        pass

    def _whilestatement():
        pass

    def _dostatement():
        pass

    def _subroutinedec():
        pass

    def _vardec():
        pass

    def _subroutinebody():
        pass

    def _statementlist():
        pass

    def _expressionlist():
        pass

    def _letstatement():
        pass

    def _expression():
        pass

    def _term():
        pass

    ###### Helper Methods ######
    
    def _getleveltag():
        pass

    def _getopentag():
        pass

    def getclosetag():
        pass

    def _incindent():
        self._curindent += 1

    def _decindent():
        self._curindent -= 1

    def _getindent():
        return ' ' * self.INDENTAMOUNT * self._curindent
