import codecs
import numpy as np
from sklearn.manifold import TSNE
from gensim.models import Word2Vec as w2v
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


m = w2v.load("../train/model_12/notes_12.model")


colors=[]
list = []
f = codecs.open("diagnoses.txt","r","utf-8")
for line in f:
    list.append(m[line.strip()])
    colors.append("red")
len1 = len(list)
    
f = codecs.open("medications.txt","r","utf-8")
for line in f:
    list.append(m[line.strip()])
    colors.append("blue")
len2 = len(list)
f = codecs.open("procedures.txt","r","utf-8")    
for line in f:
    list.append(m[line.strip()])
    colors.append("green")
len3 = len(list)    
Z = np.array(list)    


#model = TSNE(n_components=2, random_state=0, perplexity = 100, metric = 'cosine')
#np.set_printoptions(suppress=True)
#model.fit_transform(Z)

pca = PCA(n_components=2)
Z = pca.fit(Z).transform(Z)

x = Z[:,0]
y = Z[:,1]

#print x,y
#fig = plt.figure(figsize=(5,5))

diag = plt.scatter(x[0:len1], y[0:len1], c='red', s = 40, marker='o')
med = plt.scatter(x[len1:len2], y[len1:len2], c='green', s = 40, marker='x')
pro = plt.scatter(x[len2:len3], y[len2:len3], c='blue', s = 40, marker='+')

plt.title("PCA of MIMIC III dataset")
plt.legend((diag,med,pro),
          ('Diagnoses', 'Medications', 'Procedures'),
            scatterpoints=1,
            loc='upper right',
           fontsize = 10
          )

plt.savefig("scatter.png")
plt.show()
