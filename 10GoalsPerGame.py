#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Poisson distribution of goals
"""

import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

#Load in Wyscout data
#Data: https://figshare.com/collections/Soccer_match_event_dataset/4415000/2
#Article: https://www.nature.com/articles/s41597-019-0247-7
#Documentation: https://apidocs.wyscout.com/matches-wyid-events

with open('wyscout/events/events_Germany.json') as f:
    data = json.load(f)

data_df = pd.DataFrame(data)

#Identify the goals and add them to a column
shots=data_df[data_df['subEventName'].isin(['Shot','Free kick shot','Penalty'])]

shots=shots.assign(Goal = 0)
for i,shot in shots.iterrows():
    for shottags in shot['tags']:
            #Tags contain that its a goal
            if shottags['id']==101:
                shots.at[i,'Goal']=1
sum(shots['Goal'])
                
match_list=shots['matchId'].unique().tolist()
num_matches=len(match_list)
shots_in_match=[]
goals_in_match=[]
for match in match_list:
    shots_in_match.append(len(shots[shots['matchId']==match]))
    goals_in_match.append(len(shots[np.logical_and(shots['matchId']==match, (shots['Goal']==1))]))
    
    
#Set up figure
fig=plt.figure()
from pylab import rcParams
rcParams['figure.figsize'] = 12/2.54, 8/2.54
ax=fig.add_subplot(1,1,1)


#Make histogram of goals/shots
mean_goals=np.mean(goals_in_match)
goals_dist,goals_bins=np.histogram(goals_in_match, bins = np.arange(-0.5,10.5))
goals_dist=goals_dist/num_matches

#Make Poisson distribution
g=np.arange(0,10)
Poisson_g=np.zeros(10)
for i,k in enumerate(g):
    Poisson_g[i] = np.power(mean_goals,k)*np.exp(-mean_goals)/np.math.factorial(k)


#Plot data


plt.hist(g-0.5,9, weights=goals_dist)
plt.plot(g,Poisson_g, color='black')
ax.set_yticks(np.arange(0,0.3,0.1)) 
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_position('zero')    
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xticks(np.arange(0,10,1))
ax.set_ylabel('Proportion of matches')
ax.set_xlabel('Number of goals scored')
plt.show()    

#Save the figure to a pdf
fig.savefig('output/PoissonDistributionGoals.pdf' , dpi=None, bbox_inches="tight")


    
#Exercise: 
#1, Make a histogram of shots per game
#2, Find the mean and standard deviation for shots per game 
#3, Show that shots per game is roughtly normally distributed.