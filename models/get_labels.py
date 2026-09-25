def get_labels(idx):
    LABELS = [['Rebecca_Black', 'Google+', 'Ryan_Dunn', 'Casey_Anthony', 'Battlefield_3', 'iPhone_5 Adele', 'TEPCO',
               'Steve_Jobs', 'iPad_2'],
              ['Whitney_Houston', 'Gangnam_Style', 'Hurricane_Sandy', 'iPad_3', 'Diablo_3', 'Kate_Middleton',
               'Olympics_2012', 'Amanda_Todd', 'Michael_Clarke_Duncan', 'SOPA'],
              ['PlayStation_4', 'North_Korea', 'Samsung_Galaxy_4', 'Royal_Baby', 'Boston_Marathon', 'Harlem_Shake',
               'Cory_Monteith iPhone_5S', 'Paul_Walker', 'Nelson_Mandela'],
              ['Robin_Williams', 'World_Cup', 'Ebola', 'Malaysia_Airlines', 'ALS_Ice_Bucket_Challenge', 'Flappy_Bird',
               'Conchita_Wurst', 'ISIS', 'Frozen', 'Sochi_Olympics'],
              ['Lamar_Odom', 'Jurassic_World', 'American_Sniper', 'Caitlyn_Jenner', 'Ronda_Rousey', 'Paris', 'Agario',
               'Chris_Kyle', 'Fallout_4', 'Straight_Outta_Compton'],
              ['Powerball', 'Prince', 'Hurricane_Matthew', 'Pokemon_Go', 'Slither.io', 'Olympics', 'David_Bowie',
               'Trump', 'Election', 'Hillary_Clinton'],
              ['hurricane_irma', 'matt_lauer', 'tom_petty', 'super_bowl', 'las_vegas_shooting',
               'mayweather_vs_mcgregor_fight', 'solar_eclipse', 'hurricane_harvey', 'aaron_hernandez',
               'fidget_spinner'],
              ['World_Cup', 'Avicii', 'Mac_Miller', 'Stan_Lee', 'Black_Panther', 'Meghan_Markle', 'Anthony_Bourdain',
               'XXXTentacion', 'Stephen_Hawking', 'Kate_Spade'],
              ['Disney_Plus', 'Cameron_Boyce', 'Nipsey_Hussle', 'Hurricane_Dorian', 'Antonio_Brown', 'Luke_Perry',
               'Avengers_Endgame', 'Game_of_Thrones', 'iPhone_11', 'Jussie_Smollett'],
              ['Election_results', 'Kobe_Bean_Bryant', 'Zoom', 'IPL', 'India_vs_New_Zealand', 'Coronavirus_update',
               'Coronavirus_symptoms', 'Joe_Biden', 'Google_Classroom', 'oronavirus'],
              # ['手机', '笔记本', '休闲裤', '洗衣凝珠', '衬衫'],
              # shopping

              ['switch', 'laptop', 'airpods', 'headphones', 'earbuds', 'ipad', 'ssd', 'fitbit', 'game_of_thrones',
               'fire_stick'],
              ['toilet_paper', 'external_hard_drive', 'instant_pot', 'tablet', 'micro_sd_card', 'kindle', 'tv',
               'air_fryer', 'bluetooth', 'roku'],


              # 拼音
              ['shouji', 'bijiben', 'kuzi', 'chenshan', 'weishengzhi', 'lianyiqun', 'xiyiningzhu', 'nanxie', 'nvxie',
               'dianshi'],

              # 最后 ebay
              ['gaming_chair', 'apple_watch', 'monitor', 'ps4', 'alexa', 'paper_towels', 'desk', 'office_chair',
               'ring_doorbell', 'luggage'],






              # medicine
              ['cough', 'headache', 'heart disease', 'hepatitis', 'leukemia', 'meningitis', 'rabies', 'stroke', 'AIDS', 'cystitis'],
              ['cefuroxime', 'aspirin', 'coronavirus', 'careers', 'medical_records', 'map', 'insurance_accepted', 'telemedicine', 'ibuprofen depression'],
              ['influenza', 'diarrhea', 'covid19', 'breast_cancer', 'erectile_dysfunction', 'hemorrhoids', 'canker_sore', 'anemia', 'hypertension', 'rhinitis'],

              ]
    return LABELS[idx - 1]


def get_labels_2(idx):
    LABELS = [['PlayStation_4', 'North_Korea', 'Samsung_Galaxy_4', 'Royal_Baby', 'Boston_Marathon', 'Harlem_Shake',
               'Cory_Monteith iPhone_5S', 'Paul_Walker', 'Nelson_Mandela'],
              ['Robin_Williams', 'World_Cup', 'Ebola', 'Malaysia_Airlines', 'ALS_Ice_Bucket_Challenge', 'Flappy_Bird',
               'Conchita_Wurst', 'ISIS', 'Frozen', 'Sochi_Olympics'],
              ['Lamar_Odom', 'Jurassic_World', 'American_Sniper', 'Caitlyn_Jenner', 'Ronda_Rousey', 'Paris', 'Agario',
               'Chris_Kyle', 'Fallout_4', 'Straight_Outta_Compton'],
              ['Powerball', 'Prince', 'Hurricane_Matthew', 'Pokemon_Go', 'Slither.io', 'Olympics', 'David_Bowie',
               'Trump', 'Election', 'Hillary_Clinton'],
              ['hurricane_irma', 'matt_lauer', 'tom_petty', 'super_bowl', 'las_vegas_shooting',
               'mayweather_vs_mcgregor_fight', 'solar_eclipse', 'hurricane_harvey', 'aaron_hernandez',
               'fidget_spinner'],
              ['World_Cup', 'Avicii', 'Mac_Miller', 'Stan_Lee', 'Black_Panther', 'Meghan_Markle', 'Anthony_Bourdain',
               'XXXTentacion', 'Stephen_Hawking', 'Kate_Spade'],
              ['Disney_Plus', 'Cameron_Boyce', 'Nipsey_Hussle', 'Hurricane_Dorian', 'Antonio_Brown', 'Luke_Perry',
               'Avengers_Endgame', 'Game_of_Thrones', 'iPhone_11', 'Jussie_Smollett'],
              ['Election_results', 'Kobe_Bean_Bryant', 'Zoom', 'IPL', 'India_vs_New_Zealand', 'Coronavirus_update',
               'Coronavirus_symptoms', 'Joe_Biden', 'Google_Classroom', 'oronavirus'],
              ['Australia_vs_India', 'India_vs_England', 'IPL', 'NBA', 'Euro_2021', 'Copa_America', 'India_vs_New_Zealand', 'T20_World_Cup', 'Squid_Game', 'DMX'],
              ['Wordle', 'India_vs_England', 'Ukraine', 'Queen_Elizabeth', 'Ind_vs_SA', 'World_Cup', 'India_vs_West_Indies', 'iPhone14' 'Jeffrey_Dahmer', 'Indian_Premier_League']
              ]
    return LABELS[idx - 1]