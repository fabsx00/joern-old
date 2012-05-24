
from Row2StringConverter import Row2StringConverter
from sourceutils.pythonASTFilter.pruning.ParseTreeFilter import PRUNED

class DefaultRow2String(Row2StringConverter):
    def __init__(self):
        self.structureNodes = ['if', 'for', 'while', 'do', 'switch', 'break', 'return', 'continue',
                               'else', 'params', 'cond']
        
    def convert(self, row):
        rowType = row[0]
        if rowType in self.structureNodes:
            return str(row[0])
        elif rowType == PRUNED:
            return PRUNED
        else:
            rowContent = self._removeRowPositionAndType(row)
            # handle decl, param and call
            if rowType in ['decl', 'param']:
                return rowType + ' ' + self.extractType(rowContent)
                # return self.extractType(rowContent)
            else: # op, else
                return str(''.join(rowContent))
            