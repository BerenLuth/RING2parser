from bs4 import BeautifulSoup as Soup
import numpy as np
import time

# this can be also e_Energy
WEIGHT_PARAMETER = "e_Distance"


class GraphMatrix:

    # If you don't pass any parameter it'll load the default file included in this repo
    def __init__(self, file):
        print("Loagind matrix from file:", file)
        start_time = time.time()
        xml = open(file, "r").read()
        xml = Soup(xml, 'lxml')

        self.nodes = len(xml.find_all("node"))
        self.edges = len(xml.find_all("edge"))
        self.matrix = np.zeros((self.nodes, self.nodes))

        for edge in xml.find_all("edge"):
            # print(edge['source'], edge['target'])
            src = int(edge['source'][1:])
            trg = int(edge['target'][1:])
            weight = float(edge.find(key=WEIGHT_PARAMETER).get_text())
            self.matrix[src][trg] = weight

        self.print_info()
        print("Total time: ", time.time() - start_time, "\n")

    def print_matrix(self):
        print(self.matrix)

    def get_element(self, row, col):
        return self.matrix[row][col]

    def get_rows(self):
        return self.nodes

    def get_cols(self):
        return self.nodes

    def print_info(self):
        print("Number of nodes:", self.nodes, "\nNumber of edges:", self.edges)

