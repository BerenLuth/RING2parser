from src.graphs_parser import GraphMatrix as gm
import numpy as np
import time

class BetweenessCentrality:

    @staticmethod
    def short_paths(graph: gm):
        print("\nStarting Floyd-Warshall\n")
        stime = time.time()
        n = graph.get_dimen()
        dist = np.zeros((n, n))
        #pred = [[None]*n]*n
        pred = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                el = graph.get_element(i, j)[0]
                dist[i][j] = el
                if el < 100000.0:
                    pred[i][j] = i
                else:
                    pred[i][j] = None

        print("Initialization finished\nTime taken:", time.time() - stime)
        print("Espected time:", (time.time() - stime) * n*1.5 / 60, " minutes\n\n")

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
        print("**************************************\nTotal time: ", time.time() - stime, "\n")
        return dist, pred

