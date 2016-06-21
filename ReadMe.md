# Diagnoses Prediction Model

## Introduction 
This is an unsupervised learning model to predict the patient diagnoses in the future. The data set is [MIMIC III](http://mimic.physionet.org), which is developed by MIT lab. 

I extracted 7k+ discharge reports from the *NOTEEVENTS.csv* (A notes table in the MIMIC III database which has more than 20k reports). 

## Data
MIMIC is an openly available dataset developed by the MIT Lab for Computational Physiology, comprising deidentified health data associated with >40,000 critical care patients. It includes demographics, vital signs, laboratory tests, medications, and more.

*MIMIC-III, a freely accessible critical care database. Johnson AEW, Pollard TJ, Shen L, Lehman L, Feng M, Ghassemi M, Moody B, Szolovits P, Celi LA, and Mark RG. Scientific Data (2016). DOI: 10.1038/sdata.2016.35*

## Feature

I have extracted 3 kinds of data as the feature for train and predict the diagnoses. 

* Diagnoses
* Medications
* Procedures

## Language Model
As we all know, Word2Vec is a efficiency and flexible tool to generate the word vectors and nerual network language model. So I trained the MIMIC III data by word2vec with **window = 200** and **size = 400**.

## Workflow
	1.Request the data
	2.Extract all notes and features
	3.NLP and conjunct the feature phrases
	4.Train the language model
	5.Get the feature word vector
	6.Build the events matrix
	7.Build and split the discharge reports database
	8.Build the feature tables
	9.Prediction model
	10.Visual
	
