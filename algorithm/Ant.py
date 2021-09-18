import random
from algorithm.Greedy import Greedy
from graph import DirectedGraph
from utils.array_helper import expand_array

class Ant(Greedy):
  def __init__(self) -> None:
      super().__init__()
      self.ant_count = 1
      self.feromon_half_vapor_time = 0
      self.min_feromon = 0.1
      self.max_feromon = 1.0
      self.feromon_generated_at_not_worse_result_rte = 0
      self.starvation_cycles = 1

      self.vertex_degree_weight = 1.0
      self.chain_length_weight = 1.0
      self.unique_vertex_weight = 1.0

      self.starvation_level = 0

  def spectrum_order(self):
    """
    Override
    """
    spectrum_order = super().spectrum_order()
    self.graph = DirectedGraph.from_spectrum(self.spectrum, self.k)
    if self.has_negative_errors():
      self.max_vertex_degree = self.graph.max_degree()
    else:
      self.max_vertex_degree = self.graph.max_degree_by_weight(1)
    self.max_quality = self.quality(spectrum_order)
    self.feromon = [[0 for _ in self.spectrum] for _ in self.spectrum]
    self.order_list = [i for i in range(len(self.spectrum))]
    self.best_path = spectrum_order
   
    print('Found greedy quality: ' + str(self.max_quality))
    for iw in enumerate(self.spectrum):
        next_vertices_matrix = self.graph.index(iw[0])
        if self.has_negative_errors():
          for _, row in enumerate(next_vertices_matrix):
              for _, j in enumerate(row):
                self.feromon[iw[0]][j] = self.min_feromon
        else:
            for _, j in enumerate(next_vertices_matrix[1]):
              self.feromon[iw[0]][j] = self.min_feromon
    self.apply_feromon(spectrum_order, self.quality_to_applied_feromon(self.quality(spectrum_order)))
    while self.starvation_level < self.starvation_cycles:
        self.cycle()
    return self.best_path


  def quality(self, spectrum_order):
    vertex_degree_quality = self.vertex_degree_weight * float(sum(map(lambda iw: self.get_degree(iw[0]), spectrum_order))) / float(self.max_vertex_degree * self.max_vertex_degree)
    chain_length_quality = self.chain_length_weight * float(len(spectrum_order)) / float(self.n - self.k + 1)
    unique_vertex_quality = self.unique_vertex_weight * float(len(set(spectrum_order))) / float(self.n - self.k + 1)
    return (vertex_degree_quality + chain_length_quality + unique_vertex_quality) / (self.vertex_degree_weight + self.chain_length_weight + self.unique_vertex_weight)

  def get_degree(self, i):
    if self.has_negative_errors():
      return self.graph.get_degree(i)
    return self.graph.get_degree_by_weight(i, 1)

  def cycle(self):
    self.starvation_level += 1
    spectrum_orders = []
    for _ in range(self.ant_count):
        spectrum_order, valid = self.walk()
        if valid:
          spectrum_orders.append(spectrum_order)
    for _, spectrum_order in spectrum_orders:
      quality = self.quality(spectrum_order)
      if quality >= self.max_quality:
          self.apply_feromon(spectrum_order, self.quality_to_applied_feromon(quality))
      if quality > self.max_quality:
          self.starvation_level = 0
          self.max_quality = quality
          self.best_path = spectrum_order
          print('Found better quality: ' + quality)
        
  def quality_to_applied_feromon(self, quality):
    return quality * (self.max_feromon - self.min_feromon)

  def walk(self):
    n = self.n - self.k
    current_vertex = self.root
    spectrum_order = [current_vertex]
    while n > 0:
      next_vertex, step = self.next_vertex(current_vertex)
      spectrum_order.append(next_vertex)
      n = n - step
    return spectrum_order, n == 0

  def next_vertex(self, current_vertex):
    index = random.choices(self.order_list, weights=self.feromon[current_vertex], k=1)[0]
    return self.graph.flat_index(current_vertex)[index]

  def apply_feromon(self, spectrum_order, value):
    for i, spectrum_index_weight in enumerate(spectrum_order[0:-1]):
        row = self.feromon[spectrum_index_weight[0]]
        next_spectrum_index = spectrum_order[i + 1][0]
        row[next_spectrum_index] = min(row[next_spectrum_index] + value, self.max_feromon)
