#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd

col = ['TEXT']
df = pd.read_csv("../MIMIC_III/NOTEEVENTS.csv", skipinitialspace=True, usecols=col, nrows=10000)
fout = open("../Data/train.data", "w")
fout.writelines(df.TEXT)
fout.close()