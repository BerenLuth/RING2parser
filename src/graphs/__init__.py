from bs4 import BeautifulSoup as Soup
import numpy as np
import time

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

        self.nodes = nodes
        self.matrix = np.zeros((self.nodes, self.nodes, len(files)))
        self.edges = []
        self.N_floors = len(files)

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

    def print_matrix(self):
        print(self.matrix)

    def get_element(self, row, col):
        return self.matrix[row][col]

    def get_rows(self):
        return self.nodes

    def get_cols(self):
        return self.nodes

    def print_info(self):
        n_edges = 0
        for edge in self.edges:
            n_edges += edge
        print("# Nodes:\t", self.nodes, "\n# Floors:\t", self.N_floors, "\n# Edges:\t", n_edges)

