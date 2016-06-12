# coding=utf-8

import re
import codecs
import string
from string import maketrans
import collections

f1=codecs.open('../Data/train.data','r','utf-8') #读取文本
f2=codecs.open('../Train/event_list/diagnosis_list.bak','w','utf-8') #写入文本
isDiag = False
dict= {}

cnt = 0
p=re.compile(r"(?:[^a-zA-Z]+)")

for line in f1:
    if "Discharge Diagnosis:" in line:
        isDiag = True
        continue
    if isDiag:
        if line in ['\n', '\r\n']:
            isDiag = False
            continue
        
        result=p.match(line)
        if result:
            line = line.replace(result.group(0), "")
        line = line.lower().strip()
        cnt = cnt + 1
        if line not in dict:
            dict[line] = 1
        else:
            dict[line] = dict[line] + 1

f2.write("Total Discharge Diagnoses:\t{}\n".format(cnt))

#Sort the diagnoses dictionary
od = sorted(dict.items(), key=lambda x:x[1], reverse = True)
for a in od:
    f2.write(str(a) + '\n')

f1.close()
f2.close()
        
    