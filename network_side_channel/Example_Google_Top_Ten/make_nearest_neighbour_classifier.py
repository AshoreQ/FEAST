#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Goes through all training data, and populates a JSON object with values
and labels corresponding to packet count and Google searched term.
"""

import os

from nearest_neighbour_classify_module import NearestNeighbourClassifier
from pcap_miner import get_total_packet_count

DATA_FOLDER = "TrainData"
JSON_NAME = "nearest_neighbour_classifier.json"

#Declare the classifier
nn_classifier = NearestNeighbourClassifier()

#Train the classifier
for pcap_file in os.listdir(DATA_FOLDER):
	
	if 'hurricane_irma' in pcap_file:
		ground_truth = 'hurricane_irma'
	elif 'matt_lauer' in pcap_file:
		ground_truth = 'matt_lauer'
	elif 'tom_petty' in pcap_file:
		ground_truth = 'tom_petty'
	elif 'super_bowl' in pcap_file:
		ground_truth = 'super_bowl'
	elif 'las_vegas_shooting' in pcap_file:
		ground_truth = 'las_vegas_shooting'
	elif 'mayweather_vs_mcgregor_fight' in pcap_file:
		ground_truth = 'mayweather_vs_mcgregor_fight'
	elif 'solar_eclipse' in pcap_file:
		ground_truth = 'solar_eclipse'
	elif 'hurricane_harvey' in pcap_file:
		ground_truth = 'hurricane_harvey'
	elif 'aaron_hernandez' in pcap_file:
		ground_truth = 'aaron_hernandez'
	elif 'fidget_spinner' in pcap_file:
		ground_truth = 'fidget_spinner'
	
	total_packets = get_total_packet_count("{}/{}".format(DATA_FOLDER, pcap_file))
	nn_classifier.learn(total_packets, ground_truth)
#Save the classifier
nn_classifier.save_learned_data(JSON_NAME)


	

