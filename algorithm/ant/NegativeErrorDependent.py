from algorithm.ant.ErrorDependent import ErrorDependent

class NegativeErrorDependent(ErrorDependent):
    def __init__(self, min_feromon, graph) -> None:
        super().__init__(min_feromon, graph)
        self.max_vertex_degree = graph.max_degree()

    def feromon_index_lists_rows(self, next_vertices_matrix):
        index_weights = []
        index_random_weights = []
        lists_indexes = [[None for _ in range(self.graph.size)] for _ in range(self.graph.max_weight + 1)]
        
        for weight, next_row in enumerate(next_vertices_matrix):
            for _, next in enumerate(next_row):
                lists_indexes[weight][next] = len(index_weights)
                index_weights.append((next, weight))
                index_random_weights.append(self.min_feromon)
        for index, index_weight in enumerate(index_weights):
            lists_indexes[index_weight[1]][index_weight[0]] = index
                
        return index_weights, index_random_weights, lists_indexes

    def get_degree(self, vertex_id):
        return self.graph.get_degree(vertex_id)