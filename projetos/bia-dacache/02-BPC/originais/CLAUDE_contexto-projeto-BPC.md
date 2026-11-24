# BPC — Projeto Pricing (War Room + Shield)

> Cobre as 2 frentes de Pricing onde a Beatriz é focal.
> Última atualização: 2026-05-27

## O que está aqui

| Subprojeto | Pasta | Escopo |
|---|---|---|
| **War Room KMI PIX** | `War-Room-KMI-PIX\` | BPC PIX KMI Home Electronics MLB |
| **Shield Against Asians** | `Shield\` | BPC vs Shopee/Amazon, vertical H&T, ASPs |

## Contexto histórico (já documentado)

Antes de qualquer ação, considerar os documentos mestres existentes na raiz desta pasta:
- `BPC_Projeto_Contexto_Mestre.md` — contexto geral do projeto BPC HE
- `Shield_Shopee_Contexto_Mestre.md` — contexto mestre do Shield vs Shopee
- `BPC_Handoff_ClaudeCode.md` — handoff Cowork → Code (tabelas, fórmulas, regras, sellers)
- `bpc-reader_SKILL.md` — cópia local da skill oficial (use a skill ativa, não esta cópia)

## A) War Room KMI PIX — resumo operacional

**Objetivo**: monitorar e fechar gap do BPC PIX KMI de HOME ELECTRONICS em MLB.

### Filtros LOCKED
```sql
WHERE SIT_SITE_ID = 'MLB'
  AND FAVORABILITY_TYPE = 'BOX_ALL_ABC_PIX'
  AND KMI = 'true'                                       -- STRING lowercase
  AND COALESCE(FLG_BULKY, 'false') != 'true'             -- W/o H&B (em PIX, sempre fora)
  AND VERTICAL = 'HOME ELECTRONICS'
  AND DOM_AGG_1 IN (6 D1s HE)
```

### Métricas e meta
- **Meta BPC PIX KMI MLB geral Q1'26**: 0,5210 (52,10%) — fonte: skill `bpc-reader`
- **Real Q1'26 MLB geral**: 0,5021 (50,21%) — gap **-1,89 pp**
- **Meta BPC PIX KMI MLB HE**: [PREENCHER — buscar com Maira ou War Room]
- **Real BPC PIX KMI MLB HE**: [PREENCHER após validar com Maira]

### Foco atual (móvel)
Hipótese vigente: ofensor principal = **MGL (Magalu)** Winner, célula Small/Kitchen, marca Mondial.
Outras frentes em discussão. **Sempre consultar Beatriz se hipótese mudou** antes de assumir.

### Cadência
- Tema **on going** — sem entregável fixo
- Conversas e notas (Gemini) serão coladas pela Beatriz no chat — registrar como atualização de contexto

### Stakeholders
- Liderança alvo: **Maira Fanchin Garcia** (gerente Large Appliances)
- Originalmente atrelado a Brands/Farming (Sebah, Felipe) porque ofensores principais estavam embaixo deles, mas o reporte é pra liderança em geral

## B) Shield Against Asians — resumo operacional

**Objetivo**: monitorar BPC vs Shopee (foco) e Amazon, vertical H&T (Home Electronics + Technology), com leitura segmentada por ASP.

### Escopo da Beatriz
- Beatriz olha **apenas Home Electronics**. Tech é com **Lucas Kotinda**.
- Para BPC geral HE: olhar 3 D1s focais (LARGE APPLIANCES, HEATING/COOLING & AIR QUALITY, AUDIO & GENERAL ELECTRONICS)
- Para deeps: **sempre Large Appliances**

### Lentes de análise
- **BOX** (preço à vista — `BOX_ALL_ABC`)
- **SHP** (frete — `SHP_ALL_ABC`)
- **PIX** (preço PIX — `BOX_ALL_ABC_PIX`)

### Faixas ASP (BRL)
`<200` · `200-500` · `500-1500` · `1500-3000` · `>3000`

### Competidores
- **`SPE`** Shopee (foco principal)
- **`AMB`** Amazon (maior ofensor real)
- **`MGL`** Magalu (acompanhamento)
- **`AMR` (Americanas) excluída por decisão**

### Cadência
- Acompanhamento **recorrente**, entregável **mensal (PPT)** ao final do mês
- Cada mês ataca uma ASP/célula crítica diferente — **não há template fixo**

### Stakeholders
- **Julia de Cassia Arcoverde** organiza o squad
- Apresentação pra liderança H&T

## Tabelas e regras (resumo — detalhe em `bpc-reader`)

- Tabela principal: `meli-bi-data.WHOWNER.BT_COM_FAVORABILITY`
- KMI, FLG_BULKY, FLG_COMP_1P são **STRING lowercase** ('true'/'false')
- `COMP_RIVAL_NAME_WINNER` é top-level (sem UNNEST)
- Para marca: `UPPER(COALESCE(REAL_BRAND, BRAND))`
- **Winner view** (`COMP_SITE_ID_WINNER='XXX'`) para oportunidade vs competidor
- **UNNEST view** (`UNNEST(COMPETITORS)`) quando se quer todas as visitas do competidor
- Limite scan BQ 100 GB → adicionar `MELI_ID_TYPE='PRODUCT'` reduz 60-70%
