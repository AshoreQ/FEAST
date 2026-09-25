#!/bin/bash

#Remove the old database if it exists
rm objectsdb.sqlite3 || echo "Object DB never existed"


#Initialize the database
python initialize_db.py objectsdb.sqlite3

#Populate the database with Hurricane Irma entries
for f in $(find TrainData/ -type f -name "*_hurricane_irma_*")
do
	python process_google_trace.py $f objectsdb.sqlite3 HurricaneIrma TRAIN
done


#Populate the database with Matt Lauer entries
for f in $(find TrainData/ -type f -name "*_matt_lauer_*")
do
	python process_google_trace.py $f objectsdb.sqlite3 MattLauer TRAIN
done


#Populate the database with Tom Petty entries
for f in $(find TrainData/ -type f -name "*_tom_petty_*")
do
	python process_google_trace.py $f objectsdb.sqlite3 TomPetty TRAIN
done


#Populate the database with Super Bowl entries
for f in $(find TrainData/ -type f -name "*_super_bowl_*")
do
	python process_google_trace.py $f objectsdb.sqlite3 SuperBowl TRAIN
done


#Populate the database with Las Vegas shooting entries
for f in $(find TrainData/ -type f -name "*_las_vegas_shooting_*")
do
	python process_google_trace.py $f objectsdb.sqlite3 LasVegasShooting TRAIN
done


#Populate the database with Mayweather vs McGregor Fight entries
for f in $(find TrainData/ -type f -name "*_mayweather_vs_mcgregor_fight_*")
do
	python process_google_trace.py $f objectsdb.sqlite3 MayweatherVsMcGregorFight TRAIN
done


#Populate the database with Solar eclipse entries
for f in $(find TrainData/ -type f -name "*_solar_eclipse_*")
do
	python process_google_trace.py $f objectsdb.sqlite3 SolarEclipse TRAIN
done


#Populate the database with Hurricane Harvey entries
for f in $(find TrainData/ -type f -name "*_hurricane_harvey_*")
do
	python process_google_trace.py $f objectsdb.sqlite3 HurricaneHarvey TRAIN
done


#Populate the database with Aaron Hernandez entries
for f in $(find TrainData/ -type f -name "*_aaron_hernandez_*")
do
	python process_google_trace.py $f objectsdb.sqlite3 AaronHernandez TRAIN
done


#Populate the database with Fidget spinner entries
for f in $(find TrainData/ -type f -name "*_fidget_spinner_*")
do
	python process_google_trace.py $f objectsdb.sqlite3 FidgetSpinner TRAIN
done


