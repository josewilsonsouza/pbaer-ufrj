import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt

def dark_theme():
    dark_style = """
    <style>
    .reportview-container {
        background: #111;
        color: #F8F8FF;
    }
    </style>
    """
    st.markdown(dark_style, unsafe_allow_html=True)

# Chama a função para aplicar o tema escuro
dark_theme()


# Título do aplicativo
st.set_page_config(layout="wide")

st.title('PBAER')
st.sidebar.image('logo_ufrj.png', use_column_width=True)

@st.cache_data
def carregar_dados_CENTROS():
    df = pd.read_csv('Media_EVA_RET_SUC_por_CENTRO.csv',sep=';',encoding='utf-8')
    cols=['CO_ANO','CENTRO','EVASAO','RETENCAO','SUCESSO']
    df = df.loc[:,cols]
    df = df.melt(id_vars=['CO_ANO','CENTRO'], var_name='Taxas', value_name='Percentuais')
    df['Percentuais'] = df.Percentuais/100
    return df

@st.cache_data
def carregar_dados_CURSOS():
    df = pd.read_csv('Eva_Ret_Suc_CURSOS.csv',sep=';',encoding='utf-8')
    cols=['CO_ANO','CO_CURSO','NO_CURSO','CENTRO','Evasao','Retencao','Sucesso']
    df = df.loc[:,cols]
    df = df.melt(id_vars=['CO_ANO','CO_CURSO','CENTRO','NO_CURSO'], var_name='Taxas', value_name='Percentuais')
    df['Percentuais'] = df.Percentuais/100
    return df

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
        codigos = df['CO_CURSO'].unique()
        cursos = [list(df.loc[df.CO_CURSO==codigo].NO_CURSO)[0] for codigo in codigos]
        boxselect = [f'{n} - {c}' for c,n in zip(codigos,cursos)]
        
        box_cursos = st.selectbox("Selecione o CURSO", sorted(boxselect))
        curso_selecionado = int(box_cursos.split(' ')[-1])
        df_filter = df.loc[df.CO_CURSO == curso_selecionado].copy()
        
        grafico = alt.Chart(df_filter).mark_line(point=True).encode(
        x=alt.X('CO_ANO',scale=alt.Scale(domain=[2010, 2023]), 
                axis=alt.Axis(format='d'), title='ANO' ),
        
        y=alt.Y('Percentuais', scale=alt.Scale(domain=[0, 1], nice=10), title=None,
                axis=alt.Axis(format='%')),
        
        color=alt.Color('Taxas',
                        scale=alt.Scale(range=['OrangeRed','orange','green']))
        )+alt.Chart(df_filter).mark_point(opacity=0.3,size=110, filled=True).encode(
            x='CO_ANO',
            y='Percentuais',
            color = 'Taxas')
            
        mostrar_rotulos = st.checkbox("Mostrar Rótulos Cursos")
        if mostrar_rotulos:
            
            texto = alt.Chart(df_filter).mark_text(align='left', baseline='middle', 
                                                   dx=5, color='yellow').encode(
            x='CO_ANO',
            y='Percentuais:Q',
            text=alt.Text('Percentuais:Q', format='.0%')  # Formata os valores como percentuais
            )
             
            grafico = (grafico + texto)
        
        grafico = grafico.properties(width=450, 
                                     height=300).configure_legend(
                                         orient='bottom').interactive()
                
        st.altair_chart(grafico)

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
        df_filter = df.loc[df.CENTRO == centros]
    
        grafico = alt.Chart(df_filter).mark_line(point=True).encode(
        x=alt.X('CO_ANO',scale=alt.Scale(domain=[2010, 2023]), 
                axis=alt.Axis(format='d'), title='ANO' ),
        
        y=alt.Y('Percentuais', scale=alt.Scale(domain=[0, 1], nice=10), title=None,
                axis=alt.Axis(format='%')),
        
        color=alt.Color('Taxas',
                        scale=alt.Scale(range=['OrangeRed','orange','green']))
        )+alt.Chart(df_filter).mark_point(opacity=0.3,size=110, filled=True).encode(
            x='CO_ANO',
            y='Percentuais',
            color = 'Taxas')
            
        mostrar_rotulos = st.checkbox("Mostrar Rótulos")
        if mostrar_rotulos:
            
            texto = alt.Chart(df_filter).mark_text(align='left', baseline='middle', 
                                                   dx=5, color='yellow').encode(
            x='CO_ANO',
            y='Percentuais:Q',
            text=alt.Text('Percentuais:Q', format='.0%')  # Formata os valores como percentuais
            )
             
            grafico = (grafico + texto)
        
        grafico = grafico.properties(width=450, 
                                     height=300).configure_legend(orient='bottom').interactive()
                
        st.altair_chart(grafico)

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
        #if st.checkbox('Mostrar dados CURSOS'):
         #   df_CURSOS
    with fig2:
        grafico_Geral_CENTROS(df_CENTROS)
        #if st.checkbox('Mostrar dados CENTROS'):
         #   df_CENTROS
        
elif recorte == "Por Cota":
    st.write("Conteúdo de COTA aqui...")
