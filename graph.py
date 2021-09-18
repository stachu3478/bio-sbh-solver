from utils.array_helper import expand_array

def match_oligos(o1, o2, size=None):
    for step in range(1, size or (len(o1) - 0)):
        if o1[step:] == o2[:-step]:
            yield step
    yield size or (len(o1) - 1)


class DirectedGraph:
    def from_spectrum(self, spectrum, k):
        graph = DirectedGraph(len(spectrum), k)
        max_oligo_cut = k  # - 1  # supress -1
        for i1, oligo1 in enumerate(spectrum):
            for i2, oligo2 in enumerate(spectrum):
                for step in match_oligos(oligo1, oligo2, size=max_oligo_cut):
                    graph.pin(i1, i2, step)

        return graph  # .freeze()

    def __init__(self, size, max_weight):
        self.vertex_edges_by_weight = [[[] for _ in range(max_weight + 1)] for _ in range(size)]
        self.vertex_edges = [[] for _ in range(size)]
        self.vertex_degree_by_weight = [[0 for _ in range(max_weight + 1)] for _ in range(size)]
        self.vertex_degree = [0 for _ in range(size)]
        self._max_degree = 0
        self._max_degree_by_weight = [0 for _ in range(max_weight + 1)]

    def const_index(self, i):
        return self.vertex_edges_by_weight[i]

    def const_get(self, i, j):
        return self.const_index(i)[j]

    def flat_index(self, i):
        return self.vertex_edges[i]

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
        return self.const_index(i)

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
        return self.const_get(i, j)

    def get_degree(self, i):
        return self.vertex_degree[i]

    def get_degree_by_weight(self, i, j):
        return self.vertex_degree_by_weight[i][j]

    def pin(self, fromVertex, toVertex, weight):
        self.vertex_edges_by_weight[fromVertex][weight].append(toVertex)

        flat_edges = expand_array(self.vertex_edges, fromVertex)
        flat_edges.append((toVertex, weight))
        self.vertex_degree_by_weight[fromVertex][weight] += 1
        self.vertex_degree_by_weight[toVertex][weight] += 1
        self.vertex_degree[fromVertex] += 1
        self.vertex_degree[toVertex] += 1
        current_max_degree = max(self.vertex_degree_by_weight[fromVertex][weight], self.vertex_degree_by_weight[toVertex][weight], self.vertex_degree[fromVertex], self.vertex_degree[toVertex])
        self._max_degree = max(self._max_degree, current_max_degree)
        self._max_degree_by_weight[weight] = max(self._max_degree_by_weight[weight], current_max_degree)

    def max_degree(self):
        return self._max_degree

    def max_degree_by_weight(self, weight):
        return self._max_degree_by_weight[weight]

    def freeze(self):
        self.vertex_edges_by_weight = tuple(
            [tuple(a) for i, a in enumerate(self.vertex_edges_by_weight)])
        return self

    def vertex_count(self):
        return len(self.vertex_edges_by_weight)


DirectedGraph.from_spectrum = classmethod(DirectedGraph.from_spectrum)
