"""
                Copyright (C) 2020 Theodoros Siklafidis

    This file is part of GRATIS.

    GRATIS is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GRATIS is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with GRATIS. If not, see <https://www.gnu.org/licenses/>.
"""

import sys
from time import sleep
from tkinter import END


def betweenness_centrality(shortest_paths, num_of_vertices, text_area, thread):
    nodes_betweenness = {}
    value = None
    for i in range(num_of_vertices):
        if thread.isStopped():
            sys.exit(0)
        nodes_betweenness[i] = 0

    for i in range(num_of_vertices):
        path_appearances = 0
        node_betweenness = 0
        for k, v in shortest_paths.items():
            if k != str(i):
                for key, value in v.items():
                    if key != str(i):
                        for j in range(len(value)):
                            for node in value[j]:
                                if thread.isStopped():
                                    sys.exit(0)

                                if str(i) == node:
                                    path_appearances += 1
                                    # print(f"Node {str(i)} found in path {value[j]} --> {path_appearances}")
                    try:
                        node_betweenness += path_appearances / len(value)
                        # print(f"{i}: +{path_appearances / len(value)}")

                    except ZeroDivisionError:
                        node_betweenness += 0

                    path_appearances = 0

        nodes_betweenness[i] = node_betweenness

    for k, v in nodes_betweenness.items():
        text_area.insert(END, f"\nNode v{k + 1} with betweenness centrality: {v:.5f}")
        text_area.insert(END, "\n")
        text_area.see("end")
        sleep(.01)  # Do not remove this.

        # print(f"Node {k} with betweenness centrality: {v}")

    message = "\n[+] Finished Betweenness Centrality analysis.\n"
    text_area.insert(END, message)
    text_area.see("end")
    sleep(.01)  # Do not remove this.
