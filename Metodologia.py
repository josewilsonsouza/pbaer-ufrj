**⚠️OBS.** As categorias de um dado recorte serão chamadas de classes ou grupos. Exemplo: o recorte SEXO tem as classes/grupos MASCULINO e FEMININO.

## 📉 Evasão
**DEFINIÇÃO (Taxa de Evasão).** Saída antecipada, antes da conclusão do ano, série ou ciclo, por desistência (independentemente do motivo) (INEP, 2017).
Calculamos o percentual de alunos que se evadem no primeiro ano dos cursos de graduação:

$$
\mathrm{TEV}_a = \left (1 - \dfrac{M_a - I_a}{M_{a-1} - C_{a-1}} \right)\times 100
$$
- $\mathrm{TEV}_a$ - Taxa de Evasão no ano $a$
- $a$ — Ano
- $M$ — Número de matriculados
- $I$ — Número de ingressantes
- $C$ — Número de concluintes

##### EVASAO - TOTAL: CASO ETNIA 

**DEFINIÇÃO (Taxa de Evasão Total).** Representa a taxa de evasão calculada considerando **o conjunto total de estudantes**, independentemente do grupo específico de etnia. Ou seja, agrega os dados de todas as categorias de etnia (como Branca, Preta, Parda etc.), fornecendo uma visão geral da evasão **dentro do recorte Étnico**, mas **sem distinguir entre os grupos**.

Para uma dada etnia $j$:

$$
\mathrm{TEVT}_a^{(j)} = \dfrac{M_{a-1}^{(j)} - C_{a-1}^{(j)} +I_a^{(j)} - M_a^{(j)}}{M_{a-1}-C_{a-1} }
$$

- $a$: Ano de referência da evasão.
- $j$: Grupo ou classe pertencente ao recorte ETNIA (Branca, Preta ou Parda).
- $M_a^{(j)}$: Número de alunos do grupo $j$ matriculados no ano $a$.
- $C_a^{(j)}$: Número de alunos do grupo $j$ que concluíram o curso no ano $a$.
- $I_a^{(j)}$: Número de ingressantes do grupo $j$ no ano $a$.
- $M_a$: Total de alunos (de todos os grupos) matriculados no ano $a$.
- $C_a$: Total de alunos (de todos os grupos) que concluíram o curso no ano $a$.
---

## ⏳ Retenção

**DEFINIÇÃO (Taxa de Retenção).** Condição intermediária de insucesso, na qual o aluno permanece na universidade após o período de integralização do seu curso (INEP, 2017).

$$
\mathrm{TRE}_a = \dfrac{I_{a-d} - C_{a,a-d} - \mathrm{EV}_{a-d}}{I_{a-d} - \mathrm{EV}_{a-d}} \times 100
$$

- $\mathrm{TRE}_a$: Taxa de Retenção no ano $a$
- $a$ : Ano base da consulta
- $d$ : Duração do curso
- $I_{a-d}$ : Número de ingressantes no ano $a-d$
- $C_{a,a-d}$ : Concluintes no ano base que ingressaram no ano $a-d$
- $\mathrm{EV}_{a-d}$ : Número de evadidos do ano $a-d$


Para o cálculo da **Taxa de Retenção**, é necessário estimar quantos estudantes que ingressaram em um determinado ano acabaram evadindo ao longo do tempo.
Como os dados disponíveis são agregados por ano e não acompanham cada estudante individualmente ao longo do tempo (isto é, não são longitudinais), foi adotada uma **metodologia de estimação baseada em coortes**.

##### 🧠 Hipótese Adotada

1. Admitimos que a **taxa de evasão observada em um determinado ano** representa, em grande parte, a evasão dos estudantes que **ingressaram no ano anterior**.
Ou, simbolicamente:

$$
\mathrm{EV}_{p-d} \approx \mathrm{TEV}_{p-d+1} \cdot I_{p-d}
$$

✅ **A maioria das evasões ocorre nos primeiros períodos do curso**, o que torna essa aproximação razoável.

✅ Em **contextos com dados agregados**, essa técnica é amplamente utilizada para reconstituir trajetórias estudantis.

✅ Permite **calcular indicadores por coorte**, como a retenção, mesmo sem dados individuais.

2. Assumimos $C_{a,a-d} \approx C_a$. Ou seja, assumimos que todos que concluiram o curso em $a$ ingressaram em $a-d$.

##### RETENCAO - TOTAL: CASO ETNIA
**DEFINIÇÃO.** Para uma **classe** $j$ de um dado recorte, a **Taxa de Retenção Total** da classe $j$, $\mathrm{TERT}_a^{(j)}$, calcula a taxa de retenção  de $j$ em relação ao total de alunos. 

$$
\mathrm{TERT}_a^{(j)} = \dfrac{I_{a-d}^{(j)}-\mathrm{EV}_{a-d}^{(j)}-C_a^{(j)}}{I_{a-d}-\mathrm{EV}_{a-d}}
$$

- $ \mathrm{TERT}_a^{(j)} $: Taxa de Retenção do grupo $j$, no ano $ a$, em relação ao total.
- $ I_{a-d}^{(j)} $: Número de ingressantes da classe $ j $ no ano $ a-d $.
- $ \mathrm{EV}_{a-d}^{(j)} $: Número estimado de evadidos da classe $ j $ que ingressaram no ano $ a-d $.
- $ C_a^{(j)} $: Número de concluintes da classe $ j $ no ano $ a $.
- $ I_{a-d} $: Total de ingressantes (de todas as classes de todos os recortes) no ano $ a-d $.
- $ \mathrm{EV}_{a-d} $: Total estimado de evadidos (de todas as classes de todos os recortes) que ingressaram no ano $ a-d $.

🔍 **Interpretação:**
Esse indicador mostra, para um grupo específico, quantos estudantes ainda permanecem ativos (estão retidos) **em relação à base total** de estudantes que deveriam estar ativos, **descontando concluintes e evadidos**.

---

## 🎓 Sucesso

**DEFINIÇÃO.** É o Índice de conclusão do curso no ano $a$.

$$
\mathrm{TSU}_a = \dfrac{C_{a}}{I_{a-d}} \times 100
$$

- $C_{a}$: Total de concluintes no ano $a$
- $I_{a-d}$: Total de ingressantes no ano $a-d$

##### SUCESSO - TOTAL

**DEFINIÇÃO.** É o Índice de conclusão da classe $j$ de um dado recorte do curso no ano $a$.

$$
\mathrm{TSUT^{(j)}}_a = \dfrac{C^{(j)}_{a}}{I_{a-d}} \times 100
$$

---
### REFERÊNCIAS
- FÓRUM DE PRÓ-REITORES DE PLANEJAMENTO E
ADMINISTRAÇÃO. **Grupo de Trabalho Indicadores** – GT. In: ANAIS do
4º FORPLAD. Ouro Preto: IFES – Instituições Federais de Ensino
Superior, 2015. P. 197.

- INEP, Diretoria de Estatísticas Educacionais. **Metodologia de Cálculo
dos indicadores de fluxo da educação superior**. [S.l.]: INEP, Brasília, 2017.
