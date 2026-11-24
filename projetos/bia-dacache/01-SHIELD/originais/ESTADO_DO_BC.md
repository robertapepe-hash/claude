# Estado do BC — o que está de pé

**Atualizado:** 2026-08-21 · **Owner:** Beatriz Dacache
**Grid (v12):** https://grid.adminml.com/d/01M0DSBDBHEAV3650Q913YSP6Y/view ⚠️ *visibilidade `public`*
**Este documento é a fonte da verdade do que vale.** O histórico completo, incluindo os caminhos abandonados, está em `premissas_bc_shopee_asp_home.md`.

---

## 1. O que o BC é

Frear o avanço da Shopee em **Home Electronics** (Large Appliances, Small Appliances, Heating & Cooling) trazendo sellers MELI para perto. O KPI de compromisso é o **ratio = faturamento Shopee ÷ faturamento MELI**. Horizonte: **jul-dez/2026**, sendo **set-dez/26 a janela acionável**.

---

## 2. Regra de ouro do perímetro — **D1 cheia, sempre**

**Todo número de capa é D1 cheia, sem recorte de faixa de ASP.** Decidido em 21/08/2026, a pedido da Beatriz: *"os números macro precisam bater com os números dos documentos oficiais."*

A faixa de ASP continua no BC, mas **só como eixo de alocação** do incremental (aba 1) — nunca para compor o número de capa.

**A prova de que fecha:** MELI no semestre jul-dez/25, base Planning (D1 cheia) × DM Eficiência (soma dos segmentos):

| D1 | Planning | DM Eficiência | gap |
|---|---|---|---|
| LARGE | 2.852,0 | 2.855 | **0,1%** |
| SMALL | 2.273,7 | 2.270 | **0,2%** |
| H&C | 1.693,5 | 1.694 | **0,03%** |

No perímetro isso não fechava: Small dava 1.789 contra 2.270 — **27% de diferença**.

---

## 3. As três D1s — tratamento diferente para cada

| D1 | ratio H2'25 | ratio hoje (Q2'26) | jul-dez/26 | tratamento |
|---|---|---|---|---|
| **LARGE** | 20,7% | 30,0% | **42,7%** → 39,7% com camadas | ✅ **projeção validada** |
| **SMALL** | 29,2% | 44,1% | **45,2%** → 44,0% com camadas | ✅ **projeção quantificada** |
| **H&C** | 27,3% | 48,2% | **banda 45-70%** → 38-60% | 🔴 **sem projeção — banda + evidência** |
| *Large + Small* | 24,5% | 36,2% | 43,8% → 41,4% | soma das duas quantificadas |

**Validação em D1 cheia — MELI de julho/26, um passo à frente.** O motor ajusta até jun/26 (último mês fechado do Planning) e projeta julho; o realizado vem do DM Eficiência.

| D1 | projetado | realizado | erro |
|---|---|---|---|
| LARGE | 642,4 | 641,3 | **+0,17%** ✅ |
| SMALL | 496,8 | **513,8** | −3,3% |
| H&C | 224,8 | 221,1 | +1,7% |

*O realizado de Small (513,8) é o número oficial que a Beatriz já conhecia (514 Mi). A base D1 cheia reproduz o oficial.*

**Small — o "alívio sazonal" era artefato do perímetro.** Na versão anterior o ratio caía de 35,5% para 28,7% no semestre e era preciso explicar que isso era sazonalidade, não vitória. **Em D1 cheia essa queda não existe:** 44,1% hoje → 45,2% projetado, praticamente estável. Não há nada a explicar — e o banner de sazonalidade foi removido do painel.

**H&C** — quatro métodos deram **42%, 46%, 52% e 77%**, e o motor em D1 cheia dá **67%**. Dispersão dessa ordem não é margem de erro: é a categoria dizendo que não é projetável. Causas: D1 mais sazonal (pico nov-jan, vale abr-jun — o modelo ancora no vale para projetar no pico), degrau de dado em out/25 que contamina qualquer YoY, e pior desempenho no backtest. Os 67% caem **dentro da banda declarada**, na parte de cima.

---

## 3. H&C — a evidência que substitui a projeção

Fatos medidos, sem modelo:
- o ratio saiu de **13% (jul/25) para 43-48% (Q2/26)** — **triplicou em doze meses**
- nossa **Carteira Assessorada encolhe −21,4%** — e ela é **69% da categoria**
- **Frio Peças**, maior loja da Shopee em H&C, vende **9x mais lá do que com a gente** (57,3 vs 6,5 Mi em mai+jun/26)
- os 5 grupos cotados vendem **231% mais na Shopee** que no MELI
- **1P é só 5,5%** da categoria — essa alavanca não existe aqui

---

## 4. As camadas de recuperação — uma regra única

> 🔴 **ESTA SEÇÃO ESTÁ EM REVISÃO — não usar os números abaixo antes de decidir.**
> A auditoria cruzada de 21/08/2026 (`AUDITORIA_21ago.md`) encontrou três erros materiais aqui:
> **(1)** a lista de grupos do bloco BC está desatualizada (8/3/5 em vez de 10/6/8, de antes de Electrolux e Philco entrarem);
> **(2)** com a lista certa o gap do BC cai de **296 para 121 Mi** (e vira **zero** em Small e H&C, porque esses grupos crescem acima da categoria);
> **(3)** o gap de H&C (314) foi calculado sobre a Carteira Assessorada **total**, então **conta os 65 Mi do bloco BC duas vezes**.
> Além disso, a régua "gap vs ritmo da D1" provavelmente **não é a régua certa para o bloco BC** — ver Parte 4 da auditoria.

**Período do gap: o semestre jul-dez/26 inteiro** — não é por mês. A base de comparação é o que o bloco faturou em **jul-dez/25**.
**Referência:** o crescimento da própria D1, medido jul/26 vs jul/25 no DM Eficiência — Large **+54,6%** · Small **+43,9%** · H&C **+19,1%**.
**Gap medido** = `base H2'25 × (referência − crescimento próprio do bloco)`. Em palavras: *quanto o bloco deixa de faturar no semestre por estar crescendo mais devagar que a categoria.* O total é a soma dos gaps medidos.
*Por que não "ritmo da carteira": em H&C a carteira encolhe 7,4% — seria pedir que os sellers encolhessem.*

| bloco | LARGE | SMALL | H&C | **TOTAL** |
|---|---|---|---|---|
| **BC — grupos cotados** (negociação seller a seller) | 208 | 23 | 65 | **296** |
| **Demais segmentos — BAU** (a definir) | 112 | 57 | 314 | **483** |
| **TOTAL a recuperar no semestre (R$ Mi)** | **320** | **80** | **379** | **779** |
| *média por mês, para referência* | *53* | *13* | *63* | *130* |

**O gap fora dos grupos cotados não está alocado.** Ele foi medido e existe; **como será distribuído entre carteira assessorada, Seller Dev e 1P é decisão do time, não premissa do modelo.** Qualquer um dos três pode colaborar. *(Decisão de 21/08 — antes o modelo zerava carteira e 1P porque já crescem acima da referência; isso dava direção que ainda não queremos dar.)*

⚠️ **Não agregar recalculando o gap sobre o bloco somado.** O crescimento ponderado dos demais segmentos em Large é **+60,7%** — acima da referência — e o gap viraria **zero**, derrubando o total de 320 para 208. O total vem da soma dos gaps medidos **por segmento**; a agregação é só de apresentação.

**A maior alavanca de todo o HE não está em Large:** é o gap de **H&C (379 Mi, dos quais 314 fora dos grupos cotados)** — e ele está concentrado na Carteira Assessorada, nosso próprio portfólio gerido, encolhendo 21%.

---

## 5. Composição por segmento (H2'25 e YoY de julho)

| D1 | 1P | Carteira Assessorada | Seller Dev |
|---|---|---|---|
| LARGE | 920 · **+64,4%** | 1.634 · **+57,7%** | 301 · **+16,8%** 🔴 |
| SMALL | 598 · +47,0% | 696 · **+54,8%** | **976** · **+36,3%** 🔴 |
| H&C | 93 · +19,6% | **1.173** · **−7,4%** 🔴🔴 | 428 · **+75,2%** |

**H&C está invertida:** o segmento que mais controlamos encolhe, e a cauda longa é o que cresce.
**Em Small o maior segmento é o Seller Dev (43%)** — ou seja, a maior oportunidade está na camada de menor controlabilidade.

---

## 6. A migração dos sellers — a evidência central

**Os grupos cotados vendem mais na Shopee do que no MELI.** (mai+jun/26, R$ Mi)

| D1 | MELI | Shopee | Shopee ÷ MELI |
|---|---|---|---|
| LARGE (10 grupos) | 147,3 | 236,0 | **160%** |
| SMALL (6 grupos) | 43,7 | 89,9 | **206%** |
| H&C (8 grupos) | 65,4 | 151,2 | **231%** |
| **TOTAL** | **256,4** | **477,1** | **186%** |

**Electrolux é o caso emblemático:** MELI **41,3 → 38,9 (−6%)** enquanto Shopee vai de **0 → 52,3** (abriu loja oficial em ago/25). O grupo cresceu **+121%** e **105% desse crescimento foi para a Shopee**. Saiu de 100% MELI para 57% Shopee em 11 meses. **Não é um seller fraco — é um seller forte cujo crescimento inteiro perdemos.**

**Engage é a prova reversa:** cresceu **+106% no MELI** e ficou flat na Shopee. Único caso de migração na nossa direção.

**Concentração:** os 6 grupos originais passaram de **24% (jul/25) para 57,3% (jun/26)** de tudo que a Shopee fatura em Large.

### A fórmula da substituição
Um real trazido da Shopee move **os dois lados** do ratio, então vale mais que um real de venda nova:

$$\text{eficiência} = \frac{1+r}{r} = 1 + \frac{\text{MELI}}{\text{Shopee}}$$

Em Large (D1 cheia, jul-dez/26): **3,34x**. R$ 100 Mi de substituição valem R$ 334 Mi de venda nova, em efeito sobre o ratio.
Como a eficiência é $1+1/r$, **a substituição vale mais onde a Shopee ainda é pequena** (r = 20% → 6x). Defender território que ainda dominamos é mais eficiente que reagir onde já perdemos.

### A janela acionável são 4 meses, não 6
A base da Shopee fecha em **jun/26**, então o semestre inteiro (jul-dez/26) aparece como pendente. Mas **julho e agosto já passaram** — são meses que ainda não auditamos, não meses em que podemos agir. **Os dias acionáveis são set, out, nov e dez/26.** Os cenários de recuperação são dimensionados nesses quatro meses.

**Cenários em Large** — os 10 grupos cotados faturam **115,2 Mi/mês** na Shopee (jun/26). "Recuperar 30%" significa: se eles passassem a vender com a gente 30% do que hoje vendem lá.

| se trouxéssemos… | entra por mês | nos 4 meses acionáveis | equivale a venda nova | ratio jul-dez/26 |
|---|---|---|---|---|
| 20% do que vendem lá | 23,0 Mi | 92 Mi | 299 Mi (×3,25) | 44,5% → 39,9% |
| 30% | 34,6 Mi | 138 Mi | 449 Mi (×3,25) | 44,5% → 37,8% |
| 50% | 57,6 Mi | 230 Mi | 748 Mi (×3,25) | 44,5% → **33,6%** |

*O ratio da coluna final é o da janela set-dez/26 (44,5%), não o do semestre inteiro (42,7%).*

---

## 7. Como a projeção é feita

Média de duas regras (a média cancela viés: a primeira subestimou 11% no backtest, a segunda superestimou 13%, a média ficou em +0,9% — Bates & Granger, 1969):

**Regra 1 — YoY sobre o mês real do ano anterior:** $F = \text{real}(m-12) \times (1 + \text{YoY} \times \varphi^{k})$, com o YoY dos últimos 6 meses fechados.

**Regra 2 — decomposição multiplicativa:** $F = \text{nível dessazonalizado} \times \prod(1 + g\varphi^{j}) \times S_m$, onde $S_m$ é o índice sazonal por mês-calendário (log-linear; MELI 2023-26, Shopee 2024-26), o nível vem dos **últimos 3 meses fechados (L3M)** e $g$ é a tendência recente.

**Amortecimento $\varphi = 0{,}9$** (damped trend, Gardner & McKenzie 1985) — o crescimento continua mas desacelera, e a projeção não explode no horizonte longo.

### Validação e viés (em D1 cheia)
Checagem de julho/26: ver §3. Backtest (ajuste até dez/25 → previsão de jan-jun/26), erro do ratio: **Large 10,9% · Small 23,3% · H&C 24,2%**.

⚠️ **O motor subestima a Shopee.** Viés no backtest: **−14% em Large** e **−34% em Small**. Em D1 cheia as duas regras erram para o mesmo lado, então a média **não cancela** o viés (em perímetro cancelava: −11% e +13% → +0,9%). **Os ratios projetados são o piso, não o teto** — o risco real é maior. Na direção de um BC isso é conservador: não há como acusar o número de estar inflado.

---

## 8. Fontes — e o papel de cada uma

| fonte | papel | observação |
|---|---|---|
| `SBOX_MKPBR.DM_MARKET_ASP_MONTHLY_VERTICAL_D1` | **nível de mercado** por D1 × faixa de ASP | Planning · defasagem ~2 meses (fecha jun/26) · **não tem 1P/3P nem seller** |
| `WHOWNER.DM_EFICIENCIA_MLB` | **acompanhamento**, segmento e seller | já tem jul/26 · `SUM(GMV_LC) WHERE NMV_FLG AND GMV_FLG`, por `ORD_CLOSED_DT` · **não tem faixa de ASP** |
| `WHOWNER.DM_YIPIT_SHOPEE_ITEMS` | **composição por loja** da Shopee | fecha jun/26 · nível item → loja |
| `depara_grupos_economicos.csv` | consolidação de cust_id em grupo econômico | Elux tem loja oficial + Full; Shop EV = grupo Kill inteiro |

**Validação GMV × NMV:** o `TGMV_MELI` do Planning bate com o NMV líquido do DM Eficiência — gap de **0,1%**. É isso que permite transitar entre as duas bases.

**Yipit e Planning são a MESMA fonte de Shopee** (verificado em 21/08/2026): `GMV_SHOPEE` do Planning == `NMV_LC` do Yipit agregado por D1 × mês, com erro de **0,00% a 0,15%** em 18 combinações. A descrição da tabela Yipit diz "Source: Planning MLB". ⚠️ *Isso corrige o que estava escrito aqui antes ("as duas não reconciliam, não dividir entre elas") — **é válido dividir uma pela outra**, e portanto o share do grupo dentro da Shopee da D1 é uma métrica legítima: os 10 grupos são **62,4%** de tudo que a Shopee fatura em Large (jun/26).* A **defasagem** continua real: Yipit/Planning fecham em jun/26, o DM tem jul/26.

---

## 9. Limitações declaradas

1. **O GMV da Shopee é estimativa de painel**, não dado transacional. Usar **tendência e ratio**, não nível absoluto.
2. **O motor subestima a Shopee** em D1 cheia (−14% Large, −34% Small no backtest). Ver §7.
3. ~~Distorção do perímetro de faixas.~~ **Resolvido em 21/08/2026** — tudo passou a D1 cheia. Para registro do que era: no perímetro, o ratio de Small aparecia como 35,5% quando o real era 44,1% (**8,6 pp escondidos**), porque o critério de faixa-foco exigia SOB MELI ≥5% e em Small a Shopee vive exatamente onde nosso SOB é pequeno — 49-79 (ratio 199%), 19-49 (148%), até 19 (1.053%) ficavam de fora. Em Large e H&C a distorção era de meio ponto.
4. **O YoY dos segmentos é medido em julho isolado** (mês único).
5. **As camadas entram integralmente já em julho**, sem rampa — ajustar quando o plano tiver data de início.
6. **Nada aqui prova causalidade.** A correlação entre a entrada dos sellers na Shopee e a estagnação aqui é forte, mas parte do crescimento lá pode ser demanda nova. Por isso a substituição entra como **cenário**, não como previsão.
7. **O incremental não é o pedido do BC.** É o tamanho do problema. Precisa ser rateado entre BAU, BC e 1P antes de virar pedido de verba.

---

## 10. O Grid — 5 abas

| aba | conteúdo |
|---|---|
| **1 · Diagnóstico por faixa** | evolutivo Shopee × MELI por D1 e faixa de ASP · **é a visão de alocação**; abre com as 11 faixas marcadas, então o default já é D1 cheia |
| **2 · D1s consolidadas** | as três D1s com o tratamento de cada uma, o gap do semestre e as premissas |
| **3 · Migração dos sellers** | MELI vs Shopee por grupo econômico · **seleção múltipla de grupos** (chips ou clique na linha do ranking) · ranking atacar/proteger derivado do dado · cenários na janela de 4 meses |
| **4 · Realizado × Projetado** | gráfico contínuo com a fronteira em jun/26, em D1 cheia |

*A aba 5 (Simulador) foi **apagada** em 21/08/2026, com aprovação da Beatriz: tinha sido construída no perímetro de faixas-foco e os valores não coincidiam mais com as demais. O método está registrado em `premissas_bc_shopee_asp_home.md` §7 e o arquivo original permanece em `simulador_desafio.html`.*

**Regras de comunicação travadas:** nenhum jargão sem tradução na tela · unidade em todo cabeçalho · período explícito em toda referência · referência histórica sempre ao lado do alvo · glossário na página · evolutivo mensal é peça central · quadro sempre com colunas = histórico + projeção e linhas = KPIs (faturamento, MoM, YoY de Shopee e MELI, ratio).

---

## 11. Pendências

1. **Small e H&C: listas de sellers** — Beatriz vai enviar as definitivas. As atuais vieram de um print e foram confirmadas por nome.
2. **Perímetro de Small** — decidir se migra para D1 cheia (resolve a subestimação de 9 pp e torna a validação contra o DM exata).
3. **Rateio BAU × BC × 1P** — o incremental de 779 Mi precisa ser dividido. O time de farming entra aqui para estimar a verba e a eficiência.
4. **Capacidade de seller** — validar se os grupos cotados conseguem entregar, com os cubos do Shield (`seller_cap_cube`, `grupos_economicos`).
5. **Rampa de entrada** — as camadas hoje entram todas em julho; ajustar quando houver data de início.
6. **Faturamento dos grupos na Shopee por faixa de ASP** — para dimensionar a substituição por faixa.

---

## 12. Armadilhas técnicas registradas

- **PowerShell não diferencia maiúsculas em variáveis.** Três bugs silenciosos nesta sessão: `$n`×`$N`, `$sS`×`$SS`, `$h2`×`$H2` (este destruiu um array e zerou resultados). **Nunca usar nomes que difiram só por caixa.**
- **`continue` em `foreach` aninhado** pode escapar os dois loops — usar `if`.
- **Precedência da vírgula:** `@($x-2, $x-1, $x)` é lido como `$x - (2, $x-1, $x)`. Parentizar.
- **Arrays esparsos em JS:** `map` pula buracos e o `join` os transforma em vazio, desalinhando células de tabela. Usar `new Array(n).fill(null)`.
- **bq CLI:** ler `.sql` com `[System.IO.File]::ReadAllText` (remove BOM) e colapsar em uma linha.
- **Custo do DM Eficiência:** ~1,2-1,4 GB por mês de partição, dirigido pelas **colunas** referenciadas, não pelas linhas. Filtrar D1 ou cust_id **não** reduz o scan.
- **Sempre conferir a última competência disponível na fonte** antes de definir janelas (o Yipit fecha um mês antes do DM — isso já gerou uma comparação de 2 contra 3 meses).
