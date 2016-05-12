#Prediction Model
import psycopg2
import csv
import codecs
import numpy as np


conn = psycopg2.connect("dbname=mimic user=mimic")
cur = conn.cursor()

#Load Diagnoses Length
cur.execute("SELECT id FROM selDiagnoses")
len_diagnoses = cur.rowcount

#Build Events Dictionary
cur.execute("SELECT * FROM selEvents")
result = cur.fetchall()

dict = {}
for record in result:
    dict[str(record[1])] = int(record[0])

#Load Similarity Matrix
len_event = cur.rowcount 

matrix = np.zeros(shape=(len_event,len_diagnoses))

f = codecs.open("../BuildMatrix/matrix.csv","rb","utf-8")
reader = csv.reader(f)

x = y = 0
for row in reader:
    for point in row:
        #print x,y
        matrix[x][y] = point
        y += 1
    x += 1
    y = 0

    

#Build Event Sequences
def trick(r):
    return r.strip("{}").split(",")

def getList(r1,r2,r3):
    "Get an event sequence"
    list = trick(r1) + trick(r2) + trick(r3)
    return list

cur.execute("SELECT * FROM trainData ORDER BY subject_id")
result = cur.fetchall()


subject_id = result[0][1]
list = []
for record in result:
    #print record[0],subject_id
    
    if subject_id == record[1]:
        list += getList(record[4], record[5], record[6])
    else:
        #print list
        if list:
            seq = np.zeros(shape=(1,len_event))
            for i in list:
                seq[0,int(i)] = 1
            #print seq
            print np.dot(seq, matrix)
            #Seq * Similarity Matrix (subject_id)

            break
        subject_id = record[1]
        list = []
        
    
