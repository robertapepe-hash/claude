# Manual de BPC — o que você precisa saber para não errar

> Consolidação do canon com o **tribal knowledge** que não está no catálogo de dados.
> Detalhe completo em `originais/BPC_Handoff_ClaudeCode.md` e `originais/BPC_Projeto_Contexto_Mestre.md`.
> **A referência oficial é a skill `bpc-reader`** — consulte-a antes deste documento.

---

## 1 · Fórmulas canônicas

### BPC
```sql
ROUND(SAFE_DIVIDE(SUM(VISITS_CHEAPER + VISITS_EQUAL), SUM(VISITS_MATCH)), 4)
```

### Oportunidade
```
Opp = VISITS_EXPENSIVE / VISITS_MATCH = 1 − BPC
```
A soma das oportunidades por competitor winner **fecha** em `1 − BPC` da categoria. Use isso como check.

### Share of Opportunity (SoO) por competidor X
```
SoO_X = SUM(VISITS_EXPENSIVE onde COMP_SITE_ID_WINNER = 'X') / SUM(VISITS_MATCH total da D1)
```

### Atribuição ponderada — quanto uma célula move o todo
```
impacto_pp = Δbpc_célula × (visits_célula / visits_universo)
```

### Cascata de impacto — da célula até a vertical
```
+X pp de BPC na célula, vs competidor C
  → impacto no agregado vs C  = X × (visits_célula / total_vs_C)
  → impacto na vertical       ≈ X × (visits_célula / total_vs_C) × (vs_C / total_vertical)
```

### ASP do item (a partir de `DM_EFICIENCIA_MLB`)
```sql
ASP = SUM(F_NMV_LC) / SUM(F_NSI)
```

### Aporte de Benefits ao BPC
```sql
ROUND(SAFE_DIVIDE(
  SUM(CASE WHEN STATUS_PREVIO='EXPENSIVE' AND STATUS_POS IN ('CHEAPER','MATCH') AND OPTINED = 1
           THEN VISITS_L30D ELSE 0 END),
  SUM(VISITS_L30D)), 4)
-- por campanha: AND TIPO_CAMPANA = '<nome>'
```

### Conversão para USD — lag T-2 obrigatório
```sql
JOIN currency CC
  ON CC.SIT_SITE_ID = H.SIT_SITE_ID
 AND CC.TIM_DAY = DATE_SUB(H.TIM_DAY, INTERVAL 2 DAY)
```
⚠️ **Filtre a favorabilidade a partir do 3º dia do range**, senão os dois primeiros dias somem no JOIN.
Buckets padrão em USD: `<50` · `50–100` · `100–500` · `500+`.

### CSI (cuotas sin interés) — para quem tocar outros sites
Métrica = `SUM(C.VISITS_MATCH)` com `UNNEST(competitors) AS C`.
Filtros obrigatórios: `MAX_CUOTAS_SIN_INT_MELI IS NOT NULL AND C.MAX_CUOTAS_SIN_INT IS NOT NULL`.
Thresholds de ASP: MLB ≥ R$ 100 · MLM ≥ MXN 1.200 · MLA ≥ ARS 50.000. MLA usa `BOX_ALL_ABC_CUOTAS`.

---

## 2 · Tabelas e chaves

| Tabela | Grão | Para quê |
|---|---|---|
| `WHOWNER.BT_COM_FAVORABILITY` | item × dia × site × metodologia × competidor | **central de BPC** |
| `WHOWNER.DM_EFICIENCIA_MLB` | pedido × item × dia | NMV/NSI/ASP, modal, região, segmento |
| `SBOX_REVENUE_MKP.BOC_BENEFITS_ITEM_DAY_DASHBOARD` | item × dia | aporte de Benefits ⚠️ scan 89-117 GB |
| `WHOWNER.LK_CURRENCY_CONVERTION` | site × dia | `USD_RATIO`, lag T-2 |
| `WHOWNER.DM_COM_COMPETENCIA` | item × dia | Buy Box, rebate $, preço de partida/chegada |

**A chave é a mesma com nomes diferentes:**
`BT_COM_FAVORABILITY.MELI_ID` ≡ `BOC_BENEFITS.ITE_ITEM_ID` ≡ `DM_EFICIENCIA_MLB.ITE_ITEM_ID`

**As datas também:**
`TIM_DAY` (favorabilidade) · `ORD_CLOSED_DT` (eficiência) · `DAY_MONTH_YEAR` (benefits)

> A view de `BT_COM_FAVORABILITY` em `WHOWNER` é **enriquecida** — tem ~50 colunas a mais que o schema raw
> (TITLE, BRAND, REAL_BRAND, PERMALINK, segmento de seller, asesor, flags, NMV_L30D…). Não vá procurar
> essas informações em outra tabela.

**Testadas e descartadas:** `LK_BT_ITE_ITEMS_TITLE` (não existe) · `DM_ITE_ITEMS_SUBSET` (sem permissão) ·
`LK_ITE_ITEMS_PICTURES` (não tem título).

---

## 3 · Metodologias (`FAVORABILITY_TYPE`)

| Tipo | O que é | Quando usar |
|---|---|---|
| `BOX_ALL_ABC` | preço à vista | visão padrão · **allMeli sempre** |
| `BOX_ALL_ABC_PIX` | preço com PIX | **padrão de MLB** para BOX, KMI, KC e Vertical |
| `SHP_ALL_ABC` | frete | competitividade logística |
| `BOX_MATCH_SELLER` | apples-to-apples (mesmo seller) | comparações específicas |
| `BOX_ALL_ABC_CUOTAS` | cuotas | MLA |

**Mapa por site:**

| Seção | allMeli | MLB | MLA | MLM / MCO / MLC |
|---|---|---|---|---|
| BPC BOX / KMI / KC / Vertical | `BOX_ALL_ABC` | `BOX_ALL_ABC_PIX` | `BOX_ALL_ABC_CUOTAS` | `BOX_ALL_ABC` |
| BPC 1P | `BOX_1P_AB` / `BOX_1P_ABC` | idem | idem | idem |

> **allMeli sempre `BOX_ALL_ABC`** — para evitar dupla contagem entre sites.

---

## 4 · Winner view vs UNNEST view

| | Winner view | UNNEST view |
|---|---|---|
| Sintaxe | `COMP_SITE_ID_WINNER = 'MGL'` | `UNNEST(COMPETITORS) C WHERE C.COMP_SITE_ID = 'MGL'` |
| Considera | só quando esse competidor é o melhor do match | todas as visitas em que ele aparece |
| Responde | **oportunidade** — quanto custa reverter | presença total no universo |

A Winner view é **subconjunto** da UNNEST. **Para War Room e para qualquer leitura de oportunidade: Winner
view.** `COMP_RIVAL_NAME_WINNER` é coluna **top-level** — não precisa de UNNEST.

---

## 5 · Filtros travados do War Room PIX KMI HE

```sql
WHERE SIT_SITE_ID       = 'MLB'
  AND FAVORABILITY_TYPE = 'BOX_ALL_ABC_PIX'
  AND KMI               = 'true'                       -- STRING lowercase
  AND COALESCE(FLG_BULKY, 'false') != 'true'           -- em PIX, H&B fica SEMPRE fora
  AND VERTICAL          = 'HOME ELECTRONICS'
  AND DOM_AGG_1 IN ('SMALL APPLIANCES','LARGE APPLIANCES','HEATING, COOLING & AIR QUALITY',
                    'AUDIO & GENERAL ELECTRONICS','TELEVISIONS & STREAMING DEVICES',
                    'HOUSEHOLD APPLIANCES PARTS')
```

**Prefira `VERTICAL = 'HOME ELECTRONICS'` à lista de D1s** — é mais robusto: pega item de HE que esteja
fora das 6 D1s padrão e exclui item de outra vertical com D1 de nome parecido. Pode usar os dois juntos.

**Qualquer mudança nesses filtros deve ser sinalizada antes de rodar, não decidida sozinha.**

---

## 6 · As 16 regras que não estão no catálogo

1. **`KMI` é STRING lowercase** (`'true'`/`'false'`), nunca booleano. Vale na favorabilidade e no benefits.
2. **`FLG_BULKY` é STRING lowercase.** Filtro canônico de "sem H&B": `COALESCE(FLG_BULKY,'false') != 'true'`.
   **Em qualquer análise de PIX, H&B fica sempre fora** — é regra fixa, não opcional.
3. **`FLG_COMP_1P` e `C.COMP_FLAG_FIRST_PARTY` também são STRING lowercase.**
4. **`COMP_RIVAL_NAME_WINNER` é top-level** — sem UNNEST.
5. **Neste projeto a vertical é sempre HOME ELECTRONICS.**
6. **allMeli usa `BOX_ALL_ABC`** — nunca PIX nem CUOTAS.
7. **MLB usa `BOX_ALL_ABC_PIX`** para tudo, porque PIX é o preço-âncora no Brasil.
8. **O padrão do War Room HE é bloqueado.** Mudança se flaga, não se decide.
9. **A hipótese de foco é móvel** (MGL/Small/Kitchen/Mondial quando saí) — a liderança redireciona.
10. **Winner view para oportunidade.** UNNEST só quando quiser todas as visitas do competidor.
11. **Marca sempre `COALESCE(REAL_BRAND, BRAND)`** — `REAL_BRAND` é o campo limpo. E **liste as duas
    grafias** de marcas com acento (`'BRITÂNIA','BRITANIA'`): a base tem as duas.
12. **USD: lag T-2 obrigatório**, e comece o range em D+3.
13. **`MELI_ID` ≡ `ITE_ITEM_ID`** — sinônimos em tabelas diferentes.
14. **`BOC_BENEFITS` usa `DAY_MONTH_YEAR`** e é a tabela mais cara — sempre filtre datas.
15. **Convenções de output:** K/Mi/Bi · 1 casa decimal com vírgula · deltas em **pp** com sinal · visitas em
    % de SoV com absoluto abreviado entre parênteses · tom direto, insight primeiro.
16. **Filtro de data explícito, sempre.** Custo é responsabilidade de quem escreve a query.

---

## 7 · Universo de referência

**As 6 D1s de Home Electronics (`DOM_AGG_1`):**
SMALL APPLIANCES · LARGE APPLIANCES · HEATING, COOLING & AIR QUALITY · AUDIO & GENERAL ELECTRONICS ·
TELEVISIONS & STREAMING DEVICES · HOUSEHOLD APPLIANCES PARTS

**Competidores em MLB (`COMP_SITE_ID`):**

| Código | Competidor | Papel |
|---|---|---|
| `AMB` | Amazon Brazil | maior ofensor real em todas as D1s |
| `MGL` | MagazineLuiza | ofensor estrutural do War Room |
| `SPE` | Shopee | foco do Shield |
| `CBH` | Casas Bahia | ⚠️ confirmar o valor exato em produção |
| `AMR` | Americanas | **excluída** por decisão minha — share irrelevante |
| `ALB` | Aliexpress | bucket "Others" |

**Segmento de seller (`SEGMENTO_SELLER_DETAIL`):**
`ASESORADO PF` (carteira Paid Farming — foco do War Room) · `SD ASESORADO` / `SD NO ASESORADO` (Seller Dev) ·
`CBT ASESORADO` / `CBT NO ASESORADO` / `CBT MT ASESORADO` · `FIRST PARTY` (1P) · `3P ASESORADO DIRECTO`

⚠️ **`ITEM_PARTY_TYPE='3P'` ≠ `SEGMENTO_SELLER_DETAIL != 'FIRST PARTY'`.** O segundo inclui CBT, que
**puxa o BPC para baixo**. Escolha conforme a pergunta e declare qual usou.

**Regiões (`RECEIVER_STATE`, formato `BR-SP`):**
Norte AC AM AP PA RO RR TO · Nordeste AL BA CE MA PB PE PI RN SE · Centro-Oeste DF GO MS MT ·
Sudeste ES MG RJ SP · Sul PR RS SC

**Janelas:** Q fechado · QTD · MTD (até D-1 ou D-2) · **datas duplas** (03/03, 04/04, 05/05… — eventos de pricing)

---

## 8 · Prompt inicial para uma sessão nova

> *Trabalhamos KPIs de pricing e BPC HE/MLB. Consulte a skill `bpc-reader` e o
> `BPC_Projeto_Contexto_Mestre.md` antes de responder. Filtros default do War Room:
> `SIT_SITE_ID='MLB'`, `FAVORABILITY_TYPE='BOX_ALL_ABC_PIX'`, `KMI='true'`,
> `COALESCE(FLG_BULKY,'false')!='true'` (em PIX, H&B fica sempre fora), `VERTICAL='HOME ELECTRONICS'`.
> Análises de oportunidade vs competidor usam Winner view (`COMP_SITE_ID_WINNER='XXX'`); UNNEST view só
> quando se quer todas as visitas do competidor. Output: 1 casa decimal com vírgula, K/Mi/Bi, deltas em pp,
> tom direto.*
