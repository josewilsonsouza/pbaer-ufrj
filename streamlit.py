import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Título do aplicativo
st.set_page_config(layout="wide")

st.title('PBAER')
st.sidebar.image('logo_ufrj.png', use_column_width=True)

@st.cache_data
def carregar_dados_CENTROS():
    tabela = pd.read_csv('Media_EVA_RET_SUC_por_CENTRO.csv',sep=';',encoding='utf-8')
    return tabela
    
@st.cache_data
def carregar_dados_CURSOS():
    tabela = pd.read_csv('Eva_Ret_Suc_CURSOS.csv',sep=';',encoding='utf-8')
    return tabela

## SELECIONA O CURSO
def grafico_Geral_CURSOS(df):
    '''
    Função que Plota o gráfico, SEM RECORTE, do CURSO selecionado

    Parameters
    ----------
    df : dataframe.

    Returns
    -------
    grafico.

    '''
    with st.container():
            
        cursos = st.selectbox("Selecione o CURSO", sorted(df['CO_CURSO'].unique()))
        df_filter = df.loc[df.CO_CURSO == cursos].copy()
        
        indicadores = ['Evasao', 'Retencao', 'Sucesso']
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

## SELECIONA O CENTRO
def grafico_Geral_CENTROS(df):
    '''
    Função que Plota o gráfico, SEM RECORTE do CENTRO selecionado

    Parameters
    ----------
    df : dataframe.

    Returns
    -------
    grafico.

    '''
    with st.container():
            
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

############################################################################

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
        
#############################################################################

recorte = st.sidebar.radio("RECORTES", ['Sem recorte',"Por Rede de Origem", "Por Cota","Por Etnia"])
# Determinar qual seção exibir
df_CENTROS = carregar_dados_CENTROS()
df_CURSOS = carregar_dados_CURSOS()

if recorte == "Sem recorte":
    st.header("Análise GERAL")
    st.write("---")
    
    fig1, fig2 = st.columns(2)
    with fig1:
        grafico_Geral_CURSOS(df_CURSOS)
        if st.checkbox('Mostrar dados CURSOS'):
            df_CURSOS
    with fig2:
        grafico_Geral_CENTROS(df_CENTROS)
        if st.checkbox('Mostrar dados CENTROS'):
            df_CENTROS
    
elif recorte == "Por Cota":
    st.write("Conteúdo de COTA aqui...")
