
from sourceutils.pythonASTFilter.PythonPrunedASTProcessor import PythonPrunedASTProcessor
from DotDrawer import DotDrawer

class ASTPlotter(PythonPrunedASTProcessor):
    def __init__(self):
        PythonPrunedASTProcessor.__init__(self)
        self.drawer = DotDrawer()
        
    def handlePrunedTree(self):
        
        prunedTree = self.tree
        
        self.drawer.beginDraw()
        self.drawer.drawHeader()
        self._traverseFunction(prunedTree)
        self.drawer.drawFooter()
        self.drawer.endDraw()
                
    def _traverseFunction(self, node):
        
        rootNodeLabel = str(node.row)
        if rootNodeLabel.find('[\'water') == 0:
            style = 'dashed'
            fontColor = 'grey'
        else:
            style=''
            fontColor = 'black'
            
        rootNodeId = self.drawer.drawNode(rootNodeLabel, 'http://foo', 'white', style, fontColor)
        for child in node.children:
            childNodeId = self._traverseFunction(child)
            self.drawer.drawLink(rootNodeId, childNodeId)
        
        return rootNodeId
        