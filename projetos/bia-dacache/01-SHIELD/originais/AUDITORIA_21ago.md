# Auditoria cruzada das 4 abas — 21/08/2026

Revisão pedida pela Beatriz depois da virada para D1 cheia: *"revise todas as abas, tudo que voce fez, se os numeros (só os que deveriam) batem de uma aba pra outra."*
Método: extração dos números **renderizados** (não do código-fonte) de cada aba do `grid_v12.html`, via JS no browser, e reconciliação.

---

## PARTE 1 — O que reconcilia ✅

### 1.1 Abas 1, 2 e 4 fecham exatamente

Somei as 11 faixas da aba 1 e comparei com a série da aba 2 e da aba 4:

| D1 | período | Shopee | MELI | ratio | aba 1 | aba 2 | aba 4 |
|---|---|---|---|---|---|---|---|
| LARGE | H2'25 | 590,7 | 2.852,0 | 20,7% | ✓ | ✓ | ✓ |
| LARGE | Q2'26 | 511,4 | 1.703,6 | 30,0% | ✓ | ✓ | ✓ |
| SMALL | H2'25 | 664,6 | 2.273,7 | 29,2% | ✓ | ✓ | ✓ |
| SMALL | Q2'26 | 591,6 | 1.341,4 | 44,1% | ✓ | ✓ | ✓ |
| H&C | H2'25 | 462,3 | 1.693,5 | 27,3% | ✓ | ✓ | ✓ |
| H&C | Q2'26 | 303,4 | 629,2 | 48,2% | ✓ | ✓ | ✓ |

Projeção jul-dez/26 (abas 2 e 4): LARGE 1.756,9 / 4.110,7 = **42,7%** · SMALL 1.352,2 / 2.991,1 = **45,2%** · H&C sem projeção. Idênticas nas duas abas.

### 1.2 A aba 3 soma corretamente na seleção múltipla
Electrolux sozinha = 52,3 Mi/mês na Shopee (jun/26); + 3 GREEN = 82,9; MELI 38,9 → 51,8. Soma, não substitui. "Todos" volta a 115,2 / 82,5.

### 1.3 O `PROJ` da aba 3 vem da mesma projeção
`{LARGE:{m:2843,s:1264}}` = soma set-dez/26 do motor (589,2+616,0+1075,9+561,7 e 292,3+301,1+363,2+307,5). Consistente com a aba 2.

### 1.4 O que **não deve** bater, e por quê
- **MELI da aba 3 (grupos) vs MELI da aba 2 (D1 total):** a aba 3 é um subconjunto — só a Carteira Assessorada (`3P - VERTICALES`) e só os grupos cotados.
- **Shopee da aba 3 (Yipit) vs Shopee da aba 2 (Planning):** fontes diferentes que **não reconciliam por construção**. Nunca dividir uma pela outra.

---

## PARTE 2 — O que NÃO reconcilia ❌

### 2.1 🔴 CRÍTICO — a lista de grupos da aba 2 está desatualizada

A aba 2 usa a lista **antes** de você mandar somar Electrolux e Philco. A aba 3 usa a lista atualizada.

| D1 | aba 2 diz | aba 3 tem | base H2'25 aba 2 | base H2'25 real (aba 3) | erro |
|---|---|---|---|---|---|
| LARGE | "8 grupos cotados" | **10 grupos** | 439 | **448,5** | −2,1% |
| SMALL | "3 grupos cotados" | **6 grupos** | 75 | **108,3** | **−30,7%** |
| H&C | "5 grupos cotados" | **8 grupos** | 284 | **373,5** | **−24,0%** |

Lista real (união = 10 grupos): 3 GREEN · DUFRIO · EFACIL · ELECTROLUX · ENGAGE ELETRO · FRIO PECAS · INFOAR · OUTLET DAS FABRICAS · PHILCO/BRITANIA · SHOP EV (KILL).
Presentes em LARGE: todos os 10 · SMALL: 6 · H&C: 8.

### 2.2 🔴 CRÍTICO — o gap do bloco BC muda radicalmente com a lista certa

Crescimento próprio dos grupos, jul/26 vs jul/25 (mesma régua da referência), medido no dado da aba 3:

| D1 | grupos jul/25 | grupos jul/26 | cresc. próprio | referência D1 | gap recalculado | aba 2 mostra |
|---|---|---|---|---|---|---|
| LARGE | 64,5 | 82,3 | **+27,6%** | +54,6% | **121,1** | 208 |
| SMALL | 12,1 | 21,1 | **+74,4%** | +43,9% | **0** *(acima)* | 23 |
| H&C | 30,2 | 42,5 | **+40,7%** | +19,1% | **0** *(acima)* | 65 |
| **total** | | | | | **121** | **296** |

O crescimento implícito na aba 2 (54,6 − 208/439) era **+7,2%** em Large. O real dos 10 grupos é **+27,6%**.

### 2.3 🔴 CRÍTICO — o gap de H&C conta o bloco BC duas vezes

O BAU de H&C mostra **314**. Reproduzindo: `1.173 × (19,1 − (−7,4))/100 = 310,8` — ou seja, foi calculado sobre a **Carteira Assessorada TOTAL**, que **inclui os grupos do BC**.
Deveria ser sobre a carteira **menos** os grupos cotados: `889 × 0,265 = 235,6`.
A coluna de base da própria linha diz 1.410 (= 1.694 − 284), coerente com "menos os grupos" — **mas o gap foi calculado sobre outra base**. Logo os 65 Mi do BC estão dentro dos 314.

### 2.4 🟠 O gap do BAU de Small não reproduz dos próprios inputs

Segundo a tabela de diagnóstico da própria aba: Seller Dev = 976 a +36,3%, referência +43,9% → gap = `976 × 0,076 = 74,2`.
A tabela de camadas mostra **57**. Diferença de **23%**. Não consegui reproduzir os 57 de nenhum caminho.

*(Large reproduz: `301 × 0,378 = 113,8` vs 112 mostrado — arredondamento, ok.)*

### 2.5 🟠 Duas taxas diferentes para a mesma coisa, na mesma aba

Em H&C, sobre o crescimento da Carteira Assessorada:
- banner de evidência: **"encolhe −21,4%"**
- tabela de diagnóstico: **−7,4%**

São a mesma métrica. Uma das duas está com janela errada (provável: −21,4% é outra janela, não jul/26 vs jul/25). Precisa ser resolvido antes de ir para a liderança — é o número mais citado do caso de H&C.

### 2.6 🟠 Mecanismos diferentes para o mesmo tipo de conta

- **Aba 2** — "com as camadas": `ratio = Shopee / (MELI + camadas)`. **Incremental puro**: a Shopee não muda.
- **Aba 3** — cenários de recuperação: `ratio = (Shopee − recuperado) / (MELI + recuperado)`. **Substituição**: tira dela e soma em nós.

Os dois efeitos "com ação" não são comparáveis, e nada na tela diz isso. Em Large: aba 2 mostra 42,7% → 39,7% (−3,1 pp) com 320 Mi; aba 3 mostra 44,5% → 37,8% (−6,7 pp) com 138 Mi. **A aba 3 parece mais eficiente porque usa outro mecanismo, não porque a ação seja melhor.**

### 2.7 🟡 Janelas diferentes para a mesma métrica

| métrica | aba 2 | aba 3 | motivo |
|---|---|---|---|
| ratio projetado de Large | **42,7%** | **44,5%** | semestre jul-dez vs janela set-dez |
| eficiência da substituição em Large | **3,34x** | **3,25x** | idem |

Está declarado no rodapé da aba 3, mas são dois números para a mesma coisa em telas vizinhas.

### 2.8 🟡 A eficiência de H&C na aba 3 usa base realizada

Large e Small usam a projeção set-dez/26; H&C, que não tem projeção, usa o **realizado de Q2'26** (629/303 → 3,08x). A eficiência só depende do ratio, então o número é válido — mas a base é diferente das outras duas e isso não está na tela.

### 2.9 🟡 A ser verificado: "os grupos são 57,3% do que a Shopee fatura em Large"

Está na §6 do `ESTADO_DO_BC.md`. Se o denominador vier do **Planning**, viola a regra de não dividir Yipit por Planning (`115,2/184,65 = 62,4%`, não 57,3%). Se vier do **total Yipit de Large**, está correto. Não é verificável com o payload atual da aba 3 (que só traz os grupos cotados). **Precisa ser reconferido na query original.**

---

## PARTE 3 — A pergunta dela: o desafio do BC bate com a soma das oportunidades dos sellers?

**Não. E a proximidade aparente é coincidência.**

| | valor |
|---|---|
| Aba 2 — bloco "BC — grupos cotados" (semestre) | **296 Mi** |
| Aba 3 — recuperar 30% na janela de 4 meses | **250,6 Mi** *(Large 138,2 · Small 35,8 · H&C 76,6)* |

Parecem próximos (18% de diferença), mas medem coisas diferentes em bases diferentes:
janela (6 vs 4 meses) · mecanismo (incremental vs substituição) · lista de grupos (8/3/5 vs 10/6/8) · e o 296 está errado (§2.2).

**Traduzindo o gap da aba 2 em % de recuperação** (Shopee dos grupos × 4 meses acionáveis = Large 460,8 · Small 119,2 · H&C 255,2 · total 835,2):

| D1 | gap aba 2 | % da Shopee dos grupos que teria de vir | com o gap corrigido |
|---|---|---|---|
| LARGE | 208 | **45,1%** | 121 → **26,3%** |
| SMALL | 23 | 19,3% | 0 → — |
| H&C | 65 | 25,5% | 0 → — |
| total | 296 | 35,4% | 121 → 14,5% |

---

## PARTE 4 — O problema de método (o mais grave)

**A régua "gap vs ritmo da D1" mede a coisa errada quando aplicada ao bloco do BC.**

Com a lista certa de grupos, ela dá **BC = 0** em Small e em H&C — porque os grupos cotados crescem **mais rápido** que a categoria no nosso lado (+74,4% vs +43,9% em Small; +40,7% vs +19,1% em H&C).

Mas esses mesmos grupos, hoje:

| D1 | faturam com a gente (jun/26) | faturam na Shopee (jun/26) | Shopee ÷ MELI |
|---|---|---|---|
| SMALL | 20,4 | 29,6 | **145%** |
| H&C | 30,3 | 63,7 | **210%** |
| LARGE | 82,5 | 115,2 | **140%** |

**A tese do BC é essa segunda tabela, não a primeira.** Um seller pode crescer 74% conosco e ainda estar dando o dobro do volume para a Shopee. A régua do ritmo da D1 responde *"quanto deixamos na mesa por crescer devagar"* — que é a pergunta certa para o **BAU**, e a pergunta errada para o **BC**.

### Complicação adicional: a referência é um mês só

`jul/26 vs jul/25` é comparação de **mês isolado**. Em H&C isso engana: os grupos vinham de **79,7 Mi/mês em jan/26** e caíram para **30,3 em jun/26**; jul/25 foi um mês fraco (30,2), então o YoY de julho dá +40,7% enquanto a tendência dos últimos seis meses é de queda forte. Já estava declarado como limitação, mas aqui ela **muda o sinal** de uma conclusão.

---

## PARTE 5 — Recomendação

**Separar as duas perguntas, cada uma com sua régua:**

1. **Bloco BC = substituição.** Dimensionar pelo que os grupos cotados dão para a Shopee (aba 3), em cenários de recuperação na janela acionável. É a tese do BC e é o número que o time de farming negocia seller a seller.
2. **Bloco BAU = gap vs ritmo da D1.** Mantém a régua atual, mas: (a) excluindo os grupos do BC da base (corrige o duplo-contagem de H&C), (b) refazendo o gap de Small, (c) trocando o YoY de mês isolado por uma janela de 3 meses.
3. **Um só mecanismo no ratio.** Escolher: ou tudo incremental, ou tudo substituição, ou mostrar as duas linhas lado a lado com rótulo explícito.
4. **Resolver o −21,4% vs −7,4%** de H&C antes de qualquer apresentação.
5. **Alinhar a janela** — ou tudo em jul-dez, ou tudo em set-dez. Recomendo **set-dez** (é o acionável) e mover o semestre para nota.

**Decisão que é dela:** como dimensionar o bloco BC (item 1). Isso muda o número de capa do BC.
