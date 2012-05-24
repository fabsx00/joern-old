#!/usr/bin/env python2
from sourceutils.codeTree.CodeTreeWalker import CodeTreeWalker
from CodeIndexCreator import CodeIndexCreator
import sys

def usage():
    print('usage: %s <codeTreeRoot>' % (sys.argv[0]))

def main(projectRoot):
   
    print('Creating index for %s' %(projectRoot))
    
    codeTreeWalker = CodeTreeWalker(projectRoot)
    codeTreeWalker.setFilenameFilterRegex('ast\.(csv)$')
    processor = CodeIndexCreator()
   
    for csvFilename in codeTreeWalker:
        processor.processCSVRows(csvFilename)
    processor.saveResults(projectRoot)
    
if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        usage()
        sys.exit()
    
    projectRoot = sys.argv[1]    
    main(projectRoot)
    