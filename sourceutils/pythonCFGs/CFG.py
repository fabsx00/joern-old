
from sourceutils.csvASTs.CSVRowAccessors import getCSVRowCondition

class CFG:
    def __init__(self):
        self.nodes = list() # list of basic blocks
        self.edges = list() # (src,dst)-pairs
        self.labeledNodes = list() # list of (id, row) pairs
    
    # returns the ID
    def addNode(self, s):
        self.nodes.append(s)
        return len(self.nodes) - 1

    def addEdge(self, src, dst, predicate = None):
        self.edges.append((src, dst, predicate))

    def removeEdgesFrom(self, src):
        for i in xrange(len(self.edges)):
            if self.edges[i][0] == src:
                del self.edges[i]
                return
    
    def removeEdge(self, src, dst):
        
        for i in xrange(len(self.edges)):
            if self.edges[i][0] == src and self.edges[i][1] == dst:
                del self.edges[i]
                return
        
    def getNodeById(self, i):
        return self.nodes[i]
    
    def getCurrentNodeId(self):
        return len(self.nodes) - 1

    def appendToLatestNode(self, s):
        lastBasicBlock = self.nodes[-1]
        lastBasicBlock.rows.append(s)
    
    def registerSuccessors(self):
        for (src, dst, pred) in self.edges:
            self.nodes[src].successors.append((dst,pred))
      
        
class BasicBlock:
    def __init__(self, firstRow = None):
        self.rows =list()
        if firstRow:
            self.rows.append(firstRow)
        
        self.successors = []
      
        self.blockType = ''
      
      
    def getLastInstrType(self):
        return self.rows[-1][0]
    
    def getCondition(self):
        return getCSVRowCondition(self.rows[0])
        