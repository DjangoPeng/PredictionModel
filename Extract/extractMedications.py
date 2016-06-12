# coding=utf-8

import re
import codecs
import string
from string import maketrans
import collections


f1=codecs.open('../Data/train.data','r','utf-8') 
f2=codecs.open('../Train/event_list/medication_list.bak','w','utf-8') 

isMed = False
dict= {}

p=re.compile(r"(?:[^a-zA-Z]+)")
cnt = 0

for line in f1:
    if "Discharge Medications:" in line:
        #cnt+=1
        isMed = True
        continue
    if isMed:
        if line in ['\n', '\r\n']:
            isMed = False
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


f2.write("Total Discharge Medications:\t{}\n".format(cnt))
#Sort the medications dictionary
od = sorted(dict.items(), key=lambda x:x[1], reverse = True)
for a in od:
    f2.write(str(a) + '\n')

f1.close()
f2.close()

        
    