from src.graphs_parser import GraphMatrix
from src.graphs_parser import matrix_to_file
from src.graph_measures import BetweenessCentrality as bc

# It's exatcly the same file just to try read from multiple files
#x = GraphMatrix("../assets/6a90_network.xml", "../assets/6a90_network.xml")
# print(x.get_element(0, 3))

x = GraphMatrix.init_random_test(8, 1, 0.6)
# x.print_matrix()

paths = bc.short_paths(x)
matrix_to_file(x, paths[0], paths[1])

