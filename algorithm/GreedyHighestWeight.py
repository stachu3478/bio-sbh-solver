from array import array
from algorithm.GreedyBase import GreedyBase

class GreedyHighestWeight(GreedyBase):
  def __init__(self) -> None:
      super().__init__()

  def sbh_negative(self, n, graph, root):
      if n == 0:
          return []
      if n < 0:
          return None

      vertex_by_desc_weight = list(map(lambda a: [-1, a], graph.const_index(root).copy()))
      for w, wa in enumerate(vertex_by_desc_weight):
          wa[0] = w
      vertex_by_desc_weight.reverse()
      for w, vertex_by_weight in vertex_by_desc_weight:
          for _, match in enumerate(vertex_by_weight):
              result = self.sbh_negative(
                  n - w, graph, match)
              if result is not None:
                  result.insert(0, (match, w))
                  return result
