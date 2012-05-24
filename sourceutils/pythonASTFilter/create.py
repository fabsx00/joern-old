#!/usr/bin/env python2


from PythonASTToPrunedAST import PythonASTToPrunedAST
from sourceutils.codeTree.CodeTreeWalker import CodeTreeWalker

def main(projectRoot, nodeFilter, row2StringConverter):

    codeTreeWalker = CodeTreeWalker(projectRoot)
    codeTreeWalker.setFilenameFilterRegex('ast\.pickl$')
    processor = PythonASTToPrunedAST()
    
    processor.setFilter(nodeFilter)
    processor.setRow2StringConverter(row2StringConverter)
       
    for pythonASTFilename in codeTreeWalker:
        processor.loadTreeFromFile(pythonASTFilename)
        processor.processChildren()
   
if __name__ == '__main__':
    main()