# Price Point HE — Metodologia do Instrumento de Inteligência Preço × Conversão

**Autoria:** Beatriz Dacache (Focal Pricing BR · vertical Home Electronics) + Claude Code
**Atualizado:** 2026-06-28 · **Status:** desenho em co-design — **PRÉ-EXECUÇÃO (nada rodado ainda)**
**Origem:** deck `BIDS - Price Point.pptx` (Commerce Business Insights & Data Science) + canon BPC (skill `bpc-reader`) + Shield (`Documents\Claude\Projects\BPC\Shield`)

> Documento **vivo e auditável**. Registra TODAS as decisões travadas e os pontos abertos, com fórmulas,
> pra que a metodologia seja transparente e **transferível a outros times**.

---

## 0. Mudança de moldura (pós-pausa de 27/jun) — LER PRIMEIRO

Isto nasceu como uma "foto de desperdício" one-shot. **Após alinhamento, o objetivo mudou:**

**Não é análise pontual. É um instrumento PERENE de inteligência para a vertical HE.** A partir do
modelo causal do time de Data, ele deve permitir: **diagnosticar** onde nosso preço/investimento ganha ou
perde conversão, **acompanhar no tempo**, **gerar insights e planos** e **medir impacto** — com foco
prioritário em **ganhar vs Shopee** (ponte direta com o Shield). A "quantificação do desperdício" vira
**um dos outputs**, não o fim.

---

## 1. O que herdamos do Data vs o que é nosso

| Elemento | Herdado do deck? | O que é nosso |
|---|---|---|
| CVR, Treatment, g, dist, efeitos fixos | Sim (conceito) | A fórmula operacional nas **nossas** tabelas |
| Limiares **4 / 5 / 10** | **Sim — usamos como régua-padrão** | Testar se valem **por faixa de ASP** (nível 4) |
| Causalidade desconto→CVR p/ **>70 USD MLB** | **Sim — tomamos como dado** | — |
| Faixas de ASP | Conceito sim, mas em USD | Trocar pelas do **Shield (R$)** |
| **Investimento $** | Não (deck não mede $) | Inteiramente nosso |
| **Classificação da carteira viva** | Não | Inteiramente nosso |
| **Cortes alternativos / validação por ASP** | Não | Inteiramente nosso |

**Limite da herança causal:** herdamos que *o mecanismo existe* na faixa >70 USD. **Não** herdamos que o
número exato seja 4/5/10 para Large — o "70+" deles é um balde aberto e não sabemos quanto é linha branca.
Por isso o nível 4 existe.

---

## 2. O modelo do Data (a receita herdada)

Regressão **three-way fixed effects** sobre experimentos de Rebates MLB 2025 × scraping (9,9k itens),
**ponderada por visits**, **erros clusterizados por campanha**. Isola o efeito do desconto limpando item,
data e campanha.

- **Eq. 1 (matched):** `CVR = β(Treat×g) + α·Treat + γ·g + μ_camp + η_item + τ_data + ε`
  → efeito do tratamento = `α + β·g`; vira significativo a partir de **g ≈ 4%**.
- **Eq. 2 (prêmio):** `CVR = β(Treat×dist) + α·Treat + γ·dist + θ·d + δ·d² + μ + η + τ + ε`
  → separa desconto mecânico (`θd + δd²`, com retorno decrescente) do **prêmio de posição** (`dist`).

**Limiares (ASP-dependentes no deck):** matched 4% (≥15 USD; <15 USD precisa ~10%), landing ≤10%,
piso ≥5% mais barato. **Sem diferença por competidor.** (MLM: 3%/12%, menos robusto.)

Detalhe do racional e de como os % saem das equações: ver seção "explicação" no histórico do projeto.

---

## 3. Espectro de rigor (níveis) e caminho escolhido

| Nível | O que é | Entrega | Status |
|---|---|---|---|
| 1. Causal c/ experimento | reestimar FE em dados A/B nossos | nossos limiares causais | **dependente do Data** (msg enviada) |
| 2. FE observacional | mesma fórmula, controle = mesmo item em dias sem rebate | nossos limiares (c/ ressalva de timing endógeno) | **upgrade** se o nível 4 indicar |
| **3. Adotar limiares + diagnóstico por ASP** | aplica 4/5/10 e classifica nossa carteira | priorização/diagnóstico | **ESCOLHIDO — ponto de partida** |
| **4. Testar cortes / correlação por ASP** | varre cortes p/ ver onde a virada cai | indício de limiar próprio | **ESCOLHIDO — em paralelo ao 3** |

**Decisão:** começar em **3 + 4**; subir pro **2** se o 4 indicar que Large vira em outro ponto; **1** só
se o Data tiver algo reaproveitável.

---

## 4. Unidade de análise — painel item-dia único (DECISÃO)

**Grão = item × dia**, cobrindo dias **COM e SEM** rebate.
Motivo (definido pela Beatriz): preço é por item/dia, e **dias sem rebate carregam sinal** — podemos estar
perdendo pra concorrência sem ação. Um recorte "só rebate" perderia isso.
→ **Substitui** o desenho anterior de "duas camadas / dedup por REBATE_ID".

**Colunas do painel:**

| coluna | de onde vem |
|---|---|
| item, dia | `MELI_ID`/`ITE_ITEM_ID`, `TIM_DAY` |
| preço meli do dia (box e pix) | original ou rebatado conforme o dia |
| preço rival do dia (por competidor, box e pix) | `BEST_RIVAL_*` e `COMPETITORS` / `BT_COM_FAVORABILITY` |
| rebate ativo? (sim/não) | há `REBATE` no dia |
| investimento do dia (box/pix) | `AMOUNT_REBATE_MELI` (ver §5) |
| g (tamanho do desconto) | derivado, só em dia com rebate |
| visits, orders → CVR | `VISITS`, `QTY_ORDERS_DAY` |
| faixa ASP (Shield) | derivada de ASP fixo de referência (ver §6) |

---

## 5. Fontes de dado e reconciliação de investimento

| Tabela | Papel |
|---|---|
| `meli-bi-data.WHOWNER.DM_COM_COMPETENCIA` | **espinha** item-dia: rebate $ + preços partida/chegada + preço rival |
| `meli-bi-data.WHOWNER.BT_COM_FAVORABILITY` | **lente box/pix por competidor** + favorabilidade (papel ativo, não só reconciliação) |
| `meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB` | **reconciliação de investimento** por alavanca (DXI/DXB) |

**Investimento por lente (DECISÃO):**
- **box:** `AMOUNT_REBATE_MELI` ↔ reconciliar com **DXI** (DM_EFICIENCIA)
- **pix:** `AMOUNT_REBATE_MELI` (metodologia pix) ↔ reconciliar com **DXB** (DM_EFICIENCIA)

**V1 CONFIRMADO (maio/2026):** `AMOUNT_REBATE_MELI` é **POR UNIDADE** (parcela MELI do desconto unitário).
- Identidade `AMOUNT_REBATE_MELI + AMOUNT_REBATE_SELLER = ORIGINAL_PRICE − REBATE_PRICE` vale (razão mediana = **1,0**).
- É **~3,1% do preço** (mediana). A parcela MELI do desconto total tem **mediana ~10%** (seller ~90%) —
  ⚠️ **DIRECIONAL, NÃO citar como fato:** é mediana **por linha**, **MLB inteiro**, **1 semana**. O que está
  sólido é a *direção* (MELI banca a menor parte). Quantificar **ponderado por volume, escopo HE, na janela**
  antes de afirmar o número. (Veio da query de ~27M linhas, não dos prints.)
- Valor **constante por rebate, repetido a cada dia** (99,9% dos multi-dia; média 6,6 dias).
- ➡️ **$ investido = Σ(`AMOUNT_REBATE_MELI` × unidades vendidas) por item-dia.** NÃO somar o campo cru, NÃO dedup.
  Unidades = `QTY_ORDERS_DAY` (proxy — confirmar orders vs unidades).

**DXI vs DXB (espiada `DM_EFICIENCIA` — refinamento importante):** tabela é **nível ordem-item**
(`ITE_ITEM_ID`, `ORD_CLOSED_DT`, unidades `SI`) → joinável por item-dia, com **$ realizado**. Levers **distintos**:
- **DXI** = **Desconto por Ítem** (guarda-chuva — **NÃO é só pré-acordo**). Composição HE mai/26 (% DXI MELI):
  **PRE_ACORDO 69,4%**, ON_DEMAND 15,0%, PRICING_MATCHING_MELI_ALL 8,0%, SMART_COFINANCED 4,2%, PRICING_MATCHING 3,5%.
  `DXI_INVESTMENT_LC` MELI + `_SELLER_LC`; subtipo em `DXI_CAMPAIGN_SUBTYPE`. = **rebate box** (≈ AMOUNT_REBATE_MELI).
  Nota: **PRICING_MATCHING(_MELI_ALL) ~11,5%** = gasto explícito de matching vs concorrência (campanha do time
  de Pricing; MELI banca mais por ter **PM100%** = cobrimos 100% do gap). Isolável p/ a tese.
- **DXB** = Desconto **Bancário** (`DXB_INVESTMENT_LC`; `DXB_PAYMENT_METHOD` inclui **PIX**) = lever **separado**.
- ➡️ **Investimento box = DXI; investimento pix = DXI + DXB(PIX).** `AMOUNT_REBATE_MELI` (=DXI) **NÃO carrega Pix**
  (confirma intuição da Beatriz) → **lente pix precisa do `DM_EFICIENCIA`** (DXB-Pix).
- DM_EFICIENCIA dá o **$ realizado por lever** (ordem) em R$ → **possível fonte primária de investimento** (a decidir na V1-p2).

**V1-p2 MEDIDO (HE, maio/2026):** DXI MELI **R$ 35,7 Mi** vs seller **R$ 249,1 Mi** → MELI banca **~12,5%** do
pré-acordo (corrobora o ~10%, agora agregado/HE). DXB MELI **R$ 10,6 Mi**, **93% Pix (R$ 9,8 Mi)** → Pix é
incremento real, **~27% do DXI MELI** e **não está no `AMOUNT_REBATE_MELI`**. DXI = 1,46% do GMV; DXB-Pix = 0,40%
(MELI total ~1,9% do GMV — abaixo do palpite 3-7%, provável diferença de base).
➡️ **TRAVADO (V1):** fonte primária de investimento = **`DM_EFICIENCIA`** (box = DXI [todos subtipos]; pix = DXI + DXB-Pix;
$ realizado, grão ordem-item joinável). `DM_COM` fica como **posição/transição** (preços + rival). `DXI_INVESTMENT_LC`
já É o "por-unidade × unidades" realizado → dispensa reconstruir via `AMOUNT_REBATE_MELI`.

**Atenção a grão:** DM_EFICIENCIA (DXI/DXB) é tipicamente **agregado** (não item-dia, a confirmar). Se o
`AMOUNT_REBATE_MELI` **carregar pix**, o pix fica item-dia; se **não**, o investimento-pix só existe
agregado (DXB) → leitura pix em grão mais grosso ou DXB usado p/ **calibrar**.

**Cofinanciamento seller (CRÍTICO):** o delta DE→POR é **cofinanciado** — `$ MELI` (DXI/DXB/AMOUNT_REBATE)
+ aporte do seller (que pode ter **inflado o preço DE**). Regras:
- **Investimento atribuído ao MELI = só a porção MELI**, nunca o delta total.
- **Competitividade real = preço POR (chegada)** — NÃO afetada por DE inflado (é o que o comprador paga/compara).
- **`dist_partida`** = **referência robusta** (preço do item em **dias sem rebate** / mediana); `ORIGINAL_PRICE`
  (DE) só **fallback** (item sempre rebatado). **V8 mostrou DE inflado:** mediana +3,5%, mas **~49% dos itens >5%**
  e **~25% >20%** acima do preço real → o DE distorceria a partida. Afeta só "quanto fechamos", não a chegada (POR real).

**Lente por competidor (RESOLVIDO — espiada de schema):**
- `DM_COM_COMPETENCIA`: pix só do **best rival** (`BEST_RIVAL_MIN_PRICE_PIX`); array `COMPETITORS` tem
  preço por competidor (MIN_PRICE/ADJUSTED/EFFECTIVE) mas **não pix limpo por competidor nomeado**.
- `BT_COM_FAVORABILITY`: **box vs pix via `FAVORABILITY_TYPE`** + favorabilidade **por competidor nomeado**
  (`COMP_RIVAL_NAME_WINNER` + array `COMPETITORS`), canônica/Shield-consistente — **sem rebate $**.
- **Decisão:** best-rival + $ + transições → **DM_COM** (autossuficiente). Competidor nomeado em box/pix →
  **JOIN** `DM_COM × BT_COM_FAVORABILITY` por `MELI_ID/ITE_ITEM_ID + TIM_DAY + SIT_SITE_ID`.
- **Custo:** BT_COM é clusterizada por `FAVORABILITY_TYPE` → cada lente (box, pix) adiciona scan; filtrar site/data/D1.

---

## 6. Definições operacionais (fórmulas)

Tudo em **R$ nativo** (réguas são razões → currency-agnostic). Para competidor `k` e lente `L` (box/pix):

```
dist_k_L      = preço_meli_L / preço_rival_k_L − 1          (>0 = MeLi mais caro)
dist_partida  = usa ORIGINAL_PRICE   (dia sem rebate: preço corrente)
dist_chegada  = usa REBATE_PRICE     (só dia com rebate)
g             = (ORIGINAL_PRICE − REBATE_PRICE) / ORIGINAL_PRICE   (tamanho do desconto)
```

**Estados** (banda de match `m`): `EXPENSIVE` se `dist > +m`; `MATCH` se `|dist| ≤ m`; `CHEAPER` se `dist < −m`.

**Parâmetros** (por faixa de ASP; Large/alto ASP = valores do deck):

| parâmetro | valor | papel |
|---|---|---|
| `m` (banda match) | **1%** (atual BPC) **e 4%** (efetiva) | rodar as duas |
| piso | **−5%** | já barato demais |
| teto (landing) | **+10%** | aterrissou longe |
| gap mínimo | **+4%** | era caro o suficiente pra valer |

**Faixa de ASP — base Shield (R$):** `<200 · 200–500 · 500–1500 · 1500–3000 · >3000` (Premium = 1500+).

**ASP de referência por item (REGRA TRAVADA):** = **mediana do preço cheio (pré-rebate, box, R$)** do
item sobre uma janela de **3 meses "normais"**, calculada **uma vez por item** e mantida **fixa** em todas
as observações item-dia (evita o item "pular" de faixa quando o rebate derruba o preço — lição do Shield:
tier pelo ASP fixo, não pelo `PRICE_MELI` diário).
- **Por que preço cheio:** usar o preço praticado (com rebate) criaria circularidade — o item mais rebatado
  cairia numa faixa mais baixa por causa do próprio tratamento.
- **Janela de referência (instância atual):** **Fev/Mar/Abr 2026.** Princípio geral (perene): 3 meses
  consecutivos normais, evitando (i) janeiro/ressaca de BF e (ii) sazonalidade forte (Dia das Mães, BF).
- **Fallback:** item com < ~30 dias de histórico na janela → "ASP de referência indefinido" (não alocado).

**Período de ANÁLISE (distinto da referência):** **Abr/Mai/Jun 2026** (junho MTD, até 27/06). É o retrato
mais atual e inclui maio (Dia das Mães), onde o duelo de preço vs Shopee é mais revelador. Como reportamos
**taxas/correlações** (não valores absolutos), o mês parcial não distorce; sem outra sazo até o fim do mês.

**Cruzamento (#3, mecânico):** a faixa de ASP é atributo **por item** → join simples em cada linha item-dia.

---

## 7. Classificação — 3 eixos (sobre o painel item-dia)

### Eixo 1 — Qualidade do investimento (dias COM rebate) — mutuamente exclusivo
| # | Caixa | Regra | Leitura |
|---|---|---|---|
| 1 | **Piso — já barato** | `dist_partida ≤ −5%` | $ sem retorno |
| 2 | **Gap pequeno** | `0 < dist_partida < +4%` | fechar não move CVR |
| 3 | **Landing alto** | `dist_chegada > +10%` | uplift baixo |
| 4 | **Zona de uplift** ✅ | `dist_partida ≥ +4%` e `dist_chegada ≤ +10%` e `dist_partida > −5%` | o bom |

→ **$ realocável = caixas 1 + 2 + 3**, com **`$ = Σ(AMOUNT_REBATE_MELI × unidades)`** (ver §5 / V1). Prioridade resolvida (caixas naturalmente exclusivas).

### Eixo 2 — Transição (dias COM rebate) — leitura Shield
- `estado_partida → estado_chegada` (ex.: `expensive→cheaper`, `cheaper→cheaper`…)
- **alvo:** `expensive→cheaper` · **tóxicos:** `cheaper→cheaper`, `match→cheaper`
- **Métrica-chave (pergunta Beatriz):** `Σ $ de rebate cuja chegada NÃO é cheaper` vs **Shopee**, aberto
  por **faixa ASP** e **lente box/pix** → "dinheiro que não virou posição vencedora vs Shopee".
  Revela $ que **ganha no box mas não no pix** (= tese Shield quantificada).
- **Saída "threshold-light" (1º entregável candidato):** `Σ $ que ficou expensive→expensive` (e
  `cheaper→cheaper`) por **D1 × faixa ASP × lente (box/pix)**. **NÃO depende dos limiares 4/5/10** — só do
  corte de match `m` (rodar m=1% e 4%). Robusta à validação do nível 4; pode sair antes dela.
- **Lente de ALAVANCA (campanha DXI) — pedido da Beatriz, dimensão-chave:** cruzar a transição com
  `DXI_CAMPAIGN_SUBTYPE` (**pré-acordo / smart cofinanced / pricing-matching / on-demand**) × ASP × competidor →
  **qual alavanca melhor vira `expensive→cheaper` vs Shopee** (= "qual lever combate mais"). Acionável: realocar
  pra alavanca que mais vira posição. Habilitado pela arquitetura (subtipo+$ do DM_EFICIENCIA × posição do DM_COM).
  Nota: PRICING_MATCHING = PM (time de Pricing); MELI banca mais por causa do **PM100%** (cobre 100% do gap).

### Eixo 3 — Exposição (dias SEM rebate) — métrica = **visitas / % SoV** (NÃO R$: não há spend)
Gradiente de oportunidade perdida por distância de preço vs competidor:

| Faixa (dia sem rebate) | Leitura |
|---|---|
| `dist ≤ m` (match/cheaper) | **Competitivo "de graça"** — ganhando sem gastar |
| +match a +10% | já no alcance — ganho barato (rebate pequeno) |
| +10% até **teto_MELI** | recuperável **só com nosso lever** |
| teto_MELI até **teto_negociado** | recuperável **com deal cofinanciado** (seller + MELI) |
| > teto_negociado | **estrutural** — fora do alcance de rebate (custo/sourcing) |

- **teto_MELI** = p90 histórico da profundidade do **rebate MELI** por faixa ASP → `1,10/(1−d)−1`.
- **teto_negociado** = p90 histórico do **desconto total** (DE→POR) por faixa ASP → idem.

---

## 8. Perímetro e recortes

**Perímetro (TRAVADO):** vertical **HE = 6 D1s** (rótulos exatos do de-para `De-Para Dominios Home
Electronics.xlsx`):
`AUDIO & GENERAL ELECTRONICS` · `HOUSEHOLD APPLIANCES PARTS` · `SMALL APPLIANCES` ·
`TELEVISIONS & STREAMING DEVICES` · `HEATING, COOLING & AIR QUALITY` · `LARGE APPLIANCES`.
Análise primária **HE × ASP** (pooled); **D1 = lente secundária** *data-gated* (ver §1 e §9).
**Party type (TRAVADO):** investimento/alavanca = **3P apenas.** 1P tem **DXI = DXB = 0** (confirmado HE mai/26:
1P R$530Mi GMV / **R$0** investimento ~22% do GMV HE; 3P R$1,9Bi / R$35,7Mi DXI) — 1P move preço por margem interna,
não por rebate auditado. 1P entra só como **contexto de competitividade** (lever invisível no dado).
> A revisar: `HOUSEHOLD APPLIANCES PARTS` (peças/spare) tem dinâmica de acessório — candidato a destacar/excluir.
> Large e Shopee **não são escopo** — são *recortes de leitura prioritários* (ação/Shield), não filtro.

**Saídas sliceáveis por:**
- **faixa ASP** (Shield, R$) · **competidor** (best rival = barra dura; Shopee/Amazon/Magalu)
- **lente** (box / pix) · **D1** (secundária) · **tempo** (perene → acompanhamento)

Régua de limiar é **competidor-agnóstica** (deck), mas o **diagnóstico** abre por competidor.

---

## 9. Validação dos limiares na nossa categoria (nível 4)
Aplicar 4/5/10 como padrão (nível 3) **e**, em paralelo, **varrer cortes por faixa de ASP** pra ver se a
virada empírica cai em 4/5/10 em cada faixa. Se uma faixa discordar (ex.: premium virar em ~7%),
**sinalizar e recalibrar só aquela faixa**. Restrição: **poder estatístico** (nº de campanhas/clusters,
espalhamento de desconto/distância) — lição do MLM (amostra fina → ruído).

---

## 10. Narrativa de apresentação (acordada)
Introdução/pergunta **deles** → slide metodológico **do que adaptamos** → **nossos resultados**.
Espinha dorsal do Data, leitura nossa.

---

## 11. Decisões TRAVADAS × pontos ABERTOS

**Travadas:**
- Instrumento perene (não one-shot); foco vs Shopee.
- Herdar causalidade p/ >70 USD; Pix é **lente** (box+pix), não premissa.
- Grão = painel item-dia único (com e sem rebate).
- Espinha DM_COM_COMPETENCIA + favorabilidade p/ box/pix + DM_EFICIENCIA p/ reconciliar.
- Investimento: box↔DXI, pix↔DXB.
- 3 eixos de classificação; parâmetros m=1%&4%, piso −5%, teto +10%, gap +4%.
- Caminho de rigor 3+4 (2 upgrade, 1 via Data).
- **ASP de referência** = mediana do preço cheio, 3 meses normais (instância: **Fev/Mar/Abr 2026**), fixo por item.
- **Janelas:** referência ASP = Fev/Mar/Abr 2026 · **análise = Abr/Mai/Jun 2026 (Jun MTD até 27/06)**.
- **Perímetro:** HE = 6 D1s (de-para) · análise HE × ASP, D1 secundária data-gated · Large/Shopee = leitura, não escopo.
- **Eixo 1 — prioridade:** caixas são **naturalmente quase exclusivas** (rebate só baixa preço → g1<g0); ordem piso → gap pequeno → landing alto → zona; edge "match na partida / −5%<g0<0" cai em zona (ou bucket "neutro" opcional).
- **Eixo 3:** métrica = **visitas/% SoV**; gradiente com 2 tetos (teto_MELI = p90 rebate MELI; teto_negociado = p90 desconto total); competitivo "de graça" = dist≤m.
- **Cofinanciamento:** investimento = só porção MELI; competitividade = preço POR (chegada); **`dist_partida` = referência robusta (não-rebate)** — DE só fallback (V8: DE inflado, ~25% dos itens >20%).
- **Investimento (V1 TRAVADO):** fonte = `DM_EFICIENCIA` (box = **DXI** [Desconto por Ítem, todos subtipos: PRE_ACORDO ~69% + ON_DEMAND/PRICING_MATCHING/SMART]; pix = DXI + **DXB-Pix**; $ realizado, grão ordem-item).
- **Posição/lente por competidor:** best-rival → DM_COM; competidor nomeado (box/pix) → BT_COM_FAVORABILITY. Junta tudo por `ITE_ITEM_ID/MELI_ID + dia (+site)`.

**Abertos (restantes):**
- ✅ Desenho fechado. Resta só o **gate de execução:** validações de dado (§12, V1–V8) antes do 1º número.

---

## 12. Validações de dado pendentes (antes de qualquer número oficial)
- **V1 — parte 1 ✅ (maio/2026):** `AMOUNT_REBATE_MELI` é **por unidade** (identidade MeLi+Seller=DE−POR, mediana 1,0;
  ~3,1% do preço; MELI ~10% do desconto, seller ~90%). $ = Σ(campo × unidades).
- **V1 — parte 2 ✅ (HE, maio/2026):** DXI MELI R$35,7Mi / seller R$249,1Mi (MELI ~12,5%); DXB-Pix MELI R$9,8Mi
  (~27% do DXI MELI, **fora** do AMOUNT_REBATE_MELI). DXI = Desconto por Ítem (PRE_ACORDO 69% + ON_DEMAND 15% +
  PRICING_MATCHING ~11,5% + SMART 4%). → **TRAVADO: investimento de `DM_EFICIENCIA`** (box=DXI, pix=DXI+DXB-Pix);
  DM_COM = posição. **✅ V1 FECHADA.**
- **V2 ✅ (HE, mai/26):** cobertura de preço **100%** (MELI+rival) em box e pix p/ Shopee/Amazon/Magalu → lente
  pix viável. Shopee com menos linhas (~120k) mas alto volume de visitas (~385M) → ok em HE; afina em D1×ASP (data-gate).
- **V3 ✅ (HE, 1ª sem mai/26):** preços DM_COM × BT_COM batem **99,998%** (dentro de 1%; mediana de diferença = 0)
  em ~1,05M item-dias → join consistente.
- **V4 (resolvido):** rótulos D1 exatos vêm do de-para (6 D1s) → usar match exato, não LIKE.
- **V7:** **NÃO** excluir H&B (consistente com Shield).
- **V8 ✅ (HE, mai/26):** DE (`ORIGINAL_PRICE`) inflado vs preço real (dias sem rebate): mediana +3,5%, **~49% >5%**,
  **~25% >20%** (80,6k itens c/ ambos). → **partida = referência robusta**, não o DE bruto (DE só fallback).
- **p90 dos tetos (Eixo 3):** profundidade histórica de desconto por faixa ASP — `teto_MELI` (porção MELI)
  e `teto_negociado` (desconto total DE→POR). Usar p90 empírico, **não** os 3-7% de palpite.

---

## 13. Dependência externa — time de Data (nível 1)
Mensagem enviada pedindo: **(a)** notas metodológicas, **(b)** código/notebook Python do modelo,
**(c)** query/dataset do painel (idealmente re-rodável p/ outra cesta). **Pergunta extra:** o `g`/Treatment
deles usou o **desconto TOTAL ou só a porção MELI**? Como trataram o **DE inflado**? Em paralelo, tocamos
3+4 do nosso lado. Se vier algo reaproveitável, reavaliamos a rota.

---

## 14. Limitações
- Sem A/B nosso → **causalidade limpa não é reproduzível por nós**; níveis 2–4 são associação ajustada /
  descritivo (aplicam o veredito causal do Data).
- Depende da qualidade/cobertura do scraping de preço.
- Rebates seller-funded (`AMOUNT_REBATE_SELLER`) fora do "$ MELI".
- Pooling de HE assume efeito comparável entre sub-categorias → ASP entra como segmento, não premissa.

---

## 15. Atualização — migração p/ a base do Pricing + funil (Q2 2026)

**Data:** 2026-07. Após receber as 8 queries do time de Pricing, a análise de **box** migrou p/ a base validada deles. Isto **SUPERSEDE** as seções 5–9 onde houver conflito (ex.: banda ±4%, ASP fixo Fev/Mar/Abr).

- **Fonte (box):** `SBOX_REVENUEMKPBR.SITUACAO_REBATE_TESTE` (saída da query #7 do Pricing) — rebate decomposto item×dia×campanha, já chancelado. É um **pipeline de 7 etapas** (favorabilidade limpa → estado dia-antes "_SUJO" → estado durante "_TOTAL_SUJO_2" → cola $ → hound → consolida).
- **Investimento = `CP_INVESTMENTS_LC`**, que em HE **é idêntico ao DXI** (auditado: 35,65 = 35,65 Mi, mai/26). **Pix (DXB-Pix) está FORA** dessa base → é camada nossa, à parte (Pix = fase seguinte).
- **Banda de posição = ±1%** (Pricing/BPC). O ±4% do Data serve p/ correlacionar CONVERSÃO, não p/ classificar posição — decisão da Beatriz.
- **Transição:** partida = dia ANTES do rebate (`START_DATE_REBATE−1`); chegada = durante. `exp→cheaper` = virou p/ barato **ou empate** (o balde une cheaper+match; separar exige ajuste no Pricing).
- **Renomeação:** "não vencedor" → **"com erro de leitura"** (item SEM preço de rival no dia — `COMP_PRICE_RIVAL` nulo — NÃO é exp→exp). Absorve o resíduo de join (~R$7 Mi).
- **Funil (estrutura travada):**
  - **Camada 1** — partição de 100% do DXI: `exp→exp · exp→cheaper/match · cheaper→cheaper · fora do hound · com erro de leitura` (R$ e %; nº de itens fica p/ quando re-rodarmos c/ COUNT DISTINCT).
  - **Camada 2** — quebras por **D1 / alavanca / ASP**, **só** os 3 baldes com status de preço (exclui fora do hound + erro de leitura = "problema de leitura/cobertura", não de competitividade).
- **ASP (RESOLVIDO 2026-07):** trocada a referência FIXA Fev/Mar/Abr por **preço MELI na MESMA janela (Q2)** — mediana da favorability (box, produto), com **fallback NMV/NSI da `DM_EFICIENCIA`** (cobre todo item vendido). "Sem ASP" caiu de ~R$40 Mi p/ **R$ 0,1 Mi** (~0). Buraco fechado. Off-target (fora hound + erro leitura) segue saindo na Camada 1.
- **Período:** Q2 (Abr–Jun 2026), pela consistência da base.
- **Achados-chave (Q2, box):** DXI total R$113,8 Mi; off-target (fora hound 16,2 + erro leitura 30,8) = R$47 Mi; no hound c/ status = R$66,6 Mi; **PM (price matching) vira ~55%** (mais eficiente); **pré-acordo** domina o gasto e vira ~22%. Rival do box = **Amazon** (não Shopee → reforça tese de que Shopee é no Pix).
- **Entregável:** funil interativo (filtro D1/ASP) no Grid `01KW89RWFKQ9YQQTJMSQRZYVEP`.
- **CVR:** segue adiado (validação com Data).

---

## 16. Pix — step 2 (kickoff p/ o próximo chat)

**Objetivo:** replicar o funil na lente **Pix**, onde deve morar a disputa vs Shopee (no box a Shopee é só 5-8% do gasto; o rival do box é a Amazon). Camada **NOSSA, fora da base do Pricing** (que é box/DXI).

**Fontes (todas WHOWNER — a bq CLI do bdacache LÊ; não precisa do sandbox do Pricing):**
- **Investimento Pix** = `meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB`: `DXB_INVESTMENT_LC` com `DXB_PAYMENT_METHOD='PIX'` (~R$9,8Mi/mês HE, ~27% do DXI). Campanha em `DXB_CAMPAIGN_ID`. Filtros: `VERTICAL='HOME ELECTRONICS'`, 3P, Q2 (Abr–Jun 2026). Contexto box junto = `DXI_INVESTMENT_LC` / `CP_INVESTMENTS_LC`.
- **Posição Pix** = `meli-bi-data.WHOWNER.BT_COM_FAVORABILITY` com `FAVORABILITY_TYPE='BOX_ALL_ABC_PIX'` (a de box é `'BOX_ALL_ABC'`): `PRICE_MELI`, `COMP_PRICE_RIVAL`, `COMP_SITE_ID_WINNER` (SPE/AMB/MGL…), `VISITS_DAY`, `MELI_ID_TYPE='PRODUCT'`.
- **ASP de referência** = mesma janela Q2 (mediana da favorability PIX + fallback NMV/NSI da DM_EFICIENCIA) — zera o "sem ASP", igual fizemos no box.

**Consistência com o box (manter):** banda ±1%; mesmas faixas de ASP; mesmo funil (Camada 1 = 5 categorias somando 100%; Camada 2 = quebras só no hound por D1/alavanca/ASP); renomeação "erro de leitura"; foco no recorte **Shopee-winner**.

**1ª decisão do chat novo:** **Pix "leve"** (posição caro/empate/barato ±1% + gasto DXB-Pix, por ASP × alavanca × competidor, foco Shopee-winner) — **recomendado** — vs **Pix "completo"** (replicar a transição partida→chegada também no Pix; mais caro/complexo, porque o Pricing NÃO entrega Pix pronto — teríamos que reconstruir).

**Artefatos do box (congelado):** Grid `01KW89RWFKQ9YQQTJMSQRZYVEP` (v10) + HTML `Documents\Claude\Projects\BPC\Price-Point\Funil_Box_Grid.html`. NÃO precisa mexer no box p/ o Pix.
