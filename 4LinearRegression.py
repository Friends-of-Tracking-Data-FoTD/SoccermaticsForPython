#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An example of linear regression
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

#Some made up data
minutes_played=np.array([120,452,185,708,340,561])
goals_scored=np.array([1,6,3,7,3,5])

#Set up dataframe
minutes_model = pd.DataFrame()
minutes_model = minutes_model.assign(minutes=minutes_played)
minutes_model = minutes_model.assign(goals=goals_scored)

fig,ax=plt.subplots(num=1)
ax.plot(minutes_played, goals_scored, linestyle='none', marker= '.', markerSize= 12, color='black')
ax.set_ylabel('Goals scored')
ax.set_xlabel('Minutes played')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xlim((0,750))
plt.ylim((0,8))

#Slope of one goal per 90 played
#b=1/90
#Intercept
a=0


#Slope determined by linear regression
model_fit=smf.ols(formula='goals_scored ~ minutes_played -1 ', data=minutes_model).fit()
print(model_fit.summary())        
[b]=model_fit.params

x=np.arange(800,step=0.1)
y= a + b*x 

ax.plot(minutes_played, goals_scored, linestyle='none', marker= '.', markerSize= 12, color='black')
ax.plot(x, y, color='black')

#Show distances to line
for i,mp in enumerate(minutes_played):
    ax.plot([mp,mp],[goals_scored[i],a+b*mp], color='red')


plt.show()
fig.savefig('Output/LinearRelationship' + str(round(1/b)) + '.pdf', dpi=None, bbox_inches="tight")   

