import psycopg2

def trick(r):
    "Convert tuple element to string"
    return r.strip("[()]").split(",")

def extend(events, cur):
	"Extend events list"
	record = cur.fetchall()
	for i in range(cur.rowcount):
		events.extend(trick(record[i][0]))
	return events

conn = psycopg2.connect("dbname=mimic user=mimic")
cur = conn.cursor()


cur.execute("DELETE FROM selEvents")

events = []
cur.execute("SELECT original_name FROM selDiagnoses")
events = extend(events, cur)

cur.execute("SELECT original_name FROM selMedications")
events = extend(events, cur)

cur.execute("SELECT original_name FROM selProcedures")
events = extend(events, cur)

id = 0
for event in events:
    cur.execute("INSERT INTO selEvents (id_event, event) VALUES(%s,%s);",(id,event))
    id += 1

conn.commit()
cur.close()
conn.close()
