from .ParseTreeFilter import ParseTreeFilter

class IdentityFilter(ParseTreeFilter):
    def __init__(self):
        ParseTreeFilter.__init__(self)
        nodeTypesOfInterest = []
        self.setNodeTypesOfInterest(nodeTypesOfInterest)
    
        