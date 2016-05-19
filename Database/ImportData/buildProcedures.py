#Build Procedures Table
import psycopg2
import csv

conn = psycopg2.connect("dbname=mimic user=mimic")
cur = conn.cursor()

diagFile = open('../Table/procedures.csv', 'rb')
reader = csv.reader(diagFile)

cur.execute("DELETE FROM selProcedures")

rownum = 0 
for row in reader:
    #save header
    if rownum == 0:
        header = row
    else:
        #insert diagnosis into table
        cur.execute("insert into selProcedures (id, original_name, connected_name) values (%s, %s, %s)", 
                    (rownum - 1, row[0].strip(" "), row[1]))
    rownum += 1

conn.commit()
cur.close()
conn.close()

