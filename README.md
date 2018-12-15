# RING2parser
Parser for Protein analyzer RING 2.0 (University of Padua) with basic graph measurements

## Instructions
You can launch this project in two ways:

1. Open this project in pycharm and simply launch the \__main\__.py file (in the root directory of the project). 
Remember to fill variables in the beginning of  \__main\__.py according to what you want to analyze, and in case of errors you can also try to adjust cache and output directories in /arc/graphs_parser/\__int\__.py

2. Launch this from terminal:
    * arg[1] = position of the xml file that represents the graph
    * arg[2] = type of interaction.
        This value can assume different values like: ALL (to analyze all the interactions together) or HBOND, IONIC and other types of interections (if present in the graph)
