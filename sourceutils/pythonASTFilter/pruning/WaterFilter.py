from ParseTreeFilter import ParseTreeFilter

class WaterFilter(ParseTreeFilter):
    def __init__(self):
        ParseTreeFilter.__init__(self)
        nodeTypesOfInterest = ['water']
        self.setNodeTypesOfInterest(nodeTypesOfInterest)
        self.keepNodesOfInterest = False
        
        