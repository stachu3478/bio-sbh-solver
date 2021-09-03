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
  def validate(self):
    if self.n < self.k:
        raise Exception(
            'Długość dna jest krótsza niż długość oligonukleotydu!')
    if self.errors not in ('none', 'negative', 'positive', 'all'):
        raise Exception('Nieznany typ błędu!')
    if self.k != len(self.initial_oligo):
        raise Exception('Zła długość początkowego oligonukleotydu!')
    for oligo in self.spectrum:
        if self.k != len(oligo):
            raise Exception('Zła długość oligonukleotydu w spektrum!')
    if self.initial_oligo not in self.spectrum:
        self.spectrum.append(self.initial_oligo)

  def reconstruct(initial_oligo, spectrum, spectrum_order):
    reconstructed = initial_oligo
    if spectrum_order is not None:
        for _, connection in enumerate(spectrum_order):
            reconstructed = reconstructed + \
                spectrum[connection[0]][-connection[1]:]
    return reconstructed

  def solve(self):
    """
    Returns
    -------
    string
      Złożone potencjalne DNA
    """
    self.validate()
    spectrum_order = self.spectrum_order()
    return self.reconstruct(spectrum_order)

  def spectrum_order(self):
    """
    Returns
    -------
    string
      Złożone potencjalne DNA
    """
    raise NotImplementedError
