#!/bin/bash

CONTAINER_NAME=$1

#Open a new private window in Firefox
open_private(){
	docker exec $CONTAINER_NAME xte 'key Alt_L'
	sleep 1
	docker exec $CONTAINER_NAME xte 'key f'
	sleep 1
	docker exec $CONTAINER_NAME xte 'key w'
	sleep 1
}

#Close the private window
close_private(){
	docker exec $CONTAINER_NAME xte 'key Alt_L'
	sleep 1
	docker exec $CONTAINER_NAME xte 'key f'
	sleep 1
	docker exec $CONTAINER_NAME xte 'key d'
	sleep 15
}

mkdir samples

#Populate the shopping cart with n from 1 to 8 items
for n in `seq 1 8`
do
	echo "Testing for $n items in shopping cart"
	
	##Open a new private window
	#open_private
	
	sleep 5
	
	#Populate the shopping cart
	./remote_automate_ebay_clicking.sh $CONTAINER_NAME $n
	
	#Get a network traffic sample for each popup ranging from 280px to 2840px in steps of 40px therefore 65 samples
	docker exec $CONTAINER_NAME /ebay_shoppingcart/local_automate_popup_exploit.sh 280 2840 40
	
	#Download the samples from the Docker container
	mkdir samples/$n
	cd samples/$n
	for h in `seq 280 40 2840`
	do
		docker cp "$CONTAINER_NAME:/exploit_height_$h.pcap" .
	done
	cd ..
	cd ..
	
	#Close the private window
	close_private
	
done
