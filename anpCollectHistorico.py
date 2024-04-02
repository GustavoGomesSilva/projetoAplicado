import pandas as pd

# resumoSemanaldf = pd.read_excel("https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/precos-revenda-e-de-distribuicao-combustiveis/shlp/semanal/semanal-municipios-2022-2024.xlsx",header=11)

# print(resumoSemanaldf)
# resumoSemanaldf['ESTADO']             = resumoSemanaldf['ESTADO'].astype('category')
# resumoSemanaldf['MUNICÍPIO']          = resumoSemanaldf['MUNICÍPIO'].astype('category')
# resumoSemanaldf['PRODUTO']            = resumoSemanaldf['PRODUTO'].astype('category')
# resumoSemanaldf['UNIDADE DE MEDIDA']  = resumoSemanaldf['UNIDADE DE MEDIDA'].astype('category')
# resumoSemanaldf['DATA INICIAL']       = resumoSemanaldf['DATA INICIAL'].astype('category')
# resumoSemanaldf['DATA FINAL']         = resumoSemanaldf['DATA FINAL'].astype('category')

# print(resumoSemanaldf)
# resumoSemanaldf.to_parquet('resumoSemanal2022_2024.parquet.gzip', compression='gzip') 

resumoSemanal = pd.read_parquet('resumoSemanal2022_2024.parquet.gzip')  

precoMedio = resumoSemanal.query("MUNICÍPIO=='UBERABA' and PRODUTO=='OLEO DIESEL S10'")['PREÇO MÉDIO REVENDA']

print(precoMedio)