from tkinter import END
from time import sleep
import sys


def closeness_centrality(Vertices, geodesic_paths, text_area, thread):
    node_avg_distances = {}
    maximum = 0
    maximum_node: int

    for i in range(Vertices):
        avg_distance = 0
        for j in range(Vertices):
            if thread.isStopped():
                sys.exit(0)
            try:
                avg_distance += 1 / geodesic_paths[str(i)][str(j)]

            except ZeroDivisionError:
                avg_distance += 0

        node_avg_distances[i] = avg_distance

        text_area.insert(END, "\nAverage distance of node v{} to all others is: {:.5}"
                              .format(i + 1, float(avg_distance)))
        text_area.insert(END, "\n")
        text_area.see("end")
        sleep(.01)  # Do not remove this.

        # print("Average distance of node v{} to all others is: {}".format(i+1, avg_distance))

        if maximum < node_avg_distances[i] not in [0, 1]:
            maximum = node_avg_distances[i]
            maximum_node = i
        else:
            pass

    message = "\nGraph Centrality: Node v{} with maximum average distance: {:.5}\n".format(maximum_node + 1,
                                                                                           float(maximum))
    text_area.insert(END, message)
    text_area.see("end")
    sleep(.01)  # Do not remove this.
