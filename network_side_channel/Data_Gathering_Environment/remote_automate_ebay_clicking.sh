#!/bin/bash

CONTAINER_NAME=$1
ITEM_COUNT=$2

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

#Load the main page of www.ebay.ca
load_ebay(){
	docker exec $CONTAINER_NAME xte 'str https://www.ebay.ca'
	sleep 2
	docker exec $CONTAINER_NAME xte 'key Return'
	sleep 20
}

#Load the given link specified by the first argument
load_link(){
	PAGEURL=$1
	docker exec $CONTAINER_NAME xte 'keydown Control_L'
	docker exec $CONTAINER_NAME xte 'key l'
	docker exec $CONTAINER_NAME xte 'keyup Control_L'
	sleep 2
	docker exec $CONTAINER_NAME xte "str $PAGEURL"
	sleep 2
	docker exec $CONTAINER_NAME xte 'key Return'
	sleep 20
}

#Click add to cart
click_add_to_cart(){
	sleep 1
	docker exec $CONTAINER_NAME xte 'mousemove 50 100'
	sleep 1
	docker exec $CONTAINER_NAME xte 'mouseclick 1'
	sleep 1
}

	
#Open a private window
open_private

sleep 10

#Load the website
load_ebay

#Wait momentarily
sleep 30

if (( ITEM_COUNT > 0 ))
then
	#--- BEGIN UNIT 1 ---
	echo "Loading Ebay link 1"
	#Load the first link
	load_link https://www.ebay.ca/itm/282841843301
	
	#Wait momentarily
	sleep 30
	
	#Add to cart
	click_add_to_cart
	
	#Wait momentarily
	sleep 30
	#--- END UNIT 1 ---
fi

if (( ITEM_COUNT > 1 ))
then
	#--- BEGIN UNIT 2 ---
	#Load the second link
	load_link https://www.ebay.ca/itm/322438188918

	#Wait momentarily
	sleep 30

	#Add to cart
	click_add_to_cart

	#Wait momentarily
	sleep 30
	#--- END UNIT 2 ---
fi


if (( ITEM_COUNT > 2 ))
then
	#--- BEGIN UNIT 3 ---
	#Load the third link
	load_link https://www.ebay.ca/itm/272607373784

	#Wait momentarily
	sleep 30

	#Add to cart
	click_add_to_cart

	#Wait momentarily
	sleep 30
	#--- END UNIT 3 ---
fi


if (( ITEM_COUNT > 3 ))
then
	#--- BEGIN UNIT 4 ---
	#Load the fourth link
	load_link https://www.ebay.ca/itm/172955806624

	#Wait momentarily
	sleep 30

	#Add to cart
	click_add_to_cart

	#Wait momentarily
	sleep 30
	#--- END UNIT 4 ---
fi

if (( ITEM_COUNT > 4 ))
then
	#--- BEGIN UNIT 5 ---
	#Load the fifth link
	load_link https://www.ebay.ca/itm/282234837631

	#Wait momentarily
	sleep 30

	#Add to cart
	click_add_to_cart

	#Wait momentarily
	sleep 30
	#--- END UNIT 5 ---	
fi


if (( ITEM_COUNT > 5 ))
then
	#--- BEGIN UNIT 6 ---
	#Load the sixth link
	load_link https://www.ebay.ca/itm/152899845340

	#Wait momentarily
	sleep 30

	#Add to cart
	click_add_to_cart

	#Wait momentarily
	sleep 30
	#--- END UNIT 6 ---
fi

if (( ITEM_COUNT > 6 ))
then
	#--- BEGIN UNIT 7 ---
	#Load the seventh link
	load_link https://www.ebay.ca/itm/302119553538

	#Wait momentarily
	sleep 30

	#Add to cart
	click_add_to_cart

	#Wait momentarily
	sleep 30
	#--- END UNIT 7 ---
fi


if (( ITEM_COUNT > 7 ))
then
	#--- BEGIN UNIT 8 ---
	#Load the eighth link
	load_link https://www.ebay.ca/itm/292273610350

	#Wait momentarily
	sleep 30

	#Add to cart
	click_add_to_cart

	#Wait momentarily
	sleep 30
	#--- END UNIT 8 ---
fi

