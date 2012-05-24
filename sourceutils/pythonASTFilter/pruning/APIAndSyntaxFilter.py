from ParseTreeFilter import ParseTreeFilter

class APIAndSyntaxFilter(ParseTreeFilter):
    def __init__(self):
        ParseTreeFilter.__init__(self)
        nodeTypesOfInterest = ['call', 'param', 'decl', 'if', 'else',
                               'while', 'for','do', 'switch', 'return', 'break', 'continue', 'op']
        self.setNodeTypesOfInterest(nodeTypesOfInterest)
    
        