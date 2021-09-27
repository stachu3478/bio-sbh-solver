#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from Solver import Solver
from generator import SbhInstance

if len(sys.argv) < 2:
      print('Podaj nazwę pliku z instancją do rozwiązania.')
      exit(1)
algorithm_name = 'Greedy'
if len(sys.argv) > 2:
      algorithm_name = sys.argv[2]
instance_path = sys.argv[1] # 'instances/n300k7pe0ne0.04.txt'
instance = SbhInstance.read(instance_path)
solver = Solver()
solver.read_from_instance(instance, algorithm_name=algorithm_name)
print(instance.sequence)
print(solver.solve())
solver.rate(instance.sequence)
