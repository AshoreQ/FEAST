#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from pcap_miner import getSessionSymbolString


OUR_IP = "172.19.0.2"

def getBayesianStats(PCAP_FILE, CLASSIFIER_FILE):
	#Load the Baysian classifier
	f_baysian = open(CLASSIFIER_FILE, 'r')
	classifier_map = json.loads(f_baysian.read())
	f_baysian.close()

	#Get network activity correlated with HTTP event
	SESSION_TRACE = {}
	#for session_sym in getSessionSymbolString(PCAP_FILE, OUR_IP, REMOTE_IP):
	for session_sym in getSessionSymbolString(PCAP_FILE, OUR_IP, None):
		session_index = str(session_sym[0])
		session_packet_size = session_sym[1]
		if session_index in SESSION_TRACE:
			SESSION_TRACE[session_index].append(session_packet_size)
		else:
			SESSION_TRACE[session_index] = [session_packet_size]

	#Debug printing
	#for stream_index in range(0, len(SESSION_TRACE.keys())):
	#	print "Stream: {} -- Size: {}".format(str(stream_index), sum(SESSION_TRACE[str(stream_index)]))
	#	print SESSION_TRACE[str(stream_index)]
	#	print ""
		

	#Get unique packet sizes
	#print "--- Unique Packet Sizes ---"
	unique_sizes = []
	for stream_index in range(0, len(SESSION_TRACE.keys())):
		for pkt_size in SESSION_TRACE[str(stream_index)]:
			if pkt_size not in unique_sizes:
				unique_sizes.append(pkt_size)
				#print pkt_size


	#Get all runs through 1370 bytes
	estimated_large_object_sizes = []
	for stream_index in range(0, len(SESSION_TRACE.keys())):
		prev_size = None
		inSession = False
		running_count_size = 0
		for pkt_size in SESSION_TRACE[str(stream_index)]:
			if prev_size is None:
				prev_size = 0
			
			#Do processing..
			
			#Enter a session
			if pkt_size == 1370 and inSession == False:
				inSession = True
				running_count_size = prev_size
			
			#In middle of session
			if pkt_size == 1370 and inSession == True:
				running_count_size += pkt_size
			
			#End of session
			if pkt_size != 1370 and inSession == True:
				running_count_size += pkt_size
				estimated_large_object_sizes.append(running_count_size)
				running_count_size = 0
				inSession = False
			
			
			#Complete processing...
			prev_size = pkt_size

	#print "--- Object Sizes ---"
	estimated_large_object_sizes.sort()
	already_stored = []
	baysian_probabilities = []
	for obj_size in estimated_large_object_sizes:
		if obj_size not in already_stored:
			already_stored.append(obj_size)
			#print obj_size
			#Apply Baysian classification
			if str(int(obj_size)) not in classifier_map:
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
				true_prob = float(classifier_map[str(int(obj_size))][0])
				false_prob = float(classifier_map[str(int(obj_size))][1])
				b_prob = true_prob / (true_prob + false_prob)
				baysian_probabilities.append(b_prob)


	#print ""
	#print ""
	#print ""
	#print "P({}) = {}, counted {} times".format(CLASSIFIER_FILE, max(baysian_probabilities), baysian_probabilities.count(max(baysian_probabilities)))
	
	max_prob = max(baysian_probabilities)
	max_count = baysian_probabilities.count(max(baysian_probabilities))
	return (max_prob, max_count)
	
