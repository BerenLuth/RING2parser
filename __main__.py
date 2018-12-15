from src.graphs_parser import GraphMatrix, print_output
from src.graph_measures import GraphMeasures as measures
from src.graphs_parser import matrix_to_cache
from src.graph_measures import *

# write ALL for compute all the interactions together
INTERACTION = interaction_to_key("all")

# It's exactly the same file just to try read from multiple files
x = GraphMatrix("../assets/3rvy_van0_network.xml")
# x = GraphMatrix.init_random_test(100, 1, 0.01)

# print(x.get_element(0, 3))
# x.print_matrix()


paths = measures.short_paths(x, interaction=INTERACTION, to_file=True)

if paths is not None:
    closeness = measures.closeness(x.get_dimen(), paths[0])
    betweenness = measures.betweenness(x.get_dimen(), paths[1])
    print_output(x, closeness, betweenness, interaction=INTERACTION)
