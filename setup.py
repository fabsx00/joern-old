from distutils.core import setup

files = ["sourceutils/*"]

setup(name = "lain",
    version = "0.0.1",
    description = "Lain is a collection of command line tools enabling development of language aware code analysis tools for C/C++ even when only parts of the source code are available.",
    author = "Fabian Yamaguchi",
    author_email = "fabs@phenoelit.de",
    url = "http://codeexploration.blogspot.de",
    packages = ['sourceutils', 'sourceutils/codeIndex', 'sourceutils/codeTree',
                'sourceutils/csvASTs', 'sourceutils/misc', 'sourceutils/plotting',
                'sourceutils/pythonASTFilter', 'sourceutils/pythonASTFilter/pruning', 'sourceutils/pythonASTFilter/pruning/row2string',  
                'sourceutils/pythonCFGFilter', 'sourceutils/pythonCFGFilter/pruning', 'sourceutils/pythonCFGFilter/pruning/row2string',  
                'sourceutils/pythonASTs', 'sourceutils/pythonCFGs'                
],
    package_data = {'sourceutils' : files , 'sourceutils/csvASTs' : ['CodeSensor.jar']},
    scripts = ["lain_filter_asts", "lain_filter_cfgs", "lain_index", "lain_parse", "lain_plot"],
    # long_description = """Really long text here.""" 
    
    #classifiers = []     
) 
