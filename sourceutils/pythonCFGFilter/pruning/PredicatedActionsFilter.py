from CFGFilter import CFGFilter

class PredicatedActionsFilter(CFGFilter):
    def __init__(self):
        CFGFilter.__init__(self)
        nodeTypesOfInterest = ['call', 'param', 'decl', 'if', 'else',
                               'while', 'for','do', 'switch', 'return', 'break',
                               'continue', 'arg', 'goto', 'label', 'water', 'op']
        
        self.setNodeTypesOfInterest(nodeTypesOfInterest)
        
        self.dontExpandNodes = ['arg', 'goto', 'cond', 'return']
        self.mergeRows = ['water', 'op']
