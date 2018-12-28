from sys import maxsize
import sys


def find_all_paths(graph, start, end, thread, path=None):
    if thread.isStopped():
        sys.exit(0)

    if path is None:
        path = []

    path = path + [start]

    if start == end:
        if len(path) > 1:
            # for n in range(len(path)):
            #     path[n] = str(int(path[n]) + 1)
            return [path]

        else:
            return []

    if start not in graph.keys():
        return []

    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, thread, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


def find_shortest_paths(all_possible_paths, thread):
    # Find all Geodesic paths for each route from i to j
    shortest_paths = {}
    geodesic_path_length = maxsize
    for k, v in all_possible_paths.items():
        shortest_paths[k] = {}
        for key, value in v.items():
            if len(value) != 0:
                shortest_paths[k][key] = []
                for i in range(len(value)):
                    if thread.isStopped():
                        sys.exit(0)

                    if len(value[i]) < geodesic_path_length:
                        geodesic_path_length = len(value[i])

                for path in value:
                    if len(path) == geodesic_path_length:
                        shortest_paths[k][key].append(path)

            geodesic_path_length = maxsize
    # ================================================================

    # Remove Reversed Geodesic paths
    for k, v in shortest_paths.items():
        for key, value in v.items():
            for path in value:
                for key2, value2 in shortest_paths[key].items():
                    for comp_path in value2:
                        if thread.isStopped():
                            sys.exit(0)

                        if path == comp_path[::-1]:
                            value2.remove(comp_path)
    # ================================================================

    # Debugging Purposes
    # for k, v in shortest_paths.items():
    #     print("{{{}".format(k))
    #     print("\t", end="")
    #     for key, value in v.items():
    #         print("{{{}:\n\t\t[".format(key))
    #         print("\t\t", end="")
    #
    #         for path in value:
    #             if len(path) != 0:
    #                 print("\t{}".format(path))
    #                 print("\t\t", end="")
    #             else:
    #                 pass
    #         print(" ]")
    #         print("\t", end="")
    #     print()
    # ================================================================

    return shortest_paths
