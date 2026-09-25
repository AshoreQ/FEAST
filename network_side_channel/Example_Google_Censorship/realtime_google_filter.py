#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	Before running this program add the following iptables rules:
		- sudo iptables -t raw -A PREROUTING -s <CONTAINER_IP> -j NFQUEUE --queue-num 0
		- sudo iptables -I DOCKER -d <CONTAINER_IP> -j NFQUEUE --queue-num 0
	
	After running this program remove the iptables rules:
		- sudo iptables -t raw -D PREROUTING -s <CONTAINER_IP> -j NFQUEUE --queue-num 0
		- sudo iptables -D DOCKER -d <CONTAINER_IP> -j NFQUEUE --queue-num 0
	
"""


from determine_type_module import getHybridClassifierType

from scapy.all import *
import nfqueue

import socket
import sys

CLASSIFIERS = ["classifier__hurricane_irma.json","classifier__matt_lauer.json","classifier__tom_petty.json","classifier__super_bowl.json","classifier__las_vegas_shooting.json","classifier__mayweather_vs_mcgregor_fight.json","classifier__solar_eclipse.json","classifier__hurricane_harvey.json","classifier__aaron_hernandez.json","classifier__fidget_spinner.json"]
NN_CLASSIFIER = "nearest_neighbour_classifier.json"
NN_CLASSIFIER_LABELS = ["hurricane_irma","matt_lauer","tom_petty","super_bowl","las_vegas_shooting","mayweather_vs_mcgregor_fight","solar_eclipse","hurricane_harvey","aaron_hernandez","fidget_spinner"]

"""
Define what should be censored as a list of censorable objects.
	- First item in tuple is classifier result
	- Second item in tuple is minimum packet length of captured session
	- Third item in tuple is maximum packet length of captured session
"""
CENSORSHIP = [("classifier__hurricane_irma.json", 130, 150)]

if len(sys.argv) > 1:
	doBypass = bool(sys.argv[1] == "bypass")
else:
	doBypass = False


drop_traffic = False #Should traffic be dropped or not
captured_session = []
def process(i, payload):
	global drop_traffic
	data = payload.get_data()
	if doBypass:
		return
	if drop_traffic:
		print "!!! Your Internet has been censored !!!"
		#Keep VNC port open
		pkt = IP(data)
		if pkt.haslayer(TCP):
			if pkt[TCP].dport != 5900 and pkt[TCP].sport != 5900:
				payload.set_verdict(nfqueue.NF_DROP)
		return
	#print dir(payload)
	pkt = IP(data)
	if pkt.haslayer(TCP):
		tcp_layer = pkt.getlayer(TCP)
		if tcp_layer.dport != 5900 and tcp_layer.sport != 5900:
			captured_session.append(pkt)
	
			#Try to classify this session
			hybrid_result = getHybridClassifierType(captured_session, CLASSIFIERS, NN_CLASSIFIER_LABELS, NN_CLASSIFIER)		
			print "!!! Hybrid Result is {}. Length of session is {} !!!".format(hybrid_result, len(captured_session))
			
			#Flip the killswitch?
			for censor_item in CENSORSHIP:
				censor_label = censor_item[0]
				size_min = censor_item[1]
				size_max = censor_item[2]
				if hybrid_result == censor_label and len(captured_session) in range(size_min, size_max):
					drop_traffic = True



q = nfqueue.queue()
q.open()
q.bind(socket.AF_INET)
q.set_callback(process)
q.create_queue(0)

try:
	#while True:
		#q.try_run()
	q.try_run()
except KeyboardInterrupt:
	print "Exit..."
	q.unbind(socket.AF_INET)
	q.close()
