# RING2parser
Parser for Protein analyzer RING 2.0 (University of Padua http://protein.bio.unipd.it/ring/) with basic graph measurements such as __shortest paths__ on the graph, __betweenness centrality__ and __closeness centrality__.

## Disclamer
This project was made during bioinformatics class at Ca' Foscari University of Venice.
We tried to keep it clean and modular but it's not really ready-to-use and it requires a minimum knowledge of python.

## Usage
You can launch this project in two ways:

1. Open this project in pycharm and simply launch the __\__main\__.py__ file (in the root directory of the project). 
Remember to fill variables in the beginning of  this file according to what you want to analyze (file / interaction), and in case of errors you can also try to adjust __cache__ and __output__ directories in __/src/graphs_parser/\__int\__.py__

2. Launch this from terminal:
    * arg[1] = position of the xml* file that represents the graph
    * arg[2] = type of interaction.
        This variable can assume different values like: __ALL__ (that analyze all the interactions together combining them) or __HBOND__, __IONIC__ and other types of interections (if they're present in the graph)


*The xml file must be the output computed from http://protein.bio.unipd.it/ring/ (you can find some of these files in __assets/__ folder)

## Classes

* __GraphMatrix__ (src.graph_parser): the constructor requires file name (that must be xml file from RING) and it provides basic functions for matrix (such as reading element by position, number of nodes and others) and also a basic operation on file name to get the name of protein (as string).

## Methods

* __short_paths__ (src.graph_measures): evaluate shortest paths of a graph, return distance, predecessors (both are matrix n\*n)
   - required parameters: graph (GraphMatrix)
   - optional parameters: interaction (a string that represent the type of interaction, default value is "all"), multi_edge_function (a function that takes a list and return an int, default value is minimum, other available functions are maximum and average), to_file (bool, used to call the function matrix_to_cache, default value is false)
         
* __closeness__ (src.graph_measures): evaluate closeness of a graph, return a list of closeness value for each node
   - required parameters: n (int, it represents number of nodes of the graph), dist (distance matrix n\*n) 
         
* __betweenness__ (src.graph_measures): evaluate betweenness of a graph, return a list of betweenness value for each node
   - required parameters: n (int, it represents number of nodes of the graph), pred (predecessors matrix n\*n) 
   
* __matrix_to_cache__ (src.graph_parser): save distance and predecessor matrices (output of short_paths) to a file on cache folder
   - required parameters: graph (GraphMatrix), dist (distance matrix of the graph), pred (predecessors matrix of the graph)
   - optional parameters: interaction (string representing the type of interaction analyzed, used to build the file name and default value is empty string)

* __cache_to_matrix__ (src.graph_parser): load a file (output of matrix_to_cache) to memory
   - required parameters: graph (GraphMatrix)
   - optional parameters: interaction (string representing the type of interaction analyzed, used to build the file name and default value is empty string)
   
* __print_output__ (src.graph_parser): save the result of closeness and betweenness to a file, this is saved as .csv for an easy consultation and eventually co create graphs related to these results
   - required parameters: graph (GraphMatrix), closeness (matrix n\*n result of closeness function), betweenness (matrix n\*n result of betweenness function)
   - optional parameters: interaction (string representing the type of interaction analyzed, used to build the file name and default value is empty string)
