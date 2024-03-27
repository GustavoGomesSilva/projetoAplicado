import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import googlemaps
import json

print('************************\n\n\n************************')

gmaps2 = googlemaps.Client(key='AIzaSyBkyO5wbc1eAJ_sDg86VM-_4zhC7k_YHd4')

directions_result = gmaps2.directions("Uberlandia, MG", "Porto Alegre, RS", mode="driving")

distance = directions_result[0]['legs'][0]['distance']
duration = directions_result[0]['legs'][0]['duration']
dfsteps =  directions_result[0]['legs'][0]['steps']

path = list()
for step in dfsteps:
  path.append([step['start_location']['lng'], step['start_location']['lat']])

path = ', '.join(map(str,path))
path = '{ "path" : [' + path + ']}'

json_object = json.loads(path)

dfPath = pd.json_normalize(json_object)


st.pydeck_chart(
    pdk.Deck(
        map_style = None,
        initial_view_state = pdk.ViewState(
            latitude=dfsteps[0]['start_location']['lat'],
            longitude=dfsteps[0]['start_location']['lng'],
            zoom=10,
            pitch=2,
        ),
        layers=[
            pdk.Layer(
                'PathLayer',
                data=dfPath,
                pickable=True,
                get_color='[30, 70, 240]',
                width_scale=20,
                width_min_pixels=2,
                get_path="path",
                get_width=2
            )
        ]
    )
)