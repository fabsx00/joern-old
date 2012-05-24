
from CFGFilter import CFGFilter

class IdentityFilter(CFGFilter):
    def __init__(self):
        CFGFilter.__init__(self)
        nodeTypesOfInterest = []
        self.setNodeTypesOfInterest(nodeTypesOfInterest)
    
        