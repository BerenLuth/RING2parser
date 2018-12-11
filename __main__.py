from src.graphs_parser import GraphMatrix
from src.graph_measures import BetweenessCentrality as bc

# It's exatcly the same file just to try read from multiple files
#x = GraphMatrix("../assets/6a90_network.xml", "../assets/6a90_network.xml")
# print(x.get_element(0, 3))

x = GraphMatrix.init_random_test(100, 2)
x.print_matrix()

#paths = bc.short_paths(x)
#print(paths)
