from algorithm.GreedyBase import GreedyBase

class GreedyLeastWeight(GreedyBase):
  def __init__(self) -> None:
      super().__init__()


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
