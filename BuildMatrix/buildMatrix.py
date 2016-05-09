# coding = utf-8

import codecs
import numpy as np
from gensim.models import Word2Vec as w2v

model = w2v.load("../Train/model_10/notes_10.model")

f1 = codecs.open("diagnoses.txt", "r", "utf-8")
f2 = codecs.open("allevents.txt", "r", "utf-8")

diagnoses = []
for diag in f1:
    diagnoses.append(diag.strip())


events = []
for event in f2:
    events.append(event.strip())

matrix = [[0 for x in range(30)] for x in range(160)]

for i in range(len(events)):
    for j in range(len(diagnoses)):
        print i,j
        matrix[i][j] = model.similarity(events[i], diagnoses[j])

np.savetxt("matrix.csv", matrix, delimiter = ',')

