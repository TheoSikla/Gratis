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
