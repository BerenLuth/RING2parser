from src.graphs_parser import GraphMatrix
from src.graph_measures import GraphMeasures as measures
from src.graphs_parser import matrix_to_file

# It's exactly the same file just to try read from multiple files
# x = GraphMatrix("../assets/6a90_network.xml", "../assets/6a90_network.xml")
x = GraphMatrix.init_random_test(8, 1, 0.6)

# print(x.get_element(0, 3))
# x.print_matrix()

paths = measures.short_paths(x)
matrix_to_file(x, paths[0], paths[1])

