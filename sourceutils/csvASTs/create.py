#!/usr/bin/env python2
from sourceutils.codeTree.CodeTreeWalker import CodeTreeWalker
from CodeToCSVAST import CodeToCSVAST

import sys

def usage():
    print('usage: %s <codeTreeRoot>' % (sys.argv[0]))
        
def main(projectRoot):
   
    print('Creating ASTs in CSV format for %s' %(projectRoot))
    
    codeTreeWalker = CodeTreeWalker(projectRoot)
    codeTreeWalker.setFilenameFilterRegex('source')
    codeToCSVAST = CodeToCSVAST()
    
    for sourceFile in codeTreeWalker:
        dirForSourceFile = codeTreeWalker.getDirForFilename(sourceFile)
        codeToCSVAST.run(sourceFile)
        codeToCSVAST.save(dirForSourceFile)
  
if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        usage()
        sys.exit()
    
    projectRoot = sys.argv[1]    
    main(projectRoot)
    