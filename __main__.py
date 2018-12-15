import sys

from src.graphs_parser import GraphMatrix, print_output
from src.graph_measures import GraphMeasures as measures
from src.graph_measures import *

### VARIABLE INITIALIZATION

# FILL THESE FIELDS BEFORE EXECUTION (Or pass them as args from terminal)
FILE_NAME = "../assets/3rvy_van0_network.xml"
INTERACTION = "ALL"   # This can assume values like ALL, HBOND, IONIC

# TERMINAL ARGUMENTS
if len(sys.argv) == 3:
    FILE_NAME = sys.argv[1]
    INTERACTION = sys.argv[2]



### MAIN ###

# It's exactly the same file just to try read from multiple files
x = GraphMatrix(FILE_NAME)

interaction = interaction_to_key(INTERACTION)
paths = measures.short_paths(x, interaction=interaction, to_file=True)

if paths is not None:
    closeness = measures.closeness(x.get_dimen(), paths[0])
    betweenness = measures.betweenness(x.get_dimen(), paths[1])
    print_output(x, closeness, betweenness, interaction=interaction)

