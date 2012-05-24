import re, os

dot = 'dot -Tpng %s -o %s'
dotFilename = '.tmp.dot'
outputFilename = '.tmp.png'
viewer = 'eog %s'

class DotDrawer:

    def beginDraw(self):
        if os.path.exists(dotFilename):
            os.remove(dotFilename)
        if os.path.exists(outputFilename):
            os.remove(outputFilename)
        self.outfile = file(dotFilename, 'w')
        self.nodeCounter = 0
   
    def drawHeader(self):
        self.outfile.write('digraph myGraph{')
        # self.outfile.write('rankdir=LR;')
        # self.outfile.write('splines=false;')
        # self.outfile.write('overlap=false;')
        self.outfile.write('node [shape=box];\n\n')        
    
    def drawNode(self, name, url, color, style='', fontColor='black'):
        name = self.cleanUpSignature(name)
        nodeId = 'node%d' % (self.nodeCounter)
        
        self.outfile.write('%s [label="%s" URL="%s" style="%s" fillcolor="%s" fontcolor="%s"]\n'
                           % (nodeId, name, url, style, color, fontColor))

        self.nodeCounter += 1
        return nodeId

    def drawLink(self, source, dest, label = None):
        if label == None: label = ''
        source = self.cleanUpSignature(source)
        dest = self.cleanUpSignature(dest)
        label = self.cleanUpSignature(label)
        self.outfile.write('"%s":s->"%s":n [ label="%s"] ;\n' % (source, dest, label))

    def drawFooter(self):
        self.outfile.write('}')

    def cleanUpSignature(self, signature):
        signature = signature.replace('"', '\\"')
        
        signature = signature.replace('\n', '')
        signature = signature.replace('\t', '')
        signature = re.sub('[ ]+', ' ', signature)
        signature = signature.replace(';', ';\\n')
        # signature = signature.replace('(', '\\n(', 1)
        # signature = signature.replace(',', ',\\n')
        return signature
    
    def endDraw(self):
        self.outfile.close()
        os.system(dot % (dotFilename, outputFilename))
        os.system(viewer % (outputFilename))
