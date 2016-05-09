#Split Train and Test Dataset
import psycopg2

conn = psycopg2.connect("dbname=mimic user=mimic")
cur = conn.cursor()

cur.execute("select subject_id, admission_date, discharge_date, diagnosis, medication, procedure from report_1 order by subject_id, admission_date desc")
resultList = cur.fetchall()
id_train = id_test = 0
subject_id = '0'
for record in resultList:
    if subject_id != str(record[0]):
        #print subject_id, record[0]
        subject_id = str(record[0])
        id_test += 1
        id_train += 1
        cur.execute("insert into testData (id_test, subject_id, admission_date, discharge_date, diagnosis, medication, procedure) values(%s,%s,%s,%s,%s,%s,%s);",
                   (id_test, subject_id, record[1], record[2], record[3], record[4], record[5]))
    else:
        id_train += 1
        cur.execute("insert into trainData (id_train, subject_id, admission_date, discharge_date, diagnosis, medication, procedure, id_test) values(%s,%s,%s,%s,%s,%s,%s,%s);",
                    (id_train, subject_id, record[1], record[2], record[3], record[4], record[5], id_test))
        
    
conn.commit()
cur.close()
conn.close()