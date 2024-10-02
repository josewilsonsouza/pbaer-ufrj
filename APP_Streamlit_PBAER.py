import streamlit as st
import pandas as pd
import altair as alt
from altair_data_server import data_server
#------------------------------------------------------------------------------------------------------#
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

#------------------------------------------------------------------------------------------------------#

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
    
    df_traj['ANO_INGRESSO'] = 'Turmas de ' +  df_traj['ANO_INGRESSO'].astype(str)
    
    return df_traj

#######################################################################################################

class Recorte:
  GERAL = ['EVASAO','RETENCAO','SUCESSO']
  PROCEDENCIA = ['PROCESCPUBLICA','PROCESCPRIVADA','PROCNAOINFORMADA']
  COTA = ['RVETNICO','RVREDEPUBLICA','RVSOCIAL_RF']
  ETNIA = ['BRANCA','PRETA','PARDA']
  SEXO = ['MASC', 'FEM']
  ETNIA_TOTAL = ETNIA

class Rotulos:
  GERAL = ['EVASAO','RETENCAO','SUCESSO']
  PROCEDENCIA = ['PUBLICA','PRIVADA','NAO INFORMADA']
  COTA = ['ETNICO','REDE PUBLICA','SOCIAL']
  ETNIA = ['BRANCA','PRETA','PARDA']
  SEXO = ['MASCULINO', 'FEMININO']
  ETNIA_TOTAL = ETNIA

class CentrosRecortes:
  CENTROS = ['CCMN', 'CT', 'CCJE', 'CFCH', 'CCS', 'CLA', 'MACAE', 'CAXIAS', 'UFRJ']
  RECORTES = ['PROCEDENCIA','COTA','ETNIA','SEXO','GERAL','ETNIA_TOTAL']

class Coningmat:
    MAT = 'MATRICULADOS'
    ING = 'INGRESSANTES'
    CONC = 'CONCLUINTES'

#######################################################################################################

@st.cache_data
def carregar_dados_CENTROS(ref = None):
    
    if ref == 'TOTAL':
        df = pd.read_csv('DADOS_APP/DADOS_CENTROS_REF_TOTAL.csv')
    else:
        df = load_data_centros()
        
    cols_melt = ['NU_ANO_CENSO','CENTRO', 'QT_ING','QT_MAT','QT_CONC']
    df = df.melt(id_vars = cols_melt, var_name='Taxas', value_name='Percentuais')
    df['Percentuais'] = df.Percentuais/100
    
    return df
#------------------------------------------------------------------------------------------------------#

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

 #------------------------------------------------------------------------------------------------------#

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
#------------------------------------------------------------------------------------------------------#

@st.cache_data
def load_coningmat(var='MATRICULADOS'):
    data = pd.read_csv(f'DADOS_APP/{var}.csv',sep=',')
    return data
#------------------------------------------------------------------------------------------------------#

def data_con_ing_mat(curso_ou_centro, recorte, var = 'MATRICULADOS'):

    if recorte != 'GERAL':

        RECORTE, ROTULOS = Recorte(), Rotulos()
        VARS = getattr(RECORTE, recorte)
        NAMES = getattr(ROTULOS, recorte)

        data = load_coningmat(var)

        if curso_ou_centro == 'UFRJ':
            data['CENTRO'] = 'UFRJ'

        data = data.query('CENTRO == @curso_ou_centro or CO_CURSO == @curso_ou_centro').reset_index(drop=True)
        data = data.rename(columns={f'{var}_{new_name}':old for new_name,old in zip(VARS, NAMES)})

        no_curso =  data.loc[1, 'NO_CURSO']
        cols = ['NU_ANO_CENSO', var]

        data = data[cols+NAMES]
        data = data.groupby(by=['NU_ANO_CENSO'], as_index = False).sum(numeric_only=True)

        for classe in NAMES:
            data.loc[:,classe] = data.loc[:,classe]/data.loc[:, var]
        data = data.melt(id_vars=['NU_ANO_CENSO', var], var_name=recorte, value_name=f'PERC_{var}')

        if isinstance(curso_ou_centro, str):
            data = data.assign(CENTRO = curso_ou_centro)
        else:
            data = data.assign(CO_CURSO = curso_ou_centro, NO_CURSO = no_curso)

    else:
        cols = ['NU_ANO_CENSO','CO_CURSO','NO_CURSO','CENTRO']
        M,I,C = ['MATRICULADOS','INGRESSANTES', 'CONCLUINTES']

        df1 = load_coningmat(M).loc[:,cols+[M]]
        df2 = load_coningmat(I).loc[:,cols+[I]]
        df3 = load_coningmat(C).loc[:,cols+[C]]
        
        dfs = [df1, df2, df3]
        if curso_ou_centro == 'UFRJ':
              for df in dfs:
                  df['CENTRO'] = 'UFRJ'

        data = pd.DataFrame()

        for df in dfs:

            df = df.query('CENTRO == @curso_ou_centro or CO_CURSO == @curso_ou_centro').reset_index(drop=True)
            no_curso =  df.loc[1, 'NO_CURSO']
            df = df.groupby(by=['NU_ANO_CENSO'], as_index = False).sum(numeric_only=True)
            df = df.melt(id_vars = ['NU_ANO_CENSO'], value_vars = df.columns.to_list()[-1], var_name = 'ALUNOS', value_name = 'TOTAL')

            if isinstance(curso_ou_centro, str):
                df = df.assign(CENTRO = curso_ou_centro)
            else:
                df = df.assign(CO_CURSO = curso_ou_centro, NO_CURSO = no_curso)
            data = pd.concat([data, df])

    return data
    
####################################################################################################### 

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
        else:
            df = df.loc[df.CO_CURSO == curso_ou_centro].copy()
        
        #cores = ['OrangeRed', 'orange', 'green', 'blue', 'cyan']
            
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
        
        color=alt.Color('Taxas', title = 'Legenda')
        )+alt.Chart(df).mark_point(opacity=0.3,size=110, filled=True).encode(
            x='NU_ANO_CENSO',
            y='Percentuais',
            color=alt.Color('Taxas'))
       
        grafico = grafico.properties(width=450,height=400).configure_legend(orient='bottom').interactive()

    return grafico,df
        
#------------------------------------------------------------------------------------------------------#

def grafico_TRAJETORIA(curso_ou_centro, indicador):
    
    df = df_trajetoria()
    
    if isinstance(curso_ou_centro, str):
        if curso_ou_centro == 'UFRJ':
            dados = df
            dados['CENTRO'] = 'UFRJ'
            
        else:
            dados = df.loc[df.CENTRO == curso_ou_centro].copy()
        valor_Y = f'average({indicador})'

    else:
        dados = df.loc[df.CO_CURSO == curso_ou_centro].copy()
        valor_Y = indicador
    
    grafico = alt.Chart(dados).mark_line(point=True).encode(
    x = alt.X('ANO_REFERENCIA', axis = alt.Axis(format='d'), title = 'ANO'),
    y = alt.Y(valor_Y,scale=alt.Scale(domain=[0,100], nice = 10), title = indicador),
    color = alt.Color('ANO_INGRESSO', title = 'TURMA'),
    tooltip = ['ANO_REFERENCIA','ANO_INGRESSO','CENTRO']
    ).interactive()
    
    return grafico

#------------------------------------------------------------------------------------------------------#

def grafico_coningmat_recorte(curso_ou_centro, recorte, var):
  '''
  Função que plota o gráfico de percentual/total de ingressantes, concluintes e matriculados por recorte.
  '''

  df = data_con_ing_mat(curso_ou_centro, recorte, var)

  if recorte == 'GERAL':
    name_y = 'TOTAL'
    legend_y = name_y
    name_color = 'ALUNOS'
    format_y = 'd'
  else:
    name_y = f'PERC_{var}'
    legend_y = f'% {var}'
    name_color = recorte
    format_y = '%'

  chart_var = alt.Chart(df).mark_bar().encode(
      x=alt.X('NU_ANO_CENSO:N', title='ANO'),
      y=alt.Y(f'{name_y}:Q', axis=alt.Axis(format=format_y), title = legend_y),
      color=f'{name_color}:N',
      tooltip=[f'{name_y}:Q', f'{name_color}:N', 'NU_ANO_CENSO:N']
      ).configure_legend(orient='bottom').interactive()

  return chart_var

#------------------------------------------------------------------------------------------------------#

def grafico_coningmat_CENTROS(var='MATRICULADOS'):
    '''
    Função que plot o gráfico de totais de matriculados, ingressantes ou concluintes por centro.
    '''
    dvar = load_coningmat(var)
    cols = ['NU_ANO_CENSO','CO_CURSO','NO_CURSO','CENTRO']
    dvar = dvar.loc[:,cols+[var]]
    dvar = dvar.groupby(by=['NU_ANO_CENSO', 'CENTRO'], as_index = False).sum(numeric_only=True)

    chart_var = alt.Chart(dvar).mark_bar(cornerRadius=3).encode(
        x=alt.X('NU_ANO_CENSO:N', axis = alt.Axis(format='d'), title='ANO'),
        y=f'{var}:Q',
        color='CENTRO:N',
        tooltip=['CENTRO', var, 'NU_ANO_CENSO:N']
        )

    return chart_var

#######################################################################################################
#######################################################################################################

box_taxa = ['EVASAO', 'RETENCAO', 'SUCESSO']

dfcentros = load_data_centros()
dfcursos = load_data_cursos()
dfcursos = dfcursos.query('CO_CURSO != 116844 or NU_ANO_CENSO != 2012') #dado ruim do bcmt

for t in box_taxa:
    dfcursos[t] = dfcursos[t]/100
    dfcentros[t] = dfcentros[t]/100

#------------------------------------------------------------------------------------------------------#

txs, inds, met, faq = st.tabs(['Evasão-Rentenção-Sucesso',"Indicadores de Trajetória", 'Metodologia de Cálculo','FAQ'])

with txs:

    df_cursos = load_cursos()
    taxa = st.radio('SELECIONE A TAXA', box_taxa, horizontal=True)

    
    # CAIXA DE SELECAO DO RECORTE
    box_recorte = CentrosRecortes.RECORTES
    centro = st.selectbox("CENTROS", sorted(CentrosRecortes.CENTROS),8)
    recorte_centros = st.selectbox('RECORTE PARA OS CENTROS', sorted(box_recorte), key='rec_centro_visivel')

    if recorte_centros == 'ETNIA_TOTAL':
        st.altair_chart(grafico_recorte(recorte_centros, centro, taxa,'TOTAL')[0], use_container_width=True)
    else:
        st.altair_chart(grafico_recorte(recorte_centros, centro, taxa)[0], use_container_width=True)

    desativa_rec_centro = recorte_centros == 'GERAL'

    if recorte_centros == 'GERAL':
        desativa_sel_centro = True

    totais = ['MATRICULADOS','INGRESSANTES','CONCLUINTES']

    coningmat_centro = st.selectbox('Total de alunos do CENTRO selecionado :point_down:', totais, key = 'alunos_centros',
        disabled = desativa_rec_centro)

    st.markdown(f"<h4 style='text-align: center;'>{centro} </h4>", unsafe_allow_html=True)
    st.altair_chart(grafico_coningmat_recorte(centro, recorte_centros, coningmat_centro), use_container_width=True)

#------------------------------------------------------------------------------------------------------#

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
    ).properties(width=450, height=400).interactive()
                 
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
        
    #title = 'MEDIA ANUAL DE <span style="color: OrangeRed;">'+taxa+'</span> DA UFRJ'
    st.header('TOTAL DE ALUNOS POR CENTRO', divider='gray')
    #g = (chart + rotulo).properties()
    
    #st.markdown(f"<h3 style='text-align: center;'>{title}</h3>", unsafe_allow_html=True)
    #st.altair_chart(g, use_container_width=True)

    coningmat = st.selectbox('Selecione',['MATRICULADOS','INGRESSANTES','CONCLUINTES'])

    st.altair_chart(grafico_coningmat_CENTROS(coningmat), use_container_width=True)

#------------------------------------------------------------------------------------------------------#

with inds:

    desc = ['TAP - Taxa de Permanência', 'TCA - Taxa de Conclusão Acumulada',
            'TCAN - Taxa de Conclusão Anual', 'TDA - Taxa de Desistência Acumulada',
            'TADA - Taxa de Desistência Anual']

    dftrajetoria = df_trajetoria()
    options = st.selectbox('Escolha um indicador', desc)
    option = options.split(' ')[0]
    name_ind = options.split('-')[1]

    centro = st.selectbox("CENTRO", sorted(CentrosRecortes.CENTROS))

    st.altair_chart(grafico_TRAJETORIA(centro, option),
                    use_container_width=True)

# gráfico de todos os centros:
#------------------------------------------------------------------------------------------------------#

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
            text='MEDIA ANUAL '+option+' DA UFRJ',
            align='center',
            anchor='middle'
        )
    )

    st.altair_chart(media_anual, use_container_width=True)

#------------------------------------------------------------------------------------------------------#

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
