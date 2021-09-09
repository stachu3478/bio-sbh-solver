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
solver = Greedy.from_instance(instance)
# instance.save('text.txt')
# instance.introduce_negative_repeat_errors()
# instance.introduce_negative_leak_errors(0.10)
print(instance.sequence)
print(solver.solve())
solver.rate(instance.sequence)
