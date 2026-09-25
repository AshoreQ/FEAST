#!/bin/bash

JINGDONG='手机 电脑'

feed_google(){
	echo "feed"
	search_string=$1
	echo $search_string
	echo $search_string | fold -w3 | while read char; do echo $char; sleep 1; done
}

for word in $JINGDONG
do
	#echo "${word//_/ }"
	feed_google "${word//_/ }"
done
