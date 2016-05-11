import psycopg2
import codecs

conn = psycopg2.connect("dbname=mimic user=mimic")
cur = conn.cursor()

f = codecs.open("../Table/allevents_o.txt","r","utf-8")

cur.execute("DELETE FROM selEvents")

events = []
id = 0

for event in f:
    cur.execute("INSERT INTO selEvents (id_event, event) VALUES(%s,%s);",(id,str(event).strip()))
    id += 1

conn.commit()
cur.close()
conn.close()
