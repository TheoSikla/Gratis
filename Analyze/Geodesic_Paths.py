from Analyze.Dijkstra import dijkstra
from tkinter import END
import sys
from time import sleep


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
