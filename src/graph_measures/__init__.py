from src.graphs_parser import GraphMatrix as gm, matrix_to_file, interaction_to_key
import numpy as np
import time


def average(edges: list):
    tot = 0
    for edge in edges:
        tot += edge
    return tot/len(edges)


def minimum(edges: list):
    return min(edges)

def maximum(edges: list):
    return max(edges)


class GraphMeasures:

    @staticmethod
    def short_paths(graph: gm, interaction: str="all", multi_edge_function=minimum, to_file: bool=False):
        interaction = interaction_to_key(interaction)
        floor = graph.get_floor(interaction)
        if floor is -2:
            print("Interaction value not valid")
            return None

        print("#############################\n## Starting floyd-warshall ##\n#############################\n")
        stime = time.time()
        n = graph.get_dimen()
        dist = np.zeros((n, n))
        pred = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                # Mode all interactions, default keep the minimum value
                if floor is -1:
                    el = multi_edge_function(graph.get_elements_list(i, j))
                # if we're looking for a specific interaction we read it
                else:
                    el = graph.get_element_floor(i, j, floor)

                dist[i][j] = el
                if el < 100000.0:
                    pred[i][j] = i
                else:
                    pred[i][j] = None

        print(dist)
        print("Initialization finished\nTime taken:", time.time() - stime)
        print("Expected time:", int((time.time() - stime) * n*1.5 / 60), " minutes\n\n")

        stime = time.time()
        counter = 0
        tot = n*n*n
        # pb = tot / 1000000
        for h in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][j] > dist[i][h] + dist[h][j]:
                        dist[i][j] = dist[i][h] + dist[h][j]
                        pred[i][j] = pred[h][j]
                    if counter % 10000000 == 0:
                        print("Progress:", str(round(counter/tot*100, 1)) + "%", "\t\tTotal cycles:", str(counter) + "/" + str(tot))
                    counter += 1
        print("Progress: 100%", "\t\tTotal cycles:", str(counter) + "/" + str(tot))
        print("*******************************\nTotal time:", int((time.time() - stime) * n*1.5 / 60), "minutes\n\n")

        if to_file is True:
            matrix_to_file(graph, dist, pred, interaction)

        return dist, pred

    @staticmethod
    def closeness(n, dist):
        cn = np.zeros(n)
        for i in range(n):
            for j in range(n):
                cn[i] += dist[i][j]
        for k in range(n):
            cn[i] = n / cn[i]
        return cn

    @staticmethod
    def betweeness(n, pred):
        bn = np.zeros((n))
        for i in range(n):
            for j in range(n):
                if pred[i][j] is not None:
                    bn[pred[i][j]] += 1
        for k in range(n):
            bn[i] = bn[i] / (n * n)
        return bn



