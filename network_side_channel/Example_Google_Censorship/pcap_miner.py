#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scapy.all import *

def get_total_packet_count(packet_capture):
	#packet_capture = rdpcap(pcap_file)
	return len(packet_capture)

def getSessionSymbolString(packet_capture, local_ip, remote_ip):
	session_ports = []
	#packet_capture = rdpcap(pcap_file)
	print "[DEBUG] There are {} packets in this session".format(len(packet_capture))
	for pkt in packet_capture:
		if not pkt.haslayer(IP):
			continue
		ip_pkt = pkt.getlayer(IP)
		#Only focus on TCP streams
		if ip_pkt.haslayer(TCP):
			tcp_pkt = ip_pkt.getlayer(TCP)
			#Just the server response for now...
			if ((ip_pkt.src == remote_ip or remote_ip is None) and ip_pkt.dst == local_ip):
				#...then this is a packet of interest...
				#...get the destination port and payload size
				tcp_destination = tcp_pkt.dport
				tcp_payload_size = len(tcp_pkt.payload)
				#...we are not concerned with the exact dport number, just keep streams separate
				if tcp_destination in session_ports:
					session_number = session_ports.index(tcp_destination)
				else:
					session_number = len(session_ports)
					session_ports.append(tcp_destination)
				
				#Yield a "symbol" containing (stream identifier, payload size)
				yield (session_number, tcp_payload_size, pkt.time)
			
