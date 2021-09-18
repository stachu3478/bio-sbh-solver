from algorithm.Base import Base
import sys
from graph import DirectedGraph

class Greedy(Base):
  def __init__(self) -> None:
      super().__init__()

  def spectrum_order(self):
    """
    Override
    """
    spectrum_order = None
    graph = DirectedGraph.from_spectrum(self.spectrum, self.k)
    root = self.root
    nucl_to_be_discovered = self.n - self.k
    for _ in self.recursion_limit(self.n + 20):
      if self.has_negative_errors():
          spectrum_order = self.sbh_negative(nucl_to_be_discovered, graph, root)
      else:
          spectrum_order = self.sbh_non_negative(nucl_to_be_discovered, graph, root)
    return spectrum_order


  def sbh_negative(self, n, graph, root):
      if n == 0:
          return []
      if n < 0:
          return None

      for w, vertex_by_weight in enumerate(graph.const_index(root)):
          for _, match in enumerate(vertex_by_weight):
              result = self.sbh_negative(
                  n - w, graph, match)
              if result is not None:
                  result.insert(0, (match, w))
                  return result


  def sbh_non_negative(self, n, graph, root):
      if n == 0:
          return []

      for _, match in enumerate(graph.const_get(root, 1)):
          result = self.sbh_non_negative(
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
