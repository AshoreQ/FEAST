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
