#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from pcap_miner import getSessionSymbolString
from traffic_classifier import ChunkFilter

OUR_IP = "172.19.0.2"
MIN_GAPTIME = 0.25

time_filter = ChunkFilter(MIN_GAPTIME)

def getBayesianStats(PCAP_FILE, CLASSIFIER_FILE):
	#Load the Baysian classifier
	f_baysian = open(CLASSIFIER_FILE, 'r')
	classifier_map = json.loads(f_baysian.read())
	f_baysian.close()

	estimated_exchanges = []
	
	#Get network activity correlated with HTTP event
	for session_sym in getSessionSymbolString(PCAP_FILE, OUR_IP, None):
		session_index = str(session_sym[0])
		session_packet_size = session_sym[1]
		session_packet_time = session_sym[2]
		#print "Packet Time: {}".format(session_packet_time)
		#if session_index in SESSION_TRACE:
		#	SESSION_TRACE[session_index].append(session_packet_size)
		#else:
		#	SESSION_TRACE[session_index] = [session_packet_size]
		this_chunk = time_filter.feed_packet(session_sym)
		if this_chunk is None:
			#print "Not a chunk"
			continue
		
		#print "Processing chunk"
		#If there is an actual chunk of network activity, extract features from it
		total_rx = 0
		for ck_packet in this_chunk:
			total_rx += ck_packet[1]
		
		estimated_exchanges.append(total_rx)



	#estimated_exchanges.sort()
	#already_stored = []
	baysian_probabilities = []
	for obj_size_index in range(0,len(estimated_exchanges)):
		obj_key = str(estimated_exchanges[obj_size_index]) + ':' + str(obj_size_index)
		#if obj_size not in already_stored:
		#	already_stored.append(obj_size)
		#print obj_size
		#Apply Baysian classification
		if obj_key not in classifier_map:
			baysian_probabilities.append(0.0)
		else:
			"""
			Bayes' Theorem: The probability that this feature corresponds
			to the given candidate is equal to probability that this
			candidate produces the given feature multiplied by the probability
			of the candidate (which we simplify to 1.0) divided by the sum
			of probability of feature given candidate plus probability of
			feature given not candidate
			"""
			true_prob = float(classifier_map[obj_key][0])
			false_prob = float(classifier_map[obj_key][1])
			b_prob = true_prob / (true_prob + false_prob)
			baysian_probabilities.append(b_prob)

	
	#Also apply Bayes' theorem for the estimated number of exchanges (chunks)
	if "CHUNKS:" + str(len(estimated_exchanges)) not in classifier_map:
		bayes_for_chunks = 0.0
	else:
		true_prob = float(classifier_map["CHUNKS:" + str(len(estimated_exchanges))][0])
		false_prob = float(classifier_map["CHUNKS:" + str(len(estimated_exchanges))][1])
		bayes_for_chunks = true_prob / (true_prob + false_prob)
	
	max_prob = max(baysian_probabilities)
	max_count = baysian_probabilities.count(max(baysian_probabilities))
	#print "[DEBUG] Bayesian Probabilities: {}".format(baysian_probabilities)
	
	#total_packets = get_total_packet_count(PCAP_FILE)
	
	return (max_prob, max_count, baysian_probabilities)
	#return baysian_probabilities
	

