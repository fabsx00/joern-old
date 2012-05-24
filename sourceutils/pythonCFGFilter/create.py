#!/usr/bin/env python2
from sourceutils.codeTree.CodeTreeWalker import CodeTreeWalker
from PythonCFGToPrunedCFG import PythonCFGToPrunedCFG

import sys

def usage():
    print('usage: %s <codeTreeRoot>' % (sys.argv[0]))
        
def main(projectRoot, f, r):
   
    print('Creating filtered CFGs for %s' %(projectRoot))
    
    codeTreeWalker = CodeTreeWalker(projectRoot)
    codeTreeWalker.setFilenameFilterRegex('cfg.pickl')
    
    for cfgFilename in codeTreeWalker:
        processor = PythonCFGToPrunedCFG()
        
        processor.setFilter(f)
        processor.setRow2StringConverter(r)
        
        processor.applyFilterToNodes(cfgFilename)
        processor.save()
        
          
if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        usage()
        sys.exit()
    
    projectRoot = sys.argv[1]    
    main(projectRoot)
    