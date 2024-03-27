import pandas as pd

# resumoSemanaldf = pd.read_excel("https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/arquivos-lpc/2024/resumo_semanal_lpc_2024-02-11_2024-02-17.xlsx", sheet_name="MUNICIPIOS", header=9)

# resumoSemanaldf['ESTADO']             = resumoSemanaldf['ESTADO'].astype('category')
# resumoSemanaldf['MUNICÍPIO']          = resumoSemanaldf['MUNICÍPIO'].astype('category')
# resumoSemanaldf['PRODUTO']            = resumoSemanaldf['PRODUTO'].astype('category')
# resumoSemanaldf['UNIDADE DE MEDIDA']  = resumoSemanaldf['UNIDADE DE MEDIDA'].astype('category')
# resumoSemanaldf['DATA INICIAL']       = resumoSemanaldf['DATA INICIAL'].astype('category')
# resumoSemanaldf['DATA FINAL']         = resumoSemanaldf['DATA FINAL'].astype('category')

# resumoSemanaldf.to_parquet('resumoSemanal.parquet.gzip', compression='gzip') 

#resumoSemanal = pd.read_parquet('resumoSemanal.parquet.gzip')  

resumoSemanal = pd.read_parquet('resumoSemanal.parquet.gzip')
precoMedio = resumoSemanal.query("MUNICÍPIO=='UBERABA' and PRODUTO=='OLEO DIESEL S10'")['PREÇO MÉDIO REVENDA'].values[0]

print(precoMedio)