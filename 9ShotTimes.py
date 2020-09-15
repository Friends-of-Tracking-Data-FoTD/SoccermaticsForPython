#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot Histogram of Times of Shots and Goals
"""
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib

#Load in Wyscout data
with open('wyscout/events/events_Germany.json') as f:
    data = json.load(f)

data_df = pd.DataFrame(data)

#Identify the goals and add them to a column
shots=data_df[data_df['subEventName']=='Shot']
shots.assign(Goal = 0)
for i,shot in shots.iterrows():
    for shottags in shot['tags']:
            #Tags contain that its a goal
            if shottags['id']==101:
                shots.at[i,'Goal']=1

half='1H'
isgoal=0

#Find the particular shots I am interested in
if isgoal:
    the_shots=shots[np.logical_and((shots['matchPeriod']==half), (shots['Goal']==1))]['eventSec']
else:
    the_shots=shots[(shots['matchPeriod']==half)]['eventSec']
    
#Basic shot statistics
total_shots=len(the_shots)
number_of_matches=len(np.unique(shots['matchId']))
shots_per_match=total_shots/number_of_matches
shots_per_min=total_shots/48




from pylab import rcParams
rcParams['figure.figsize'] = 12/2.54, 8/2.54

matplotlib.font_manager.FontProperties(family='Helvetica',size=11)

#Set up figure
fig=plt.figure()
ax=fig.add_subplot(1,1,1)

#Plot histogram of shots
plt.hist(the_shots/60, bins = range(0,49))
plt.plot([0, 48],[shots_per_min, shots_per_min], color='black')
 
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_position('zero')    
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xticks(np.arange(0,48,5))
ax.set_xlabel('Time elapsed in ' + half[0] + ' half')
if isgoal==0:
    ax.set_ylabel('Number of shots over the season')
    ax.set_yticks(np.arange(0,120,20))
    ax.set_ylim(0,130) 
else:
    ax.set_ylabel('Number of goals over the season')
    ax.set_yticks(np.arange(0,20,2))
    ax.set_ylim(0,20) 
    
    
plt.show()    

#Save the figure to a pdf
if isgoal:
    fig.savefig('Output/TimesOfGoals' + half +'.pdf' , dpi=None, bbox_inches="tight")
else:
    fig.savefig('Output/TimesOfShots' + half +'.pdf' , dpi=None, bbox_inches="tight")
