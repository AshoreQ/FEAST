#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from scapy.all import *

SAMPLES_DIR = "RESULTS"

#Dynamically populate addresses of CDN servers based on DNS replies
CDN_SERVERS = []

def getAkami_IP(PCAP_FILE):
	packet_capture = rdpcap(PCAP_FILE)
	for pkt in packet_capture:
		if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 1:
			#print pkt.summary()
			#print repr(pkt[DNS])
			domain_name = pkt[DNS].qd.qname
			domain_ips = pkt[DNS].an
			domain_ip = None
			for i in range(0, pkt[DNS].ancount):
				#print "DNS Answer of type {}".format(pkt[DNSRR][i].type)
				if pkt[DNSRR][i].type == 1:
					#print "Contains IP {}".format(pkt[DNSRR][i].rdata)
					domain_ip = pkt[DNSRR][i].rdata
					
			#	if 'rdata' in ans:
			#		domain_ip = ans.rdata
			print "{}  --> {}".format(domain_name, domain_ip)
			#print len(domain_ips)
			if domain_name == "i.ebayimg.com." and domain_ip is not None:
				CDN_SERVERS.append(str(domain_ip))


def containsAkamai(PCAP_FILE):
	packet_capture = rdpcap(PCAP_FILE)

	contains_akamai = False
	for pkt in packet_capture:
		if pkt.haslayer(IP):
			iplayer = pkt.getlayer(IP)
			if iplayer.src in CDN_SERVERS or iplayer.dst in CDN_SERVERS:
				#Has traffic from akamai
				contains_akamai = True

	return contains_akamai

def byteCountAkamai(PCAP_FILE):
	packet_capture = rdpcap(PCAP_FILE)

	running_byte_count = 0
	for pkt in packet_capture:
		if pkt.haslayer(IP):
			iplayer = pkt.getlayer(IP)
			if iplayer.src in CDN_SERVERS or iplayer.dst in CDN_SERVERS:
				#Has traffic from akamai
				if iplayer.haslayer(TCP):
					running_byte_count += len(iplayer[TCP].payload)

	return running_byte_count

def packetCountAkamai(PCAP_FILE):
	packet_capture = rdpcap(PCAP_FILE)

	running_packet_count = 0
	for pkt in packet_capture:
		if pkt.haslayer(IP):
			iplayer = pkt.getlayer(IP)
			if iplayer.src in CDN_SERVERS or iplayer.dst in CDN_SERVERS:
				#Has traffic from akamai
				if iplayer.haslayer(TCP):
					running_packet_count += 1

	return running_packet_count


first_instance_of_akamai = {}
bytes_exchanged_with_akamai = {}
packets_exchanged_with_akamai = {}

for cart_items in range(1,9):
	first_instance_of_akamai[str(cart_items)] = None
	bytes_exchanged_with_akamai[str(cart_items)] = {}
	packets_exchanged_with_akamai[str(cart_items)] = {}
	
	#print ""
	#print os.listdir("{}/{}".format(SAMPLES_DIR, cart_items))
	#print ""
	for pcap_name in os.listdir("{}/{}".format(SAMPLES_DIR, cart_items)):
		pcap_filepath = "{}/{}/{}".format(SAMPLES_DIR, cart_items, pcap_name)
		
		#Clear cache of CDN servers
		CDN_SERVERS = []
		
		#Get Akami IP - dynamically populate
		getAkami_IP(pcap_filepath)
		
		if containsAkamai(pcap_filepath):
			print "Contact to Akamai Server in file: {}".format(pcap_filepath)
			
			height_extractor = re.compile("exploit_height_(\d+)\.pcap")
			height_match = height_extractor.match(pcap_name)
			exploit_height = int(height_match.group(1))
			
			if first_instance_of_akamai[str(cart_items)] is None:
				first_instance_of_akamai[str(cart_items)] = exploit_height
			
			if exploit_height < first_instance_of_akamai[str(cart_items)]:
				first_instance_of_akamai[str(cart_items)] = exploit_height
			
			#Get the number of bytes received from akamai
			bytes_exchanged_with_akamai[str(cart_items)][str(exploit_height)] = byteCountAkamai(pcap_filepath)
			
			#Get the number of packets received from akamai
			packets_exchanged_with_akamai[str(cart_items)][str(exploit_height)] = packetCountAkamai(pcap_filepath)


print ""
print ""

for cart_items in range(1,9):
	print "First instance for {} items is at window height {}".format(cart_items, first_instance_of_akamai[str(cart_items)])


print ""
print ""

for cart_items in range(1,9):
	hits_count = 0
	print "<{} items>".format(cart_items)
	for exploit_h in range(280, 2841, 40):
		try:
			print "\t Exploit Height: {} --> {} bytes, {} packets".format(exploit_h, bytes_exchanged_with_akamai[str(cart_items)][str(exploit_h)], packets_exchanged_with_akamai[str(cart_items)][str(exploit_h)])
			hits_count += 1
		except KeyError:
			pass
	print "</{} items>".format(cart_items)
	print "Total hits: {}/65".format(hits_count)
	print ""

