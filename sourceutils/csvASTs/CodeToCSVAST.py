import subprocess

AST_FILENAME = 'ast.csv'

class CodeToCSVAST:
    
    def __init__(self):
        self.codeSensorLocation = None
    
    def run(self, filename):
        self._runCodeSensorOnFile(filename)
    
    def _runCodeSensorOnFile(self, filename):
        
        if not self.codeSensorLocation:
            self.codeSensorLocation = '/'.join(__file__.split('/')[:-1]) + '/' + 'CodeSensor.jar'
        self.out = subprocess.Popen( ['java', '-jar', self.codeSensorLocation,
                                 '%s' % (filename)],
                               stdout=subprocess.PIPE).communicate()[0]

    def save(self, dirForSourceFile):
        f = open(dirForSourceFile + '/' + AST_FILENAME, 'wb')
        f.write(self.out)
        f.close()
