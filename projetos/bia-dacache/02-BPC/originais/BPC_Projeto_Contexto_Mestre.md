# Projeto BPC — Contexto Mestre

Documento de referência para todas as tasks dentro do projeto BPC. Atualizado em 2026-05-15. Autora: Beatriz Dacache.

---

## 1\. Quem sou eu e o que faço

**Beatriz Dacache** — focal de BPC (Buyer Price Competitiveness) para a vertical **Home Electronics (HE) em MLB**.

Responsável por:

- Diagnóstico de competitividade em PIX KMI da vertical
- Plano de ação tático com Brands, Farming e Pricing
- Comunicação com diretoria \+ VP sobre estado da vertical
- Coordenação do War Room BPC HE
- Apoio em frente Shield Against Asians (squad)

Times principais com quem falo:

- **Direção HE** (macro)
- **Brands** (Sebah Marques — marcas prioritárias)
- **Farming/Asesorado PF** (Felipe Lopardo — carteira de sellers)
- **Pricing** (programa PIX Match, paridade, elegibilidade)
- **Renato Prado Valentin** (Mondial marca)

---

## 2\. Definições e fórmulas

### BPC (Buyer Price Competitiveness)

`BPC = (VISITS_CHEAPER + VISITS_EQUAL) / VISITS_MATCH`

Quanto **maior**, melhor (mais vezes Meli ≤ competidor).

### Oportunidade (visits expensive share)

`Opp = VISITS_EXPENSIVE / VISITS_MATCH = 100% - BPC`

Soma das oportunidades por competitor winner \= 100% \- BPC total da categoria.

### Atribuição ponderada

`impact_HE_pp = Δbpc_unit × (visits_unit / visits_universe)`

Usado pra dimensionar quanto um movimento numa célula (D1/marca/seller) move o BPC da vertical (ou do universo vs MGL).

### Cascata de impacto vs MGL

```
+X pp BPC unit vs MGL
  → impacto em vs MGL agregado = X × (visits_unit / total_vs_MGL)
  → impacto na vertical ≈ X × (visits_unit / total_vs_MGL) × (vs_MGL / vertical)
```

Hoje peso de **MGL Winner em HE ≈ 20%** (287 Mi de 1.436 Mi visits).

---

## 3\. Tabelas principais

### BT\_COM\_FAVORABILITY (`meli-bi-data.WHOWNER`)

Tabela central de BPC. Granularidade: item × dia × metodologia.

Campos-chave:

- `ITE_ITEM_ID` — chave de join
- `SIT_SITE_ID` — site (filtrar 'MLB')
- `FAVORABILITY_TYPE` — metodologia (ver §4)
- `TIM_DAY` — data
- `KMI` — string 'true' (lowercase)
- `FLG_BULKY` — string 'true' \= H\&B (Heavy & Bulky)
- `DOM_AGG_1` / `DOM_AGG_2` / `DOM_AGG_3` — D1/D2/D3
- `BRAND` / `REAL_BRAND` — marca (usa COALESCE(REAL\_BRAND, BRAND))
- `CUS_NICKNAME` / `CUS_CUST_ID_SEL` — seller
- `SEGMENTO` — SELLER DEV / TO / CARTERA GESTIONADA
- `SEGMENTO_SELLER_DETAIL` — SD ASESORADO, ASESORADO PF, CBT ASESORADO, etc.
- `ITEM_PARTY_TYPE` — '1P' ou '3P'
- `FLG_COMP_1P` / `FLG_COMP_3P` / `FLG_COMP_CBT` — flags do competidor
- `COMP_SITE_ID_WINNER` — competidor winner (top-level)
- `COMP_RIVAL_NAME_WINNER` — nome winner
- `COMPETITORS` — ARRAYcom todos competidores matched (use UNNEST)
- `VISITS_MATCH` / `VISITS_CHEAPER` / `VISITS_EQUAL` / `VISITS_EXPENSIVE`

### DM\_EFICIENCIA\_MLB (`meli-bi-data.WHOWNER`)

Granularidade: pedido × item × dia.

Campos-chave:

- `ITE_ITEM_ID` — join com BT\_COM\_FAVORABILITY
- `ORD_CLOSED_DT` — data do pedido (DATE)
- `ORD_ORDER_ID` — pedido
- `SHIPPING_MODE` — me1 / me2
- `PICKING_TYPE` — FBM / XD / FLEX / DS / OTHER
- `LOGISTIC_TYPE` — fulfillment / cross\_docking / xd\_drop\_off / self\_service / drop\_off
- `RECEIVER_STATE` — UF destino (formato `BR-SP`)
- `F_NMV_LC` — NMV em moeda local
- `F_NSI` — NSI
- `ITE_ITEM_UNIT_PRICE` / `ITE_ITEM_FULL_UNIT_PRICE` — preços

**ASP do item** \= SUM(F\_NMV\_LC) / SUM(F\_NSI)

---

## 4\. Metodologias BPC

| Tipo | Significado | Quando usar |
| :---- | :---- | :---- |
| `BOX_ALL_ABC` | Preço à vista | Visão padrão BOX |
| `BOX_ALL_ABC_PIX` | Preço à vista PIX | **Padrão War Room KMI HE** |
| `SHP_ALL_ABC` | Frete | Análise de competitividade de frete |
| `BOX_MATCH_SELLER` | Apples-to-apples (mesmo seller) | Comparação específica |

---

## 5\. Filtros padrão e nomenclaturas

### Filtros padrão War Room HE

- `SIT_SITE_ID = 'MLB'`
- `FAVORABILITY_TYPE = 'BOX_ALL_ABC_PIX'`
- `KMI = 'true'`
- `COALESCE(FLG_BULKY, 'false') != 'true'` (sem H\&B)
- D1 IN (6 D1s de HE — ver §6)

### Período convenções

- **Q1'26** \= 2026-01-01 a 2026-03-31 (Q1 fechado)
- **Quarter QTD** \= primeiro dia do trimestre corrente até o último dia disponível na base
- **MTD** \= primeiro dia do mês corrente até o último dia disponível na base (geralmente D-1 ou D-2)
- **Datas Duplas** \= datas onde dia \= mês (03/03, 04/04, 05/05, etc.) — eventos de pricing

### Competidores principais MLB

- `AMB` \= Amazon
- `MGL` \= Magalu
- `SPE` \= Shopee
- `CBH` \= Casas Bahia
- `AMR` \= Americanas (**EXCLUIR** das análises — irrelevante por decisão da Bia)

### D1s de Home Electronics (6)

1. SMALL APPLIANCES
2. LARGE APPLIANCES
3. HEATING, COOLING & AIR QUALITY
4. AUDIO & GENERAL ELECTRONICS
5. TELEVISIONS & STREAMING DEVICES
6. HOUSEHOLD APPLIANCES PARTS

### Regiões Brasil (mapeamento RECEIVER\_STATE)

- **Norte**: BR-AC, BR-AM, BR-AP, BR-PA, BR-RO, BR-RR, BR-TO
- **Nordeste**: BR-AL, BR-BA, BR-CE, BR-MA, BR-PB, BR-PE, BR-PI, BR-RN, BR-SE
- **Centro-Oeste**: BR-DF, BR-GO, BR-MS, BR-MT
- **Sudeste**: BR-ES, BR-MG, BR-RJ, BR-SP
- **Sul**: BR-PR, BR-RS, BR-SC

### Segmento Seller (SEGMENTO\_SELLER\_DETAIL)

- `ASESORADO PF` — carteira assessorada **Paid Farming** (foco principal)
- `SD ASESORADO` / `SD NO ASESORADO` — **Seller Dev** (seller em desenvolvimento), assessorado ou não
- `CBT ASESORADO` / `CBT NO ASESORADO` / `CBT MT ASESORADO` — Cross Border Trade
- `FIRST PARTY` — 1P
- `ASESORADO` — genérico

### Visões competitor

- **Winner view** (`COMP_SITE_ID_WINNER = 'XXX'`) — só quando esse competidor é o melhor do match
- **UNNEST view** (`UNNEST(COMPETITORS) C WHERE C.COMP_SITE_ID = 'XXX'`) — todas as visits onde o competidor aparece, mesmo sem ser winner

Pra War Room MGL: **Winner view** é a referência.

---

## 6\. Workstreams ativas

### A) War Room BPC PIX KMI HE

**Objetivo**: Fechar gap em PIX KMI HE atacando o ofensor estrutural MGL.

**Status Q2 QTD 2026**:

- BPC HE PIX KMI w/o H\&B \= \~47%
- BPC vs MGL Winner em HE \= **32,8%** (60-pp gap)
- **D1 foco**: SMALL APPLIANCES (50% do universo vs MGL, BPC vs MGL 29,4%)
- **D2 foco**: KITCHEN (74% de Small, BPC vs MGL 27,3%)
- **Marca foco**: MONDIAL (em Kitchen — 97% das visits Mondial-em-Small estão em Kitchen, BPC vs MGL 17,8%)
- **Sellers cirúrgicos vs MGL**:
  - Mercado Livre Eletronicos (1P) — 53% do universo Mondial vs MGL, BPC vs MGL 17%
  - LOJAOFICIALCASASBAHIA (Asesorado PF) — BPC vs MGL 9,8%
  - DUTRA\_MAQUINAS (Asesorado PF) — BPC vs MGL 4,8% ⚠️
  - LOI BRASIL (Asesorado PF) — BPC vs MGL 8,7%
  - MEGABYTE MAGAZINE (Asesorado PF, em Small) — BPC vs MGL 14,7%

**Quick wins ocultos** (auditoria de paridade, não War Room):

- LOJAGAZIN (BPC \~8%), VGSHOPOFICIAL (BPC \~5%) — provável erro sistêmico de catálogo

**Mensagem enviada no grupo** (15/05/2026): drill down Small → Kitchen → Mondial → Sellers, ótica vs MGL Winner, com cascata de impacto ponderado.

---

### B) Shield Against Asians (BPC vs Shopee)

**Objetivo**: Apoiar squad Shield com leitura de BPC vs SPE.

**Entregáveis gerados**:

- `Shield_BPC_HE_vs_Shopee_Jan-Mai_2026.xlsx`
- `Shield_BPC_Tech_vs_Shopee_Jan-Mai_2026.xlsx`

Conceito MS Ratio: NSI Meli vs NSI Shopee na vertical/categoria, leitura mensal MoM em pp, BOX \+ PIX, por D1 × ASP.

---

### C) Grid Dashboard BPC KMI HE

**Objetivo**: Dashboard HTML interativo pra leitura semanal autônoma da diretoria, Brands e Farming.

**Arquivo atual**: `/mnt/outputs/Grid_BPC_KMI_HE.html` (V5, \~220 KB)

- 3 abas: Overview / Marcas / Sellers
- Quick Start strip role-based (Diretoria / Brands / Farming)
- KPIs, gráficos semanais/mensais/datas duplas
- Best & Worst por dimensão (Offender/Promoter)
- Visual exec match com bench de KMI Pricing

**Scheduled task**: `refresh-grid-bpc-kmi-he` (toda segunda 7h)

- Local: `C:\Users\bdacache\Documents\Claude\Scheduled\refresh-grid-bpc-kmi-he\SKILL.md`
- Roda 4-6 queries, rebuild HTML, sobe pro Grid MELI

**Status**: pronto pra validação final \+ compartilhamento.

---

### D) Análise Modais de Entrega (ME1 vs ME2)

**Objetivo**: Avaliar competitividade de items H\&B em ME1 vs ME2 (3P, Asesorado PF).

**Findings**:

- **BOX (preço)**: ME1 vence ME2 sempre, gap **10,5 pp** em Mai
- **SHP (frete)**: ME2 vence ME1, gap **12-24 pp** sustentado
- **Por ASP**: ME1 vence em 0-1499 BOX; em 1500+ BOX virou ME1 em Mai (de empate pra \+12pp)
- **Por região (Asesorado PF)**:
  - Sudeste: ME1 vence em preço (+16 pp), ME2 vence frete
  - Sul: ME1 vence ainda mais forte (+26 pp BOX 0-1499)
  - **Nordeste: INVERTE** — ME2 vence em BOX (única região) ⚠️
  - Centro-Oeste / Norte: empate, volumes baixos

**Hipótese central**: pra mover BPC frete em H\&B, empurrar sellers ME1 → ME2. Pra mover preço, atenção em sellers ME2 que estão piorando.

---

## 7\. Outputs gerados (na pasta de outputs)

- `Diagnostico_BPC_HE_Q2_YTD_v2.pptx` — apresentação War Room (4 slides)
- `Deep_Dive_Sellers_Brands_WarRoom_KMI_HE.md` — análise tática Sellers \+ Marcas
- `BPC_analysis_kit.md` — kit de continuidade (SQLs mestras \+ valores ref)
- `Grid_BPC_KMI_HE.html` — dashboard interativo V5
- `Shield_BPC_HE_vs_Shopee_Jan-Mai_2026.xlsx` \+ Tech equivalente
- `BPC_Projeto_Contexto_Mestre.md` — este doc

---

## 8\. Skills e ferramentas

- `bpc-reader` — skill oficial do time de Pricing (instalada em `.claude/skills/bpc-reader/SKILL.md`). **Consultar antes de qualquer pergunta de BPC.**
- `metric-agent-mcp` — execução de SQL no BigQuery (tabelas WHOWNER)
- `datty-mcp` — busca no catálogo de dados
- `meli-directory-mcp` — info de colaboradores

---

## 9\. Convenções de output

- **Números absolutos**: abreviar com K / Mi / Bi (ex: 1.436.643.150 → "1,4 Bi")
- **Percentuais**: 1 casa decimal, vírgula (ex: "47,1%")
- **Deltas**: em pp com sinal (ex: "+8,3 pp", "-2,7 pp")
- **Tabelas**: visits em % (SoV) com absoluto abreviado em parênteses cinza ao lado
- **Tom**: direto, executivo, sem encheção. Insight primeiro, suporte depois.

---

## 10\. Próximos passos pendentes

1. Validar e enviar Grid V5 final pro Grid MELI
2. Acompanhar reuniões War Room iniciais (sellers/marcas prioritárias)
3. Investigar elegibilidade PIX Match dos sellers prioritários (com Pricing)
4. Auditoria de paridade LOJAGAZIN / VGSHOPOFICIAL (provável erro catálogo)
5. Próxima onda de marcas: Electrolux (2ª prioritária após Mondial)

---

*Última atualização: 2026-05-15 · Beatriz Dacache*
