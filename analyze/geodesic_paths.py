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
from analyze.dijkstra import dijkstra


def find_geodesics(edges, num_of_vertices, text_area, thread):
    geo_paths = {}
    graph_diameter = 0
    start_node: int
    end_node: int
    for i in range(num_of_vertices):
        if thread.isStopped():
            sys.exit(0)
        geo_paths[str(i)] = {}

    for i in range(num_of_vertices):
        for j in range(num_of_vertices):
            if thread.isStopped():
                sys.exit(0)
            if i == j:
                geo_paths[str(i)][str(j)] = 0
            elif i != j and i < j:
                try:
                    hops, path, path_pajek = dijkstra(edges, str(i), str(j))

                    geo_paths[str(i)][str(j)] = hops
                    geo_paths[str(j)][str(i)] = hops

                    path_str = str(path_pajek)
                    text_area.insert(END, f"\nv{i + 1} ==> v{j + 1}: ")
                    text_area.insert(END, path_str)
                    text_area.insert(END, "\n")
                    text_area.see("end")
                    sleep(.01)  # Do not remove this.

                    if graph_diameter < hops:
                        start_node = i
                        end_node = j
                        graph_diameter = hops

                except TypeError:
                    geo_paths[str(i)][str(j)] = 0
                    geo_paths[str(j)][str(i)] = 0

                    text_area.insert(END, f"\nv{i + 1} ==> v{j + 1}: ")
                    text_area.insert(END, "None")
                    text_area.insert(END, "\n")
                    text_area.see("end")
                    sleep(.01)  # Do not remove this.

    # for i in range(num_of_vertices):
    #     for j in range(num_of_vertices):
    #         print(f"{i} ==> {j}: {geo_paths[str(i)][str(j)]}")

    text_area.insert(END, f"\nGraph Diameter: From node v{start_node + 1} to node v{end_node + 1} with {graph_diameter} hops.\n")
    text_area.see("end")
    sleep(.01)  # Do not remove this.

    return geo_paths
