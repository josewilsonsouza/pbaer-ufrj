import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Título do aplicativo
st.title('PBAER')
st.sidebar.image('logo_ufrj.png', use_column_width=True)

@st.cache_data
def carregar_dados():
    tabela = pd.read_csv('Media_EVA_RET_SUC_por_CENTRO.csv', sep=';', encoding='utf-8')
    return tabela

def grafico_GERAL(df):
    '''
    Função que Plota o gráfico do Centro selecionado

    Parameters
    ----------
    df : dataframe.

    Returns
    -------
    grafico.

    '''
    with st.container():
        
        st.header("Análise GERAL")
    
        st.write("---")
        df = carregar_dados_CENTROS()
        centros = st.selectbox("Selecione o CENTRO", sorted(df['CENTRO'].unique()))
        df_filter = df.loc[df.CENTRO == centros].copy()
        
        indicadores = ['EVASAO', 'RETENCAO', 'SUCESSO']
        labels = ['Evasão', 'Retenção', 'Sucesso']
        
        fig, ax = plt.subplots(figsize=(7,4))
        x = df_filter['CO_ANO']
        
        for ind, label in zip(indicadores, labels):
            ax.plot(x, df_filter[ind], 'o-', label = label, antialiased=True)
            
            y_ticks = np.arange(0, 110, 10)
            x_ticks = np.arange(2010, 2023, 1)
            ax.set_xticks(x_ticks)
            ax.set_yticks(y_ticks)
            ax.set_xlabel('Ano')
            ax.set_ylabel('%')
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig)


def grafico_RedeOrigem_CURSOS(df):
    '''
    Função que Plota o gráfico do curso selecionado

    Parameters
    ----------
    df : dataframe.

    Returns
    -------
    grafico.

    '''
    with st.container():
        
        st.header("Análise GERAL")
    
        st.write("---")
        centros = st.selectbox("Selecione o CENTRO", sorted(df['CENTRO'].unique()))
        df_filter = df.loc[df.CENTRO == centros].copy()
        
        indicadores = ['EVASAO', 'RETENCAO', 'SUCESSO']
        labels = ['Evasão', 'Retenção', 'Sucesso']
        
        fig, ax = plt.subplots(figsize=(7,4))
        x = df_filter['CO_ANO']
        
        for ind, label in zip(indicadores, labels):
            ax.plot(x, df_filter[ind], 'o-', label = label, antialiased=True)
            
            y_ticks = np.arange(0, 110, 10)
            x_ticks = np.arange(2010, 2023, 1)
            ax.set_xticks(x_ticks)
            ax.set_yticks(y_ticks)
            ax.set_xlabel('Ano')
            ax.set_ylabel('%')
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig)

recorte = st.sidebar.radio("RECORTES", ["Por Rede de Origem", "Por Cota","Por Etnia",'Sem recorte'])
# Determinar qual seção exibir
if recorte == "Sem recorte":
    grafico_GERAL()
    
elif recorte == "Por Cota":
    st.write("Conteúdo de COTA aqui...")
