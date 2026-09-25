#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bayesian_classify_pcap_module import getBayesianStats

def getBayesianType(PCAP_FILE, TYPE_A_CLASSIFIER, TYPE_B_CLASSIFIER):
	
	type_a_test_results = getBayesianStats(PCAP_FILE, TYPE_A_CLASSIFIER)
	type_b_test_results = getBayesianStats(PCAP_FILE, TYPE_B_CLASSIFIER)

	if type_a_test_results[0] > type_b_test_results[0]:
		#print "Capture is of type {}".format(TYPE_A_CLASSIFIER)
		return TYPE_A_CLASSIFIER

	if type_b_test_results[0] > type_a_test_results[0]:
		#print "Capture is of type {}".format(TYPE_B_CLASSIFIER)
		return TYPE_B_CLASSIFIER

	#They must both have an equal max probability
	if type_a_test_results[1] > type_b_test_results[1]:
		#print "Capture is of type {}".format(TYPE_A_CLASSIFIER)
		return TYPE_A_CLASSIFIER

	elif type_b_test_results[1] > type_a_test_results[1]:
		#print "Capture is of type {}".format(TYPE_B_CLASSIFIER)
		return TYPE_B_CLASSIFIER

	else:
		#print "Unknown type of capture"
		return None
