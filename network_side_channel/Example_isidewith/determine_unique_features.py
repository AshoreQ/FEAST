#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import sqlite3
import json

OBJECTS_DB = sys.argv[1]
CANDIDATE_LABEL = sys.argv[2]
CLASSIFIER_FILE = sys.argv[3]

#Connect to the database
DB_CONN = sqlite3.connect(OBJECTS_DB)
DB_CUR = DB_CONN.cursor()


"""
Build a dictionary mapping object size to tuple (P(TP), P(FP)) where
P(TP) is the true positive probability and P(FP) is the false positive
probability.
"""
classifier_map = {}

def get_tp_fp_rates(size, label):
	this_cur = DB_CONN.cursor()
	tp = 0
	fp = 0
	for sz, lbl in this_cur.execute("SELECT obj_size, obj_label FROM object_size_map"):
		if sz == size:
			#Match. Is it true or false?
			if lbl == label:
				tp += 1
			else:
				fp += 1
	
	return (tp, fp)


#Build the classifier_map
for sz, lbl in DB_CUR.execute("SELECT obj_size, obj_label FROM object_size_map"):
	print sz
	#Add this size to the classifier_map if it's not there already
	if str(int(sz)) not in classifier_map.keys():
		classifier_map[str(int(sz))] = get_tp_fp_rates(sz, CANDIDATE_LABEL)

		
#Display the results of the classifier
#for feature in classifier_map:
#	print "TP({}) = {}, FP({}) = {}".format(feature, classifier_map[feature][0], feature, classifier_map[feature][1])


#Order the best features for classification
ratio_map = {}
for feature in classifier_map:
	try:
		ratio_map[feature] = float(classifier_map[feature][0])/float(classifier_map[feature][1])
	except ZeroDivisionError:
		if classifier_map[feature][0] != 0:
			ratio_map[feature] = 100*classifier_map[feature][0]
		else:
			ratio_map[feature] = 0


#semi_ordered_classifiers = []

for key in sorted(ratio_map.iteritems(), key=lambda (k,v): (v,k)):
	feature = key[0]
	print "TP({}) = {}, FP({}) = {}".format(feature, classifier_map[feature][0], feature, classifier_map[feature][1])
	#semi_ordered_classifiers.append((feature, classifier_map[feature][0], classifier_map[feature][1]))
	#print key


#for oc in sorted(semi_ordered_classifiers, key=lambda tup: tup[1]):
#	print oc

#Save the classifier_map
f_json = open(CLASSIFIER_FILE, 'w')
f_json.write(json.dumps(classifier_map))
f_json.close()
