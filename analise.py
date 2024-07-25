import pandas as pd
import numpy as np
#Pego os dados necessários
df = pd.read_csv('./DADOS_APP/DADOS_CURSOS.csv')
dados = df.loc[:,['NU_ANO_CENSO','NO_CURSO','CO_CURSO','EVASAO','RETENCAO','SUCESSO']]

# Supondo que 'dados' é seu DataFrame
def medias_taxas_anos(dados): # Passa o DataFrame como argumento
    # Definindo as colunas
    EVASAO = 'EVASAO'
    RETENCAO = 'RETENCAO'
    SUCESSO = 'SUCESSO'
    ANO_CENSO = 'NU_ANO_CENSO'
    
    # Filtrando os anos de interesse
    anos_interesse = range(2017, 2023)
    dados_filtrados = dados[dados[ANO_CENSO].isin(anos_interesse)]
    
    # Inicializando o dicionário para armazenar as médias
    anos = {ano: [0, 0, 0] for ano in anos_interesse}
    
    # Calculando as somas das taxas por ano
    for ano in anos_interesse:
        dados_ano = dados_filtrados[dados_filtrados[ANO_CENSO] == ano]
        anos[ano][0] = dados_ano[EVASAO].sum()
        anos[ano][1] = dados_ano[RETENCAO].sum()
        anos[ano][2] = dados_ano[SUCESSO].sum()
    
    # Dividindo pelo número de entradas para obter as médias
    for ano in anos.keys():
        n = len(dados_filtrados[dados_filtrados[ANO_CENSO] == ano])
        if n > 0:
            anos[ano] = [taxa / n for taxa in anos[ano]]
    
    return anos

def cursos_mais_proximos_media(dados, medias):
    """
    Função que compara os dados dos cursos com as médias calculadas
    e retorna os 5 cursos com os índices mais próximos da média.
    
    Parâmetros:
    dados - DataFrame com os dados dos cursos (Nome, Ano, Evasão, Retenção, Sucesso)
    medias - Dicionário com as médias das taxas por ano
    
    Retorno:
    cursos_proximos - Lista dos códigos dos 5 cursos com índices mais próximos da média
    """
    # Definindo as colunas
    EVASAO = 'EVASAO'
    RETENCAO = 'RETENCAO'
    SUCESSO = 'SUCESSO'
    ANO_CENSO = 'NU_ANO_CENSO'
    CODIGO_CURSO = 'CO_CURSO'

    anos_interesse = range(2017, 2023)

    # Inicializando um dicionário para armazenar as diferenças acumuladas por curso
    diferencas_cursos = {}

    # Filtrando os dados para incluir apenas os anos de interesse
    dados_filtrados = dados[dados[ANO_CENSO].isin(anos_interesse)]

    # Filtrando cursos que estão presentes em todos os anos de interesse
    cursos_validos = dados_filtrados.groupby(CODIGO_CURSO).filter(
        lambda x: x[ANO_CENSO].nunique() == len(anos_interesse)
    )[CODIGO_CURSO].unique()

    for _, row in dados_filtrados.iterrows():
        ano = row[ANO_CENSO]
        if ano not in anos_interesse:
            continue
        codigo_curso = row[CODIGO_CURSO]
        if codigo_curso not in cursos_validos:
            continue
        evasao = row[EVASAO]
        retencao = row[RETENCAO]
        sucesso = row[SUCESSO]

        # Calculando a diferença absoluta entre os índices e as médias
        diff_evasao = abs(evasao - medias[ano][0])
        diff_retencao = abs(retencao - medias[ano][1])
        diff_sucesso = abs(sucesso - medias[ano][2])

        # Somando as diferenças para obter uma métrica acumulada
        diff_total = diff_evasao + diff_retencao + diff_sucesso

        if codigo_curso not in diferencas_cursos:
            diferencas_cursos[codigo_curso] = 0

        diferencas_cursos[codigo_curso] += diff_total

    # Ordenando os cursos pelas menores diferenças acumuladas
    cursos_ordenados = sorted(diferencas_cursos.items(), key=lambda x: x[1])

    # Selecionando os 5 cursos mais próximos da média
    cursos_proximos = [curso for curso, _ in cursos_ordenados[:5]]

    return cursos_proximos

# Exemplo de uso
# df_cursos = pd.DataFrame({ ... })  # DataFrame com os dados dos cursos
# medias = medias_taxas_anos(dados)  # Chamada da função anterior para obter as médias
# curso_proximo = curso_mais_proximo_media(df_cursos, medias)
# print(curso_proximo)

print(cursos_mais_proximos_media(dados,medias_taxas_anos(dados)))