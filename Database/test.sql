SELECT *
FROM selDiagnoses
;

SELECT *
FROM report_1
WHERE diagnosis='{sepsis}'
;

SELECT *
FROM selMedications
;

SELECT *
FROM testData
ORDER BY subject_id
LIMIT 100
;

SELECT *
FROM report_1
LIMIT 10
;

SELECT *
FROM report_1
WHERE subject_id = 305
;

SELECT *
FROM trainData
LIMIT 100
;

SELECT *
FROM selEvents
;

SELECT *
FROM selDiagnoses
;

SELECT *
FROM trainData 
ORDER BY id_train
limit 10
;