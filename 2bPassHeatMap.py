#Make a heat map of all teams passes during a tournament
#Set match id in match_id_required.

#Function to draw the pitch
import matplotlib.pyplot as plt
import numpy as np
from pandas.io.json import json_normalize
from FCPython import createPitch

#Size of the pitch in yards (!!!)
pitchLengthX=120
pitchWidthY=80

#The team we are interested in
#team_required ="United States Women's"
team_required ="England Women's"
team_required ="Sweden Women's"
#team_required ="Germany Women's"


#Find the matches they played
match_id_required=[]
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
    team_passes = (df['team_name']==team_required)
    df = df[team_passes]
    
    #A dataframe of shots
    passes_match = df.loc[df['type_name'] == 'Pass'].set_index('id')
    
    
    if i==0:
        passes = passes_match
    else:
        passes.append(passes_match)

    print('Match: ' + str(match_id) + '. Number of passes is: ' + str(len(passes_match)))


#Set number of matches
number_of_matches=i+1

#Size of the pitch in yards (!!!)
pitchLengthX=120
pitchWidthY=80

#Plot the passes
(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')
for i,thepass in passes.iterrows():
    x=thepass['location'][0]
    y=pitchWidthY-thepass['location'][1]
    passCircle=plt.Circle((x,y),1,color="blue")      
    passCircle.set_alpha(.2)   
    ax.add_patch(passCircle)
    #dx=thepass['pass_end_location'][0]-x
    #dy=thepass['pass_end_location'][1]-y
    #passArrow=plt.Arrow(x,y,dx,dy,width=1,color="blue")
    #ax.add_patch(passArrow)


fig.set_size_inches(10, 7)
fig.savefig('Output/passes.pdf', dpi=100) 
plt.show()


x=[]
y=[]
for i,apass in passes.iterrows():
    x.append(apass['location'][0])
    y.append(pitchWidthY-apass['location'][1])

H_Pass=np.histogram2d(y, x,bins=10,range=[[0, pitchWidthY],[0, pitchLengthX]])

from FCPython import createPitch
(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')
pos=ax.imshow(H_Pass[0]/number_of_matches, extent=[0,120,0,80], aspect='auto',cmap=plt.cm.Reds)
fig.colorbar(pos, ax=ax)
ax.set_title('Number of passes per match')
plt.xlim((-1,121))
plt.ylim((-3,83))
plt.tight_layout()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()





    

