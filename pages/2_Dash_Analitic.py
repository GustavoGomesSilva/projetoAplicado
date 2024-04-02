import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from datetime import datetime
import numpy as np

st.set_page_config(
    page_title="Dash board de preços"
)

st.title('Painel analitico de preços')

resumoSemanalBrasil = pd.read_parquet('resumoSemanalBrasil.parquet.gzip')

resumoSemanalBrasil = resumoSemanalBrasil.rename(
    columns={
        "DATA INICIAL": "DATA_INICIAL",
        "DATA FINAL": "DATA_FINAL"
    }
)

precoMedioBrasil = resumoSemanalBrasil.query("PRODUTO=='OLEO DIESEL S10' or PRODUTO=='GASOLINA COMUM' or PRODUTO=='ETANOL HIDRATADO' or PRODUTO=='GASOLINA ADITIVADA'")

ultimosPrecosMedioBrasil = precoMedioBrasil.query("DATA_INICIAL=='2024-03-17'")
penultimosPrecosMedioBrasil = precoMedioBrasil.query("DATA_INICIAL=='2024-03-10'")

st.header('Ultimos preços praticados')

col1, col2, col3, col4 = st.columns(4)

with col1:
    precoRevendaEtanol = ultimosPrecosMedioBrasil.query("PRODUTO=='ETANOL HIDRATADO'")['PREÇO MÉDIO REVENDA'].values[0]
    penultimosPrecoRevendaEtanol = penultimosPrecosMedioBrasil.query("PRODUTO=='ETANOL HIDRATADO'")['PREÇO MÉDIO REVENDA'].values[0]

    delta = round(precoRevendaEtanol - penultimosPrecoRevendaEtanol, 2)

    st.metric(label="Etanol", value="R$ " + str(precoRevendaEtanol), delta=delta, delta_color="inverse")

with col2:
    precoRevendaGasolinaComum = ultimosPrecosMedioBrasil.query("PRODUTO=='GASOLINA COMUM'")['PREÇO MÉDIO REVENDA'].values[0]
    penultimosPrecoRevendaGasolinaComum = penultimosPrecosMedioBrasil.query("PRODUTO=='GASOLINA COMUM'")['PREÇO MÉDIO REVENDA'].values[0]

    delta = round(precoRevendaGasolinaComum - penultimosPrecoRevendaGasolinaComum, 2)

    st.metric(label="Gasolina Comum", value="R$ " + str(precoRevendaGasolinaComum), delta=delta, delta_color="inverse")

with col3:
    precoRevendaGasolinaAditivada = ultimosPrecosMedioBrasil.query("PRODUTO=='GASOLINA ADITIVADA'")['PREÇO MÉDIO REVENDA'].values[0]
    penultimosPrecoRevendaGasolinaAditivada = penultimosPrecosMedioBrasil.query("PRODUTO=='GASOLINA ADITIVADA'")['PREÇO MÉDIO REVENDA'].values[0]

    delta = round(precoRevendaGasolinaAditivada - penultimosPrecoRevendaGasolinaAditivada, 2)

    st.metric(label="Gasolina Aditivada", value="R$ " + str(precoRevendaGasolinaAditivada), delta=delta, delta_color="inverse")

with col4:
    precoRevendaOleoDiesel = ultimosPrecosMedioBrasil.query("PRODUTO=='OLEO DIESEL S10'")['PREÇO MÉDIO REVENDA'].values[0]
    penultimosPrecoRevendaOleoDiesel = penultimosPrecosMedioBrasil.query("PRODUTO=='OLEO DIESEL S10'")['PREÇO MÉDIO REVENDA'].values[0]

    delta = round(precoRevendaOleoDiesel - penultimosPrecoRevendaOleoDiesel, 2)

    st.metric(label="Oleo Diesel S10", value="R$ " + str(precoRevendaOleoDiesel), delta=delta, delta_color="inverse")

relacaoGasolinaAlcool = round(precoRevendaEtanol / precoRevendaGasolinaComum, 2)

vantagemTipoAbastecimento = "Gasolina Comum" if relacaoGasolinaAlcool >= 0.7 else "Etanol"

st.text('Relação Gasolina Comum x Etanol: ' + str(relacaoGasolinaAlcool))
st.text('Vantagem abastecimento: ' + vantagemTipoAbastecimento)


st.divider()

st.header('Histórico de preços')

values = st.slider(
    '',
    value=( datetime(2012, 12, 30), datetime(2024, 3, 17) ),
    format="DD/MM/YYYY"
) 

dataInicio  = values[0]
dataFim     = values[1]

precoMedioBrasil = precoMedioBrasil.query("DATA_INICIAL >= '"+str(dataInicio)+"' and DATA_INICIAL <= '"+str(dataFim)+"'")

fig = px.line(precoMedioBrasil, x="DATA_INICIAL", y="PREÇO MÉDIO REVENDA", color='PRODUTO')

st.plotly_chart(fig, theme="streamlit")

precoMedioEtanolBrasil = resumoSemanalBrasil.query("PRODUTO=='ETANOL HIDRATADO'")
precoMedioGasolinaBrasil = resumoSemanalBrasil.query("PRODUTO=='GASOLINA COMUM'")

precoMedioCoeficiente = precoMedioGasolinaBrasil['PREÇO MÉDIO REVENDA'].values.reshape(-1, 1)

model = LinearRegression()
model.fit(precoMedioCoeficiente, precoMedioEtanolBrasil['PREÇO MÉDIO REVENDA'])


precoMedioEtanolBrasilUltimoAno = resumoSemanalBrasil.query("PRODUTO=='ETANOL HIDRATADO' and DATA_INICIAL >= '2023-01-01'")
precoMedioGasolinaBrasilUltimoAno = resumoSemanalBrasil.query("PRODUTO=='GASOLINA COMUM' and DATA_INICIAL >= '2023-01-01'")

precoMedioCoeficienteUltimoAno = precoMedioGasolinaBrasilUltimoAno['PREÇO MÉDIO REVENDA'].values.reshape(-1, 1)

modelUltimoAno = LinearRegression()
modelUltimoAno.fit(precoMedioCoeficienteUltimoAno, precoMedioEtanolBrasilUltimoAno['PREÇO MÉDIO REVENDA'])



st.text('Observações sobre os dados históricos:')
st.text('- Alto Indice de correlação entre a Gasolina e o Etanol: ' + str(round(model.coef_[0], 2)))
st.text('- Periodo pós pandemia, 2023 em diante a correlação entre a Gasolina e o Etanol é negativa de (' + str(round(modelUltimoAno.coef_[0], 2)) + ') represetando um direção oposta atual')
st.text('- Aumento subito durante o periodo de pandemia entre os anos 2020 e 2022')





st.divider()

st.header('Consulta preços por estado:')

resumoSemanal = pd.read_parquet('resumoSemanal.parquet.gzip')

estados = resumoSemanal["ESTADO"].unique().sort_values()
produtos = resumoSemanal["PRODUTO"].unique().sort_values()

col1, col2 = st.columns(2)

with col1:
    optionsEstado = st.selectbox('Selecione o estado:', estados)

with col2:
    optionsProdutos = st.selectbox('Selecione o tipo combustível:', produtos)

precoMedio = resumoSemanal.query("PRODUTO=='"+str(optionsProdutos)+"' and ESTADO=='"+str(optionsEstado)+"'")

precos = precoMedio[['MUNICÍPIO', 'PRODUTO', 'PREÇO MÉDIO REVENDA', 'PREÇO MÍNIMO REVENDA', 'PREÇO MÁXIMO REVENDA']]
precos = precos.reset_index(drop=True)

st.table(precos)





st.divider()

st.header('Média preços por estado:')

estados = resumoSemanal["ESTADO"].unique().sort_values()

precosMedioEstado = []
precosMedioEstadoValue = []

for estado in estados:
    value = round(resumoSemanal.query("ESTADO=='"+str(estado)+"'")['PREÇO MÉDIO REVENDA'].mean(), 2)
    
    precosMedioEstado.append(estado)
    precosMedioEstadoValue.append(value)


precosMedios = pd.DataFrame({'Estado': precosMedioEstado, 'Preço Meédio': precosMedioEstadoValue})

st.table(precosMedios)









#calcular correlacao
