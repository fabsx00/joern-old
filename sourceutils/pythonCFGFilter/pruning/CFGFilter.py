from sourceutils.pythonCFGs.CFG import CFG, BasicBlock

class CFGFilter():
    
    def __init__(self):
        self.nodeTypesOfInterest = []
        self.keepNodesOfInterest = True
        self.dontExpandNodes = []
    
    def setRow2StringConverter(self, r):
        self.row2StringConverter = r
    
    def prune(self, cfg):
        prunedCfg = CFG()
        prunedCfg.edges = cfg.edges
                
        for basicBlock in cfg.nodes:
            prunedBasicBlock = self.pruneBasicBlock(basicBlock)
            prunedCfg.addNode(prunedBasicBlock)
        
        prunedCfg.registerSuccessors()
        
        return prunedCfg
    
    def pruneBasicBlock(self, basicBlock):
        newNode = BasicBlock()
        newNode.blockType = basicBlock.blockType
        
        dontExpand = False
        dontExpandLevel = -1
        lastRowType = None
        
        for row in basicBlock.rows:
            rowType = row[0]
            rowLevel = row[3]
            if dontExpand:
                if rowLevel > dontExpandLevel:
                    continue
                else:
                    dontExpand = False
            
            
            if not self.pruneRow(row):
                rowAsString = self.row2StringConverter.convert(row)   
                
                if len(newNode.rows) > 0 and lastRowType in self.mergeRows and rowType in self.mergeRows:
                        newNode.rows[-1] += (rowAsString)
                else:
                    newNode.rows.append(rowAsString)
            
            lastRowType = rowType
            
            if rowType in self.dontExpandNodes:
                dontExpand = True
                dontExpandLevel = rowLevel    
        return newNode
    
    def pruneRow(self, row):
        return self.mustPruneRow(row)
        
    def setNodeTypesOfInterest(self, l):
        self.nodeTypesOfInterest = l
       
    def mustPruneRow(self, row):
        nodeType = row[0]
        if (len(self.nodeTypesOfInterest) == 0): return False
        if self.keepNodesOfInterest and (nodeType in self.nodeTypesOfInterest): return False
        if (not self.keepNodesOfInterest) and (not(nodeType in self.nodeTypesOfInterest)): return False 
        return True
    