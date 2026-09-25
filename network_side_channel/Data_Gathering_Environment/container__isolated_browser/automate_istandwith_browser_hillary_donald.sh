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
	sleep 15
}


#Load the isidewith website
load_website(){
	sleep 1
	xte 'mousemove 50 100'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}

#Populate with Trump1 answers
trump1(){
	sleep 1
	xte 'mousemove 100 100'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}

#Populate with Trump2 answers
trump2(){
	sleep 1
	xte 'mousemove 200 100'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}

#Populate with Trump3 answers
trump3(){
	sleep 1
	xte 'mousemove 250 100'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}

#Populate with Trump4 answers
trump4(){
	sleep 1
	xte 'mousemove 350 100'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}

#Populate with Sanders1 answers
sanders1(){
	sleep 1
	xte 'mousemove 450 100'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}

#Populate with Sanders2 answers
sanders2(){
	sleep 1
	xte 'mousemove 520 100'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}

#Populate with Sanders3 answers
sanders3(){
	sleep 1
	xte 'mousemove 600 100'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}

#Populate with Sanders4 answers
sanders4(){
	sleep 1
	xte 'mousemove 700 100'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}

#Populate with Clinton1 answers
clinton1(){
	sleep 1
	xte 'mousemove 800 100'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}

#Populate with Clinton2 answers
clinton2(){
	sleep 1
	xte 'mousemove 900 100'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}

#Populate with Clinton3 answers
clinton3(){
	sleep 1
	xte 'mousemove 960 100'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}

#Populate with Clinton4 answers
clinton4(){
	sleep 1
	xte 'mousemove 1050 100'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}

#Submit responses
submit_answers(){
	sleep 1
	xte 'mousemove 1200 100'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}


for i in `seq 1 $RUN_TIMES`
do
	echo "Running Test $i"
	
	#--- BEGIN UNIT ---
	
	#Open a new private window in Firefox
	open_private
	
	#Load the isidewith website
	load_website
	
	#Wait for it to load
	sleep 40
	
	#Populate with Trump1 answers
	trump1
	
	#Wait
	sleep 45
	
	#Start recording network traffic
	./capture_command.sh &
	capture_pid=$!
	sleep 10
	
	#Submit the responses
	submit_answers
	
	#Wait three minutes for results to be obtained
	sleep 180
	
	#Stop recording network traffic
	pkill -P $capture_pid
	sleep 5
	
	#Save the captured_packets
	mv captured_packets.pcap trump1_trial_$i.pcap
	
	#Close the private window
	close_private
	
	#--- END UNIT ---
	
	#--- BEGIN UNIT ---
	
	#Open a new private window in Firefox
	open_private
	
	#Load the isidewith website
	load_website
	
	#Wait for it to load
	sleep 40
	
	#Populate with Trump2 answers
	trump2
	
	#Wait
	sleep 45
	
	#Start recording network traffic
	./capture_command.sh &
	capture_pid=$!
	sleep 10
	
	#Submit the responses
	submit_answers
	
	#Wait three minutes for results to be obtained
	sleep 180
	
	#Stop recording network traffic
	pkill -P $capture_pid
	sleep 5
	
	#Save the captured_packets
	mv captured_packets.pcap trump2_trial_$i.pcap
	
	#Close the private window
	close_private
	
	#--- END UNIT ---
	
	#--- BEGIN UNIT ---
	
	#Open a new private window in Firefox
	open_private
	
	#Load the isidewith website
	load_website
	
	#Wait for it to load
	sleep 40
	
	#Populate with Trump3 answers
	trump3
	
	#Wait
	sleep 45
	
	#Start recording network traffic
	./capture_command.sh &
	capture_pid=$!
	sleep 10
	
	#Submit the responses
	submit_answers
	
	#Wait three minutes for results to be obtained
	sleep 180
	
	#Stop recording network traffic
	pkill -P $capture_pid
	sleep 5
	
	#Save the captured_packets
	mv captured_packets.pcap trump3_trial_$i.pcap
	
	#Close the private window
	close_private
	
	#--- END UNIT ---
	
	#--- BEGIN UNIT ---
	
	#Open a new private window in Firefox
	open_private
	
	#Load the isidewith website
	load_website
	
	#Wait for it to load
	sleep 40
	
	#Populate with Trump4 answers
	trump4
	
	#Wait
	sleep 45
	
	#Start recording network traffic
	./capture_command.sh &
	capture_pid=$!
	sleep 10
	
	#Submit the responses
	submit_answers
	
	#Wait three minutes for results to be obtained
	sleep 180
	
	#Stop recording network traffic
	pkill -P $capture_pid
	sleep 5
	
	#Save the captured_packets
	mv captured_packets.pcap trump4_trial_$i.pcap
	
	#Close the private window
	close_private
	
	#--- END UNIT ---
	
	#--- BEGIN UNIT ---
	
	#Open a new private window in Firefox
	open_private
	
	#Load the isidewith website
	load_website
	
	#Wait for it to load
	sleep 40
	
	#Populate with Clinton1 answers
	clinton1
	
	#Wait
	sleep 45
	
	#Start recording network traffic
	./capture_command.sh &
	capture_pid=$!
	sleep 10
	
	#Submit the responses
	submit_answers
	
	#Wait three minutes for results to be obtained
	sleep 180
	
	#Stop recording network traffic
	pkill -P $capture_pid
	sleep 5
	
	#Save the captured_packets
	mv captured_packets.pcap clinton1_trial_$i.pcap
	
	#Close the private window
	close_private
	
	#--- END UNIT ---

	#--- BEGIN UNIT ---
	
	#Open a new private window in Firefox
	open_private
	
	#Load the isidewith website
	load_website
	
	#Wait for it to load
	sleep 40
	
	#Populate with Clinton2 answers
	clinton2
	
	#Wait
	sleep 45
	
	#Start recording network traffic
	./capture_command.sh &
	capture_pid=$!
	sleep 10
	
	#Submit the responses
	submit_answers
	
	#Wait three minutes for results to be obtained
	sleep 180
	
	#Stop recording network traffic
	pkill -P $capture_pid
	sleep 5
	
	#Save the captured_packets
	mv captured_packets.pcap clinton2_trial_$i.pcap
	
	#Close the private window
	close_private
	
	#--- END UNIT ---
	
	#--- BEGIN UNIT ---
	
	#Open a new private window in Firefox
	open_private
	
	#Load the isidewith website
	load_website
	
	#Wait for it to load
	sleep 40
	
	#Populate with Clinton3 answers
	clinton3
	
	#Wait
	sleep 45
	
	#Start recording network traffic
	./capture_command.sh &
	capture_pid=$!
	sleep 10
	
	#Submit the responses
	submit_answers
	
	#Wait three minutes for results to be obtained
	sleep 180
	
	#Stop recording network traffic
	pkill -P $capture_pid
	sleep 5
	
	#Save the captured_packets
	mv captured_packets.pcap clinton3_trial_$i.pcap
	
	#Close the private window
	close_private
	
	#--- END UNIT ---
	
	#--- BEGIN UNIT ---
	
	#Open a new private window in Firefox
	open_private
	
	#Load the isidewith website
	load_website
	
	#Wait for it to load
	sleep 40
	
	#Populate with Clinton4 answers
	clinton4
	
	#Wait
	sleep 45
	
	#Start recording network traffic
	./capture_command.sh &
	capture_pid=$!
	sleep 10
	
	#Submit the responses
	submit_answers
	
	#Wait three minutes for results to be obtained
	sleep 180
	
	#Stop recording network traffic
	pkill -P $capture_pid
	sleep 5
	
	#Save the captured_packets
	mv captured_packets.pcap clinton4_trial_$i.pcap
	
	#Close the private window
	close_private
	
	#--- END UNIT ---

done
