__author__ = "Theodoros Siklafidis"
__name__ = "Gratis"
__version__ = "1.0"
__license__ = "GNU General Public License v3.0"

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

        text_area.insert(END, f"\nAverage distance of node v{i + 1} to all others is: {float(avg_distance):.5}")
        text_area.insert(END, "\n")
        text_area.see("end")
        sleep(.01)  # Do not remove this.

        # print(f"Average distance of node v{i + 1} to all others is: {avg_distance}")

        if maximum < node_avg_distances[i] not in [0, 1]:
            maximum = node_avg_distances[i]
            maximum_node = i
        else:
            pass

    message = f"\nGraph Centrality: Node v{maximum_node + 1} with maximum average distance: {float(maximum):.5}\n"
    text_area.insert(END, message)
    text_area.see("end")
    sleep(.01)  # Do not remove this.
