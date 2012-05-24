from distutils.core import setup

files = ["sourceutils/*"]

setup(name = "lain",
    version = "0.0.1",
    description = "Lain is a collection of command line tools enabling development of language aware code analysis tools for C/C++ even when only parts of the source code are available.",
    author = "Fabian Yamaguchi",
    author_email = "fabs@phenoelit.de",
    url = "http://codeexploration.blogspot.de",
    packages = ['sourceutils'],
    package_data = {'sourceutils' : files },
    scripts = ["lain_filter_asts", "lain_filter_cfgs", "lain_index", "lain_parse", "lain_plot"],
    # long_description = """Really long text here.""" 
    
    #classifiers = []     
) 