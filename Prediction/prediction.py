#Prediction Model
import psycopg2
import csv
import codecs
import numpy as np


def trick(r):
    "Split all events"
    return r.strip("{}").split(",")

def get_list(r1,r2,r3):
    "Get an event list"
    list = trick(r1) + trick(r2) + trick(r3)
    return list


conn = psycopg2.connect("dbname=mimic user=mimic")
cur = conn.cursor()

#Load Diagnoses Length
cur.execute("SELECT id FROM selDiagnoses")
len_diagnoses = cur.rowcount

#Build Events Dictionary
cur.execute("SELECT * FROM selEvents")
result = cur.fetchall()

event_dict = {}
for record in result:
    event_dict[str(record[1])] = int(record[0])

    
#Build Test Dataset Dictionary
cur.execute("SELECT id_test, diagnosis FROM testData")
result = cur.fetchall()

test_dict = {}
for record in result:
    str_list = trick(record[1])
    int_list = []
    for i in str_list:
        int_list.append(int(i))
    test_dict[record[0]] = int_list

#Create Lists
positive = [0] * len_diagnoses
sample = [0] * len_diagnoses
    
#Load Similarity Matrix
len_event = cur.rowcount 

matrix = np.zeros(shape=(len_event,len_diagnoses))

f = codecs.open("../BuildMatrix/matrix.csv","rb","utf-8")
reader = csv.reader(f)

x = y = 0
for row in reader:
    for point in row:
        #print x, y, point
        matrix[x][y] = point
        y += 1
    x += 1
    y = 0

    
#Build Event Sequences
cur.execute("SELECT * FROM trainData ORDER BY id_train")
result = cur.fetchall()


subject_id = result[0][1]
id_test = result[0][7]
list = []
for record in result:
    #print record[0],subject_id
    
    if subject_id == record[1]:
        #record[4-6] individually represent diagnoses, medications & procedures
        list += get_list(record[4], record[5], record[6])
    else:
        #print list
        if list:
            seq = np.zeros(shape=(1,len_event))
            for i in list:
                if i:
                    seq[0,int(i)] = 1
            p_diagnoses = np.dot(seq, matrix)
            arg_list = np.argsort(p_diagnoses)
            
            #print list
            #print test_dict[id]
            #print arg_list
            
            id = id_test
            if id in test_dict:
                #p_list = arg_list[0][0:len(test_dict[id])]
                p_list = arg_list[0][0:5]
            else:
                print id
                break
            
            #print p_list
            #Check the prediction
            for i in test_dict[id]:
                sample[i] += 1
                if i in p_list:
                    positive[i] += 1
                
            
            #break
       

        subject_id = record[1]
        list += get_list(record[4], record[5], record[6])
        id_test = record[7]
        
for i in range(len(sample)):
    print i, positive[i], sample[i]
