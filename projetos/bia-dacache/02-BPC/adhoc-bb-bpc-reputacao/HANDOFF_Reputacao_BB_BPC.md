# Reputação × Buy Box × BPC × Venda — Handoff técnico

> **Objetivo:** diagnosticar se a queda de reputação de um seller prejudica o negócio (perda de Buy Box, BPC, conversão, NMV) e se vale a MELI **blindar** a reputação de sellers estratégicos.
> **Escopo:** 30 top sellers assessorados (ex-1P) de **HOME ELECTRONICS / Large Appliances + TV**, **H&B (Heavy & Bulky)**, site MLB.
> **Período:** análise principal YTD Jan–Mai/26; extensão **Q2/2025 → Mai/2026 (14 meses)** para event-study e pico.
> **Autora:** Beatriz Dacache · jun/2026 · Pasta: `Ad-Hoc/2026-06-bb-bpc-reputacao/`

---

## 1. Metodologia (v2.0) — leia primeiro

A v1 (Google Sheets original) usava **"share de ganhos"** (ganhos em green ÷ total de ganhos), que é **confundido por exposição**: um seller que vive em yellow terá a maioria dos ganhos em yellow mesmo sem efeito de reputação. **Trocamos pela taxa within-seller.**

- **Normalizar sempre:** `taxa de ganho de BB (reputação R) = item-dias com GANHADOR_BB=1 e reputação R ÷ item-dias na reputação R`. Nunca "share".
- **Within-seller:** comparar cada seller **consigo mesmo** (dias green vs dias abaixo) e tirar a média dos deltas. Evita paradoxo de Simpson (sellers grandes/competitivos enviesam o pooled).
- **Grão certo por pergunta:**
  - **reputação → BB** é **item-dia** (ganhar/perder catálogo) → tabela `DM_COM_COMPETENCIA`.
  - **reputação → conversão/NMV** é **seller-dia** (a reputação é da loja) → base diária (rep + visitas + venda).
- **Separar pico vs normal** — o efeito reputação→BB é **fenômeno de pico**.
- **Reputação como gradiente ordinal:** `green_platinum > green_gold > green_silver > green > light_green > yellow > orange > red`. "Verde" = qualquer green-family + light_green; "abaixo" = yellow/orange/red. `newbie` = seller novo, **excluir**.

### Ressalvas obrigatórias (sempre declarar)
1. **`GANHADOR_BB` é proxy de menor preço MELI** (`item == BEST_MELI_MIN_PRICE`), **não** o ganhador real do Buy Box (que pondera reputação, frete etc.). Por isso reputação→BB sai fraco: o proxy é dominado por preço.
2. **Tautologia BB↔BPC:** ganhar BB (= menor preço) e ter BPC alto são quase a mesma coisa.
3. **Causalidade reversa:** picos de demanda/promo geram mais pedidos → mais atritos → reputação cai *depois*. Logo, períodos degradados têm visitas/conversão **altas** — não é a queda que melhora a venda.
4. **A blindagem "suja" a base:** o que o buyer vê é `Current` (público), que pode estar blindado (verde) sobre um `Real` pior. E a blindagem é **seletiva** (MELI escolhe quem/quando) → comparar blindado vs não-blindado é confundido por seleção.
5. **Base do BB era truncada (25k linhas)** no Sheets original; refeita completa.
6. **Generalização:** são top sellers assessorados (grandes, agressivos em preço). Não extrapolar pra sellers menores sem novo recorte.

---

## 2. Fontes e queries

| Tema | Tabela (em `meli-bi-data.WHOWNER`) | Arquivo da query |
|---|---|---|
| BB / BPC (item-dia) | `DM_COM_COMPETENCIA` | `query.sql` / `_panel_template.sql` |
| Reputação diária (Real/Current/Blindado) | `BT_REP_SELLER_REPUTATION_LOG` | `_ext_A_rep.sql` |
| Visitas diárias (escopo H&B) | `BT_VISITS_MLB_UF` (+ scope via `DM_EFICIENCIA_MLB`) | `_ext_B_vis.sql` |
| Venda diária (NMV/NSI) | `DM_EFICIENCIA_MLB` | `_ext_C_venda.sql` |

**Notas de execução**
- As tabelas existem em `meli-bi-data.WHOWNER` (os projetos Fury `pdme000107/000147` deram **Access Denied** com as credenciais da Bia — usar WHOWNER).
- `BT_VISITS_MLB_UF` é **ultragranular** (UF × item × dia × device × plataforma × CEP) e **sem clustering por seller** → o filtro de seller **não poda o scan** (~690 GB / ~US$ 4,2 em 14 meses). A query **já consolida por loja** (SUM); não há estado no output. Não há tabela de visitas pré-agregada no WHOWNER.
- BB / competitividade: `GANHADOR_BB = (item == BEST_MELI_MIN_PRICE.ITE_ITEM_ID)`; `BPC = (VISITS_MATCH + VISITS_CHEAPER) / (VISITS_MATCH + VISITS_CHEAPER + VISITS_EXPENSIVE)`.
- Base diária: join em Python por (seller_id, dia): A=rep, B=visitas, C=venda; `CVR% = NSI/Visitas*100`; dias sem atividade no escopo = 0.
- Dica Windows/encoding: rodar `cmd /c "bq query ... < query.sql > out.csv"` (o pipe do PowerShell 5.1 corrompe acento).

---

## 3. Achados confirmados

### A) Quem cai é efeito de PERFIL (logística), não de período
- Só **13/30 sellers** ficaram abaixo de verde em 14 meses (no YTD, 11/30; **19 nunca caíram**).
- **D2C 6/7 caem** (média 45% dos dias abaixo) vs **SELLER 5/23** (5,5%). **ME1 (logística própria) 7/8** (47%) vs **ME2 (logística MELI) 4/22** (3%).
- Campeões de queda: MIDEA, Electrolux, BUD — todos **D2C + ME1**. → **ME1/entrega própria acumula atritos e derruba reputação; ME2/Full se mantém verde.**

### B) Reputação → ganho de BB: escalona por cor (não é binário)
- Binário "verde vs abaixo" within-seller ≈ **0** (yellow domina o "abaixo" e yellow ≈ neutro).
- **Gradiente (dose-resposta), within-seller:** verde − yellow **+0,6 pp** · verde − orange **+2,8 pp** · verde − red **+4,6 pp**. → **quanto mais grave, maior o tombo no BB.**
- **Fenômeno de pico:** delta verde−yellow normalizado = **+4,0 pp no Q4/25** vs **−2,0 pp no YTD normal** (e +3,7 pp no recorte antigo Out–Mar, que incluía o pico).
- **orange/red são raros:** 3,5% dos item-dias, concentrados em ~6 sellers (quase todos ME1). Electrolux ficou 31 dias no vermelho (20,5% do YTD); demais 3–24 dias.

### C) Ganho de BB → BPC: firme e estável
- Ganhador de BB tem BPC **+13 pp** melhor (30 sellers) — original 5 sellers dava +23 a +28 pp. Estável entre períodos e perfis. **Ressalva: tautológico** (BB = menor preço ≈ BPC).

### D) Reputação → conversão / NMV: SEM penalidade (event-study limpo, 14m)
- Pré-tendência **plana** (desenho válido). Pós-queda pública: CVR **+0,18 a +0,25 pp** e NMV/visita **+R$2,5 a +4,5** (significativos). → **cair abaixo de verde NÃO derruba venda**; se algo, conversão sobe (reação de preço/promo — causalidade reversa).
- DiD contemporâneo confirma: degradação ↔ conversão maior, forte no orange/red.

### E) Blindagem: já existe, pesada no severo, mas efeito não-identificável
- 14% dos seller-dias blindados (**Q4/25 = 20%**, pico). ~75% do orange e ~56% do red são **mostrados como verdes** → buyer quase nunca vê severo.
- Efeito medido de "mostrar verde" na conversão: **nulo a negativo** (CVR −0,14 ns; NMV/visita −R$11**; red −1,3***). **Mas é seleção** (MELI blinda os casos mais frágeis) → **não dá pra creditar/descreditar a blindagem com observacional.**

---

## 4. Conclusão e próximos passos
- **Para top sellers assessorados, a reputação tem impacto de negócio limitado:** não move o BB de forma clara (proxy preço; só dose severa em pico), e **não há penalidade de conversão/NMV** ao cair.
- **A justificativa de receita para blindar é fraca** com os dados atuais.
- **Para decidir blindagem de verdade → A/B test** (blindar aleatoriamente um grupo): é o único jeito de furar a seleção. Considerar também canais não medidos (confiança/recompra de longo prazo, churn, retenção do seller).
- **Pendências:** (i) repetir com o **ganhador real do BB** (não o proxy de preço); (ii) recorte de **sellers menores** (reputação pode pesar mais); (iii) costurar BB/BPC (item-dia) resumido a seller-dia com a base diária pra cadeia completa.

## 5. Arquivos da pasta
- `bd_panel_master.csv` — painel BB item-dia (30 sellers, YTD).
- `bd_diaria_14m.csv` — base diária seller-dia (rep+visitas+venda, 14 meses).
- `sellers.csv` — 30 sellers + perfil (D2C/SELLER) + %ME1/%ME2.
- Queries: `query.sql`, `_panel_template.sql`, `_ext_A_rep.sql`, `_ext_B_vis.sql`, `_ext_C_venda.sql`.
- Scripts de análise: `_panel_analyze.py`, `_did.py`, `_ext_event.py`, `_ext_shield.py`, etc.
- `METODOLOGIA 2.0.docx` — método normalizado (referência canônica).
- `BB x BPC - Consolidado.xlsx` — consolidado executivo.
