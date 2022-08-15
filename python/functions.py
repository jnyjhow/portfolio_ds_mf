#importando as bibliotecas
import pandas as pd
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objs as go

from datetime import datetime

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#funcao para calcular o retorno do ativo e retornar um pivot
def pfun_pivot_calcular_retorno(filter_asset, df, tipo_pivot = 1, tipo_retorno = 'M'):
    
    if tipo_retorno == 'D':
        df_aux = df[filter_asset].pct_change().dropna().to_frame()
    else:
        df_aux = df[filter_asset].resample(tipo_retorno, kind='period').last().pct_change().dropna().to_frame()
    
    #alterando nome de uma coluna especifica
    df_aux.rename(columns = {filter_asset:'return'}, inplace = True)
    
    if tipo_pivot == 1:
        print(f'{tipo_retorno} >>>>> RETORNO DO ATIVO CALCULADO COM SUCESSO! >>>>> {filter_asset}')      
        return(df_aux)
    
    else:
        print(f'RETORNANDO DF PIVOT!')
        
        if tipo_retorno == 'M':
            print(f'DF PIVOT MENSAL >>>>> {filter_asset}')
            #criando colunas month e year para obter os dados de mês e ano
            df_aux['month'] = df_aux.index.month
            df_aux['year'] = df_aux.index.year
        
            #convertendo df para pivot com ano e mes
            df_pivot = df_aux.pivot(values='return', columns='month', index='year')
            
        elif tipo_retorno == 'Q':
            print(f'DF PIVOT TRIMESTRAL >>>>> {filter_asset}')
            #criando colunas month e year para obter os dados de mês e ano
            df_aux['quarter'] = df_aux.index.quarter
            df_aux['year'] = df_aux.index.year
        
            #convertendo df para pivot com ano e trimestre
            df_pivot = df_aux.pivot(values='return', columns='quarter', index='year')
        
        else:
            print('TIPO DE RETORNO INVALIDO!!!')
            df_pivot = None
        
        return(df_pivot)
    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
#funcao para retornar o acumulado
def pfun_calcular_retorno(df_aux):
  df = df_aux.copy()  
  df['daily_return'] = df.iloc[:,0].pct_change()
  df['acum_return'] = (1 +  df['daily_return']).cumprod()
  df['daily_return'].iloc[0] = 0
  df['acum_return'].iloc[0] = 1
  df.rename(columns={df.columns[0]: 'price'}, inplace=True)

  return df

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#funcao para gerar grafico de retorno no formato de pivot
def pfun_gerar_grafico_retorno_pivot(df, filter_asset, tipo_principal='r', tipo_retorno='Mensal', 
                                     tipo_format='.1%', n_aux=0.2):
    
    if tipo_principal == 'r':
        titulo_mod = 'Retorno'
    else:
        titulo_mod = 'Dividendo'
        n_aux_min = 0
        n_aux_max = n_aux * 2
        n_center = 0
    
    if tipo_retorno == 'Anual':
        titulo_aux = f'Janelas de {titulo_mod} (anual) - {filter_asset}'
        
    elif tipo_retorno == 'anual_real':
        titulo_aux = f'Janelas de Retorno Reais (base {n_aux}) - {filter_asset}'
        n_aux_min = n_aux * (1 - 0.3)
        n_aux_max = n_aux * (1 + 0.5)
        n_center = n_aux
        
    else:
        titulo_aux = f'{titulo_mod} {tipo_retorno} - {filter_asset}'
        
    if tipo_retorno != 'anual_real':
        n_aux_min = -n_aux
        n_aux_max = n_aux
        n_center = 0
        
    if (tipo_retorno == 'Anual' and tipo_principal == 'd'):
        n_aux_min = 0
        n_aux_max = n_aux * 20
        n_center = n_aux * 10
    
    ax = sns.heatmap(df, 
                     annot=True, 
                     fmt=tipo_format, 
                     cmap='RdYlGn', 
                     vmin=n_aux_min, 
                     vmax=n_aux_max, 
                     center=n_center, 
                     cbar=False)
        
    ax.set_title(titulo_aux, pad=15, fontdict={'fontsize':20, 'fontweight':600})
    ax.tick_params(axis = 'y', labelright =True, labelrotation=0, labelsize='large')
    ax.tick_params(axis = 'x', labeltop=True)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#funcao para gerar df pivot dos dividendos
def pfun_pivot_dividendos(df, coluna_aux=[], tipo_agg='sum'):
    df_aux = pd.pivot_table(df, values='dividendos_pagos', index='year', columns=coluna_aux, aggfunc=tipo_agg)
    return(df_aux)


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++