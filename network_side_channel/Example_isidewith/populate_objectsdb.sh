#!/bin/bash

#Remove the old database if it exists
rm objectsdb.sqlite3 || echo "Object DB never existed"


#Initialize the database
python initialize_db.py objectsdb.sqlite3

#Populate the database with Trump entries
for f in $(find TrainData/ -type f -name "*trump*")
do
	python process_isidewith_trace.py $f objectsdb.sqlite3 Trump TRAIN
done


#Populate the database with Clinton entries
for f in $(find TrainData/ -type f -name "*clinton*")
do
	python process_isidewith_trace.py $f objectsdb.sqlite3 Clinton TRAIN
done
