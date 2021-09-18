#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

import sys
from utils.algorithm_helper import choose_algorithm
from generator import SbhInstance

if len(sys.argv) < 2:
      print('Podaj nazwę folderu z instancjami do rozwiązania.')
      exit(1)
Algorithm = choose_algorithm()
if len(sys.argv) > 2:
      Algorithm = choose_algorithm(sys.argv[2])

instances = 0
perfect_runs = []
sum = 0.0
worst_case = { 'path': None, 'similarity': 100.0 }
instance_dir_path = sys.argv[1] # 'instances'
for instance_path in Path(instance_dir_path).iterdir():
    instance = SbhInstance.read(instance_path)
    solver = Algorithm.from_instance(instance)
    print(instance_path)
    solver.solve()
    instances += 1
    similarity = solver.rate(instance.sequence)
    sum += similarity
    if similarity == 100.0:
          perfect_runs.append(instance_path)
    if similarity < worst_case['similarity']:
          worst_case = worst_case = { 'path': instance_path, 'similarity': similarity }

print('---------')
print('Average similarity: ' + str(round(sum / float(instances), 2)) + '%')
print('Worst case: ' + str(worst_case['path']) + ' with similarity ' + str(worst_case['similarity']) + '%')
print('Perfect runs: ' + str(len(perfect_runs)))
for _, path in enumerate(perfect_runs):
      print(path)

