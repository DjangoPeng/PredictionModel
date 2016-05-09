#!/usr/bin/python
# -*- coding: utf-8 -*-
import string
from string import maketrans


fin = open('conj.txt','r')
newtab = []
for line in fin:
    newtab.append(line.strip())
fin.close()
   
fin = open('split.txt','r')
oldtab = []
for line in fin:
    oldtab.append(line.strip())
fin.close()

length = len(newtab)
    
fin = open('../Data/train.data', 'r')
fout = open('../Data/train_rep.data','w')

transtab = maketrans("!()+,.;<=>?@\^_`{|}~"," "*20)

for line in fin:
        
    #delete the punctuation
    line = line.lower().translate(transtab)

    #replace the diagnosis with conj_diagnosis
    for i in range(length):
        line = line.replace(oldtab[i], newtab[i])            
    fout.write(line)