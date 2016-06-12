# coding=utf-8

import re
import codecs
import string
from string import maketrans
import collections

f1=codecs.open('../Data/train.data','r','utf-8') #读取文本
f2=codecs.open('../Train/event_list/procedure_list.bak','w','utf-8') #写入文本

dict = {}
transtab = maketrans("!()+,.;<=>?@\^_`{|}~-"," "*21)

cnt=0
pattern="^([^(,.]+) \[\*{2}([\d]{1,2})-([\d]{1,2})\*{2}\]:"
p=re.compile(pattern)
for line in f1:
    cnt+=1
    sentence=line[:-1]
    iterator=p.finditer(sentence)
    cnt1=0
    for match in iterator:
        cnt1+=1
        a=[]
        if len(match.regs) == 4:
            pos=match.regs[1]
            a.append(line[pos[0]:pos[1]])
            #print a
            b = str(a).lower().translate(transtab)
            #print b
            if b in dict:
                dict[b] = dict[b] + 1
            else:
                dict[b] = 1
        #f2.writelines("line(" + str(cnt) + "):" + "\t".join(a) + "-------" + line)
    # if cnt1==0:
    #     f2.writelines("line(" + str(cnt) + "): " + line)

#Sort the procedures dictionary
od = sorted(dict.items(), key=lambda x:x[1], reverse = True)

for a in od:
    f2.write(str(a) + '\n')

f1.close()
f2.close()
