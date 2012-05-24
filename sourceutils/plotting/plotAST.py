#!/usr/bin/env python2

from ASTPlotter import ASTPlotter

def main(treeFile):
    
    processor = ASTPlotter()
    processor.process(treeFile)
    
if __name__ == '__main__':
    import sys
    main(sys.argv[1])
