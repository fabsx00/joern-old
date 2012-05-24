
from Row2StringConverter import Row2StringConverter

class CFGRow2String(Row2StringConverter):
    def __init__(self):
        self.structureNodes = ['if', 'for', 'while', 'do', 'switch', 'break', 'return', 'continue',
                               'else', 'params', 'goto', 'label', 'call', 'arg', 'cond']
        
    def convert(self, row):
        rowType = row[0]
        if rowType in self.structureNodes:
            rowContent = self._removeRowPositionAndType(row)
            return row[0]+ ": " + str(''.join(rowContent))
        else:
            rowContent = self._removeRowPositionAndType(row)
            if rowType in ['decl', 'param']:
                (declType, declIdentifier) = self.getTypeAndIdentifier(rowContent)
                return rowType + ': ' + declType + ',' + declIdentifier
                # return self.extractType(rowContent)
            else: # op, else
                return str(''.join(rowContent))
            