
from Row2StringConverter import Row2StringConverter

class IdentityRow2String(Row2StringConverter):
    def __init__(self):
        pass
    
    def convert(self, row):
        return str(self._removeRowPosition(row))
    