#!/bin/bash

RUN_TIMES=$1
export DISPLAY=:0

#Open a new private window in Firefox
open_private(){
	xte 'key Alt_L'
	sleep 1
	xte 'key f'
	sleep 1
	xte 'key w'
	sleep 1
}

#Close the private window
close_private(){
	xte 'key Alt_L'
	sleep 1
	xte 'key f'
	sleep 1
	xte 'key d'
	sleep 20
}

#Load the main search page of www.google.ca
load_google(){
	xte 'str https://www.google.ca'
	sleep 2
	xte 'key Return'
	sleep 20
}

#Feed Google autocomplete with a search term
feed_google(){
	search_string=$1
	echo $search_string | fold -w1 | while read char; do xte "key $char"; sleep 1; done
}

for i in `seq 1 $RUN_TIMES`
do
	echo "Running Test $i"
	
	#--- BEGIN UNIT (Hurricane Irma) ---
	
	#Open a new private window in Firefox
	open_private
	
	sleep 10
	
	#Load Google
	load_google
	
	#Begin capturing network traffic
	./capture_command.sh &
	capture_pid=$!
	sleep 10
	
	#Do search #1
	feed_google 'Hurricane Irma'
	
	sleep 20
	
	#Stop capturing network traffic
	pkill -P $capture_pid
	sleep 5
	
	#Save the captured_packets
	mv captured_packets.pcap search_hurricane_irma_trial_$i.pcap
	
	#Close the private window
	close_private
	
	#--- END UNIT (Hurricane Irma) ---
	
	
	#--- BEGIN UNIT (Matt Lauer) ---
	
	#Open a new private window in Firefox
	open_private
	
	sleep 10
	
	#Load Google
	load_google
	
	#Begin capturing network traffic
	./capture_command.sh &
	capture_pid=$!
	sleep 10
	
	#Do search #1
	feed_google 'Matt Lauer'
	
	sleep 20
	
	#Stop capturing network traffic
	pkill -P $capture_pid
	sleep 5
	
	#Save the captured_packets
	mv captured_packets.pcap search_matt_lauer_trial_$i.pcap
	
	#Close the private window
	close_private
	
	#--- END UNIT (Matt Lauer) ---
	
	
	#--- BEGIN UNIT (Tom Petty) ---
	
	#Open a new private window in Firefox
	open_private
	
	sleep 10
	
	#Load Google
	load_google
	
	#Begin capturing network traffic
	./capture_command.sh &
	capture_pid=$!
	sleep 10
	
	#Do search #1
	feed_google 'Tom Petty'
	
	sleep 20
	
	#Stop capturing network traffic
	pkill -P $capture_pid
	sleep 5
	
	#Save the captured_packets
	mv captured_packets.pcap search_tom_petty_trial_$i.pcap
	
	#Close the private window
	close_private
	
	#--- END UNIT (Tom Petty) ---
	
	
	#--- BEGIN UNIT (Super Bowl) ---
	
	#Open a new private window in Firefox
	open_private
	
	sleep 10
	
	#Load Google
	load_google
	
	#Begin capturing network traffic
	./capture_command.sh &
	capture_pid=$!
	sleep 10
	
	#Do search #1
	feed_google 'Super Bowl'
	
	sleep 20
	
	#Stop capturing network traffic
	pkill -P $capture_pid
	sleep 5
	
	#Save the captured_packets
	mv captured_packets.pcap search_super_bowl_trial_$i.pcap
	
	#Close the private window
	close_private
	
	#--- END UNIT (Super Bowl) ---
	
	#--- BEGIN UNIT (Las Vegas shooting) ---
	
	#Open a new private window in Firefox
	open_private
	
	sleep 10
	
	#Load Google
	load_google
	
	#Begin capturing network traffic
	./capture_command.sh &
	capture_pid=$!
	sleep 10
	
	#Do search #1
	feed_google 'Las Vegas shooting'
	
	sleep 20
	
	#Stop capturing network traffic
	pkill -P $capture_pid
	sleep 5
	
	#Save the captured_packets
	mv captured_packets.pcap search_las_vegas_shooting_trial_$i.pcap
	
	#Close the private window
	close_private
	
	#--- END UNIT (Las Vegas shooting) ---
	
	#--- BEGIN UNIT (Mayweather vs McGregor Fight) ---
	
	#Open a new private window in Firefox
	open_private
	
	sleep 10
	
	#Load Google
	load_google
	
	#Begin capturing network traffic
	./capture_command.sh &
	capture_pid=$!
	sleep 10
	
	#Do search #1
	feed_google 'Mayweather vs McGregor Fight'
	
	sleep 20
	
	#Stop capturing network traffic
	pkill -P $capture_pid
	sleep 5
	
	#Save the captured_packets
	mv captured_packets.pcap search_mayweather_vs_mcgregor_fight_trial_$i.pcap
	
	#Close the private window
	close_private
	
	#--- END UNIT (Mayweather vs McGregor Fight) ---
	
	
	#--- BEGIN UNIT (Solar eclipse) ---
	
	#Open a new private window in Firefox
	open_private
	
	sleep 10
	
	#Load Google
	load_google
	
	#Begin capturing network traffic
	./capture_command.sh &
	capture_pid=$!
	sleep 10
	
	#Do search #1
	feed_google 'Solar eclipse'
	
	sleep 20
	
	#Stop capturing network traffic
	pkill -P $capture_pid
	sleep 5
	
	#Save the captured_packets
	mv captured_packets.pcap search_solar_eclipse_trial_$i.pcap
	
	#Close the private window
	close_private
	
	#--- END UNIT (Solar eclipse) ---
	
	#--- BEGIN UNIT (Hurricane Harvey) ---
	
	#Open a new private window in Firefox
	open_private
	
	sleep 10
	
	#Load Google
	load_google
	
	#Begin capturing network traffic
	./capture_command.sh &
	capture_pid=$!
	sleep 10
	
	#Do search #1
	feed_google 'Hurricane Harvey'
	
	sleep 20
	
	#Stop capturing network traffic
	pkill -P $capture_pid
	sleep 5
	
	#Save the captured_packets
	mv captured_packets.pcap search_hurricane_harvey_trial_$i.pcap
	
	#Close the private window
	close_private
	
	#--- END UNIT (Hurricane Harvey) ---
	
	#--- BEGIN UNIT (Aaron Hernandez) ---
	
	#Open a new private window in Firefox
	open_private
	
	sleep 10
	
	#Load Google
	load_google
	
	#Begin capturing network traffic
	./capture_command.sh &
	capture_pid=$!
	sleep 10
	
	#Do search #1
	feed_google 'Aaron Hernandez'
	
	sleep 20
	
	#Stop capturing network traffic
	pkill -P $capture_pid
	sleep 5
	
	#Save the captured_packets
	mv captured_packets.pcap search_aaron_hernandez_trial_$i.pcap
	
	#Close the private window
	close_private
	
	#--- END UNIT (Aaron Hernandez) ---
	
	#--- BEGIN UNIT (Fidget spinner) ---
	
	#Open a new private window in Firefox
	open_private
	
	sleep 10
	
	#Load Google
	load_google
	
	#Begin capturing network traffic
	./capture_command.sh &
	capture_pid=$!
	sleep 10
	
	#Do search #1
	feed_google 'Fidget spinner'
	
	sleep 20
	
	#Stop capturing network traffic
	pkill -P $capture_pid
	sleep 5
	
	#Save the captured_packets
	mv captured_packets.pcap search_fidget_spinner_trial_$i.pcap
	
	#Close the private window
	close_private
	
	#--- END UNIT (Fidget spinner) ---
	
done
