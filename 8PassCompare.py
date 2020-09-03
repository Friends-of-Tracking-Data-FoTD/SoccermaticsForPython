#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 13:50:04 2020

@author: davsu428
"""
#Load in Statsbomb competition and match data
#This is a library for loading json files.
import json

#Load the competition file
#Got this by searching 'how do I open json in Python'
with open('Statsbomb/data/competitions.json') as f:
    competitions = json.load(f)
    
#Womens World Cup 2019 has competition ID 72
competition_id=72

#Load the list of matches for this competition
with open('Statsbomb/data/matches/'+str(competition_id)+'/30.json') as f:
    matches = json.load(f)

#Get all the teams
teams=[]
for match in matches:
    matches[0]
matches[0]['home_team']
matches[0]['home_team']['home_team_name']
matches[0]['away_team']['away_team_name']



for match in matches:
    home_team_name=match['home_team']['home_team_name']
    away_team_name=match['away_team']['away_team_name']
    if (home_team_name==team_required) or (away_team_name==team_required):
        match_id_required.append(match['match_id'])
        
print(match_id_required)

# Load in the data
# I took this from https://znstrider.github.io/2018-11-11-Getting-Started-with-StatsBomb-Data/


for i,match_id in enumerate(match_id_required):
    file_name=str(match_id)+'.json'
    
    #Load in all match events 
    import json
    with open('Statsbomb/data/events/'+file_name) as data_file:
        #print (mypath+'events/'+file)
        data = json.load(data_file)
    
    #get the nested structure into a dataframe 
    #store the dataframe in a dictionary with the match id as key (remove '.json' from string)
    df = json_normalize(data, sep = "_").assign(match_id = file_name[:-5])
    
    #A dataframe of shots
    passes_match = df.loc[df['type_name'] == 'Pass'].set_index('id')
    if i==0:
        passes = passes_match
    else:
        passes.append(passes_match)

    print('Match: ' + str(match_id) + '. Number of passes is: ' + str(len(passes_match)))

