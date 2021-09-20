from algorithm.ant.ErrorDependent import ErrorDependent

class NonNegativeErrorDependent(ErrorDependent):
    def __init__(self, min_feromon, graph) -> None:
        super().__init__(min_feromon, graph)
        self.max_vertex_degree = graph.max_degree_by_weight(1)


    def feromon_index_lists_rows(self, next_vertices_matrix):
        index_weights = []
        index_random_weights = []
        lists_indexes = [[None for _ in range(self.graph.size)] for _ in range(self.graph.max_weight)]
        for index, j in enumerate(next_vertices_matrix[1]):
            index_weights.append((j, 1))
            index_random_weights.append(self.min_feromon)
            lists_indexes[1][j] = index
        return index_weights, index_random_weights, lists_indexes

    def assign_feromon_row(self, row, next_vertices_matrix):
        for _, j in enumerate(next_vertices_matrix[1]):
            row[j] = self.min_feromon