from bs4 import BeautifulSoup as Soup
import numpy as np
import time
import random
import re
import csv

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
        n_nodes = 0

        for file in files:
            print("Loagind matrix from file:", file)

            xml = open(file, "r").read()
            xml = Soup(xml, 'lxml')
            parsed.append(xml)

            if n_nodes == 0:
                n_nodes = len(xml.find_all("node"))
            else:
                if n_nodes != len(xml.find_all("node")):
                    print("Error: files have different number of nodes!")
                    return

        self.file_names = files
        self.n_nodes = n_nodes
        self.nodes = []
        self.matrix = np.zeros((self.n_nodes, self.n_nodes, len(files)))
        self.edges = []
        self.n_floors = len(files)

        # initialize matrix with a really big int for floyd-warshall
        self.initialize_matrix()

        floor = 0
        for xml in parsed:
            nodes = xml.find_all("node")
            for node in nodes:
                self.nodes.append(node.find(key="v_NodeId").get_text())


            edges = xml.find_all("edge")
            self.edges.append(len(edges))

            for edge in edges:
                # print(edge['source'], edge['target'])
                src = int(edge['source'][1:])
                trg = int(edge['target'][1:])

                # Choose between DISTANCE or ENERGY
                weight = float(edge.find(key=WEIGHT_DISTANCE).get_text())
                self.matrix[src][trg][floor] = weight
                self.matrix[trg][src][floor] = weight
            floor += 1

        self.print_info()
        print("**************************************\nTotal loading time: ", time.time() - start_time, "\n")

    @staticmethod
    def init_test():
        return GraphMatrix("../assets/6a90_network.xml")

    @staticmethod
    def init_random_test(nodes, floors, density=0.1):
        graph = GraphMatrix()
        graph.file_names = ["/test.xml"]
        graph.n_nodes = nodes
        graph.n_floors = floors
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
        return self.n_nodes

    def get_node(self, n):
        return self.nodes[n][-3:]

    def name(self):
        r = re.compile('/([^/]+)\.xml')
        return r.search(self.file_names[0])[1]

    def print_info(self):
        n_edges = 0
        for edge in self.edges:
            n_edges += edge
        print("# Nodes:\t", self.n_nodes, "\n# Floors:\t", self.n_floors, "\n# Edges:\t", n_edges)

    def initialize_matrix(self):
        for row in range(self.n_nodes):
            for col in range(self.n_nodes):
                for floor in range(self.n_floors):
                    self.matrix[row][col][floor] = 100000.0


def matrix_to_file(graph: GraphMatrix, dist, pred):
    # print("Not implemented yet")

    n = graph.n_nodes
    file = open("../output/" + str(graph.name()) + "_res.csv", "w")
    # file.write("Original filename: " + str(graph.name()) + "\tNodes: " + str(n) + "\tDistance/Predecessors")
    writer = csv.writer(file, delimiter=";", lineterminator='\n')
    writer.writerow(('source', 'destination', 'distance', 'predecessor'))

    for r in range(n):
        for c in range(n):
            if not dist[r][c] == 1000 and 0 <= pred[r][c] <= graph.n_nodes:
                '''if dist[r][c] == 1000.0:
                    d = -1
                else:
                    d = dist[r][c]

                if 0 <= pred[r][c] <= graph.nodes:
                    p = pred[r][c]
                else:
                    p = -1'''
                d = dist[r][c]
                p = pred[r][c]

                writer.writerow((r, c, d, p))

    file.close()


'''                file.write("-\t")
            else:
                file.write(str(dist[r][c]) + "\t")
        file.write("\n")

    print("Writing predecessors on file: 2/2")
    file.write("\n")
    for r in range(n):
        for c in range(n):
            if 0 <= pred[r][c] <= graph.nodes:
                file.write(str(pred[r][c]) + "\t")
            else:
                file.write("-\t")
        file.write("\n")
    '''

