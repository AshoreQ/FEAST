#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import sqlite3

from pcap_miner import getSessionSymbolString
from traffic_classifier import ChunkFilter

PCAP_FILE = sys.argv[1]
OBJECTS_DB = sys.argv[2]
CANDIDATE_LABEL = sys.argv[3]
MODE = sys.argv[4]

OUR_IP = "172.19.0.2"
MIN_GAPTIME = 0.25

DB_CONN = sqlite3.connect(OBJECTS_DB)
DB_CUR = DB_CONN.cursor()

time_filter = ChunkFilter(MIN_GAPTIME)

#Get network activity correlated with HTTP event
#SESSION_TRACE = {}
#for session_sym in getSessionSymbolString(PCAP_FILE, OUR_IP, REMOTE_IP):
chunk_index = 0
for session_sym in getSessionSymbolString(PCAP_FILE, OUR_IP, None):
	session_index = str(session_sym[0])
	session_packet_size = session_sym[1]
	session_packet_time = session_sym[2]
	print "Packet Time: {}".format(session_packet_time)
	#if session_index in SESSION_TRACE:
	#	SESSION_TRACE[session_index].append(session_packet_size)
	#else:
	#	SESSION_TRACE[session_index] = [session_packet_size]
	this_chunk = time_filter.feed_packet(session_sym)
	if this_chunk is None:
		print "Not a chunk"
		continue
	
	print "Processing chunk"
	#If there is an actual chunk of network activity, extract features from it
	total_rx = 0
	for ck_packet in this_chunk:
		total_rx += ck_packet[1]
	
	chunk_index += 1
	
	#Add this feature to the database
	DB_CUR.execute("INSERT INTO object_size_map VALUES (?, ?, ?)",(total_rx, CANDIDATE_LABEL, chunk_index))

#Add the total number of chunks to the database
DB_CUR.execute("INSERT INTO total_chunk_map VALUES (?,?)", (chunk_index, CANDIDATE_LABEL))

DB_CONN.commit()
