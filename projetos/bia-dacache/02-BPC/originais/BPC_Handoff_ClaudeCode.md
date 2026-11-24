# Handoff BPC — Cowork → Claude Code

Documento de migração do projeto **BPC** (Buyer Price Competitiveness) do Cowork desktop para Claude Code. Resume contexto, modelo de dados, regras de cálculo e entregáveis. **Não é diagnóstico** — é o "manual de operação" pra dar continuidade ao trabalho em outro ambiente.

Autora: Beatriz Dacache (focal BPC HE/MLB). Última atualização: 2026-05-26.

---

## 0. Resumo base (orientação rápida)

**Quem**: Beatriz Dacache, focal de BPC para a vertical Home Electronics (HE) em MLB. Coordena War Room BPC HE, apoia frente Shield (vs Shopee), fala com Direção/Brands/Farming/Pricing.

**O que é BPC**: métrica de competitividade de preço que mede em quantas visitas com match de catálogo o Meli está ≤ preço do competidor. Quanto maior, melhor.

**Workstreams ativas do projeto** (alto nível):
- **A. War Room KMI PIX HE** — fechar gap em PIX KMI HE atacando o ofensor estrutural do momento (hipótese atual: MGL)
- **B. Shield Against Asians** — BPC vs Shopee em HE e Tech (apoio ao squad)
- **C. Grid Dashboard BPC KMI HE** — HTML interativo refrescado semanalmente

**Stack de ferramentas usadas no projeto**:
- BigQuery (`meli-bi-data.WHOWNER` e `SBOX_REVENUE_MKP`) via MCP `metric-agent-mcp` ou skill `bigquery-meli`
- Skill `bpc-reader` (oficial Pricing) — referência canônica de tabelas, fórmulas, FAVORABILITY_TYPE por site
- Doc mestre `BPC_Projeto_Contexto_Mestre.md` — contexto do projeto Beatriz

---

## 1. Tabelas BigQuery usadas

| Tabela | Granularidade | Pra quê |
|---|---|---|
| `meli-bi-data.WHOWNER.BT_COM_FAVORABILITY` | item × dia × site × metodologia × competidor | **Tabela central de BPC**. Todas as métricas BPC vêm daqui. |
| `meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB` | pedido × item × dia | NMV/NSI/ASP, modal de entrega (me1/me2), logistic type, região (RECEIVER_STATE). Usada na análise ME1 vs ME2 e ASP do item. |
| `meli-bi-data.SBOX_REVENUE_MKP.BOC_BENEFITS_ITEM_DAY_DASHBOARD` | item × dia | Aporte Benefits a BPC (cupons/rebates). ⚠️ Scan ~89–117 GB — sempre filtrar fechas. |
| `meli-bi-data.WHOWNER.LK_CURRENCY_CONVERTION` | site × dia | USD_RATIO pra converter preço local → USD (lag T-2, começar D+3). |
| `meli-bi-data.WHOWNER.LK_MLM_SPAAS_ITEM_ID_CLASICO_PH` | item | MLM-only, pra filtrar Meli Pro / cuotas clásicas em CSI. |

### Chaves de join importantes
- `BT_COM_FAVORABILITY.MELI_ID` (INT64) ≡ `BOC_BENEFITS.ITE_ITEM_ID` ≡ `DM_EFICIENCIA_MLB.ITE_ITEM_ID` — todos são o ITEM_ID do Meli, nomes diferentes em tabelas diferentes
- Datas: `BT_COM_FAVORABILITY.TIM_DAY` (DATE) vs `BOC_BENEFITS.DAY_MONTH_YEAR` (DATE) vs `DM_EFICIENCIA_MLB.ORD_CLOSED_DT` (DATE) — atenção ao nome da coluna por tabela

### Colunas-chave de `BT_COM_FAVORABILITY` (top-level, sem UNNEST)
`SIT_SITE_ID`, `FAVORABILITY_TYPE`, `TIM_DAY`, `KMI` (string lowercase), `FLG_BULKY` (string lowercase), `FLG_COMP_1P`, `FLG_COMP_3P`, `COMP_RIVAL_NAME_WINNER`, `COMP_SITE_ID_WINNER`, `VERTICAL`, `DOM_AGG_1` / `DOM_AGG_2` / `DOM_AGG_3` (D1/D2/D3), `BRAND` / `REAL_BRAND` (use `COALESCE(REAL_BRAND, BRAND)`), `CUS_NICKNAME` / `CUS_CUST_ID_SEL`, `SEGMENTO`, `SEGMENTO_SELLER_DETAIL`, `ITEM_PARTY_TYPE` ('1P'/'3P'), `MELI_ID`, `PRICE_MELI`, `COMP_PRICE_RIVAL`, `MAX_CUOTAS_SIN_INT_MELI`, `VISITS_MATCH`, `VISITS_CHEAPER`, `VISITS_EQUAL`, `VISITS_EXPENSIVE`, `VISITS_TOTAL`, `COMPETITORS` (ARRAY, requer UNNEST).

### Array `COMPETITORS` (requer `UNNEST(COMPETITORS) AS C`)
`C.COMP_SITE_ID`, `C.COMP_FLAG_FIRST_PARTY`, `C.VISITS_MATCH`, `C.VISITS_CHEAPER`, `C.VISITS_EQUAL`, `C.VISITS_EXPENSIVE`, `C.MAX_CUOTAS_SIN_INT`.

---

## 2. Métricas calculadas (fórmulas canônicas)

### 2.1 BPC padrão (BOX / KMI / Cuotas / 1P / Vertical)

```sql
ROUND(SAFE_DIVIDE(SUM(VISITS_CHEAPER + VISITS_EQUAL), SUM(VISITS_MATCH)), 4)
```

### 2.2 Oportunidade (visits expensive share)

```
Opp = VISITS_EXPENSIVE / VISITS_MATCH = 1 - BPC
```

### 2.3 BPC Cases KMI (denominador = Cheaper + Match + Expensive em items distintos)

Variante usada em "Cases" — contagem de pares dia×item distintos por bucket de preço relativo (Cheaper se Meli < 99% Rival; Match se Meli entre 99% e 101% do Rival; Expensive se Meli > 101%).

```sql
SAFE_DIVIDE(
  COUNT(DISTINCT CASE WHEN PRICE_MELI > 0 AND COMP_PRICE_RIVAL > 0
        AND PRICE_MELI < 0.99 * COMP_PRICE_RIVAL
        THEN CONCAT(CAST(TIM_DAY AS STRING), CAST(MELI_ID AS STRING)) END)
  + COUNT(DISTINCT CASE WHEN PRICE_MELI >= 0.99 * COMP_PRICE_RIVAL
        AND PRICE_MELI <= 1.01 * COMP_PRICE_RIVAL
        THEN CONCAT(CAST(TIM_DAY AS STRING), CAST(MELI_ID AS STRING)) END),
  -- denominador equivalente somando também Expensive
  ...
)
```

### 2.4 Aporte Benefits a BPC

```sql
ROUND(SAFE_DIVIDE(
  SUM(CASE WHEN STATUS_PREVIO='EXPENSIVE'
            AND STATUS_POS IN ('CHEAPER','MATCH')
            AND OPTINED = 1
            THEN VISITS_L30D ELSE 0 END),
  SUM(VISITS_L30D)
), 4)
-- Por campanha: AND TIPO_CAMPANA = 'NomeCampanha'
```

### 2.5 CSI (Cuotas sin interés)

```sql
-- Métrica: SUM(C.VISITS_MATCH) com UNNEST(competitors) AS C
-- Filtros obrigatórios:
--   MAX_CUOTAS_SIN_INT_MELI IS NOT NULL
--   AND C.MAX_CUOTAS_SIN_INT IS NOT NULL
-- Thresholds ASP por site: MLB ≥ R$100 | MLM ≥ MXN 1.200 | MLA ≥ ARS 50.000
-- MLA usa FAVORABILITY_TYPE = 'BOX_ALL_ABC_CUOTAS'
-- KC: MLB→AMB, MLM→AMX, MLA→FVG
```

### 2.6 ASP do item (a partir de `DM_EFICIENCIA_MLB`)

```sql
ASP = SUM(F_NMV_LC) / SUM(F_NSI)
```

### 2.7 Atribuição ponderada (impacto pp)

```
impact_universo_pp = Δbpc_unit × (visits_unit / visits_universo)
```

Usado pra dimensionar quanto uma célula (D1/marca/seller) move o BPC da vertical (ou do recorte vs competidor).

### 2.8 Cascata de impacto (unit → vs Competidor → vertical)

```
+X pp BPC unit vs Competidor
  → impacto em vs Competidor agregado = X × (visits_unit / total_vs_Competidor)
  → impacto na vertical ≈ X × (visits_unit / total_vs_Competidor) × (vs_Competidor / total_vertical)
```

### 2.9 Conversão preço local → USD (T-2 lag)

```sql
WITH currency AS (
  SELECT SIT_SITE_ID, TIM_DAY, USD_RATIO
  FROM `meli-bi-data.WHOWNER.LK_CURRENCY_CONVERTION`
  WHERE TIM_DAY BETWEEN '<start-2d>' AND '<end>'
)
SELECT
  ...,
  H.PRICE_MELI * CC.USD_RATIO AS price_usd
FROM `meli-bi-data.WHOWNER.BT_COM_FAVORABILITY` H
JOIN currency CC
  ON CC.SIT_SITE_ID = H.SIT_SITE_ID
  AND CC.TIM_DAY = DATE_SUB(H.TIM_DAY, INTERVAL 2 DAY)
-- ⚠️ filtrar BT_COM_FAVORABILITY a partir do dia 3 do range pra não perder os primeiros dois dias
```

Buckets ASP USD padrão: `<50`, `50–100`, `100–500`, `500+`.

---

## 3. Filtros recorrentes

### 3.1 Filtros LOCKED para qualquer análise War Room KMI PIX HE

```sql
WHERE SIT_SITE_ID = 'MLB'
  AND FAVORABILITY_TYPE = 'BOX_ALL_ABC_PIX'
  AND KMI = 'true'                                       -- STRING lowercase
  AND COALESCE(FLG_BULKY, 'false') != 'true'             -- W/o H&B
  AND DOM_AGG_1 IN (
        'SMALL APPLIANCES',
        'LARGE APPLIANCES',
        'HEATING, COOLING & AIR QUALITY',
        'AUDIO & GENERAL ELECTRONICS',
        'TELEVISIONS & STREAMING DEVICES',
        'HOUSEHOLD APPLIANCES PARTS'
      )
```

### 3.2 Mapa `FAVORABILITY_TYPE` por site (referência geral, fora do escopo War Room HE)

| Seção | allMeli | MLB | MLA | MLM / MCO / MLC |
|---|---|---|---|---|
| BPC BOX / KMI / KC / Vertical | `BOX_ALL_ABC` | `BOX_ALL_ABC_PIX` | `BOX_ALL_ABC_CUOTAS` | `BOX_ALL_ABC` |
| BPC 1P | `BOX_1P_AB` / `BOX_1P_ABC` | ídem | ídem | ídem |
| Frete (SHP) | — | `SHP_ALL_ABC` | — | — |
| Apples-to-apples | — | `BOX_MATCH_SELLER` | — | — |

> **allMeli sempre usa `BOX_ALL_ABC`** pra evitar doble conteo entre sites.

### 3.3 Janelas temporais usadas

- **Quarter fechado**: ex. `Q1'26 = 2026-01-01 a 2026-03-31`
- **QTD** (Quarter to Date): primeiro dia do trimestre corrente até último disponível na base
- **MTD** (Month to Date): primeiro dia do mês corrente até último disponível (geralmente D-1 ou D-2)
- **Datas Duplas**: 03/03, 04/04, 05/05 etc. — eventos de pricing
- **Períodos canônicos do `bpc-reader`** (Q1'25 → Q1'26): CTE com `CASE WHEN TIM_DAY BETWEEN ...`

### 3.4 Filtros de seller / segmento que apareceram

- `SEGMENTO_SELLER_DETAIL = 'ASESORADO PF'` — carteira Paid Farming (foco principal do War Room)
- `SEGMENTO_SELLER_DETAIL IN ('SD ASESORADO','SD NO ASESORADO')` — Seller Dev
- `ITEM_PARTY_TYPE = '1P'` — itens próprios Meli
- `CUS_NICKNAME = '<nickname>'` ou `CUS_CUST_ID_SEL = <id>` — corte por seller específico

### 3.5 Filtros de competidor

Existem duas formas de filtrar competidor, e elas respondem perguntas diferentes:

- **Winner view** — `COMP_SITE_ID_WINNER = 'MGL'` (ou outro código).
  Considera **apenas o melhor competidor de cada item** (o "winner" do match). É o recorte de **referência do War Room** e a base de qualquer **análise de oportunidade**: quando você quer saber em quantas visitas o competidor X está ganhando do Meli e qual é o tamanho do gap pra reverter, é aqui que se calcula.

- **UNNEST view** — `UNNEST(COMPETITORS) AS C WHERE C.COMP_SITE_ID = 'MGL'`.
  Considera **todas as visitas onde o competidor aparece** no match, mesmo quando ele não é o winner. Útil pra perguntas tipo "qual a presença total do competidor no universo?" ou pra comparações em que você quer todos os toques dele, não só os de vitória.

> **Diferença prática**: a Winner view é um **subset** da UNNEST view — todas as visitas Winner também aparecem no UNNEST, mas o UNNEST inclui também itens onde o competidor estava no match mas perdeu pra outro. Pra leitura de oportunidade vs MGL/AMB/SPE no War Room, **usar Winner view**.

### 3.6 Filtro de vertical

Neste projeto, **a vertical é sempre Home Electronics**. Aplicar como filtro fixo em qualquer análise:

```sql
AND VERTICAL = 'HOME ELECTRONICS'
```

Esse filtro é equivalente ao de `DOM_AGG_1 IN (6 D1s)` na seção 3.1, mas é mais robusto: garante que qualquer item fora dos 6 D1s padrão mas que ainda pertença a HE entre, e qualquer item de outra vertical com D1 de nome parecido fique de fora. Pode usar os dois juntos ou apenas `VERTICAL = 'HOME ELECTRONICS'`.

---

## 4. Universo: D1s, competidores, marcas, sellers

### 4.1 6 D1s de Home Electronics (`DOM_AGG_1`)

1. SMALL APPLIANCES
2. LARGE APPLIANCES
3. HEATING, COOLING & AIR QUALITY
4. AUDIO & GENERAL ELECTRONICS
5. TELEVISIONS & STREAMING DEVICES
6. HOUSEHOLD APPLIANCES PARTS

### 4.2 Competidores MLB

| Código `COMP_SITE_ID` | `COMP_RIVAL_NAME_WINNER` | Apelido |
|---|---|---|
| `AMB` | `Amazon Brazil` | Amazon |
| `MGL` | `MagazineLuiza` | Magalu |
| `SPE` | `Shopee` | Shopee |
| `CBH` | (Casas Bahia — confirmar valor exato em produção) | Casas Bahia |
| — | `Netshoes` | Netshoes |
| — | `Aliexpress-Br` | Aliexpress (share <0,1%, agrupado em Others) |
| `AMR` | (Americanas) | Listado por completude — não é foco do War Room atual, mas não é mais excluído por default |

### 4.3 Marcas que entraram em análise

- **Mondial** — marca foco atual em Kitchen (D2 dentro de Small Appliances). Stakeholder interno: Renato Prado Valentin.
- **Electrolux** — próxima onda (2ª prioritária após Mondial).

### 4.4 Sellers que apareceram em análises cirúrgicas

| Nickname | Segmento | Observação |
|---|---|---|
| `Mercado Livre Eletronicos` | 1P | Volume gigante em Mondial vs MGL |
| `LOJAOFICIALCASASBAHIA` | ASESORADO PF | — |
| `DUTRA_MAQUINAS` | ASESORADO PF | ⚠️ BPC muito baixo, atenção |
| `LOI BRASIL` | ASESORADO PF | — |
| `MEGABYTE MAGAZINE` | ASESORADO PF | Em Small Appliances |
| `LOJAGAZIN` | (a confirmar) | Quick win — provável erro sistêmico de catálogo (auditoria de paridade) |
| `VGSHOPOFICIAL` | (a confirmar) | Idem LOJAGAZIN |

### 4.5 Regiões Brasil (mapeamento `RECEIVER_STATE`)

- **Norte**: BR-AC, BR-AM, BR-AP, BR-PA, BR-RO, BR-RR, BR-TO
- **Nordeste**: BR-AL, BR-BA, BR-CE, BR-MA, BR-PB, BR-PE, BR-PI, BR-RN, BR-SE
- **Centro-Oeste**: BR-DF, BR-GO, BR-MS, BR-MT
- **Sudeste**: BR-ES, BR-MG, BR-RJ, BR-SP
- **Sul**: BR-PR, BR-RS, BR-SC

---

## 5. Regras de negócio que a Beatriz ensinou

Lista de "tribal knowledge" que não está documentada no catálogo padrão e que **deve ser aplicada sempre**:

1. **KMI é STRING lowercase** (`'true'` / `'false'`), nunca booleano. Vale pra `BT_COM_FAVORABILITY` e `BOC_BENEFITS`.
2. **`FLG_BULKY` é STRING lowercase**. Filtro W/o H&B canônico: `COALESCE(FLG_BULKY, 'false') != 'true'` (equivalente a `(FLG_BULKY IS NULL OR FLG_BULKY != 'true')`). **Em qualquer análise de PIX (`FAVORABILITY_TYPE = 'BOX_ALL_ABC_PIX'`), FLG_BULKY é sempre "não" — ou seja, H&B fica fora.** Isso é regra fixa, não opcional.
3. **`FLG_COMP_1P` e `C.COMP_FLAG_FIRST_PARTY` também são STRING lowercase** (`'true'`/`'false'`).
4. **`COMP_RIVAL_NAME_WINNER` é coluna top-level** — não precisa de UNNEST.
5. **Vertical fixa = `HOME ELECTRONICS`** — neste projeto sempre. Aplicar `VERTICAL = 'HOME ELECTRONICS'` como filtro.
6. **allMeli usa `BOX_ALL_ABC`** (nunca PIX nem CUOTAS) pra não duplicar entre sites.
7. **MLB usa `BOX_ALL_ABC_PIX`** pra tudo (BOX, KMI, KC, Vertical) — porque PIX é o preço-âncora no Brasil.
8. **Padrão War Room HE bloqueado**: PIX + KMI true + W/o H&B + 6 D1s + Vertical HE — qualquer mudança eu **flago** antes de rodar, não decido sozinha.
9. **Hipótese de foco (MGL/Small/Kitchen/Mondial) é móvel**, não dogma — a liderança pode redirecionar a qualquer momento.
10. **Use Winner view** (`COMP_SITE_ID_WINNER = 'XXX'`) pra leitura War Room vs competidor específico e pra **análises de oportunidade**. UNNEST view é só quando você quer pegar todas as visitas onde o competidor aparece, mesmo sem ser winner.
11. **Para marca use `COALESCE(REAL_BRAND, BRAND)`** (REAL_BRAND é o cleaned).
12. **Para conversão USD**, lag T-2 obrigatório + começar o range D+3 pra não perder os 2 primeiros dias por falha de JOIN.
13. **`MELI_ID` (em `BT_COM_FAVORABILITY`) ≡ `ITE_ITEM_ID`** (em outras tabelas) — são sinônimos.
14. **`BOC_BENEFITS` usa `DAY_MONTH_YEAR`** (não `TIM_DAY`). Sempre filtrar fechas — scan é caro (~89–117 GB).
15. **Convenções de output**:
    - Absolutos: K / Mi / Bi (1.436.643.150 → "1,4 Bi")
    - Percentuais: 1 casa decimal, vírgula ("47,1%")
    - Deltas: pp com sinal ("+8,3 pp" / "-2,7 pp")
    - Tabelas: visits em % (SoV) com absoluto abreviado entre parênteses
    - **Tom**: direto, exec, sem encheção. Insight primeiro, suporte depois.
16. **Atenção a custo de query**: filtros de fecha explícitos sempre. `BOC_BENEFITS` é o mais caro.

---

## 6. Entregáveis produzidos no projeto

Lista do que existe / foi gerado neste projeto (alguns ficaram na pasta `/mnt/outputs` da sessão original do Cowork, outros em arquivos de Grid MELI):

| Entregável | Tipo | Workstream | Status |
|---|---|---|---|
| `BPC_Projeto_Contexto_Mestre.md` | Markdown — contexto mestre do projeto | Todos | Vivo, atualizado em 2026-05-15 |
| `bpc-reader_SKILL.md` | Skill ref (cópia local, oficial é skill instalada) | Todos | Salvo na pasta BPC desta sessão |
| `BPC_Handoff_ClaudeCode.md` | **Este doc** — handoff pra Claude Code | Todos | Recém-criado |
| `Diagnostico_BPC_HE_Q2_YTD_v2.pptx` | Apresentação (4 slides) War Room | A. War Room | Entregue |
| `Deep_Dive_Sellers_Brands_WarRoom_KMI_HE.md` | Markdown tático Sellers + Marcas | A. War Room | Entregue |
| `BPC_analysis_kit.md` | Kit de continuidade — SQLs mestras + valores ref | A. War Room | Entregue |
| `Grid_BPC_KMI_HE.html` | Dashboard HTML V5, ~220 KB, 3 abas (Overview/Marcas/Sellers) | C. Grid | Pronto pra validação final |
| `Shield_BPC_HE_vs_Shopee_Jan-Mai_2026.xlsx` | XLSX MS Ratio HE | B. Shield | Entregue |
| `Shield_BPC_Tech_vs_Shopee_Jan-Mai_2026.xlsx` | XLSX MS Ratio Tech | B. Shield | Entregue |
| Scheduled task `refresh-grid-bpc-kmi-he` | Toda segunda 7h — refresh do Grid V5 | C. Grid | Ativa |

---

## 7. Próximos passos / pontos abertos

1. Migrar a operação do projeto pro Claude Code (objetivo deste doc).
2. Validar e enviar Grid V5 final pro Grid MELI.
3. Acompanhar reuniões War Room iniciais (sellers/marcas prioritárias).
4. Investigar elegibilidade PIX Match dos sellers prioritários (com Pricing).
5. Auditoria de paridade `LOJAGAZIN` / `VGSHOPOFICIAL` (provável erro catálogo).
6. Próxima onda de marcas: Electrolux (2ª prioritária após Mondial).
7. Confirmar valor exato em produção de `COMP_RIVAL_NAME_WINNER` pra Casas Bahia.

---

## 8. Como reproduzir no Claude Code

### MCPs / skills que precisam estar disponíveis
- **MCP**: `bigquery-insight` (ou `metric-agent-mcp`) com acesso a `meli-bi-data.WHOWNER`
- **Skill**: `bpc-reader` (skill oficial do time Pricing — caminho típico `~/.claude/skills/bpc-reader/SKILL.md`)
- **Doc projeto**: `BPC_Projeto_Contexto_Mestre.md` na raiz do projeto
- **Este doc**: `BPC_Handoff_ClaudeCode.md`

### Prompt inicial sugerido pro Claude Code
> "Trabalhamos KPIs de pricing e BPC HE/MLB. Sempre consulta `BPC_Projeto_Contexto_Mestre.md` e a skill `bpc-reader` antes de responder. Filtros default War Room: SIT_SITE_ID='MLB', FAVORABILITY_TYPE='BOX_ALL_ABC_PIX', KMI='true', COALESCE(FLG_BULKY,'false')!='true' (em PIX, H&B fica sempre fora), VERTICAL='HOME ELECTRONICS', DOM_AGG_1 IN (6 D1s HE). Análises de oportunidade vs competidor usam Winner view (`COMP_SITE_ID_WINNER='XXX'`); UNNEST view só quando se quer todas as visitas do competidor independente de ser winner. Foco atual (móvel): MGL Winner, Small/Kitchen, Mondial. Output: 1 casa decimal vírgula, K/Mi/Bi, deltas em pp, tom direto."

---

*Documento gerado em 2026-05-26 pra migração do projeto BPC do Cowork desktop pra Claude Code.*
