#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from algorithm.Greedy import Greedy
import sys
from generator import SbhInstance

if len(sys.argv) < 2:
      print('Podaj nazwę folderu z instancjami do rozwiązania.')
      exit(1)
instance_dir_path = sys.argv[1] # 'instances'
for instance_path in Path(instance_dir_path).iterdir():
    instance = SbhInstance.read(instance_path)
    solver = Greedy.from_instance(instance)
    print(instance_path)
    solver.solve()
    solver.rate(instance.sequence)
