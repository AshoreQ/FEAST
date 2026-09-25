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
	sleep 10
}

#Load the main search page of www.google.ca
load_google(){
	xte 'str https://www.google.com.hk' # 输入网址
	sleep 2
	xte 'key Return' # 按下回车
	sleep 10
}

load_baidu(){
	xte 'str https://www.baidu.com/'
	sleep 2
	xte 'key Return'
	sleep 10
}

load_bing(){
	xte 'str https://cn.bing.com/'
	#xte 'str https://cn.bing.com/?ensearch=1&FORM=BEHPTB'
	sleep 2
	xte 'key Return'
	sleep 10
}

load_jingdong(){
	xte 'str https://www.jd.com/'
	sleep 1
	xte 'key Return'
	sleep 10
	xte 'mousemove 540 72'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}


load_taobao(){
	xte 'str https://www.taobao.com/'
	sleep 1
	xte 'key Return'
	sleep 10
	xte 'mousemove 500 90'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}


load_amazon(){
	xte 'str https://www.amazon.cn/'
	sleep 1
	xte 'key Return'
	sleep 10
	xte 'mousemove 400 30'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}

load_hopkinsmedicine(){
	xte 'str https://www.hopkinsmedicine.org/'
	sleep 1
	xte 'key Return'
	sleep 15
	xte 'mousemove 1100 100'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
	xte 'mousemove 200 235'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}

load_ebay(){
	xte 'str https://www.ebay.com/'
	sleep 1
	xte 'key Return'
	sleep 30
	xte 'mousemove 450 65'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}


# 一个一个字符的输入到搜索框中
feed_word(){
  echo "feed"
	search_string=$1
	echo $search_string | fold -w1 | while read char; do xte "key $char"; sleep 1; done
	# 中文字符用下面这个
	# echo $search_string | fold -w3 | while read char; do xte "key $char"; sleep 1; done
}
: '
feed_google(){
	search_string=$1
	num1=$[RANDOM%15+5] # 5~20
	num2=10
	num=`echo "scale=2; $num1/$num2" | bc`
	echo $num
	echo $search_string | fold -w1 | while read char; do xte "key $char"; sleep $num; done
}
'

LABELS2011='Rebecca_Black Google+ Ryan_Dunn Casey_Anthony Battlefield_3 iPhone_5 Adele TEPCO Steve_Jobs iPad_2'
LABELS2012='Whitney_Houston Gangnam_Style Hurricane_Sandy iPad_3 Diablo_3 Kate_Middleton Olympics_2012 Amanda_Todd Michael_Clarke_Duncan SOPA'
LABELS2013='PlayStation_4 North_Korea Samsung_Galaxy_4 Royal_Baby Boston_Marathon Harlem_Shake Cory_Monteith iPhone_5S Paul_Walker Nelson_Mandela'
LABELS2014='Robin_Williams World_Cup Ebola Malaysia_Airlines ALS_Ice_Bucket_Challenge Flappy_Bird Conchita_Wurst ISIS Frozen Sochi_Olympics'
LABELS2015='Lamar_Odom Jurassic_World American_Sniper Caitlyn_Jenner Ronda_Rousey Paris Agario Chris_Kyle Fallout_4 Straight_Outta_Compton'
LABELS2016='Powerball Prince Hurricane_Matthew Pokemon_Go Slither.io Olympics David_Bowie Trump Election Hillary_Clinton'
LABELS2017='hurricane_irma matt_lauer tom_petty super_bowl las_vegas_shooting mayweather_vs_mcgregor_fight solar_eclipse hurricane_harvey aaron_hernandez fidget_spinner'
LABELS2018='World_Cup Avicii Mac_Miller Stan_Lee Black_Panther Meghan_Markle Anthony_Bourdain XXXTentacion Stephen_Hawking Kate_Spade'
LABELS2019='Disney_Plus Cameron_Boyce Nipsey_Hussle Hurricane_Dorian Antonio_Brown Luke_Perry Avengers_Endgame Game_of_Thrones iPhone_11 Jussie_Smollett'
LABELS2020='Election_results Kobe_Bean_Bryant Zoom IPL India_vs_New_Zealand Coronavirus_update Coronavirus_symptoms Joe_Biden Google_Classroom Coronavirus'
LABELS2021='Australia_vs_India India_vs_England IPL NBA Euro_2021 Copa_America India_vs_New_Zealand T20_World_Cup Squid_Game DMX'
LABELS2022='Wordle India_vs_England Ukraine Queen_Elizabeth Ind_vs_SA World_Cup India_vs_West_Indies iPhone14 Jeffrey_Dahmer Indian_Premier_League'
# 中文使用fold命令时注意-w后的位宽是按编码来的，中文是3位
#JINGDONG='手机 笔记本 休闲裤 衬衫 洗衣凝珠'
#medicine='influenza diarrhea covid19 breast_cancer erectile_dysfunction hemorrhoids canker_sore anemia hypertension rhinitis'
#medicine='cefuroxime aspirin coronavirus careers medical_records map insurance_accepted telemedicine ibuprofen depression'
medicine='cough headache heart_disease hepatitis leukemia meningitis rabies stroke AIDS cystitis'
#shopping='shouji bijiben kuzi chenshan weishengzhi lianyiqun xiyiningzhu nanxie nvxie dianshi'
#shopping='switch laptop airpods headphones earbuds ipad ssd fitbit game_of_thrones fire_stick'
#shopping='kindle tv air_fryer bluetooth roku toilet_paper external_hard_drive instant_pot tablet micro_sd_card'
shopping='gaming_chair apple_watch monitor ps4 alexa paper_towels desk office_chair ring_doorbell luggage'
LABELS='PlayStation_4 North_Korea Samsung_Galaxy_4 Royal_Baby Boston_Marathon Harlem_Shake Cory_Monteith iPhone_5S Paul_Walker Nelson_Mandela Robin_Williams World_Cup Ebola Malaysia_Airlines ALS_Ice_Bucket_Challenge Flappy_Bird Conchita_Wurst ISIS Frozen Sochi_Olympics Lamar_Odom Jurassic_World American_Sniper Caitlyn_Jenner Ronda_Rousey Paris Agario Chris_Kyle Fallout_4 Straight_Outta_Compton Powerball Prince Hurricane_Matthew Pokemon_Go Slither.io Olympics David_Bowie Trump Election Hillary_Clinton hurricane_irma matt_lauer tom_petty super_bowl las_vegas_shooting mayweather_vs_mcgregor_fight solar_eclipse hurricane_harvey aaron_hernandez fidget_spinner World_Cup Avicii Mac_Miller Stan_Lee Black_Panther Meghan_Markle Anthony_Bourdain XXXTentacion Stephen_Hawking Kate_Spade Disney_Plus Cameron_Boyce Nipsey_Hussle Hurricane_Dorian Antonio_Brown Luke_Perry Avengers_Endgame Game_of_Thrones iPhone_11 Jussie_Smollett Election_results Kobe_Bean_Bryant Zoom IPL India_vs_New_Zealand Coronavirus_update Coronavirus_symptoms Joe_Biden Google_Classroom Coronavirus Australia_vs_India India_vs_England IPL NBA Euro_2021 Copa_America India_vs_New_Zealand T20_World_Cup Squid_Game DMX Wordle India_vs_England Ukraine Queen_Elizabeth Ind_vs_SA World_Cup India_vs_West_Indies iPhone14 Jeffrey_Dahmer Indian_Premier_League'

# RUN_TIMES是传入的参数，控制运行次数
for i in `seq 1 $RUN_TIMES`
do
	# 遍历搜索词列表中的每一个词
	for word in $LABELS
	do
		echo "Running Test $i"
		echo "${word//_/ }"
	
	# 打开一个 Firefox 页面
		open_private
	
		sleep 10
	
	# 调用上面的函数，加载对应的页面，每一次运行就在这一个网站上反复捕获流量
		load_bing

	# 开始捕获流量，存下进程id
		./capture_command.sh &
		capture_pid=$!
		sleep 5
	
	# 调用feed_word函数，以固定节奏
		
		feed_word "${word//_/ }"
	
		sleep 10
	
	# 杀掉捕获流量的进程进程
		pkill -P $capture_pid
		sleep 5
	
	# 以搜索词和第几次运行重命名捕获的流量轨迹文件
		mv temp/captured_packets.pcap temp/search_"$word"_trial_$i.pcap
	
	# 关掉这个页面
		close_private

	done
	
done
