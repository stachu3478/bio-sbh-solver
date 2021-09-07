#!/usr/bin/env python
# -*- coding: utf-8 -*-

from algorithm.Greedy import Greedy
import sys
from generator import SbhInstance

if len(sys.argv) < 2:
      print('Podaj nazwę pliku z instancją do rozwiązania.')
      exit(1)
instance_path = sys.argv[1] # 'instances/n300k7pe0ne0.04.txt'
instance = SbhInstance.read(instance_path)
solver = Greedy()
solver.n = instance.length
solver.k = instance.oligo_length
solver.spectrum = instance.spectrum
if instance.positive_errors and instance.negative_errors:
      solver.errors = 'all'
elif instance.positive_errors:
      solver.errors = 'positive'
elif instance.negative_errors:
      solver.errors = 'negative'
else:
      solver.errors = 'none'
solver.initial_oligo = instance.initial_oligo
# instance.save('text.txt')
# instance.introduce_negative_repeat_errors()
# instance.introduce_negative_leak_errors(0.10)
print(instance.sequence)
print(solver.solve())
solver.rate(instance.sequence)
