
import re

class Row2StringConverter():
    def __init__(self):
        pass
    
    def convert(self, row):
        return self._removeRowPosition(row)
     
    def _removeRowPositionAndType(self, row):
        return row[4:]
    
    def _removeRowPosition(self, row):
        r= [row[0]]
        r.extend(row[4:])
        return  r
    
    def extractType(self, row):
        if len(row) == 1:
            return str(row[0])
                
        typeStr = row[0]
        typeStr = re.sub('\s+\*', '*', typeStr)
        typeStr = re.sub('\*\s+', '*', typeStr)
        
        idStr = re.sub('\s+\*', '*', row[1])
        idStr = re.sub('\*\s+', '*', idStr)
        idStr = idStr.replace(' [', '[')
        m = re.search('(\*+)', idStr)
        if m:
            g = m.groups()
            typeStr += g[0]
        m = re.search('((\[.*?\])+)', idStr)
        if m:
            g= m.groups()
            typeStr += g[0]
        
        return typeStr