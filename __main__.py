from src.graphs_parser import GraphMatrix
from src.graph_measures import GraphMeasures as measures
from src.graphs_parser import matrix_to_cache
from src.graph_measures import *

# It's exactly the same file just to try read from multiple files
x = GraphMatrix("../assets/3rvy_van0_network.xml")
# x = GraphMatrix.init_random_test(100, 1, 0.01)

# print(x.get_element(0, 3))
# x.print_matrix()


paths = measures.short_paths(x, interaction='HBOND', to_file=True)

if paths is not None:
    print(measures.betweenness(x.get_dimen(), paths[1]))

'''
paths = measures.short_paths(x, interaction='VDW', to_file=True)

paths = measures.short_paths(x, interaction='IAC', to_file=True)

paths = measures.short_paths(x, interaction='IONIC', to_file=True)
#paths = measures.short_paths(x, interaction="IONIC", to_file=True)
'''
