#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class ChunkFilter:
	def __init__(self, min_t):
		self.minimum_timegap = min_t
		self.packets_buffer = []
		self.prev_time = None
	
	"""
	Read in a packet (pkt) and store it in the buffer
	self.packets_buffer. If the time delta between this packet
	and the previous packet is greater than self.minimum_timegap,
	release the current chunk of packets held in self.packets_buffer
	before adding pkt to the now emptied self.packets_buffer
	"""
	def feed_packet(self, pkt, ignore=False):
		holds_chunk = False
		packet_time = pkt[2]
		if self.prev_time is None:
			self.prev_time = packet_time
		
		if abs(packet_time - self.prev_time) > self.minimum_timegap:
			#self.packets_buffer now holds a chunk of network activity
			holds_chunk = True
		
		if holds_chunk:
			this_network_chunk = self.packets_buffer[:] #Copy by value
			self.packets_buffer = [] #Delete the old packets from the buffer
			
		#Set the previous time
		if not ignore:
			self.prev_time = packet_time
		
		#Append pkt to the buffer
		if not ignore:
			self.packets_buffer.append(pkt)
		
		#Return a chunk of network packets if necessary
		if holds_chunk:
			return this_network_chunk
	


class SearchTermDetection:
	def __init__(self):
		self.trained_data = {}
		self.stored_sequence = []
	
	def train_model(self, network_trace, key_label):
		#Get total TX and RX traffic
		total_tx = 0
		total_rx = 0
		for pkt in network_trace:
			if pkt[0] == "TX":
				total_tx += pkt[1]
			elif pkt[0] == "RX":
				total_rx += pkt[1]
		
		if key_label not in self.trained_data.keys():
			self.trained_data[key_label] = []
		
		self.trained_data[key_label].append((total_tx, total_rx))
		
	def save_model(self, filename):
		f_json = open(filename, 'w')
		f_json.write(json.dumps(self.trained_data))
		f_json.close()
	
	def load_model(self, filename):
		f_json = open(filename, 'r')
		self.trained_data = json.loads(f_json.read())
		f_json.close()
	
	def model_predict(self, network_sequence):
		"""
		Determine most likely sequence of entered characters for a
		singular network_sequence
		"""
		total_rx = 0
		for pkt in network_sequence:
			if pkt[0] == "RX":
				total_rx += pkt[1]
		
		"""
		For which key in self.trained_data does total_rx most closely
		match with
		"""
		closest_key = None
		shortest_distance = None
		for search_key in self.trained_data:
			for candidate_value_tuple in self.trained_data[search_key]:
				rx_value = candidate_value_tuple[1]
				if closest_key is None:
					closest_key = search_key
					shortest_distance = abs(rx_value - total_rx)
					continue
				
				if abs(rx_value - total_rx) < shortest_distance:
					closest_key = search_key
					shortest_distance = abs(rx_value - total_rx)
		
		return (closest_key, shortest_distance)
		

	def yield_model_predict_rank(self, network_sequence, do_store=False):
		"""
		Determine most likely sequence of entered characters for a
		singular network_sequence
		"""
		total_rx = 0
		for pkt in network_sequence:
			if pkt[0] == "RX":
				total_rx += pkt[1]
		
		"""
		Yield the keys and distances in self.trained_data which most
		closely match with the given network_sequence
		"""
		check_keys = self.trained_data.keys()
		probability_table = {}
		while len(check_keys) > 0:
			closest_key = None
			shortest_distance = None
			#probability_table = {}
			for search_key in check_keys:
				for candidate_value_tuple in self.trained_data[search_key]:
					rx_value = candidate_value_tuple[1]
					if closest_key is None:
						closest_key = search_key
						shortest_distance = abs(rx_value - total_rx)
						continue
					
					if abs(rx_value - total_rx) < shortest_distance:
						closest_key = search_key
						shortest_distance = abs(rx_value - total_rx)
			
			yield_val = (closest_key, shortest_distance)
			del check_keys[check_keys.index(closest_key)]
			if do_store:
				probability_table[closest_key] = shortest_distance
				
			yield closest_key, shortest_distance
		
		if do_store:
			self.stored_sequence.append(probability_table)
	
	def clear_stored_sequence(self):
		self.stored_sequence = []
	
	def get_searchword_cost(self, searchword):
		#partial_word = ""
		searchword_costs = []
		stored_sequence_index = 0
		#for c in searchword:
		#	partial_word = partial_word + c
		#	#Lookup partial_word in all elements of self.stored_sequence[stored_sequence_index:stored_sequence_index + len(partial_word)]
		#	search_set = self.stored_sequence[stored_sequence_index:stored_sequence_index + len(partial_word)]
		#	if len(search_set) < len(searchword):
		#		break
		#	
		#	#Calculate costs of partial_word being in search_set
		#	searchword_costs = []
		#	for prob_map in search_set:
		#		searchword_costs.append(prob_map[partial_word])
		while True:
			"""
			Calculate the cost of searchword fitting into
			self.stored_sequence[stored_sequence_index:stored_sequence_index + len(searchword)]
			"""
			search_set = self.stored_sequence[stored_sequence_index:stored_sequence_index + len(searchword)]
			
			#print search_set
			
			if len(search_set) < len(searchword):
				break
			#if stored_sequence_index + len(searchword) >= len(search_set):
			#	break
			
			partial_word = ""
			running_cost = 0
			for search_index in range(0,len(search_set)):
				partial_word = partial_word + searchword[search_index]
				#print search_set[search_index]
				print "C({}) = {}".format(partial_word, search_set[search_index][partial_word])
				running_cost += search_set[search_index][partial_word]
			
			searchword_costs.append(running_cost)
			
			stored_sequence_index += 1
		
		if len(searchword_costs) == 0:
			return None
		
		return min(searchword_costs)
	
	def simple_get_cost(self, word):
		if len(word) < len(self.stored_sequence):
			return None
		
		partial_word = ""
		costs = []
		for i in range(0,len(self.stored_sequence)):
			partial_word = partial_word + word[i]
			#Lookup cost of partial_word in self.stored_sequence[i]
			costs.append(self.stored_sequence[i][partial_word])
			print self.stored_sequence[i]
		
		return costs
			


	
			
