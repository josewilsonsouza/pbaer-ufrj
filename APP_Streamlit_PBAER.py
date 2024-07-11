import streamlit as st
import pandas as pd
import altair as alt
from altair_data_server import data_server

# Título do aplicativo
dir = 'https://raw.githubusercontent.com/josewilsonsouza/PBAER_UFRJ/main/'

st.set_page_config(page_title="PBAER UFRJ", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="auto")

st.markdown(
    f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <img src="{dir}DADOS_ENSINO_SUPERIOR_UFRJ/logo_ufrj.png" width="200">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<h2 style='text-align: center;'>PBAER - UFRJ </h2>", unsafe_allow_html=True)

@st.cache_data
def load_data_centros():
    df =  pd.read_csv('DADOS_APP/DADOS_CENTROS.csv')
    return df

@st.cache_data
def load_data_cursos():
    df =  pd.read_csv('DADOS_APP/DADOS_CURSOS.csv')
    return df

@st.cache_data
def load_cursos():
    df_cursos = pd.read_csv('DADOS_ENSINO_SUPERIOR_UFRJ/CURSOS.csv')
    df_cursos = df_cursos.query('CENTRO != "EAD" ')
    return df_cursos

@st.cache_data
def df_trajetoria():
    df_traj = pd.read_csv('DADOS_ENSINO_SUPERIOR_UFRJ/Indicadores_Trajetoria.csv')
    df_centros = load_cursos().loc[:,['CO_CURSO','CENTRO']]
    df_traj = df_traj.merge(df_centros, on = ['CO_CURSO'], how = 'left')
    df_traj = df_traj.dropna(subset=['CENTRO'])
    
    df_traj['ANO_INGRESSO'] = 'Turma de ' +  df_traj['ANO_INGRESSO'].astype(str)
    
    return df_traj

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
  ETNIA_TOTAL = ETNIA

class CentrosRecortes:
  CENTROS = ['CCMN', 'CT', 'CCJE', 'CFCH', 'CCS', 'CLA', 'MACAE', 'CAXIAS', 'UFRJ']
  RECORTES = ['PROCEDENCIA','COTA','ETNIA','SEXO','GERAL']

###########################################################################################

@st.cache_data
def carregar_dados_CENTROS(ref = None):
    
    if ref == 'TOTAL':
        df = pd.read_csv('DADOS_APP/DADOS_CENTROS_TOTAL.csv')
    else:
        df = load_data_centros()
        
    cols_melt = ['NU_ANO_CENSO','CENTRO', 'QT_ING','QT_MAT','QT_CONC']
    df = df.melt(id_vars = cols_melt, var_name='Taxas', value_name='Percentuais')
    df['Percentuais'] = df.Percentuais/100
    
    return df

@st.cache_data
def carregar_dados_CURSOS(ref = None):
    
    if ref == 'TOTAL':
        df = pd.read_csv('DADOS_APP/DADOS_CURSOS_REF_TOTAL.csv')
    else:
        df = load_data_cursos()
    
    df = df.query('CO_CURSO != 116844 or NU_ANO_CENSO != 2012')#dado ruim do bcmt
        
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
            cores = ['cyan', 'Gold','Lime','coral']
        else:
            df = df.loc[df.CO_CURSO == curso_ou_centro].copy()
            cores = ['OrangeRed', 'orange', 'green', 'blue', 'cyan']
            
        if ref == 'TOTAL':
            nome_fim = '_'+ref
        else:
            nome_fim = ''
            
        if recorte != 'GERAL':
            df['Taxas'] = df['Taxas'].map({taxa+'_'+classe+nome_fim: f'{classe}' for classe in CLASSES})
        
        
        grafico = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('NU_ANO_CENSO',scale=alt.Scale(domain=[min(df.NU_ANO_CENSO), 2023]), 
                axis=alt.Axis(format='d'), title= 'ANO' ),
        
        y=alt.Y('Percentuais', scale=alt.Scale(domain = [0, 1], nice=10), title=None,
                axis=alt.Axis(format='%')),
        
        color=alt.Color('Taxas', title = 'Legenda', scale=alt.Scale(range=cores))
        )+alt.Chart(df).mark_point(opacity=0.3,size=110, filled=True).encode(
            x='NU_ANO_CENSO',
            y='Percentuais',
            color=alt.Color('Taxas'))
       
        grafico = grafico.properties(width=450,height=300).configure_legend(orient='bottom').interactive()
        
    return grafico,df
        
#############################################################################

def grafico_TRAJETORIA(curso_ou_centro, indicador):
    
    df = df_trajetoria()
    
    if isinstance(curso_ou_centro, str):
        if curso_ou_centro == 'UFRJ':
            dados = df
            
        else:
            dados = df.loc[df.CENTRO == curso_ou_centro].copy()
        valor_Y = f'average({indicador})'
    else:
        dados = df.loc[df.CO_CURSO == curso_ou_centro].copy()
        valor_Y = indicador
    
    grafico = alt.Chart(dados).mark_line(point=True).encode(
    x = alt.X('ANO_REFERENCIA', axis = alt.Axis(format='d'), title = 'ANO'),
    y = alt.Y(valor_Y,scale=alt.Scale(domain=[0,100], nice = 10), title = indicador),
    color = alt.Color('ANO_INGRESSO', title = 'TURMA')
    )
    
    return grafico

#############################################################################

box_taxa = ['EVASAO', 'RETENCAO', 'SUCESSO']

dfcentros = load_data_centros()
dfcursos = load_data_cursos()
dfcursos = dfcursos.query('CO_CURSO != 116844 or NU_ANO_CENSO != 2012') #dado ruim do bcmt

for t in box_taxa:
    dfcursos[t] = dfcursos[t]/100
    dfcentros[t] = dfcentros[t]/100
    
txs, inds, met, faq = st.tabs(['Evasão-Rentenção-Sucesso',"Indicadores de Trajetória", 'Metodologia de Cálculo','FAQ'])

with txs:

    df_cursos = load_cursos()
    taxa = st.radio('SELECIONE A TAXA', box_taxa)
        
    fig1, fig2 = st.columns(2)
    
    with fig1:
        
        col1, col2 = st.columns([1,3])
        
        with col1:
                    
            select_CENTRO = st.selectbox("CENTRO", sorted(CentrosRecortes.CENTROS),8, key = 0)
            codigos = df_cursos.query(f'CENTRO == "{select_CENTRO}"')['CO_CURSO'].unique()
            
            if select_CENTRO == 'UFRJ':
                codigos = df_cursos['CO_CURSO'].unique()
            
            cursos = [list(df_cursos.loc[df_cursos.CO_CURSO == codigo].NO_CURSO)[0] for codigo in codigos]
            
        with col2:
            
            boxselect = [f'{n} - {c}' for c, n in zip(codigos, cursos)]
            box_cursos = st.selectbox("CURSO", sorted(boxselect), key=2)    
            curso = int(box_cursos.split(' ')[-1])
    
        # CAIXA DE SELECAO DO RECORTE
        box_recorte = CentrosRecortes.RECORTES
        recorte_curso = st.selectbox('RECORTE', sorted(box_recorte))
        
        # GRAFICO DO RECORTE
        if recorte_curso == 'ETNIA_TOTAL':
            st.altair_chart(grafico_recorte(recorte_curso, curso, taxa,ref='TOTAL')[0], use_container_width=True)
        else:
            st.altair_chart(grafico_recorte(recorte_curso, curso, taxa)[0], use_container_width=True)

    with fig2:
        centro = st.selectbox("CENTROS", sorted(CentrosRecortes.CENTROS),8)
      
        recorte = st.selectbox('RECORTE PARA OS CENTROS', sorted(box_recorte))

        if recorte == 'ETNIA_TOTAL':
            st.altair_chart(grafico_recorte(recorte, centro, taxa,'TOTAL')[0], use_container_width=True)
        else:
            st.altair_chart(grafico_recorte(recorte, centro, taxa)[0], use_container_width=True)
            

    # gráfico de todos os centros:
    st.write('')
    st.header(f'{taxa}', divider='gray')
    
    CENTROS = st.multiselect("CENTROS", sorted(CentrosRecortes.CENTROS), centro)
    dfCENTRO = dfcentros.query('CENTRO in @CENTROS').copy()
        
    txt_title = 'MEDIA DE <span style="color: OrangeRed;">'+taxa+'</span> POR CENTRO'
    
    centers = alt.Chart(dfCENTRO).mark_line(point=True).encode(
        x=alt.X('NU_ANO_CENSO', scale=alt.Scale(domain=[2010, 2023]),
                axis=alt.Axis(format='d'), title='ANO'),
        y=alt.Y(taxa, scale=alt.Scale(domain=[0, 1], nice=10),
                axis=alt.Axis(format='%'), title = taxa),
        color='CENTRO'
    )+alt.Chart(dfCENTRO).mark_point(opacity=0.8).encode(
        x='NU_ANO_CENSO',
        y=taxa,
        color='CENTRO'
    ).properties(width=450, height=300).interactive()
                 
    st.markdown(f"<h3 style='text-align: center;'>{txt_title}</h3>", unsafe_allow_html=True)
    st.altair_chart(centers, use_container_width=True)

    # grafico de media anual

    chart = alt.Chart(dfcursos).mark_bar(color='#2962FF').encode(
        x=alt.X('NU_ANO_CENSO', axis=alt.Axis(format='d'),  title='ANO'),
        y=alt.Y(f'average({taxa})', axis=alt.Axis(format='%'),
                scale=alt.Scale(domain=[0, 1], nice=10), title=taxa)
        ).interactive()

    rotulo = chart.mark_text(
        align='center',
        baseline='middle',
        dy=-10,  # Deslocamento vertical
        color='Orange'
    ).encode(
        text=alt.Text(f'average({taxa})', format='.2%')
    )
        
    title = 'MEDIA ANUAL DE <span style="color: OrangeRed;">'+taxa+'</span>'

    g = (chart + rotulo).properties()
    
    st.markdown(f"<h3 style='text-align: center;'>{title}</h3>", unsafe_allow_html=True)
    st.altair_chart(g, use_container_width=True)

with inds:

    desc = ['TAP - Taxa de Permanência', 'TCA - Taxa de Conclusão Acumulada',
            'TCAN - Taxa de Conclusão Anual', 'TDA - Taxa de Desistência Acumulada',
            'TADA - Taxa de Desistência Anual']

    dftrajetoria = df_trajetoria()
    dftrajetoria['ANO_INGRESSO'] = dftrajetoria['ANO_INGRESSO'].str.replace('Turma', 'Turmas')

    options = st.selectbox('Escolha um indicador', desc)
    option = options.split(' ')[0]
    name_ind = options.split('-')[1]

    fig1, fig2 = st.columns(2)

    with fig1:
        # CAIXA DE SELEÇÃO DO CURSO

        codigos = dftrajetoria['CO_CURSO'].unique()
        cursos = [list(dftrajetoria.loc[dftrajetoria.CO_CURSO == codigo].NO_CURSO)[0] for codigo in codigos]
        boxselect = [f'{n} - {c}' for c, n in zip(codigos, cursos)]

        box_cursos = st.selectbox("CURSO", sorted(boxselect))
        curso = int(box_cursos.split(' ')[-1])

        # GRAFICO Trajetoria
        st.altair_chart(grafico_TRAJETORIA(curso, option),
                        use_container_width=True)

    with fig2:

        centro = st.selectbox("CENTRO", sorted(CentrosRecortes.CENTROS))

        st.altair_chart(grafico_TRAJETORIA(centro, option),
                        use_container_width=True)

    # gráfico de todos os centros:
    
    st.write('')
    st.header(f'{option} - {name_ind} por CENTRO', divider='gray')
    
    CENTROS = st.multiselect("CENTROS", sorted(CentrosRecortes.CENTROS), centro,key=1)
    dftrajetoriaCENTRO = dftrajetoria.query('CENTRO in @CENTROS').copy()

    grafico_centros = alt.Chart(dftrajetoriaCENTRO).mark_line(point=True).encode(
        x=alt.X('ANO_INGRESSO', title='TURMAS'),
        y=alt.Y(f'average({option})', scale=alt.Scale(
            domain=[0, 100], nice=10), title='MEDIA '+option),
        color='CENTRO'
    ).interactive().properties(
        title=alt.TitleParams(
            text='MEDIA '+option+' POR CENTRO',
            align='center',
            anchor='middle'
        )
    )
        
    st.altair_chart(grafico_centros, use_container_width=True)
    
    st.write('')
    st.header(f'{option} - {name_ind} por TURMAS', divider='gray')
    
    turmas = dftrajetoria.ANO_INGRESSO.unique()
    select_TURMAS = st.multiselect('TURMAS',sorted(turmas),turmas)
    df_select = dftrajetoria.query("ANO_INGRESSO in @select_TURMAS").copy()

    media_anual = alt.Chart(df_select).mark_line(color='OrangeRed', point=True).encode(
        x=alt.X('ANO_REFERENCIA', axis=alt.Axis(format='d'), title='ANO'),
        y=alt.Y(f'average({option})', scale=alt.Scale(
            domain=[0, 100], nice=10), title='MEDIA '+option),
        color=alt.Color('ANO_INGRESSO', title='TURMAS')
    ).interactive().properties(
        title=alt.TitleParams(
            text='MEDIA ANUAL '+option,
            align='center',
            anchor='middle'
        )
    )

    st.altair_chart(media_anual, use_container_width=True)
    
with met:
    st.title("Metodolgia de Cálculo")
    st.write("---")
       
    metodologia = 'Metodologia.py'
    # Ler o conteúdo do arquivo Metodologia.py
    with open(metodologia, 'r', encoding='utf-8') as file:
        metodologia = file.read()
    # Executar o conteúdo do arquivo Metodologia.py
    exec(metodologia)

with faq:
    st.title ("FAQ")
    st.write("---")

    perguntas = "FAQ.py"
    #Ler o conteúdo do arquivo FAQ.py
    with open(perguntas,'r',encoding='utf-8') as file:
        perguntas = file.read()
    exec(perguntas)