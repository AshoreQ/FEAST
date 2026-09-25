#!/bin/bash

#Train Hurricane Irma classifier
python determine_unique_features.py objectsdb.sqlite3 HurricaneIrma classifier__hurricane_irma.json


#Train Matt Lauer classifier
python determine_unique_features.py objectsdb.sqlite3 MattLauer classifier__matt_lauer.json


#Train Tom Petty classifier
python determine_unique_features.py objectsdb.sqlite3 TomPetty classifier__tom_petty.json


#Train Super Bowl classifier
python determine_unique_features.py objectsdb.sqlite3 SuperBowl classifier__super_bowl.json


#Train Las Vegas shooting classifier
python determine_unique_features.py objectsdb.sqlite3 LasVegasShooting classifier__las_vegas_shooting.json


#Train Mayweather vs McGregor Fight classifier
python determine_unique_features.py objectsdb.sqlite3 MayweatherVsMcGregorFight classifier__mayweather_vs_mcgregor_fight.json


#Train Solar eclipse classifier
python determine_unique_features.py objectsdb.sqlite3 SolarEclipse classifier__solar_eclipse.json


#Train Hurricane Harvey classifier
python determine_unique_features.py objectsdb.sqlite3 HurricaneHarvey classifier__hurricane_harvey.json


#Train Aaron Hernandez classifier
python determine_unique_features.py objectsdb.sqlite3 AaronHernandez classifier__aaron_hernandez.json


#Train Fidget spinner classifier
python determine_unique_features.py objectsdb.sqlite3 FidgetSpinner classifier__fidget_spinner.json

#Create the nearest neighbor classifier
python make_nearest_neighbour_classifier.py
