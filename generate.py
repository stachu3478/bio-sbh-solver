#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from generator import SbhInstance

if len(sys.argv) < 2:
      print('Podaj nazwę folderu z wygenerowanymi instancjami')
      exit(1)
base_path = sys.argv[1] # 'instances'

SbhInstance.create_series_into_folder(base_path)