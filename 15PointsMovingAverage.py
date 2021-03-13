
"""
Created on Fri Mar 12 05:53:35 2021

@author: davsu428
"""

import datetime 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dflist=[]

seasonst=[]
for year in range(5,21,1):
    if year<9:
        yeartext='0'+str(year)+'0'+str(year+1)
        yeartext2='0'+str(year)+'-0'+str(year+1)
    elif year==9:
        yeartext='0910'
        yeartext2='09-10'
    else:
        yeartext=str(year)+str(year+1)
        yeartext2=str(year)+'-'+str(year+1)
        
    seasonst=seasonst+[yeartext2]
    #For England
    performance_year = pd.read_csv("https://www.football-data.co.uk/mmz4281/"+yeartext+"/E0.csv",delimiter=',') 
    #For Spain
    #performance_year = pd.read_csv("https://www.football-data.co.uk/mmz4281/"+yeartext+"/SP1.csv",delimiter=',') 
    dflist=dflist+[performance_year]

performance= pd.concat(dflist)
        
teams=list(set(performance['AwayTeam']))


ma=38

teamdf=dict()

for team in teams:
    game=0
    rows=[]
    matches=performance[((performance['AwayTeam']==team) | (performance['HomeTeam']==team))]
    for i,match in matches.iterrows():
        game=game+1
            
        #matchdate = datetime.datetime.strptime(match['Date'],"%d/%m/%y")
        
        if match['AwayTeam']==team:
            goalsfor=match['FTAG']
            goalsagainst=match['FTHG']
            oddsfor=match['PSA']
            if match['FTR']=='A':
                points=3
                profit=oddsfor-1
            elif match['FTR']=='D':
                points=1
                profit=-1
            else:
                points=0
                profit=-1
        if match['HomeTeam']==team:
            goalsfor=match['FTHG']
            goalsagainst=match['FTAG']
            oddsfor=match['PSH']
            if match['FTR']=='H':
                points=3
                profit=oddsfor-1
            elif match['FTR']=='D':
                points=1
                profit=-1
            else:
                points=0
                profit=-1
        goaldiff=goalsfor-goalsagainst
        rows.append([matchdate,goalsfor,goalsagainst,goaldiff,points,profit,season,game])
    
    ma_goaldiff=np.convolve(goaldiff, np.ones(10)/10, mode='valid')
    
    df = pd.DataFrame(rows, columns=["Date", "For","Against","Difference","Points","Profit","Season","Game"])    
    #df = df.sort_values('Date', ascending=True)
    df['PointsRA'] = df['Points'].rolling(window=ma, win_type='triang').mean()
    teamdf[team]=df



import matplotlib.pyplot as plt
import matplotlib.dates as mdates


fig,ax=plt.subplots(num=1)

comparison1='Man City'
comp_color1='lightblue'
comparison3='Liverpool'
comp_color3='red'
comparison2='Man United'
comp_color2='darkred'

#
#comparison1='Real Madrid'
#comp_color1='blue'
#comparison2='Barcelona'
#comp_color2='darkred'
#comparison3='Ath Madrid'
#comp_color3='red'

ax.plot(teamdf[comparison1]['Game'],  teamdf[comparison1]['PointsRA'], linewidth=2, linestyle='-',color=comp_color1)
ax.plot(teamdf[comparison2]['Game'],  teamdf[comparison2]['PointsRA'], linewidth=2 , linestyle='-',color=comp_color2)
ax.plot(teamdf[comparison3]['Game'],  teamdf[comparison3]['PointsRA'], linewidth=2 , linestyle='-',color=comp_color3)

ax.set_title(str(ma) + ' game moving average')
plt.gcf().autofmt_xdate()

ax.legend([comparison1,comparison2,comparison3])

ax.set_ylim(1,3.2)

ax.set_xticks(np.arange(0,max(teamdf[comparison2]['Game']),38))
ax.set_xticklabels(seasonst)
ax.set_xlim(0,max(teamdf[comparison2]['Game'])+40)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

fig.show()

ax.set_ylabel('Rolling Average Points Per Game')
ax.set_xlabel('Season')


fig.savefig('dip.png', dpi=None, bbox_inches="tight")