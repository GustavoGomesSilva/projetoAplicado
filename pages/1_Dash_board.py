import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import googlemaps
import json
from pyproj import Geod
from shapely.geometry import Point, LineString
from shapely.ops import nearest_points
from unidecode import unidecode

import optim

st.set_page_config(
    page_title="Otimização de Rotas"
)

municipios = pd.read_excel("municipios.xls")
resumoSemanal = pd.read_parquet('resumoSemanal.parquet.gzip')

geod = Geod(ellps="WGS84")  # Your data may be from a different Geod.

gmaps = googlemaps.Client(key='')

st.title('Otimização de Rotas')

with st.sidebar:
    st.text('Dados básico do veículo:')
    consumoMedio        = st.number_input('Consumo médio (KM/L)', placeholder='Informe o Consumo médio (KM/L)')
    volumeTanque        = st.number_input('Volume do tanque (L)', placeholder='Informe o Volume do tanque (L)')
    percentualTanque    = st.number_input('Percentual do Tanque', placeholder='Informe o Percentual do Tanque abastecido')


col1, col2 = st.columns(2)

with col1:
    cidadeOrigem = st.text_input('Cidade Origem', placeholder='Informe a cidade de origem')

with col2:
    cidadeDestino = st.text_input('Cidade Destino', placeholder='Informe a cidade de destino')


if st.button('Traçar rota'):

    #try:    
    directions_result = gmaps.directions(cidadeOrigem, cidadeDestino, mode="driving")

    distance = directions_result[0]['legs'][0]['distance']
    duration = directions_result[0]['legs'][0]['duration']
    dfsteps =  directions_result[0]['legs'][0]['steps']

    path = list()
    for step in dfsteps:
        path.append([step['start_location']['lng'], step['start_location']['lat']])

    pathString = ', '.join(map(str,path))
    pathString = '{ "path" : [' + pathString + ']}'

    json_object = json.loads(pathString)

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

    st.header('Detalhes da Rota planejada:')
    st.text('Distancia Total: ' + distance['text'])
    st.text('Duração Total: ' + duration['text'])

    line = LineString((path))
    pointOrigem = Point(path[0])

    cities = []
    
    for index, row in municipios.iterrows():
        point = Point(row['LONGITUDE'], row['LATITUDE'])

        distance = geod.geometry_length(LineString(nearest_points(line, point)))
        distanceOrigin = geod.geometry_length(LineString(nearest_points(pointOrigem, point)))
        
        if distance < 20000: # Cidade no raio de 20KM
            nomeMunicipio = row['NOME_MUNICIPIO'].replace("'", "")

            precoMedio = resumoSemanal.query("MUNICÍPIO=='" + unidecode(nomeMunicipio) + "' and PRODUTO=='OLEO DIESEL S10'")['PREÇO MÉDIO REVENDA']

            if not precoMedio.empty:
                precoMedio = precoMedio.values[0]

                if precoMedio > 0:
                    
                    cities.append({
                        'cityName': nomeMunicipio,
                        'fuelPrice': precoMedio,
                        'distanceOrigin': round(distanceOrigin, 2)
                    })

    print('###############')
    print('Cidades com preço')
    print(cities)

    veiculo = {'consumo' : consumoMedio, 'volumeTanque' : volumeTanque, 'percentualTanque' : percentualTanque}

    stops = optim.optim(cities, veiculo)

    print('Cidades para abastecimento:')
    print(stops)

    st.header('Paradas na rota:')

    if stops['status'] == '01':
        st.text(stops['mensage'])
    else:
        for index, city in enumerate(stops['cities']):
            st.text('Parada ' + str(index + 1) + ' > Cidade: ' + city['cityName'] + ' - Preço combustivel: R$'  + str(city['fuelPrice']) + ' - Litros abastecidos (L): '  + str(city['litroAbastecido']) + ' - Total Gasto: R$'  + str(round(city['litroAbastecido'] * city['fuelPrice'], 2)))


    #Except:
        #st.text('Erro ao consultar rota.')
