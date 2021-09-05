from algorithm.Base import Base
import sys
from graph import DirectedGraph

class Greedy(Base):
  def __init__(self) -> None:
      super().__init__()
      self.max_o = 0

  def spectrum_order(self):
    """
    Override
    """
    spectrum_order = None
    graph = DirectedGraph.from_spectrum(self.spectrum, self.k)
    root = self.spectrum.index(self.initial_oligo)
    nucl_to_be_discovered = self.n - self.k
    for _ in self.recursion_limit(self.n + 10):
      if self.errors == 'none':
          self.sbh_perfect(nucl_to_be_discovered, graph,
                              root, supress_vertices=set([root]))
      elif self.errors == 'negative':
          spectrum_order = self.sbh_negative(nucl_to_be_discovered, graph, root, visited=[
                                0 for i in range(graph.vertex_count())])
      elif self.errors == 'positive':
          spectrum_order = self.sbh_positive(nucl_to_be_discovered, graph, root)
      else:
          spectrum_order = self.sbh_all(nucl_to_be_discovered, self.k, graph, root)
    return spectrum_order

  def sbh_perfect(self, n, graph, root, supress_vertices=set()):
      if n == 0:
          return []

      for _, match in enumerate(graph.const_get(root, 1)):
          if match in supress_vertices:
              continue
          supress_vertices.add(match)
          result = self.sbh_perfect(
              n - 1, graph, match, supress_vertices=supress_vertices)
          if result is not None:
              result.insert(0, (match, 1))
              return result
          supress_vertices.remove(match)



  def sbh_negative(self, n, graph, root, visited=[], visited_count=0):
      if n == 0:
          return []

      for w, vertex_by_weight in enumerate(graph.const_index(root)):
          for _, match in enumerate(vertex_by_weight):
              next_visited_count = visited_count
              if visited[match] == 0:
                  next_visited_count += 1
              visited[match] += 1
              result = self.sbh_negative(
                  n - w, graph, match, visited=visited, visited_count=next_visited_count)
              if result is not None:
                  result.insert(0, (match, w))
                  return result
              visited[match] -= 1


  def sbh_positive(self, n, graph, root):
      if n == 0:
          return []

      for _, match in enumerate(graph.const_get(root, 1)):
          result = self.sbh_positive(
              n - 1, graph, match)
          if result is not None:
              result.insert(0, (match, 1))
              return result

  def recursion_limit(self, limit):
    prev_recursion_limit = sys.getrecursionlimit()
    if prev_recursion_limit < limit:
        sys.setrecursionlimit(limit)
    yield
    sys.setrecursionlimit(prev_recursion_limit)
