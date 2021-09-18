"""
ALGORYTM MA NASTĘPUJĄCE DANE WEJŚCIOWE:

Parameters
----------
n : int
  Długość DNA
k : int
  Długość oligonukleotydów
spectrum : string[]
  Spektrum DNA
errors : 'none' | 'negative' | 'positive' | 'all'
  Informacje jakie błędy są w spektrum
initial_oligo : string
  Początkowy oligonukleotyd – wierzchołek początkowy dla ścieżki w grafie (to ostatnie nie jest żadnym
  szczególnym oszustwem czy jakimś wielkim ułatwieniem, w normalnych eksperymentach SBH też
  wiedzieliśmy od czego startujemy, wynika to z innych cech eksperymentu hybrydyzacyjnego).
"""
class Base:
  def __init__(self):
    self.n = None
    self.k = None
    self.spectrum = []
    self.errors = ''
    self.initial_oligo = ''

  def has_negative_errors(self):
    return self.errors == 'negative' or self.errors == 'all'

  def before_run(self):
    self.root = self.spectrum.index(self.initial_oligo)

  def spectrum_order(self):
    """
    Returns
    -------
    string
      Złożone potencjalne DNA
    """
    raise NotImplementedError
