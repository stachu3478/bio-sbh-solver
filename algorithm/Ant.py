import random
from algorithm.GreedyLeastWeight import GreedyLeastWeight
from graph import DirectedGraph
from algorithm.ant.NegativeErrorDependent import NegativeErrorDependent
from algorithm.ant.NonNegativeErrorDependent import NonNegativeErrorDependent

class Ant(GreedyLeastWeight):
  def __init__(self) -> None:
      super().__init__()
      # tuning variables
      self.ant_count = 100
      self.feromon_half_vapor_time = 2
      self.min_feromon = 1.0 # 0.00001
      self.max_feromon = 1.0
      self.feromon_generated_at_not_worse_result_rte = 0
      self.starvation_cycles = 1 # 5

      self.vertex_degree_weight = 1.0
      self.chain_length_weight = 1.0
      self.unique_vertex_weight = 1.0

      # other variables
      self.starvation_level = 0
      self.feromon_vapor_rate = 0.5 ** (1 / self.feromon_half_vapor_time)

  def before_run(self):
      super().before_run()
      self.graph = DirectedGraph.from_spectrum(self.spectrum, self.k)
      if self.has_negative_errors():
        self.error_dependent = NegativeErrorDependent(self.min_feromon, self.graph)
      else:
        self.error_dependent = NonNegativeErrorDependent(self.min_feromon, self.graph)

  def spectrum_order(self):
    """
    Override
    """
    spectrum_order = super().spectrum_order()
    print(spectrum_order)
    self.max_quality = self.quality(spectrum_order)
    self.order_list = [i for i in range(len(self.spectrum))]
    self.best_path = spectrum_order
    self.feromon = self.error_dependent.create_feromon_table(self.spectrum)
   
    print('Found greedy quality: ' + str(self.max_quality))
    self.apply_feromon(spectrum_order, self.quality_to_applied_feromon(self.quality(spectrum_order)))
    while self.starvation_level < self.starvation_cycles:
        self.cycle()
    return self.best_path


  def quality(self, spectrum_order):
    vertex_degree_quality = self.vertex_degree_weight * float(sum(map(lambda iw: self.get_degree(iw[0]), spectrum_order))) / float(self.error_dependent.max_total_vertex_degree())
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
    self.vaporate_feromon()
    print('SUccessful matches: ', len(spectrum_orders))
    for _, spectrum_order in enumerate(spectrum_orders):
      quality = self.quality(spectrum_order)
      # print(spectrum_order)
      print('Quality: ' + str(quality))
      if quality > self.max_quality:
          self.starvation_level = 0
          self.max_quality = quality
          self.best_path = spectrum_order
          self.apply_feromon(spectrum_order, self.quality_to_applied_feromon(quality))
          print('Found better quality: ' + str(quality))
        
  def quality_to_applied_feromon(self, quality):
    return quality * (self.max_feromon - self.min_feromon)

  def walk(self):
    n = self.n - self.k
    current_vertex = (self.root, 0)
    spectrum_order = []
    while n > 0:
      next_vertex, weight = self.next_vertex(current_vertex[0])
      spectrum_order.append((next_vertex, weight))
      n = n - weight
      current_vertex = (next_vertex, weight)
    return spectrum_order, n == 0

  def next_vertex(self, current_vertex):
    available_next = self.error_dependent.feromon_index_weight_list[current_vertex]
    weights = self.error_dependent.feromon_index_random_weight_list[current_vertex]
    index_weight = random.choices(available_next, weights=weights, k=1)[0]
    return index_weight[0], index_weight[1]

  def apply_feromon(self, spectrum_order, value):
    current_vertex = self.root
    for i, spectrum_index_weight in enumerate(spectrum_order):
        row = self.error_dependent.feromon_index_random_weight_list[current_vertex]
        next_spectrum_indexes_row = self.error_dependent.feromon_lists_index[current_vertex][spectrum_index_weight[1]]
        next_spectrum_index = next_spectrum_indexes_row[spectrum_index_weight[0]]
        row[next_spectrum_index] = min(row[next_spectrum_index] + value, self.max_feromon)
        current_vertex = spectrum_index_weight[0]

  def vaporate_feromon(self):
    for _, feromon_row in enumerate(self.error_dependent.feromon_index_random_weight_list):
      for j, old_value in enumerate(feromon_row):
        feromon_row[j] = max(self.min_feromon, old_value * self.feromon_vapor_rate)
