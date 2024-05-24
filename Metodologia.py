## Metodologia do Cálculo Evasão, Retenção e Sucesso

## Codificação do texto Latex

import streamlit as st

# Explicação da fórmula
st.markdown(r'''
### Fórmula para o cálculo da Evasão:
$$ Ev_p = \left (1 - \dfrac{M_p - I_p}{M_{p-1} - C_{p-1}} \right)\times 100 $$
- $p$ - Período (para nós, ano)
- $M$ - Número de matriculados
- $I$ - Número de ingressantes
- $C$ - Número de concluintes
''')

st.markdown(r'''
### Fórmula para o cálculo da Retenção:

$$ IRet_a = \dfrac{I_i - C_{a,i} - EV_i}{I_i - EV_i} \times 100 $$

ou, alternativamente,

$$ IRet_a = \left(1 - \dfrac{C_{a,i}}{I_i - EV_i} \right) \times 100 $$

onde:

- $a$ - Ano base da consulta;
- $d$ - Duração do curso;
- $i = a - d$;
- $I_i$ - Número de ingressantes no ano $i$;
- $C_{a,i}$ - Número de concluintes no ano base;
- $EV_i$ - Número de evadidos no ano $i$.

##### Cálculo do número de evadidos ($EV_i$):
Para o número de evadidos ($EV_i$) no ano $i = a-d$, estimamos fazendo

$$ EV_i = Ev_{i+1} \cdot I_i $$

onde $Ev_{i+1}$ é a taxa de evasão (em %) do ano $i+1$ e $I_i$ é o número de ingressantes do ano $i$. Com isso, obtemos

$$ IRet_a = \left(1 - \dfrac{C_{a,i}}{I_i \left(1 - \frac{Ev_{i+1}}{100}\right)} \right) \times 100. $$
''', unsafe_allow_html=True)

st.markdown(r'''
### Fórmula para o cálculo do Índice de Sucesso:

$$ ISGr_p = \dfrac{C_{p}}{Ing_{p-d}} \times 100 $$

Onde:

- $C_{p}$: Total de alunos que concluíram o curso $i$ no ano $p$;
- $Ing_{p-d}$: Quantidade de alunos que ingressaram no curso $i$ no ano $p-d$. $d$ é a duração do curso em anos.
    
''', unsafe_allow_html=True)

st.write('---')
st.title('Outras Análises')

st.markdown(r"""
## Evasão
Pelo FORPLAD:
""")

st.latex(r'e_p = 1-\dfrac{M_p-I_p}{M_{p-1} - C_{p-1}}')

st.markdown("""Isso vem do fato de que""")

st.latex(r'M_p = M_{p-1}-C_{p-1}+I_p-E_p')

# Texto descritivo
st.markdown(r"""
Onde $E_p$ é o número de evadidos no período $p$. Porém, pelos dados do INEP, são considerados apenas os alunos com matrículas iniciadas entre 1 de janeiro a 1 de julho do ano de referência. No entanto, pode ter havido ingressantes no período seguinte (.2). Assim
""")

# Equações em LaTeX
st.latex(r"M_a = M_{a-1}-C_{a-1}+I_{a}^1+I_{a}^2-E_a")
st.latex(r"I_{a}^2 - E_a = M_a - M_{a-1} + C_{a-1} - I_{a}^1")

st.markdown(r"""
Sabemos que:
""")
st.latex(r"\{ C_a \} \subseteq \{ M_a \}")
st.latex(r"\{ I_a \} \subseteq \{ M_a \}")
st.markdown(r"""
Onde
""")
st.latex(r"I_a = I_{a}^1 + I_{a}^2")
st.markdown(r"""
Suponha que conheçamos $I_a$. Nesse caso, temos
""")
st.latex(r"E_a = M_{a-1}-C_{a-1}+I_a - M_a")
st.markdown(r"""
Dividindo pelo total de alunos no ano $a$ que não são ingressantes: $M_{a-1}-C_{a-1}$
""")
st.latex(r"\dfrac{E_a}{ M_{a-1}-C_{a-1} } = 1-\dfrac{M_a-I_a}{M_{a-1}-C_{a-1} } = e_a")

st.markdown(r"""
O caso mais real, na verdade, deve considerar que matriculados podem desistir do curso, chamando os desistentes no ano $a$, que não são ingressantes, por $d_a$, temos
""")
st.latex(r"M_a = M_{a-1}-C_{a-1}+I_a - E_a - d_a \Rightarrow E_a = M_{a-1}-C_{a-1}+I_a - M_a - d_a")
st.markdown(r"""
Logo, deveríamos ter
""")
st.latex(r"e_a = 1-\dfrac{M_a-I_a}{M_{a-1}-C_{a-1}} - \dfrac{d_a}{M_{a-1} - C_{a-1} }")

st.markdown(r"""
Acontece que estamos supondo
""")
st.latex(r"\dfrac{d_a}{M_{a-1}-C_{a-1} }\approx 0")

st.markdown(r"""
Pensemos agora no caso das etnias. Vamos verificar o número de evadidos para certa etnia $j$. Nesse caso
""")
st.latex(r"E_{a}^{(j)} = M_{a-1}^{(j)} - C_{a-1}^{(j)} +I_a^{(j)} - M_a^{(j)}")
st.markdown(r"""
A proporção de evadidos da etnia $j$ em relação ao total de evadidos é dado então por
""")
st.latex(r"\dfrac{E_a^{(j)} }{E_a} = \dfrac{M_{a-1}^{(j)} - C_{a-1}^{(j)} +I_a^{(j)} - M_a^{(j)}}{M_{a-1}-C_{a-1}+I_a - M_a}")

st.latex(r"\dfrac{E_a^{(j)} }{E_a} = \dfrac{\dfrac{M_{a-1}^{(j)} - C_{a-1}^{(j)} +I_a^{(j)} - M_a^{(j)}}{M_{a-1}-C_{a-1} }} {1-\dfrac{M_a-I_a}{M_{a-1}-C_{a-1} } } = \dfrac{1}{e_a}\dfrac{M_{a-1}^{(j)} - C_{a-1}^{(j)} +I_a^{(j)} - M_a^{(j)}}{M_{a-1}-C_{a-1} }")

st.markdown(r"""
Chamando a razão de evadidos da etnia $j$ em relação ao total de alunos não ingressantes por $e_a^{(j)} $, então
""")
st.latex(r"e_a^{(j)} = \dfrac{M_{a-1}^{(j)} - C_{a-1}^{(j)} +I_a^{(j)} - M_a^{(j)}}{M_{a-1}-C_{a-1} }")
st.markdown(r"""
Com isso,
""")
st.latex(r"\dfrac{E_a^{(j)}}{E_a} = \dfrac{e_a^{(j)} }{e_a}")

st.markdown(r"""
## Retenção
Pelo FORPLAD:
""")
st.latex(r"r_a = \dfrac{I_{a-d} -C_{a,a-d}-E_{a-d} }{I_{a-d} -E_{a-d} }")
st.markdown(r"ou,")
st.latex(r"r_a = 1-\dfrac{C_{a, a-d }}{I_{a-d} -E_{a-d} }")
st.markdown(r"""
Onde $d$ é a duração do curso. $C_{a,a-d}$ refere-se aos alunos ingressantes em $a-d$ que concluíram o curso em $a$. É válido supor que $C_{a,a-d}\approx C_a$, já que não temos como saber quantos desses $C_a$ são de fato os que ingressaram em $a-d$.

A ideia é que, dos alunos que ingressaram em $a-d$ e não foram evadidos, totalizando $I_{a-d}-E_{a-d}$, $C_{a}$ concluíram o curso. Logo, os restantes são os retidos,
""")
st.latex(r"R_a \approx I_{a-d}-E_{a-d}-C_a")
st.markdown(r"""
Assim, uma estimativa razoável para a taxa de retenção é
""")
st.latex(r"r_a = 1 - \dfrac{C_a}{I_{a-d} - E_{a-d} }")
st.markdown(r"""
Sabendo que 
""")
st.latex(r"E_{a-d} = M_{a-d-1}-C_{a-d-1}+I_{a-d} - M_{a-d}")
st.markdown(r"""
temos a expressão para $r_a$:
""")
st.latex(r"r_a = 1 - \dfrac{C_a}{C_{a-d-1} + M_{a-d} - M_{a-d-1}}")
st.markdown(r"""
Para uma dada etnia $j$, os retidos são
""")
st.latex(r"R_a^{(j)} \approx I_{a-d}^{(j)}-E_{a-d}^{(j)}-C_a^{(j)}")
st.markdown(r"""
Do total de retidos, a proporção daqueles que são da etnia $j$ é dada por
""")
st.latex(r"\dfrac{R_a^{(j)} }{R_a} \approx  \dfrac{I_{a-d}^{(j)}-E_{a-d}^{(j)}-C_a^{(j)}}{I_{a-d}-E_{a-d}-C_a} = \dfrac{\dfrac{I_{a-d}^{(j)}-E_{a-d}^{(j)}-C_a^{(j)}}{I_{a-d}-E_{a-d} }}{1-\dfrac{C_a}{I_{a-d}-E_{a-d} }}")
st.markdown(r"""
Seja $r_a^{(j)}$ a proporção de alunos retidos da etnia $j$ em relação ao total de alunos ingressantes não evadidos do ano $a-d$,
""")
st.latex(r"r_a^{(j)} = \dfrac{I_{a-d}^{(j)}-E_{a-d}^{(j)}-C_a^{(j)}}{I_{a-d}-E_{a-d}}")
st.markdown(r"""
Temos, portanto,
""")
st.latex(r"\dfrac{R_a^{(j)} }{R_a} \approx \dfrac{r_a^{(j)}}{r_a}")