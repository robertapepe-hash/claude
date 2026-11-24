# Shield Against Shopee — Contexto Mestre

Documento de referência consolidado do projeto Shield Against Asians (vs Shopee) da vertical H&T em MLB.
Autora: Beatriz Dacache · Última atualização: 26/05/2026.

Serve como ponto de partida para qualquer continuação do projeto — em outra ferramenta ou outra conversa.

---

## 1. Visão geral

Análise de **competitividade de preço (BPC)** da vertical **H&T (Home Electronics + Technology)** no site **MLB** vs **Shopee (SPE)**, no contexto do squad "Shield Against Asians" do War Room mensal H&T.

Beatriz Dacache é o apoio analítico com leitura de BPC vs SPE. O foco principal dela em paralelo é BPC HE vs Magalu (projeto separado, em outro contexto).

Cadência de entrega: **QBR mensal** com diretoria H&T.

A análise sempre passa por 3 lentes:
- **BOX** (preço à vista — `BOX_ALL_ABC`)
- **SHP** (frete — `SHP_ALL_ABC`)
- **PIX** (preço PIX — `BOX_ALL_ABC_PIX`)

E por 5 faixas de ASP. Perguntas recorrentes: "como estamos vs Shopee?", "onde mora a oportunidade?", "qual seller/marca está puxando pra baixo?".

---

## 2. Tabelas BigQuery utilizadas

| Tabela | Uso |
|---|---|
| **`meli-bi-data.WHOWNER.BT_COM_FAVORABILITY`** | **Principal.** BPC, visits matched/cheaper/equal/expensive, preço Meli, preço competidor, marca, D1/D2, seller, segmento, vertical, item title. Particionada por `TIM_DAY`, clusterizada por `MELI_ID_TYPE`, `FAVORABILITY_TYPE`, `SIT_SITE_ID`, `COMP_RIVAL_NAME_WINNER`. |
| `meli-bi-data.WHOWNER.LK_MKP_ITEMS_SORTING_FEATURES` | Backup pra item title/brand. Descontinuado — a view de BT_COM_FAVORABILITY já tem `TITLE`/`BRAND`/`REAL_BRAND`/`PERMALINK` enriquecidos. |

**Tabelas testadas mas descartadas:**
- `LK_BT_ITE_ITEMS_TITLE` (não existe)
- `DM_ITE_ITEMS_SUBSET` (sem permissão de acesso)
- `LK_ITE_ITEMS_PICTURES` (não tem `ITE_ITEM_TITLE`)

**Importante:** A view em `WHOWNER` é **enriquecida** — tem ~50 colunas extras vs o schema raw do source:
- Identificação: `TITLE`, `BRAND`, `REAL_BRAND`, `PERMALINK`
- Seller: `CUS_NICKNAME`, `CUS_CUST_ID_SEL`, `SEGMENTO`, `SEGMENTO_SELLER_DETAIL`, `ASESOR`, `ASESOR_LDAP`
- Categoria: `VERTICAL`, `DOMAIN`, `DOM_AGG_1`, `DOM_AGG_2`, `DOM_AGG_3`
- Flags: `KMI`, `TMI`, `KVI`, `FLG_BULKY`, `FLG_COMP_1P`, `FLG_COMP_3P`, `FLG_COMP_CBT`, `FLG_BRANDED`, `FLG_BUYBOX`, `FLG_SUPERMARKET`
- Comerciais: `COMBO_ID`, `MAX_CUOTAS_SIN_INT_MELI`, `MAX_CUOTAS_SIN_INT_COMPETITOR_WINNER`, `SAP_VENDOR_ESTIMATED`, `NMV`, `NMV_L30D`

---

## 3. Métricas calculadas

Todas derivam dos 4 contadores de visitas (`VISITS_MATCH`, `VISITS_CHEAPER`, `VISITS_EQUAL`, `VISITS_EXPENSIVE`):

| Métrica | Fórmula | Direção |
|---|---|---|
| **BPC** | `(VISITS_CHEAPER + VISITS_EQUAL) / VISITS_MATCH` | ↑ melhor |
| **Opportunity** | `VISITS_EXPENSIVE / VISITS_MATCH` = `1 − BPC` | ↓ melhor |
| **Share of Opportunity (SoO)** por competidor X | `SUM(VISITS_EXPENSIVE WHERE COMP_SITE_ID_WINNER='X') / SUM(VISITS_MATCH total D1)` | ↓ melhor (em pp) |
| **MoM** | diferença simples em **pontos percentuais** (pp) — nunca decimal | sinal indica direção |
| **MS Ratio** | `Market Share Shopee / Market Share Meli` | ↓ melhor |
| **SOB** | Share of Business (peso da subcategoria no total) | dimensional |

### Visões de competidor (importante)

- **Winner view** → `COMP_SITE_ID_WINNER = 'X'` (nível raiz). Usado para SoO e BPC vs Winner.
- **All-items view (UNNEST)** → `UNNEST(COMPETITORS) c WHERE c.COMP_SITE_ID = 'X'`. Usado para BPC vs X "total" — todas as visitas em que X aparece, não só quando ganha.

### Atribuição ponderada (cascata vs total da vertical)

```
impact_HE_pp = Δbpc_unit × (visits_unit / visits_universe)
```

Usado pra dimensionar quanto um movimento numa célula (D1/marca/seller) move o BPC da vertical.

---

## 4. Filtros que se repetiram

| Campo | Valor padrão |
|---|---|
| `SIT_SITE_ID` | `'MLB'` (sempre) |
| `MELI_ID_TYPE` | `'PRODUCT'` (sempre — cluster field, reduz scan drasticamente) |
| `FAVORABILITY_TYPE` | `'BOX_ALL_ABC'` (preço) · `'SHP_ALL_ABC'` (frete) · `'BOX_ALL_ABC_PIX'` (pix) |
| `DOM_AGG_1` | uma das 6 D1s monitoradas (listadas abaixo) |
| **Janelas temporais** | **Mai MTD vs Abr MTD** (1-19 mesma janela) · **Mar/Abr fechado** (referência histórica) · **Datas duplas** (3.3, 4.4, 5.5) |
| Faixas ASP (via `PRICE_MELI`) | `< 200` · `200–500` · `500–1500` · `1500–3000` · `> 3000` |
| Competidor (UNNEST) | `COMP_SITE_ID = 'SPE'` (foco Shopee) |
| Segmento seller | `ITEM_PARTY_TYPE = '3P'` (3P puro) **ou** `SEGMENTO_SELLER_DETAIL != 'FIRST PARTY'` (3P + CBT) **ou** `SEGMENTO_SELLER_DETAIL = 'ASESORADO PF'` (carteira assessorada) |

**Sem filtros** (convenção da Bia): nada de `KMI`, `H&B`, vertical — tudo na conta. Exceto quando explicitamente pedido.

---

## 5. Subcategorias, sellers e marcas

### D1s monitoradas (nomes exatos da BT_COM_FAVORABILITY)

| Vertical | D1s |
|---|---|
| **Home Electronics** | `LARGE APPLIANCES` · `HEATING, COOLING & AIR QUALITY` · `AUDIO & GENERAL ELECTRONICS` |
| **Technology** | `IT PERIPHERALS, PARTS & ACCESSORIES` · `SMARTPHONES & TABLETS` · `WEARABLES` |

### Códigos de competidor (`COMP_SITE_ID`)

| Código | Competidor | Status no projeto |
|---|---|---|
| `SPE` | Shopee | Foco principal |
| `AMB` | Amazon | Maior ofensor real em todas as 6 D1s |
| `MGL` | Magalu | Acompanhamento secundário |
| `CBH` | Casas Bahia | Vetor pequeno |
| `ALB` | Aliexpress | Bucket "Others" |
| `AMR` | Americanas | **EXCLUÍDA** por decisão da Bia |

### Marcas analisadas (Large App 500-1500 BOX vs PIX)

`HQ` · `PHILCO` · `ELECTROLUX` · `ITATIAIA` · `NEWMAQ` · `BRITÂNIA` (com e sem acento — banco tem ambos) · `SUGGAR` · `COLORMAQ` · `DAKO`

Para match correto:
```sql
UPPER(COALESCE(REAL_BRAND, BRAND)) IN ('BRITÂNIA','BRITANIA', ...)
```

### Sellers agrupados (deep dive)

| Grupo | `CUS_CUST_ID_SEL` |
|---|---|
| **Engage** | 515427923, 473841624, 1151689751 |
| **REDE Marketplace** | 2355501248, 638325656 |

### Sellers do plano de blindagem H&C (contexto War Room)

WebContinental · Climario · Frio Peças · Belmicroshop · Lojas Guaibim · Carajás · Sipolatti · Bemol · Centralar · Continentalcenter · Leveros · Oficialelectrolux · Dufrio.

### Lista de 16 MELI_IDs analisados em deep dive item-level (Large App)

```
14815387, 18363110, 19119490, 19481428, 20960488, 26208554,
29586013, 34784721, 35352522, 3574533842, 38478684, 41208451,
41353416, 60867859, 62700443, 8742310
```

Sendo: 15 são `MELI_ID_TYPE='PRODUCT'` (microondas, fogões, cooktops, lavadoras, frigobares de Electrolux, Philco, Suggar, Itatiaia, Colormaq, Dako, Britânia, HQ, Praxis). O ID `3574533842` não é PRODUCT (volume irrelevante).

---

## 6. Regras de negócio (ensinadas pela Bia)

1. **MS Ratio é Market Share Shopee / Market Share Meli** — não NSI Ratio, não outra coisa.

2. **SOB = Share of Business** (não Share of Bidding).

3. **Faróis semafóricos** (status competitivo):

| Farol | Critério |
|---|---|
| 🔴 **Issue** | Tendência Meli negativa **e** Shopee positiva |
| 🟡 **Attack** | Tendências iguais, Shopee ganha MS Ratio **e** Ratio > 10% |
| ⚪ **Wait & See** | Tendências iguais, Shopee ganha MS Ratio **e** Ratio < 10% |
| 🟢 **Controlled** | Meli melhor que Shopee, ou iguais e Shopee não ganha > +0,5pp |

4. **"BPC vs Shopee Winner"** → usar `COMP_SITE_ID_WINNER='SPE'` (winner view, nível raiz).

5. **"BPC vs Shopee all items / total"** → usar `UNNEST(COMPETITORS) WHERE COMP_SITE_ID='SPE'` (não winner). Diferença crucial.

6. **Convenção ASP fixa para War Room Shopee**: `<200`, `200-500`, `500-1500`, `1500-3000`, `>3000` (substituiu a versão antiga `<79`, `79-200`, etc.).

7. **MoM sempre em pp**, nunca decimal. Valores em pp = `valor_decimal × 100` quando escrever em xlsx/pptx.

8. **AMR (Americanas) excluída** de todas as análises por decisão da Bia.

9. **MELI_IDs vs ITE_ITEM_IDs**:
   - `MELI_ID` é product-level (1 produto = vários items)
   - `ITE_ITEM_ID` é item específico do seller
   - Quando a Bia manda lista de IDs, geralmente são `MELI_ID` (product)
   - Filtrar por `MELI_ID_TYPE = 'PRODUCT'` quando agregando

10. **`ITEM_PARTY_TYPE = '3P'`** ≠ **`SEGMENTO_SELLER_DETAIL != 'FIRST PARTY'`**: o segundo inclui CBT, que puxa o BPC pra baixo. Decidir conforme contexto.

11. **Dentro do array `COMPETITORS`**: campo de preço é **`COMP_ITEM_PRICE`** (não `COMP_PRICE_RIVAL`, que é o nome no nível raiz). Cuidado.

12. **Anomalias conhecidas em `SHP_ALL_ABC`**: scrapers de frete às vezes "perdem" um competidor em datas específicas (Magalu sumiu em Mai inteiro; Shopee sumiu em 03/03 inteiro). Sempre validar volumes antes de ler delta.

13. **Limite scan BigQuery**: 100 GB por query. Quando passar, **adicionar `MELI_ID_TYPE='PRODUCT'` como filtro** (cluster pruning) reduz tipicamente 60-70%.

14. **Convenção de formatação executiva**:
    - Números absolutos: abreviar com K / Mi / Bi
    - Percentuais: 1 casa decimal, vírgula (ex: "47,1%")
    - Deltas: em pp com sinal (ex: "+8,3 pp", "-2,7 pp")

---

## 7. Entregáveis produzidos

Todos em `/mnt/BPC/` (workspace folder do usuário):

| Arquivo | O que é |
|---|---|
| `Shield_BPC_Items_vs_Shopee.html` | Dashboard interativo: dropdown de 15 MELI_IDs · evolução semanal BPC vs Shopee · preço Meli + preço Shopee · tabela de sellers que compõem o BPC do item |
| `Shield_BPC_D1_vs_Shopee_Mai_vs_Abr_2026_v4.xlsx` | Xlsx oficial: 1 aba por D1 (6 D1s) · bloco preto (BPC + Opp + SoO 5 competidores) · bloco laranja (BPC vs Shopee Winner por ASP) · seção SoO Shopee aberta por faixa ASP · refs Mar/Abr fechado · dados raw |
| `Shield_HE_Mai_2026.pptx` + `.pdf` | Deck Home Electronics: slide overview + slide heatmap |
| `Shield_Tech_Mai_2026.pptx` + `.pdf` | Deck Technology: slide overview + slide heatmap |
| Shield PDFs no Grid | doc_id HE: `01KS5XRQ9BY2VSX5W46EWBDF2T` · Tech: `01KS5XRZEWWNM3T7QVHAKHBF3M` |

### Análises ad-hoc entregues por chat (sem arquivo)

- BPC semanal item × seller (16 MELI_IDs) vs Shopee, Mar-Mai
- BPC marcas Large App 500-1500 (BOX vs PIX) Mai MTD vs Abr MTD
- BPC Large App 3P por ASP nas datas duplas (3.3, 4.4, 5.5) — BOX, SHP, PIX
- BPC Large App 3P sem First Party Mai MTD (33,1%)
- BPC sellers Engage + REDE Marketplace (SHP + PIX) por mês

---

## 8. Templates de query (reutilizáveis)

### Template A — BPC por D1 × período × competidor (UNNEST view)

```sql
WITH base AS (
  SELECT
    f.DOM_AGG_1 AS d1,
    CASE
      WHEN f.TIM_DAY BETWEEN DATE '2026-05-01' AND DATE '2026-05-19' THEN 'MAI_MTD'
      WHEN f.TIM_DAY BETWEEN DATE '2026-04-01' AND DATE '2026-04-19' THEN 'ABR_MTD'
    END AS periodo,
    c.COMP_SITE_ID AS competidor,
    c.VISITS_MATCH AS v_match,
    c.VISITS_CHEAPER + c.VISITS_EQUAL AS v_fav,
    c.VISITS_EXPENSIVE AS v_exp
  FROM `meli-bi-data.WHOWNER.BT_COM_FAVORABILITY` f,
       UNNEST(f.COMPETITORS) c
  WHERE f.SIT_SITE_ID = 'MLB'
    AND f.MELI_ID_TYPE = 'PRODUCT'
    AND f.FAVORABILITY_TYPE = 'BOX_ALL_ABC'
    AND f.DOM_AGG_1 IN ('LARGE APPLIANCES', 'HEATING, COOLING & AIR QUALITY', '...')
    AND c.COMP_SITE_ID = 'SPE'
    AND f.TIM_DAY BETWEEN DATE '2026-04-01' AND DATE '2026-05-19'
)
SELECT d1, periodo, competidor,
  SUM(v_match) AS v_match,
  SUM(v_fav)   AS v_fav,
  SUM(v_exp)   AS v_exp,
  SAFE_DIVIDE(SUM(v_fav), SUM(v_match)) AS bpc
FROM base
GROUP BY 1, 2, 3
ORDER BY 1, 2, 3;
```

### Template B — Bloco preto (Winner view + Share of Opportunity)

```sql
SELECT
  DOM_AGG_1 AS d1,
  CASE
    WHEN TIM_DAY BETWEEN DATE '2026-05-01' AND DATE '2026-05-19' THEN 'MAI'
    WHEN TIM_DAY BETWEEN DATE '2026-04-01' AND DATE '2026-04-19' THEN 'ABR'
  END AS periodo,
  CASE
    WHEN COMP_SITE_ID_WINNER = 'SPE' THEN 'Shopee'
    WHEN COMP_SITE_ID_WINNER = 'AMB' THEN 'Amazon'
    WHEN COMP_SITE_ID_WINNER = 'MGL' THEN 'Magalu'
    WHEN COMP_SITE_ID_WINNER = 'CBH' THEN 'CasasBahia'
    ELSE 'Others'
  END AS competidor,
  SUM(VISITS_MATCH)                  AS v_match,
  SUM(VISITS_CHEAPER + VISITS_EQUAL) AS v_fav,
  SUM(VISITS_EXPENSIVE)              AS v_exp
FROM `meli-bi-data.WHOWNER.BT_COM_FAVORABILITY`
WHERE SIT_SITE_ID = 'MLB'
  AND MELI_ID_TYPE = 'PRODUCT'
  AND FAVORABILITY_TYPE = 'BOX_ALL_ABC'
  AND DOM_AGG_1 IN ('...')
  AND TIM_DAY BETWEEN DATE '2026-04-01' AND DATE '2026-05-19'
GROUP BY 1, 2, 3;
```

### Template C — ASP buckets (snippet pra reusar)

```sql
CASE
  WHEN PRICE_MELI < 200  THEN '< 200'
  WHEN PRICE_MELI < 500  THEN '200-500'
  WHEN PRICE_MELI < 1500 THEN '500-1500'
  WHEN PRICE_MELI < 3000 THEN '1500-3000'
  WHEN PRICE_MELI >= 3000 THEN '> 3000'
END AS asp_bucket
```

### Template D — Filtro de marca (com acento + variações)

```sql
WHERE UPPER(COALESCE(REAL_BRAND, BRAND)) IN (
  'HQ','PHILCO','ELECTROLUX','ITATIAIA','NEWMAQ',
  'BRITÂNIA','BRITANIA','SUGGAR','COLORMAQ','DAKO'
)
```

### Template E — Agrupamento de sellers (CUS_CUST_ID_SEL)

```sql
CASE
  WHEN CUS_CUST_ID_SEL IN (515427923, 473841624, 1151689751) THEN 'Engage'
  WHEN CUS_CUST_ID_SEL IN (2355501248, 638325656)            THEN 'REDE Marketplace'
END AS seller_group
```

---

## 9. Contatos do projeto

- **Beatriz Dacache** — focal BPC HE/MLB, autora deste documento
- **Sebah Marques** — Brands, marcas prioritárias
- **Felipe Lopardo** — Farming / Asesorado PF
- **Renato Prado Valentin** — Mondial brand
- **Squad Shield**: Ana Beatriz Carneiro Fernandes, Julia De Cassia Arcoverde, Luiza Gaburo, Maira, Daphne, Giovanna

---

*Documento gerado em 26/05/2026.*
