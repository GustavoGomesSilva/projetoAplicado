import pandas as pd

# resumoSemanaldf = pd.read_excel("https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/precos-revenda-e-de-distribuicao-combustiveis/shlp/semanal/semanal-brasil-desde-2013.xlsx", header=17)

# resumoSemanaldf['PRODUTO']            = resumoSemanaldf['PRODUTO'].astype('category')
# resumoSemanaldf['UNIDADE DE MEDIDA']  = resumoSemanaldf['UNIDADE DE MEDIDA'].astype('category')
# resumoSemanaldf['DATA INICIAL']       = resumoSemanaldf['DATA INICIAL'].astype('category')
# resumoSemanaldf['DATA FINAL']         = resumoSemanaldf['DATA FINAL'].astype('category')

# resumoSemanaldf['MARGEM MÉDIA REVENDA']             = resumoSemanaldf['MARGEM MÉDIA REVENDA'].str.replace('-', '')
# resumoSemanaldf['PREÇO MÉDIO DISTRIBUIÇÃO']         = resumoSemanaldf['PREÇO MÉDIO DISTRIBUIÇÃO'].str.replace('-', '')
# resumoSemanaldf['DESVIO PADRÃO DISTRIBUIÇÃO']       = resumoSemanaldf['DESVIO PADRÃO DISTRIBUIÇÃO'].str.replace('-', '')
# resumoSemanaldf['PREÇO MÍNIMO DISTRIBUIÇÃO']        = resumoSemanaldf['PREÇO MÍNIMO DISTRIBUIÇÃO'].str.replace('-', '')
# resumoSemanaldf['PREÇO MÁXIMO DISTRIBUIÇÃO']        = resumoSemanaldf['PREÇO MÁXIMO DISTRIBUIÇÃO'].str.replace('-', '')
# resumoSemanaldf['COEF DE VARIAÇÃO DISTRIBUIÇÃO']    = resumoSemanaldf['COEF DE VARIAÇÃO DISTRIBUIÇÃO'].str.replace('-', '')

# print(resumoSemanaldf)
# resumoSemanaldf.to_parquet('resumoSemanalBrasil.parquet.gzip', compression='gzip') 

resumoSemanal = pd.read_parquet('resumoSemanalBrasil.parquet.gzip')  

precoMedio = resumoSemanal.query("PRODUTO=='OLEO DIESEL S10'")['PREÇO MÉDIO REVENDA']

print(precoMedio)