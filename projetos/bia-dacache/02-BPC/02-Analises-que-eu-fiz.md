# Inventário das análises de BPC

> O que foi produzido, o que cada uma descobriu e onde o artefato está.
> ⚠️ **Nem tudo está neste pacote.** Vários entregáveis vivem no Grid MELI ou saíram de sessões antigas do
> Cowork, cujos arquivos não ficaram na máquina. Marquei cada caso.

---

## Legenda

| Marca | Significado |
|---|---|
| 📦 | o arquivo está **neste pacote** |
| 🔗 | vive no **Grid MELI** — peça acesso ao doc |
| ⚠️ | **não localizado** — reconstruível pelo método documentado, mas o arquivo original não está aqui |

---

## A · War Room BPC PIX KMI HE

### A.1 · Diagnóstico do gap vs Magalu ⚠️
**Pergunta:** onde exatamente perdemos para o MGL em PIX KMI, e quanto vale reverter?

**Método:** Winner view (`COMP_SITE_ID_WINNER='MGL'`), drill **D1 → D2 → marca → seller**, com cascata de
impacto ponderado até a vertical.

**Achados (Q2 QTD 2026):**
- BPC vs MGL Winner em HE = **32,8%** (gap de quase 60 pp), com MGL pesando ~20% das visitas de HE
- **Small Appliances** = 50% do universo vs MGL, BPC 29,4%
- Dentro de Small, **Kitchen** = 74%, BPC 27,3%
- Dentro de Kitchen, **Mondial** — 97% das visitas Mondial-em-Small estão em Kitchen, BPC 17,8%
- Sellers cirúrgicos: Mercado Livre Eletronicos (1P, 53% do universo Mondial vs MGL, BPC 17%) ·
  LOJAOFICIALCASASBAHIA (9,8%) · **DUTRA_MAQUINAS (4,8%)** · LOI BRASIL (8,7%) · MEGABYTE MAGAZINE (14,7%)

**Por que isso funcionou como narrativa:** o drill mostra que **duas células explicam quase tudo**. Levar
"o BPC caiu" para a liderança não gera ação; levar "Small → Kitchen → Mondial → 5 sellers" gera reunião.

*Artefatos originais (`Diagnostico_BPC_HE_Q2_YTD_v2.pptx`, `Deep_Dive_Sellers_Brands_WarRoom_KMI_HE.md`,
`BPC_analysis_kit.md`) ficaram na sessão do Cowork. O método está integralmente em
`originais/BPC_Projeto_Contexto_Mestre.md` §6.*

### A.2 · Quick wins de paridade ⚠️ — **pendência aberta**
`LOJAGAZIN` (BPC ~8%) e `VGSHOPOFICIAL` (BPC ~5%). **BPC tão baixo não é problema comercial — é sintoma de
erro sistêmico de catálogo.** Auditar antes de escalar como caso de preço. Nunca foi concluída.

### A.3 · Dashboard BPC KMI HE 🔗 ⚠️
HTML interativo V5 (~220 KB), 3 abas (Overview / Marcas / Sellers), com *quick start* por papel
(Diretoria / Brands / Farming), best & worst por dimensão e comparação com o bench de KMI do Pricing.
Tinha uma **scheduled task** (`refresh-grid-bpc-kmi-he`, segundas às 7h) que rodava 4-6 queries,
reconstruía o HTML e subia no Grid.

⚠️ **Estava pronto para validação final e nunca foi assinado.** Se alguém retomar, o modelo de pipeline
mais maduro que deixo é o do Shield (`../01-SHIELD/01-Ways-of-Working-Grid-Shield.md`).

### A.4 · Modais de entrega — ME1 vs ME2 ⚠️
**Pergunta:** para itens H&B (3P, Asesorado PF), qual modal é mais competitivo?

**Achados:**
- **BOX (preço):** ME1 vence ME2 sempre — gap de **10,5 pp** em maio
- **SHP (frete):** ME2 vence ME1 — gap de **12-24 pp**, sustentado
- **Por ASP:** ME1 vence em 0-1499; em 1500+ o BOX virou para ME1 em maio (de empate para +12 pp)
- **Por região (Asesorado PF):** Sudeste ME1 +16 pp em preço · Sul ME1 +26 pp (0-1499) ·
  **Nordeste INVERTE — ME2 vence em BOX, única região** ⚠️ · Centro-Oeste e Norte empatam, volume baixo

**Hipótese central:** para mover BPC de frete em H&B, empurrar sellers de ME1 → ME2. Para preço, vigiar
sellers ME2 que estão piorando.

**Por que a inversão do Nordeste importa:** é o tipo de achado que quebra uma recomendação nacional. Se
existir plano de migração de modal, o Nordeste precisa de tratamento próprio.

### A.5 · Queries de apoio 📦
`queries-e-scripts/bpc_pix_mtd.sql` — BPC PIX por D2 × KMI com `GROUPING SETS` (MTD vs mês anterior,
mesma janela de dias). É o esqueleto mais reaproveitável que deixo: troque as datas e a D1.
`queries-e-scripts/bpc_shipping_mtd.sql` — equivalente para a lente de frete.
`queries-e-scripts/bpc_check_favtypes.sql` — sanity de quais `FAVORABILITY_TYPE` existem no recorte.

---

## B · Shield vs Shopee (BPC)

### B.1 · XLSX mensal por D1 📦
`../01-SHIELD/entregaveis/Shield_BPC_D1_vs_Shopee_Mai_vs_Abr_2026_v4.xlsx`
Uma aba por D1 (6 D1s) · bloco preto (BPC + Opp + SoO dos 5 competidores) · bloco laranja (BPC vs Shopee
Winner por faixa de ASP) · SoO da Shopee aberto por faixa · referências de março e abril fechados · dados raw.

### B.2 · Decks mensais 📦
`../01-SHIELD/entregaveis/Shield_HE_Mai_2026.pptx|.pdf` e `Shield_Tech_Mai_2026.pptx|.pdf`
(slide de overview + heatmap). Também no Grid: HE `01KS5XRQ9BY2VSX5W46EWBDF2T` · Tech `01KS5XRZEWWNM3T7QVHAKHBF3M`.

### B.3 · Dashboard item-level 📦
`../01-SHIELD/entregaveis/Shield_BPC_Items_vs_Shopee.html` — dropdown de 15 `MELI_ID`, evolução semanal do
BPC vs Shopee, preço MELI × preço Shopee e a tabela de sellers que compõem o BPC daquele item.
Foi o formato que melhor funcionou em conversa com Brands: **desce ao item que a pessoa reconhece.**

### B.4 · Share of Opportunity mensal 📦
`../01-SHIELD/entregaveis/Shield_SoO_Mensal_Large_App_BOX.html`

### B.5 · Ad hoc entregues só por chat ⚠️
BPC semanal item × seller (16 `MELI_ID`) mar-mai · BPC de marcas em Large 500-1500 comparando BOX vs PIX ·
BPC de Large 3P por ASP nas datas duplas (3.3, 4.4, 5.5) nas 3 lentes · BPC Large 3P sem 1P em maio MTD
(33,1%) · BPC dos grupos Engage e REDE Marketplace (SHP + PIX) por mês.

---

## C · Análises no Grid que não estão neste pacote 🔗

Ficam registradas aqui para que ninguém as reconstrua do zero sem saber que existem. **Peça acesso aos
docs ou reconstrua pelo método** — em todos os casos a metodologia está descrita nos documentos de contexto.

| Análise | O que é | Onde |
|---|---|---|
| **MBR HE — BPC por ASP + Cobertura** | Widget com BPC de HE por faixa de ASP / mês / data dupla, em 3 lentes (Total · Shopee · Shopee winner) + aba de cobertura da Shopee | Grid, doc `01KXPCDFV8…` |
| **BPC PIX HE — funil cobertura × preço** | Funil match-first comparando PIX de HE vs Shopee. **239 itens precisavam de PIX** (159 com gap >5%), oportunidade de **+3,26 pp de BPC** | Grid |
| **BPC marca × D2C × 1P (evolutivo)** | Metodologia mista por D1/D2 — marca e 1P via `BOX_ALL_ABC`, D2C via `BOX_MATCH_SELLER`. Replicável por categoria | Grid |

⚠️ Nota sobre a cobertura: `LK_COMP_COVERAGE_COMPETITORS` é **nível site**, não nível item — a fórmula de
cobertura precisou de calibração. Se for reusar, valide antes.

---

## D · Ad hoc que estão neste pacote 📦

| Pasta | Pergunta | Veredito |
|---|---|---|
| **`adhoc-bb-bpc-reputacao/`** | Vale a pena a MELI blindar a reputação de sellers estratégicos? | **A justificativa de receita é fraca.** Reputação → Buy Box só aparece em dose severa e em pico; **não há penalidade de conversão ou NMV** ao cair de verde |
| **`adhoc-entrada-casas-bahia/`** | A entrada da Casas Bahia no 3P foi incremental ou canibalizou? | **Somou.** +9,9 pp ao crescimento YoY de HE, com gradiente perfeito de capilaridade (Norte +17,3 pp → Sul +7,0 pp). Canibalização é ordens de magnitude menor que o NMV trazido |

Cada uma tem seu `00-RESUMO.md`.
