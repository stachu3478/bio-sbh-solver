def expand_array(array, to):
    for _ in range(to - len(array) + 1):
        array.append([])
    return array[to]


def match_oligos(o1, o2, size=None):
    for step in range(1, size or (len(o1) - 0)):
        if o1[step:] == o2[:-step]:
            yield step
    yield size or (len(o1) - 1)


class DirectedGraph:
    def from_spectrum(self, spectrum, k):
        graph = DirectedGraph()
        max_oligo_cut = k  # - 1  # supress -1
        for i1, oligo1 in enumerate(spectrum):
            for i2, oligo2 in enumerate(spectrum):
                for step in match_oligos(oligo1, oligo2, size=max_oligo_cut):
                    graph.pin(i1, i2, step)

        return graph  # .freeze()

    def __init__(self):
        self.vertex_edges_by_weight = []

    def const_index(self, i):
        return self.vertex_edges_by_weight[i]

    def const_get(self, i, j):
        return self.const_index(i)[j]

    def index(self, i):
        """
        Parameters
        ----------
        i : int
          Initial vertex

        Returns
        -------
        int[][]
          End vertices by weight
        """
        return expand_array(self.vertex_edges_by_weight, i)

    def get(self, i, j):
        """
        Parameters
        ----------
        i : int
          Initial vertex
        j : int
          Weight

        Returns
        -------
        int[]
          End vertices
        """
        return expand_array(self.index(i), j)

    def pin(self, fromVertex, toVertex, weight):
        edges_by_weight = expand_array(self.vertex_edges_by_weight, fromVertex)
        edges = expand_array(edges_by_weight, weight)
        edges.append(toVertex)

    def freeze(self):
        self.vertex_edges_by_weight = tuple(
            [tuple(a) for i, a in enumerate(self.vertex_edges_by_weight)])
        return self

    def vertex_count(self):
        return len(self.vertex_edges_by_weight)

    def voyager(self):
        pass


DirectedGraph.from_spectrum = classmethod(DirectedGraph.from_spectrum)
