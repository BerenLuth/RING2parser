from bs4 import BeautifulSoup as Soup
import numpy as np
import time
import random

WEIGHT_ENERGY = "e_Energy"
WEIGHT_DISTANCE = "e_Distance"



class GraphMatrix:

    # If you don't pass any parameter it'll load the default file included in this repo
    def __init__(self, *files):
        if len(files) == 0:
            print("You need to give at least one xml file in input")
            return

        start_time = time.time()

        parsed = []
        nodes = 0

        for file in files:
            print("Loagind matrix from file:", file)

            xml = open(file, "r").read()
            xml = Soup(xml, 'lxml')
            parsed.append(xml)

            if nodes == 0:
                nodes = len(xml.find_all("node"))
            else:
                if nodes != len(xml.find_all("node")):
                    print("Error: files have different number of nodes!")
                    return

        self.file_names = files
        self.nodes = nodes
        self.matrix = np.zeros((self.nodes, self.nodes, len(files)))
        self.edges = []
        self.N_floors = len(files)

        # initialize matrix with a really big int for floyd-warshall
        self.initialize_matrix()

        floor = 0
        for xml in parsed:
            edges = xml.find_all("edge")
            self.edges.append(len(edges))

            for edge in edges:
                # print(edge['source'], edge['target'])
                src = int(edge['source'][1:])
                trg = int(edge['target'][1:])

                # Choose between DISTANCE or ENERGY
                weight = float(edge.find(key=WEIGHT_DISTANCE).get_text())
                self.matrix[src][trg][floor] = weight
            floor += 1

        self.print_info()
        print("**************************************\nTotal loading time: ", time.time() - start_time, "\n")

    def init_test(self):
        return GraphMatrix("../assets/6a90_network.xml")

    @staticmethod
    def init_random_test(nodes, floors, density=0.1):
        graph = GraphMatrix()
        graph.file_names = ["test"]
        graph.nodes = nodes
        graph.N_floors = floors
        graph.matrix = np.zeros((nodes, nodes, floors))
        graph.edges = [0]*floors

        # initialize matrix with a really big int for floyd-warshall
        graph.initialize_matrix()

        for r in range(nodes):
            for c in range(nodes):
                for f in range(floors):
                    if r == c:
                        graph.matrix[r][c][f] = 0
                    else:
                        if random.random() < density:
                            graph.matrix[r][c][f] = random.randint(1, 10)
                            graph.edges[f] += 1

        return graph

    def print_matrix(self):
        print(self.matrix)

    def get_element(self, row, col):
        return self.matrix[row][col]

    def get_dimen(self):
        return self.nodes

    def name(self):
        return self.file_names[0]

    def print_info(self):
        n_edges = 0
        for edge in self.edges:
            n_edges += edge
        print("# Nodes:\t", self.nodes, "\n# Floors:\t", self.N_floors, "\n# Edges:\t", n_edges)

    def initialize_matrix(self):
        for row in range(self.nodes):
            for col in range(self.nodes):
                for floor in range(self.N_floors):
                    self.matrix[row][col][floor] = 100000.0


def matrix_to_file(graph: GraphMatrix, dist, pred):
    # print("Not implemented yet")

    n = graph.nodes
    file = open("../output/" + str(graph.name()) + ".txt", "w")
    file.write("Original filename: " + str(graph.name()) + "\tNodes: " + str(n) + "\tOriginal/Distance/Predecessors")

    file.write("\n")
    for r in range(n):
        for c in range(n):
            file.write(str(graph.matrix[r][c]) + "\t")
        file.write("\n")

    file.write("\n")
    for r in range(n):
        for c in range(n):
            file.write(str(dist[r][c]) + "\t")
        file.write("\n")

    file.write("\n")
    for r in range(n):
        for c in range(n):
            file.write(str(pred[r][c]) + "\t")
        file.write("\n")

    file.close()
