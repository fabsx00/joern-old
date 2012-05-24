
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
    
    def getTypeAndIdentifier(self, row):
        
        if len(row) == 1:
            return (row[0], '')
                
        typeStr = row[0]
        idStr = row[1]
        
        typeStr = re.sub('\s+\*', '*', typeStr)
        typeStr = re.sub('\*\s+', '*', typeStr)
        typeStr = typeStr.replace(' [', '[')
        idStr = re.sub('\s+\*', '*', idStr)
        idStr = re.sub('\*\s+', '*', idStr)
        idStr = idStr.replace(' [', '[')
        
        m = re.search('((\[.*\])+)', idStr)
        if m:
            
            for ins in m.groups(0):
                typeStr += ins
            
            idStr = re.sub(('((\[.*\])+)'), '', idStr)  
        
        m = re.search('(\*+)', idStr)
        
        if m:
            for ins in m.groups(0):
                typeStr += ins
            idStr = re.sub('(\*+)', '', idStr)  

        return (typeStr.strip(), idStr.strip())