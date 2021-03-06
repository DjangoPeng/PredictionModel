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
cur.execute("DELETE FROM report_1;")
cur.execute("SELECT * FROM report;")
recordList=cur.fetchall()
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
    #m=re.search(r"(Discharge Diagnosis:\n)([a-zA-Z0-9].*\n)+(\n{1,2,3})", note)
    m=re.search(r"(Discharge Diagnosis:\n)([a-zA-Z0-9].*\n)+", note)
    curDiags = []
    if m:
        #print m.group(0)
        curDiagnoses = m.group(0).lower()
        for diag in diags:
            if curDiagnoses.find(diag) >= 0:
                curDiags.append(diag)
        if len(curDiags) == 0:
            continue
    else:
        #print "---------Diagnoses--------"
        continue
                
    #Get the Medications
    #m = re.search(r"(Discharge Medications:\n)([a-zA-Z0-9].+\n)+(\n{1,2,3}})", note)
    m = re.search(r"(Discharge Medications:\n)([a-zA-Z0-9].*\n)+", note)
    curMeds = []
    if m:
        #print m.group(0)
        curMedications = m.group(0).lower()
        #print curMedications
        for med in meds:
            if curMedications.find(med) >= 0:
                curMeds.append(med)
                #print med,curMedications.find(med)
        #print curMeds
        #print record[4]


    #Get the Procedures
    curPros = []
    for pro in pros:
        if note.lower().find(pro) >= 0:
            curPros.append(pro)
    
    #Insert Record Into Report_1 Table
    cur.execute("INSERT INTO report_1 (hadm_id, subject_id, chardate, category, text, admission_date, discharge_date, diagnosis, medication, procedure) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",  
            (record[0],record[1],record[2], record[3], record[4],adDate, disDate, curDiags, curMeds, curPros))

conn.commit()
cur.close()
conn.close()
    
    
    
    
    