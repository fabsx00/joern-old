from ParseTreeFilter import ParseTreeFilter

class APISymbolsFilter(ParseTreeFilter):
    def __init__(self):
        ParseTreeFilter.__init__(self)
        nodeTypesOfInterest = ['decl', 'call', 'param']
        self.setNodeTypesOfInterest(nodeTypesOfInterest)
        