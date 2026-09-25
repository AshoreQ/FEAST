#!/bin/bash
path='../'
export path
cat 'autoword.txt' | while read line
do
	name=$line
	echo $line
	#sed $line/[[:space:]]//g
	echo ${line//_/ }   
	#echo $line	
done
