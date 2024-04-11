import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título do aplicativo
st.title('PBAER')

arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)


with st.container():
    st.subheader("Teste com o Streamlit")
    st.title("Dashboard do Projeto ")

@st.cache_data
def carregar_dados():
    tabela = pd.read_csv('Media_EVA_RET_SUC_por_CENTRO.csv', sep=';', encoding='utf-8')
    return tabela

with st.container():
    st.write("---")
    centros = st.selectbox("Selecione o CENTRO", ['CCMN','CT'])
    dados = carregar_dados() 
    dados = dados.loc[dados.CENTRO == centros].copy()
    st.scatter_chart(dados, x="CO_ANO", y="EVASAO")
