__author__ = "Theodoros Siklafidis"
__name__ = "Gratis"
__version__ = "1.0"
__license__ = "GNU General Public License v3.0"

from collections import defaultdict
from heapq import *


def dijkstra(edges, f, t):
    # https://gist.github.com/kachayev/5990802

    g = defaultdict(list)
    for l, r, c in edges:
        g[l].append((c, r))

    q, seen, mins = [(0, f, ())], set(), {f: 0}
    while q:
        (cost, v1, path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path += (v1,)
            if v1 == t:
                path_pajek = list(path)
                for i in range(len(path_pajek)):
                    path_pajek[i] = "v" + str(int(path_pajek[i]) + 1)
                return cost, path, path_pajek

            for c, v2 in g.get(v1, ()):
                if v2 in seen:
                    continue
                prev = mins.get(v2, None)
                next = cost + c
                if prev is None or next < prev:
                    mins[v2] = next
                    heappush(q, (next, v2, path))

    return float("inf")
