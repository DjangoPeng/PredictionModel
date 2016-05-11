#Split Train and Test Dataset
import psycopg2

conn = psycopg2.connect("dbname=mimic user=mimic")
cur = conn.cursor()



#Build Events Dictionary
cur.execute("SELECT * FROM selEvents")
result = cur.fetchall()

dict = {}
for record in result:
    dict[str(record[1])] = int(record[0])

    
#Delete Data
cur.execute("DELETE FROM trainData")
cur.execute("DELETE FROM testData")
    
#Split Train and Test Dataset    
cur.execute("SELECT subject_id, admission_date, discharge_date, diagnosis, medication, procedure FROM report_1 ORDER BY subject_id, admission_date DESC")
resultList = cur.fetchall()
id_train = id_test = 0
subject_id = '0'
for record in resultList:
    #convert event to id_event
    diag_id  = []
    med_id = []
    pro_id = []
    diagnoses = record[3].strip("{}").split(",")
    medications = record[4].strip("{}").split(",")
    procedures = record[5].strip("{}").split(",")
    
    #print diagnoses, medications, procedures
    for diag in diagnoses:
        diag_id.append(dict[diag.strip("\"")])
    
    if medications!=['']:
        for med in medications:
            med_id.append(dict[med.strip("\"")])

    if procedures!=['']:
        for pro in procedures:
            pro_id.append(dict[pro.strip("\"")])
        #print diag_id, med_id, pro_id

    if subject_id != str(record[0]):
        #print subject_id, record[0]
        subject_id = str(record[0])
        id_test += 1
        id_train += 1
        cur.execute("INSERT INTO testData (id_test, subject_id, admission_date, discharge_date, diagnosis, medication, procedure) values(%s,%s,%s,%s,%s,%s,%s);",
                   (id_test, subject_id, record[1], record[2], diag_id, med_id, pro_id))
    else:
        id_train += 1
        cur.execute("INSERT INTO trainData (id_train, subject_id, admission_date, discharge_date, diagnosis, medication, procedure, id_test) values(%s,%s,%s,%s,%s,%s,%s,%s);",
                   (id_train, subject_id, record[1], record[2], diag_id, med_id, pro_id, id_test))
        
    
conn.commit()
cur.close()
conn.close()