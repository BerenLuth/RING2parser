from src.graphs_parser import GraphMatrix
from src.graph_measures import GraphMeasures as measures
from src.graphs_parser import matrix_to_file
from src.graph_measures import *

# It's exactly the same file just to try read from multiple files
x = GraphMatrix("../assets/3rvy_van5_network.xml")
# x = GraphMatrix.init_random_test(100, 1, 0.01)

# print(x.get_element(0, 3))
# x.print_matrix()


paths = measures.short_paths(x, interaction='HBOND:MC_MC', to_file=True)
#paths = measures.short_paths(x, interaction="IONIC", to_file=True)
