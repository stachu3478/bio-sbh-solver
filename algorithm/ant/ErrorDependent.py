class ErrorDependent:
    def __init__(self, min_feromon, graph) -> None:
        self.graph = graph
        self.min_feromon = min_feromon
        self.max_vertex_degree = 0
    

    def max_total_vertex_degree(self):
        return self.max_vertex_degree * self.max_vertex_degree

    def create_feromon_table(self, spectrum):
        """
        Returns
        -------
        string
        Złożone potencjalne DNA
        """
        self.feromon_index_weight_list = [] # for random choice purpose [current_vertex][]
        self.feromon_index_random_weight_list = [] # for storing feromon for random choice weights by [current_vertex][]
        self.feromon_lists_index = [] # for indexing stored feromon in feromon_index_random_weight_list storing feromon by
        # [current_vertex][weight][next_vertex]
        for i, _ in enumerate(spectrum):
            next_vertices_matrix = self.graph.index(i)
            feromon_index_weights, feromon_random_weights, feromon_indexes = self.feromon_index_lists_rows(next_vertices_matrix)
            self.feromon_index_weight_list.append(feromon_index_weights)
            self.feromon_index_random_weight_list.append(feromon_random_weights)
            self.feromon_lists_index.append(feromon_indexes)
    
    def feromon_index_lists_rows(self, next_vertices_matrix):
        raise NotImplementedError("Abstract class!")