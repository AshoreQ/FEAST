#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import numpy as np
np.random.seed(0) #Run deterministically

import sklearn.naive_bayes
import sklearn.ensemble
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree

from pcap_miner import getSessionSymbolString

OUR_IP = "172.19.0.2"

#Train classifiers with samples from TrainData/
train_data = os.listdir('TrainData')
clinton_training_samples = []
trump_training_samples = []

for pcap_sample in train_data:
	if 'clinton' in pcap_sample:
		clinton_training_samples.append(pcap_sample)
	elif 'trump' in pcap_sample:
		trump_training_samples.append(pcap_sample)

print "Clinton: {}".format(clinton_training_samples)
print len(clinton_training_samples)
print ""
print "Trump: {}".format(trump_training_samples)
print len(trump_training_samples)

#Feature extraction
clinton_features = []

for clinton_sample in clinton_training_samples:
	#Get network activity correlated with HTTP event
	SESSION_TRACE = {}
	for session_sym in getSessionSymbolString("TrainData/{}".format(clinton_sample), OUR_IP, None):
		session_index = str(session_sym[0])
		session_packet_size = session_sym[1]
		if session_index in SESSION_TRACE:
			SESSION_TRACE[session_index].append(session_packet_size)
		else:
			SESSION_TRACE[session_index] = [session_packet_size]


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
	
	clinton_features.append(estimated_large_object_sizes[:])

print ""
print ""
print "Clinton Features"
print "----------------"
print ""
for cf in clinton_features:
	print "- {}".format(cf)
	print ""


trump_features = []

for trump_sample in trump_training_samples:
	#Get network activity correlated with HTTP event
	SESSION_TRACE = {}
	for session_sym in getSessionSymbolString("TrainData/{}".format(trump_sample), OUR_IP, None):
		session_index = str(session_sym[0])
		session_packet_size = session_sym[1]
		if session_index in SESSION_TRACE:
			SESSION_TRACE[session_index].append(session_packet_size)
		else:
			SESSION_TRACE[session_index] = [session_packet_size]


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
	
	trump_features.append(estimated_large_object_sizes[:])

print ""
print ""
print "Trump Features"
print "--------------"
print ""
for tf in trump_features:
	print "- {}".format(tf)
	print ""

#Train a scikit-learn model
complete_trainset = []
complete_labelset = []

#Get the maximum and minimum object sizes
tmp = []
for cf in clinton_features:
	for obj_size in cf:
		tmp.append(obj_size)

for tf in trump_features:
	for obj_size in tf:
		tmp.append(obj_size)

PACKET_MIN = min(tmp)
PACKET_MAX = max(tmp)

for cf in clinton_features:
	feature_line = []
	for i in range(PACKET_MIN, PACKET_MAX+1):
		feature_line.append(bool(i in cf))
	complete_trainset.append(feature_line[:])
	complete_labelset.append(0)

for tf in trump_features:
	feature_line = []
	for i in range(PACKET_MIN, PACKET_MAX+1):
		feature_line.append(bool(i in tf))
	complete_trainset.append(feature_line[:])
	complete_labelset.append(1)


print "len(complete_trainset) = {}".format(len(complete_trainset))
print "len(complete_labelset) = {}".format(len(complete_labelset))

#-----------------------------------------------------------------------

#...create the model
#clf = sklearn.naive_bayes.BernoulliNB() #Okay accuracy
clf = tree.DecisionTreeClassifier() #Perfect accuracy
#clf = sklearn.ensemble.AdaBoostClassifier() #Perfect accuracy
#clf = KNeighborsClassifier() #Okay accuracy

clf.fit(complete_trainset, complete_labelset)

#-----------------------------------------------------------------------

#Evaluate how well this classifier predicts
test_data = os.listdir('TestData')
clinton_testing_samples = []
trump_testing_samples = []

for pcap_sample in test_data:
	if 'clinton' in pcap_sample:
		clinton_testing_samples.append(pcap_sample)
	elif 'trump' in pcap_sample:
		trump_testing_samples.append(pcap_sample)

#Feature extraction...
clinton_test_features = []

for clinton_sample in clinton_testing_samples:
	#Get network activity correlated with HTTP event
	SESSION_TRACE = {}
	for session_sym in getSessionSymbolString("TestData/{}".format(clinton_sample), OUR_IP, None):
		session_index = str(session_sym[0])
		session_packet_size = session_sym[1]
		if session_index in SESSION_TRACE:
			SESSION_TRACE[session_index].append(session_packet_size)
		else:
			SESSION_TRACE[session_index] = [session_packet_size]


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
	
	clinton_test_features.append(estimated_large_object_sizes[:])


trump_test_features = []

for trump_sample in trump_testing_samples:
	#Get network activity correlated with HTTP event
	SESSION_TRACE = {}
	for session_sym in getSessionSymbolString("TestData/{}".format(trump_sample), OUR_IP, None):
		session_index = str(session_sym[0])
		session_packet_size = session_sym[1]
		if session_index in SESSION_TRACE:
			SESSION_TRACE[session_index].append(session_packet_size)
		else:
			SESSION_TRACE[session_index] = [session_packet_size]


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
	
	trump_test_features.append(estimated_large_object_sizes[:])

print ""
print ""

print "Clinton Results"
print "---------------"
print ""
tp_count = 0
fp_count = 0
for clinton_test_feat in clinton_test_features:
	feature_line = []
	for i in range(PACKET_MIN, PACKET_MAX+1):
		feature_line.append(bool(i in clinton_test_feat))
	pred = (clf.predict([feature_line])[0])
	if pred == 0:
		print "Should be Clinton, Predicted Clinton"
		tp_count += 1
	elif pred == 1:
		print "Should be Clinton, Predicted Trump"
		fp_count += 1
print ""
print "True Positive Rate: {}/{}, False Positive Rate: {}/{}".format(tp_count, len(clinton_test_features), fp_count, len(clinton_test_features))

print ""
print "***"
print ""

print "Trump Results"
print "-------------"
print ""
tp_count = 0
fp_count = 0
for trump_test_feat in trump_test_features:
	feature_line = []
	for i in range(PACKET_MIN, PACKET_MAX+1):
		feature_line.append(bool(i in trump_test_feat))
	pred = (clf.predict([feature_line])[0])
	if pred == 0:
		print "Should be Trump, Predicted Clinton"
		fp_count += 1
	elif pred == 1:
		print "Should be Trump, Predicted Trump"
		tp_count += 1
print ""
print "True Positive Rate: {}/{}, False Positive Rate: {}/{}".format(tp_count, len(trump_test_features), fp_count, len(trump_test_features))

