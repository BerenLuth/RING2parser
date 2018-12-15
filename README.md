# RING2parser
Parser for Protein analyzer RING 2.0 (University of Padua) with basic graph measurements

## Instructions
You can launch this project in two ways:

1. Open this project in pycharm and simply launch the __\__main\__.py__ file (in the root directory of the project). 
Remember to fill variables in the beginning of  __\__main\__.py__ according to what you want to analyze, and in case of errors you can also try to adjust __cache__ and __output__ directories in __/src/graphs_parser/\__int\__.py__

2. Launch this from terminal:
    * arg[1] = position of the xml* file that represents the graph
    * arg[2] = type of interaction.
        This value can assume different values like: __ALL__ (to analyze all the interactions together) or __HBOND__, __IONIC__ and other types of interections (if they're present in the graph)


*The xml file must be the output computed from http://protein.bio.unipd.it/ring/ (you can find some of these files in __assets/__ folder)
