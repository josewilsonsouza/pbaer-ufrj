import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título do aplicativo
st.title('Análise de Dados com Streamlit')

# Carregar os dados do arquivo local
file_path = "Dados_EVA_RET_SUC_Cursos_CCMN.xlsx"
data = pd.read_excel(file_path)
data = data.loc[data.CO_CURSO==14324].copy()

# Exibir os dados
st.write("Visualização dos dados:")
st.write(data)

# Selecionar uma coluna específica para criar o gráfico
column = st.selectbox("Evasao:", data.columns)

# Criar um gráfico simples (contagem de valores)
st.write("Gráfico de Dispersão entre 'Evasao' e 'Ano':")

fig, ax = plt.subplots()
ax.scatter(data['CO_ANO'], data['Evasao'])
ax.set_xlabel('Ano')
ax.set_ylabel('Evasao')
st.pyplot()
st.set_option('deprecation.showPyplotGlobalUse', False)
