from bs4 import BeautifulSoup as Soup
import numpy as np
import time
import random
import re
import csv

WEIGHT_ENERGY = "e_Energy"
WEIGHT_DISTANCE = "e_Distance"

REALLY_HIGH_NUMBER = 100000.0


class GraphMatrix:

    # If you don't pass any parameter it'll load the default file included in this repo
    def __init__(self, file):
        if not file:
            print("You need to give at least one xml file in input")
            return

        start_time = time.time()


        print("Loagind matrix from file:", file)

        xml = open(file, "r").read()
        xml = Soup(xml, 'lxml')

        self.interactions = dict()

        edges = xml.find_all("edge")
        floor = 0
        for edge in edges:
            tmp = interaction_to_key(edge.find(key="e_Interaction").get_text())
            if tmp not in self.interactions:
                self.interactions[tmp] = floor
                floor += 1

        print(self.interactions)

        self.file_name = file
        self.n_nodes = len(xml.find_all("node"))
        self.nodes = []
        self.matrix = np.zeros((self.n_nodes, self.n_nodes, len(self.interactions))) # [[[100000.0]*len(self.interactions)]*self.n_nodes]*self.n_nodes  # np.zeros((self.n_nodes, self.n_nodes))
        self.edges = []

        # initialize matrix with a really big int for floyd-warshall
        self.initialize_matrix()

        nodes = xml.find_all("node")
        for node in nodes:
            self.nodes.append(node.find(key="v_NodeId").get_text())

        self.edges.append(len(edges))
        for edge in edges:
            # print(edge['source'], edge['target'])
            src = int(edge['source'][1:])
            trg = int(edge['target'][1:])
            tmp_inter = edge.find(key="e_Interaction").get_text()
            interaction = self.interactions[interaction_to_key(tmp_inter)]

            # Choose between DISTANCE or ENERGY
            weight = float(edge.find(key=WEIGHT_DISTANCE).get_text())
            self.matrix[src, trg, interaction] = weight
            self.matrix[trg, src, interaction] = weight
            # print(src, trg, interaction, weight, self.matrix[src, trg])

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

    def get_elements_list(self, row, col):
        # print(self.matrix[row][col])
        return self.matrix[row, col]

    def get_element_floor(self, row, col, floor):
        # print(self.matrix[row][col][floor])
        return self.matrix[row, col, floor]

    def get_dimen(self):
        return self.n_nodes

    def get_node(self, n):
        return self.nodes[n][-3:]

    def name(self):
        r = re.compile('/([^/]+)\.xml')
        return r.search(self.file_name)[1]

    def print_info(self):
        n_edges = 0
        for edge in self.edges:
            n_edges += edge
        print("# Nodes:\t", self.n_nodes, "\n# Edges:\t", n_edges)

    def get_interaction_number(self):
        return len(self.interactions)

    def get_interaction_id(self, interaction: str):
        if "ALL" in interaction:
            return -1
        try:
            return self.interactions[interaction]
        except KeyError:
            print("This interaction is not present in this protein")
            return -2

    def initialize_matrix(self):
        for row in range(self.n_nodes):
            for col in range(self.n_nodes):
                if row != col:
                    for f in range(self.get_interaction_number()):
                        self.matrix[row, col, f] = REALLY_HIGH_NUMBER


def interaction_to_key(name: str):
    r = re.compile('(.*):.*')
    x = r.search(name.upper())
    if x is None:
        return name.upper()
    else:
        return x[1]


def matrix_to_cache(graph: GraphMatrix, dist, pred, interaction: str= ''):
    # print("Not implemented yet")

    n = graph.n_nodes
    file = open("../cache/" + str(graph.name()) + "_" + str(interaction) + ".csv", "w")
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


def cache_to_matrix(graph: GraphMatrix, interaction: str= ''):
    try:
        file = open("../cache/" + str(graph.name()) + "_" + str(interaction) + ".csv", "r")
    except FileNotFoundError:
        return None

    matrix_reader = csv.reader(file, delimiter=';', lineterminator='\n')
    next(matrix_reader)     # skip the first line (header)

    n = graph.get_dimen()
    dist = np.zeros((n, n))
    pred = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist[i, j] = REALLY_HIGH_NUMBER
            pred[i, j] = -1

    for row in matrix_reader:
        src = row[0]
        trg = row[1]
        dist[int(src), int(trg)] = row[2]
        pred[int(src), int(trg)] = row[3]

    return dist, pred
