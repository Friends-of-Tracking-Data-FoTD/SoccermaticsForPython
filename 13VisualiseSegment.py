# -*- coding: utf-8 
import math
import os
import time
import random

import numpy as np
import matplotlib.pyplot as plt

from Libraries import Functions_PreprocessTrackingData as funcs
from Libraries import Dictionaries as dicts

file_name = '20190722.Hammarby-IFElfsborg'
#file_name = '20191020.Hammarby-MalmöFF'
#file_name = '20190930.Hammarby-Örebrö'

#Names of the teams playing in OPTA format
home_team_name = 'Hammarby IF'
away_team_name = 'IF Elfsborg'
year = file_name[:4]

#First '.1' or second '.2' half of the match
data_file_name=file_name+'.1'

#Preprocesses the file in to the format we use.
if not os.path.exists('../Signality/'+year+'/Tracking Data/Preprocessed/'+data_file_name+'_preprocessed.pickle'):
    preprocessed = False
    [ball_position_not_transf,players_position_not_transf,players_team_id,events,players_jersey,
     info_match,names_of_players] = funcs.LoadDataHammarbyNewStructure2020(data_file_name,'Signality/2019/Tracking Data/')
else:
    preprocessed = True
    [ball_position_not_transf,players_position_not_transf,players_team_id,events,players_jersey,
     info_match,names_of_players,players_in_play_list] = funcs.LoadDataHammarbyPreprocessed(data_file_name,'Signality/2019/Tracking Data/')

frame=1000

team_index = players_team_id[frame].astype(int).reshape(len(players_team_id[frame]),)
players_in_play = funcs.GetPlayersInPlay(players_position_not_transf,frame)

[players_position,ball_position] = funcs.TransformCoords(players_position_not_transf,ball_position_not_transf)

color_home='green'
color_away='yellow'

from Libraries import Functions_PreprocessTrackingData as funcs
funcs.PlotSituation(players_position[frame][players_in_play],
                      ball_position[frame-10:frame],team_index[players_in_play],
                      frame,players_jersey[players_in_play],color_home,color_away)



