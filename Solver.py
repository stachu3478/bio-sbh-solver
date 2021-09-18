from utils.LevenshteinDistance import LevenshteinDistance
from algorithm.Greedy import Greedy
from algorithm.Ant import Ant

class Solver:
  def read_from_instance(self, instance, algorithm_name = 'Greedy'):
    self.algorithm_instance = self.choose_algorithm(algorithm_name)()
    self.algorithm_instance.n = instance.length
    self.algorithm_instance.k = instance.oligo_length
    self.algorithm_instance.spectrum = instance.spectrum
    if instance.positive_errors and instance.negative_errors:
          self.algorithm_instance.errors = 'all'
    elif instance.positive_errors:
          self.algorithm_instance.errors = 'positive'
    elif instance.negative_errors:
          self.algorithm_instance.errors = 'negative'
    else:
          self.algorithm_instance.errors = 'none'
    self.algorithm_instance.initial_oligo = instance.initial_oligo
    return self.algorithm_instance

  def validate(self):
    if self.algorithm_instance.n < self.algorithm_instance.k:
        raise Exception(
            'Długość dna jest krótsza niż długość oligonukleotydu!')
    if self.algorithm_instance.errors not in ('none', 'negative', 'positive', 'all'):
        raise Exception('Nieznany typ błędu!')
    if self.algorithm_instance.k != len(self.algorithm_instance.initial_oligo):
        raise Exception('Zła długość początkowego oligonukleotydu!')
    for oligo in self.algorithm_instance.spectrum:
        if self.algorithm_instance.k != len(oligo):
            raise Exception('Zła długość oligonukleotydu w spektrum!')
    if self.algorithm_instance.initial_oligo not in self.algorithm_instance.spectrum:
        self.algorithm_instance.spectrum.append(self.algorithm_instance.initial_oligo)

  def reconstruct(self, spectrum_order):
    reconstructed = self.algorithm_instance.initial_oligo
    if spectrum_order is not None:
        for _, connection in enumerate(spectrum_order):
            reconstructed = reconstructed + \
                self.algorithm_instance.spectrum[connection[0]][-connection[1]:]
    return reconstructed

  def solve(self):
    """
    Returns
    -------
    string
      Złożone potencjalne DNA
    """
    self.validate()
    self.algorithm_instance.before_run()
    spectrum_order = self.algorithm_instance.spectrum_order()
    self.result = self.reconstruct(spectrum_order)
    return self.result

  def rate(self, sequence):
    string_distance = LevenshteinDistance.compute(None, self.result, sequence)
    max_distance = max(len(self.result), len(sequence))
    similarity = 100 * (1. - float(string_distance) / float(max_distance))
    similarity = round(similarity, 2)
    print("Similarity: " + str(similarity) + "% (Levenshstein distance: " + str(string_distance) + ")")
    return similarity

  def choose_algorithm(self, name = 'Greedy'):
    if name == 'Greedy':
        return Greedy
    elif name == 'Ant':
        return Ant
    else:
        raise RuntimeError('Algorithm not found')
