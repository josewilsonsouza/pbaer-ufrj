import streamlit as st
import pandas as pd
import altair as alt

# Título do aplicativo

st.set_page_config(layout = "wide")
st.title('PBAER')
st.sidebar.image('logo_ufrj.png', use_column_width = True)

global dir
dir = 'https://raw.githubusercontent.com/josewilsonsouza/PBAER_UFRJ/main/'

@st.cache_data
def df_tajetoria():
    df_trajetoria = pd.read_csv(dir+'DADOS_ENSINO_SUPERIOR_UFRJ/Indicadores_Trajetoria.csv')
    return df_trajetoria

@st.cache_data
def df_cursos():
    df_cursos = pd.read_csv(dir+'DADOS_ENSINO_SUPERIOR_UFRJ/CURSOS.csv')
    df_cursos = df_cursos.query('CENTRO != "EAD" ')
    return df_cursos

###########################################################################################

class Recorte:
  GERAL = ['EVASAO','RETENCAO','SUCESSO']
  PROCEDENCIA = ['PROCESCPUBLICA','PROCESCPRIVADA','PROCNAOINFORMADA']
  COTA = ['RVETNICO','RVREDEPUBLICA','RVSOCIAL_RF']
  ETNIA = ['BRANCA','PRETA','PARDA']
  SEXO = ['MASC', 'FEM']

class Rotulos:
  GERAL = ['EVASAO','RETENCAO','SUCESSO']
  PROCEDENCIA = ['PUBLICA','PRIVADA','NAO INFORMADA']
  COTA = ['ETNICO','REDE PUBLICA','SOCIAL']
  ETNIA = ['BRANCA','PRETA','PARDA']
  SEXO = ['MASCULINO', 'FEMININO']

class CentrosRecortes:
  CENTROS = ['CCMN', 'CT', 'CCJE', 'CFCH', 'CCS', 'CLA', 'MACAE', 'CAXIAS', 'UFRJ']
  RECORTES = ['PROCEDENCIA','COTA','ETNIA','SEXO','GERAL']

###########################################################################################

@st.cache_data
def carregar_dados_CENTROS(ref = None):
    
    if ref == 'TOTAL':
        df = pd.read_csv(dir+'DADOS_APP/DADOS_CENTROS_TOTAL.csv')
    else:
        df = pd.read_csv(dir+'DADOS_APP/DADOS_CENTROS.csv')
        
    cols_melt = ['NU_ANO_CENSO','CENTRO', 'QT_ING','QT_MAT','QT_CONC']
    df = df.melt(id_vars = cols_melt, var_name='Taxas', value_name='Percentuais')
    df['Percentuais'] = df.Percentuais/100
    
    return df

@st.cache_data
def carregar_dados_CURSOS(ref = None):
    
    if ref == 'TOTAL':
        df = pd.read_csv(dir+'DADOS_APP/DADOS_CURSOS_REF_TOTAL.csv')
    else:
        df = pd.read_csv(dir+'DADOS_APP/DADOS_CURSOS.csv')
        
    df = df.melt(id_vars=['NU_ANO_CENSO','CO_CURSO','CENTRO','NO_CURSO',
                          'DURACAO','QT_ING','QT_MAT','QT_CONC'], 
                 var_name='Taxas',
                 value_name='Percentuais')
    
    df['Percentuais'] = df.Percentuais/100
    
    return df
 
###########################################################################################

@st.cache_data
def dados_recorte(recorte, curso_ou_centro , ref = None):
    
    if curso_ou_centro in CentrosRecortes.CENTROS:
        
        df = carregar_dados_CENTROS(ref)
        
    else:
        df = carregar_dados_CURSOS(ref)
    
    ROTULOS = Rotulos()
    CLASSES = getattr(ROTULOS, recorte)
    
    if ref == 'TOTAL':
        nome_fim = '_'+ref
    else:
        nome_fim = ''
    
    if recorte == 'GERAL':
        eva_classe, ret_classe, suc_classe = [['EVASAO'],['RETENCAO'],['SUCESSO']]
    else:
        eva_classe = ['EVASAO'+'_'+classe+nome_fim for classe in CLASSES]
        ret_classe = ['RETENCAO'+'_'+classe+nome_fim for classe in CLASSES]
        suc_classe = ['SUCESSO'+'_'+classe+nome_fim for classe in CLASSES]
    
    df_eva_classe = df.query('Taxas in @eva_classe')
    df_ret_classe = df.query('Taxas in @ret_classe')
    df_suc_classe = df.query('Taxas in @suc_classe')
        
    return df_eva_classe, df_ret_classe, df_suc_classe
    
    
########################################################################### 

def grafico_recorte(recorte, curso_ou_centro, taxa, ref = None):
    '''
    Função que Plota o gráfico para um dado RECORTE do CURSO selecionado
    '''
    with st.container():
        
        ROTULOS = Rotulos()
        CLASSES = getattr(ROTULOS, recorte)
        
        df1, df2, df3 = dados_recorte(recorte, curso_ou_centro, ref)
        
        if taxa == 'EVASAO':
            df = df1
        elif taxa == 'RETENCAO':
            df = df2
        elif taxa == 'SUCESSO':
            df = df3
        
        if isinstance(curso_ou_centro, str):
            df = df.loc[df.CENTRO == curso_ou_centro].copy()
            cores = ['cyan', 'Gold','Lime', 'green']
        else:
            df = df.loc[df.CO_CURSO == curso_ou_centro].copy()
            cores = ['OrangeRed', 'orange', 'green', 'blue', 'cyan']
            
        if recorte != 'GERAL':
            df['Taxas'] = df['Taxas'].map({taxa+'_'+classe: f'{classe}' for classe in CLASSES})
        
        
        grafico = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('NU_ANO_CENSO',scale=alt.Scale(domain=[min(df.NU_ANO_CENSO), 2023]), 
                axis=alt.Axis(format='d'), title= 'ANO' ),
        
        y=alt.Y('Percentuais', scale=alt.Scale(domain = [0, 1], nice=10), title=None,
                axis=alt.Axis(format='%')),
        
        color=alt.Color('Taxas', title = 'Legenda', scale=alt.Scale(range=cores))
        )+alt.Chart(df).mark_point(opacity=0.3,size=110, filled=True).encode(
            x='NU_ANO_CENSO',
            y='Percentuais',
            color=alt.Color('Taxas', legend=alt.Legend(title='Legenda')))
        
       
        grafico = grafico.properties(width=450,
                                     height=300,
                                     ).configure_legend(
                                         orient='bottom').interactive()
    return grafico,df
        
#############################################################################

recorte = st.sidebar.radio("RECORTES", ['Recortes',"Indicadore de Trajetória", 'Metodologia de Cálculo'])

if recorte == "Recortes":
    st.header("Análise por Recorte")
    st.write("---")
        
    df_cursos = df_cursos()
    
    
    #st.altair_chart(grafico_recorte('GERAL', 'UFRJ', taxa)[0], use_container_width=True)
    
    box_taxa = ['EVASAO', 'RETENCAO', 'SUCESSO']
    taxa = st.selectbox('SELECIONE A TAXA', box_taxa)
    
    fig1, fig2 = st.columns(2)

    with fig1:
        # CAIXA DE SELEÇÃO DO CURSO E TAXA
        codigos = df_cursos['CO_CURSO'].unique()
        cursos = [list(df_cursos.loc[df_cursos.CO_CURSO==codigo].NO_CURSO)[0] for codigo in codigos]
        boxselect = [f'{n} - {c}' for c,n in zip(codigos,cursos)]
        
        box_cursos = st.selectbox("CURSO", sorted(boxselect))
        curso = int(box_cursos.split(' ')[-1])
        # CAIXA DE SELECAO DO RECORTE
        box_recorte = CentrosRecortes.RECORTES
        recorte = st.selectbox('RECORTE', sorted(box_recorte))
        # GRAFICO
        st.altair_chart(grafico_recorte(recorte, curso, taxa)[0],use_container_width=True)
        
        
        # opção de exibição dos dados
        
        if st.checkbox('Exibir dados:'+' '+box_cursos):
           grafico_recorte(recorte, curso, taxa)[1]
           
    with fig2:
        
        
        centro = st.selectbox("CENTRO", sorted(CentrosRecortes.CENTROS))
        recorte = st.selectbox('RECORTE CENTROS', sorted(box_recorte))
        
        if recorte == 'GERAL':
            outras = [t for t in box_taxa if t != taxa]
            
            st.altair_chart(grafico_recorte(recorte, centro, taxa)[0],use_container_width=True)

            if st.checkbox('Ver UFRJ'):
                
                st.altair_chart(grafico_recorte(recorte, 'UFRJ', taxa)[0],use_container_width=True)
                
        else:
            
            st.altair_chart(grafico_recorte(recorte, centro, taxa)[0],use_container_width=True)
        

        if st.checkbox('Exibir dados:'+' '+centro):
            grafico_recorte(recorte, centro, taxa)[1]
    
elif recorte == "Metodologia de Cálculo":
    st.title("Metodolgia de Cálculo")
    st.write("---")
       
    import Metodologia_de_calculo
    
    
    
    
    
    
    
