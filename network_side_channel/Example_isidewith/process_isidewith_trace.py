#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import sqlite3

from pcap_miner import getSessionSymbolString

PCAP_FILE = sys.argv[1]
OBJECTS_DB = sys.argv[2]
CANDIDATE_LABEL = sys.argv[3]
MODE = sys.argv[4]

OUR_IP = "172.19.0.2"
REMOTE_IP = "52.84.143.148" #www.isidewith.com

DB_CONN = sqlite3.connect(OBJECTS_DB)
DB_CUR = DB_CONN.cursor()

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
for stream_index in range(0, len(SESSION_TRACE.keys())):
	print "Stream: {} -- Size: {}".format(str(stream_index), sum(SESSION_TRACE[str(stream_index)]))
	print SESSION_TRACE[str(stream_index)]
	print ""
	

#Get unique packet sizes
print "--- Unique Packet Sizes ---"
unique_sizes = []
for stream_index in range(0, len(SESSION_TRACE.keys())):
	for pkt_size in SESSION_TRACE[str(stream_index)]:
		if pkt_size not in unique_sizes:
			unique_sizes.append(pkt_size)
			print pkt_size


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

print "--- Object Sizes ---"
estimated_large_object_sizes.sort()
already_stored = []
for obj_size in estimated_large_object_sizes:
	if obj_size not in already_stored:
		already_stored.append(obj_size)
		print obj_size
		if MODE == "TRAIN":
			#Store to DB
			DB_CUR.execute("INSERT INTO object_size_map VALUES (?, ?)",(obj_size, CANDIDATE_LABEL))
		
		elif MODE == "CLASSIFY":
			print "Classifier to be implemented"

DB_CONN.commit()
