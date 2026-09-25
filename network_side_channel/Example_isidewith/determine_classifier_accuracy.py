#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from determine_type_module import getBayesianType

TRUMP_CLASSIFIER = "TrumpClassifier.json"
CLINTON_CLASSIFIER = "ClintonClassifier.json"
DATA_FOLDER = "TestData"

trump_stats = {"TruePositive": 0, "FalsePositive": 0, "Undetected": 0, "total" : 0}
clinton_stats = {"TruePositive": 0, "FalsePositive": 0, "Undetected": 0, "total": 0}

for pcap_file in os.listdir(DATA_FOLDER):
	if pcap_file[0] == 't':
		ground_truth = TRUMP_CLASSIFIER
	elif pcap_file[0] == 'c':
		ground_truth = CLINTON_CLASSIFIER
	
	test_result = getBayesianType("{}/{}".format(DATA_FOLDER,pcap_file), TRUMP_CLASSIFIER, CLINTON_CLASSIFIER)
	
	if ground_truth == TRUMP_CLASSIFIER:
		#Did the classifier get it right?
		if test_result is None:
			trump_stats['Undetected'] = trump_stats['Undetected'] + 1
		elif test_result == ground_truth:
			trump_stats['TruePositive'] = trump_stats['TruePositive'] + 1
		else:
			trump_stats['FalsePositive'] = trump_stats['FalsePositive'] + 1
		
		trump_stats["total"] = trump_stats["total"] + 1
	
	elif ground_truth == CLINTON_CLASSIFIER:
		#Did the classifier get it right?
		if test_result is None:
			clinton_stats['Undetected'] = clinton_stats['Undetected'] + 1
		elif test_result == ground_truth:
			clinton_stats['TruePositive'] = clinton_stats['TruePositive'] + 1
		else:
			clinton_stats['FalsePositive'] = clinton_stats['FalsePositive'] + 1
		
		clinton_stats["total"] = clinton_stats["total"] + 1
	
	print ""	
	print "Tested with {}, should be {}, result was {}".format(pcap_file, ground_truth, test_result)
	

print "Trump: True Positive rate = {}/{}, False Positive rate = {}/{}, Non-detection rate = {}/{}".format(trump_stats['TruePositive'],trump_stats['total'],trump_stats['FalsePositive'],trump_stats['total'],trump_stats['Undetected'],trump_stats['total'])
print "Clinton: True Positive rate = {}/{}, False Positive rate = {}/{}, Non-detection rate = {}/{}".format(clinton_stats['TruePositive'],clinton_stats['total'],clinton_stats['FalsePositive'],clinton_stats['total'],clinton_stats['Undetected'],clinton_stats['total'])
