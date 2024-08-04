#1
with st.expander("O que é o PBAER?"):
    st.write("O PBAER é o Programa de Bolsas para estudos sobre evasão, retenção e acompanhamento de egressos de cursos de graduação da Pró-Reitoria de Graduação da UFRJ. Criado em 2022, ele é conduzido por uma equipe composta pelo Prof. Joaquim Fernando Mendes da Silva, coordenador do projeto, e por seis bolsistas, alunos de graduação da UFRJ, selecionados por meio de um edital anual e que realizam pesquisas qualitativas e quantitativas para a identificação e o desenvolvimento de ações para mitigar a evasão e retenção nos cursos de graduação da UFRJ, bem como o acompanhamento de seus egressos.")

#2
with st.expander("Qual a fonte dos dados utilizados?"):
    st.write("Os dados utilizados nas pesquisas quantitativas foram obtidos na base de dados pública do Censo do Ensino Superior, disponível no site do INEP.")

#3
with st.expander("Como são calculadas curvas dos centros e da UFRJ?"):
    st.write("A partir das médias ponderadas dos valores de evasão, retenção e sucesso na graduação dos diferentes cursos que compõem um centro e a UFRJ como um todo.")

#4
with st.expander("Por que os dados referentes aos cursos ABI e seus derivados não aparecem no estudo?"):
    st.write("Os cursos ABI não têm formandos (concluintes) e os cursos derivados deles não possuem ingressantes (pelo SiSU/THE/TCE) e, portanto, não podemos aplicar as fórmulas do PROGRAD a eles. Estamos estudando alternativas para a geração dos dados desses cursos.")

#5
with st.expander("Por que nos gráficos de evasão percebemos uma queda nos valores fora do padrão em 2017?"):
    st.write("Verificamos que há um erro nos dados de alunos matriculados nas tabelas do Censo do Ensino Superior utilizadas, o que provoca essa alteração. Indicamos que esse ponto seja ignorado nas análises.")

#6
with st.expander("Devo analisar os valores ano a ano ou observar a tendência?"):
    st.write("Você pode fazer a análise das duas formas. Entendemos que analisar as tendências das curvas é importante para verificar o comportamento do curso a longo prazo e permite fazer algumas comparações com as curvas dos centros e da UFRJ como um todo. Já os pontos individuais são úteis para o estudo de alterações significativas no perfil em um determinado momento do curso e que devem ser interpretados à luz do processo histórico do curso, da unidade, da universidade e do país.")

#7
with st.expander("Esses estudos são transversais ou longitudinais?"):
    st.write("Os estudos de evasão, retenção e sucesso na graduação são estudos transversais, enquanto os indicadores de trajetória são longitudinais.")

#8
with st.expander("Por que não temos gráficos com informações sobre alunos com outros perfis, e.g., alunos indígenas ou PcD?"):
    st.write("Infelizmente, o número de alunos matriculados e pertencentes a alguns perfis é muito pequeno para permitir uma análise comparativa com outros grupos com maior número de estudantes matriculados.")

#9
with st.expander("Como analisar os gráficos por cotas, etnia, procedência ou sexo?"):
    st.write("Nesses gráficos, avaliamos o percentual de evasão, retenção e sucesso dentro de cada recorte. Por exemplo, um percentual de retenção de 40% na curva referente ao sexo feminino no gráfico de retenção de um curso significa que entre o total de alunas que se declaram desse sexo, 40%% se encontram retidas.")

#10
with st.expander("Por que no gráfico de etnia-total o percentual de evasão de um determinado grupo pode ser inferior ao esperado?"):
    st.write("Na análise desse gráfico, é essencial observar o número de alunos que se declaram pertencentes a uma determinada etnia ou raça. Se esse número for muito inferior ao da etnia/raça de maior frequência, o percentual será menor em função da baixa representatividade dos alunos daquela etnia")