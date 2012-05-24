#!/usr/bin/env python2
import sys
import pickle

from DotDrawer import DotDrawer

def main(treeFile):
    
    import sourceutils.pythonCFGs.CFG as CFG #@UnusedImport
    tree = pickle.load(open(treeFile))
    
    drawer = DotDrawer()
    drawer.beginDraw()
    drawer.drawHeader()
        
    for node in tree.nodes:
        
        nodeText = "\\n".join([str(r) for r in node.rows])
        drawer.drawNode(nodeText, '', 'white')
     
    for (src, dst, predicate) in tree.edges:
        src = 'node%d' % (src)
        dst = 'node%d' %(dst) 
        drawer.drawLink(src, dst, predicate)
     
    drawer.drawFooter()
    drawer.endDraw()

if __name__ == '__main__':
    treeFile = sys.argv[1]
    main(sys.argv[1])