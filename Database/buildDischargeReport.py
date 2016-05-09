#Build Discharge Reports Table
import re
import psycopg2


conn = psycopg2.connect("dbname=mimic user=mimic")
cur = conn.cursor()

#Load Diagnoses List
cur.execute("select original_name from selDiagnoses")
diagList=cur.fetchall()
diags = []
for diag in diagList:
    diags.append(str(diag[0]))

#Load Medications List
cur.execute("select original_name from selMedications")
medList = cur.fetchall()
meds = []
for med in medList:
    meds.append(str(med[0]))

#Load Procedures List
cur.execute("select original_name from selProcedures")
proList = cur.fetchall()
pros = []
for pro in proList:
    pros.append(str(pro[0]))
    
#Get All Reports
cur.execute("select * from report;")
recordList=cur.fetchall()
cur.execute("truncate table report_1;")
for record in recordList:
    #Get the discharge report text
    note = str(record[4])
    #print note
    
    #Get the Admission Date
    m=re.search(r"(Admission Date:)(\ )+(\[\*{2})(\d{4}\-\d{1,2}\-\d{1,2})(\*{2}\])", note)
    if m:
        adDate=m.group(4)
    else:
        continue
    
    #Get the Discharge Date
    m=re.search(r"(Discharge Date:)(\ )+(\[\*{2})(\d{4}\-\d{1,2}\-\d{1,2})(\*{2}\])", note)
    if m:
        disDate=m.group(4)
    else:
        continue
    
    #Get the Diagnoses
    m=re.search(r"(Discharge Diagnosis:\n)([a-zA-Z0-9].*\n)+(\n{2,3})", note)
    if m:
        curDiags = []
        curDiagnoses = m.group(0).lower()
        for diag in diags:
            if curDiagnoses.find(diag) > 0:
                curDiags.append(diag)
    if len(curDiags) == 0:
        continue
                
    #Get the Medications
    m = re.search(r"(Discharge Medications:\n)([a-zA-Z0-9].*\n)+(\n{2,3})", note)
    if m:
        curMeds = []
        curMedications = m.group(0).lower()
        for med in meds:
            if curMedications.find(med):
                curMeds.append(med)
                
    
    #Get the Procedures
    curPros = []
    for pro in pros:
        if note.lower().find(pro):
            curPros.append(pro)
    
    #Insert Record Into Report_1 Table
    cur.execute("insert into report_1 (hadm_id, subject_id, chardate, category, text, admission_date, discharge_date, diagnosis, medication, procedure) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",  
            (record[0],record[1],record[2], record[3], record[4],adDate, disDate, curDiags, curMeds, curPros))

conn.commit()
cur.close()
conn.close()