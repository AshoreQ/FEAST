#!/usr/bin/python

import json
from pcap_miner import get_total_packet_count

class NearestNeighbourClassifier:
	def __init__(self):
		self.trained_data = []
	
	def learn(self, data, label):
		self.trained_data.append((label, data))
	
	def save_learned_data(self, jsonfile):
		f_json = open(jsonfile, 'w')
		f_json.write(json.dumps(self.trained_data))
		f_json.close()
	
	def load_learned_data(self, jsonfile):
		f_json = open(jsonfile, 'r')
		self.trained_data = json.loads(f_json.read())
		f_json.close()
	
	def nearest_neighbour(self, point):
		neighbourhood = self.trained_data
		min_dist = None
		closest_match = None
		for sample in self.trained_data:
			label = sample[0]
			data = sample[1]
			if closest_match is None:
				closest_match = label
			if min_dist is None:
				min_dist = abs(data - point)
			if abs(data - point) < min_dist:
				min_dist = abs(data - point)
				closest_match = label
			
		return closest_match, min_dist
	
	def distance_to_nearest(self, test_point, test_label):
		min_dist = None
		for sample in self.trained_data:
			label = sample[0]
			data = sample[1]
			
			if test_label == label:
				if min_dist is None:
					min_dist = abs(test_point - data)
				
				if abs(test_point - data) < min_dist:
					min_dist = abs(test_point - data)
			
		return min_dist


def getNearestNeighbourStats(PCAP_FILE, classifier_file):
	my_classifier = NearestNeighbourClassifier()
	my_classifier.load_learned_data(classifier_file)
	
	#Get the number of packets in PCAP_FILE
	pkt_count = get_total_packet_count(PCAP_FILE)
	
	#Classify based on pkt_count
	return my_classifier.nearest_neighbour(pkt_count)

def getNearestDist(PCAP_FILE, test_label, classifier_file):
	my_classifier = NearestNeighbourClassifier()
	my_classifier.load_learned_data(classifier_file)
	
	#Get the number of packets in PCAP_FILE
	pkt_count = get_total_packet_count(PCAP_FILE)
	
	#Classify based on pkt_count
	return my_classifier.distance_to_nearest(pkt_count, test_label)
