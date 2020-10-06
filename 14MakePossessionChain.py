#Written by Sebastian and Jernej at Twelve

import json
from pandas import json_normalize
import random
from plotly import graph_objects, offline


class Field ():

    def __init__(self):
        figure = graph_objects.Figure()

        figure.update_layout(width=900*1.388, height=900, autosize=False, plot_bgcolor="white")
        figure.update_xaxes(range=[-0.03, 1.03])
        figure.update_yaxes(range=[-0.03, 1.03])

        self.figure = figure

        self.__draw_full()

    def add_title(self, main_title: str):
        """
        Adds a title to the pitch visualization
        """
        self.figure.update_layout(title={'text': main_title, 'x': 0.48, 'y': 0.91,
                                         'xanchor': 'center', 'yanchor': 'top'})

    def save(self, name: str):
        """Saves PNG and html image"""
        offline.plot(self.figure, filename=f"{name}", auto_open=False)

    def __draw_full(self):
        # Contour
        self.figure.add_shape(type="rect", x0=0, y0=0, x1=1, y1=1)
        # Half way line
        self.figure.add_shape(type="line", x0=0.5, y0=0, x1=0.5, y1=1)
        circle_radius = 0.0915
        self.figure.add_shape(type="circle", x0=0.5-circle_radius*0.72, y0=0.5 -
                              circle_radius, x1=0.5+circle_radius*0.72, y1=0.5+circle_radius)
        # Defensive goal area
        self.figure.add_shape(type="rect", x0=0, y0=0.211, x1=0.170, y1=0.789)
        self.figure.add_shape(type="rect", x0=0, y0=0.368, x1=0.058, y1=0.632)
        self.figure.add_shape(type="rect", x0=-0.01, y0=0.447, x1=0.0, y1=0.553)
        # Attacking goal area
        self.figure.add_shape(type="rect", x0=0.83, y0=0.211, x1=1.0, y1=0.789)
        self.figure.add_shape(type="rect", x0=0.942, y0=0.368, x1=1.0, y1=0.632)
        self.figure.add_shape(type="rect", x0=1.0, y0=0.447, x1=1.01, y1=0.553)


def add_possession_chain_sb(figure, chain, team_name: str, opacity: int = 1.0):
    this_team_color = "#1F77B4"
    other_team_color = "#FF7F0E"

    chain_x = []
    chain_y = []
    text = []
    colors = []
    outcomes = []
    times = []
    counter = 0
    try:
        for idx, row in chain.iterrows():
            event_name = row['type_name']
            event_loc = row['location']

            # Transform  coordinates
            x = round((event_loc[0] * (100 / 120)) / 100, 3)
            y = round(((80 - event_loc[1]) * (100 / 80)) / 100, 3)  # Reverse it because opta pitch is 0,100 and statsbomb 100,0

            color = this_team_color

            # slightly shift events that has the same coodinates
            if x in chain_x and y in chain_y:
                x = x + random.choice([-0.001, 0.001])
                y = y + random.choice([-0.001, 0.001])

            if row['possession_team_id'] != row['team_id']:
                color = other_team_color
                x = round(1.000 - x, 3)
                y = round(1.000 - y, 3)

            chain_x.append(x)
            chain_y.append(y)
            if row['possession_team_id'] == row['team_id']:
                text.append(f"{counter}.{event_name}")
            else:
                text.append(f"{counter}.{event_name}")

            colors.append(color)
            times.append(f"{row['minute']}{row['second']}")
            outcomes.append('circle')
            counter += 1

    except Exception as err:
        print(err)

    line_color = "#7F7F7F"

    figure.add_trace(
        {'mode': 'markers+lines+text',
         'textposition': 'top center',
         'type': 'scatter',
         'x': chain_x,
         'y': chain_y,
         'hovertemplate': "Time: %{hovertext}<br>Event: %{text}",
         'text': text,
         'opacity': opacity,
         'hovertext': times,
         'marker': {'color': colors, 'size': 8, 'symbol': outcomes},
         'line': {'color': line_color, 'dash': 'solid'},
         'name': "{} {}:{} ".format(chain.iloc[0]['minute'], chain.iloc[0]['second'],team_name)
         }
    )

# MAIN METHOD

match_id_required = 69301
home_team_required ="England Women's"
away_team_required ="Sweden Women's"

# Load in the data
# I took this from https://znstrider.github.io/2018-11-11-Getting-Started-with-StatsBomb-Data/
file_name=str(match_id_required)+'.json'

#Load in all match events 
import json
with open('Statsbomb/data/events/'+file_name) as data_file:
    data = json.load(data_file)



match_events = json_normalize(data, sep="_") # Tranform data to DataFrmae

relevand_possessions = match_events[(match_events['type_id'] == 16)]['possession'].unique()  # all uniques possessions with shot

 # Create Pitch
ground = Field()
ground.add_title('Possession chains')

for possession in relevand_possessions:

    df = match_events[match_events['possession'] == possession] # get all events of the possession

    # add each event
    add_possession_chain_sb(ground.figure, df, team_name= df.iloc[0]['team_name'])

#Look in the file below for the visulasiation of chains.
ground.save('possessions.html')
