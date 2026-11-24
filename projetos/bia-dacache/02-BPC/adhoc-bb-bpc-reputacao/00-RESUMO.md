# Reputação × Buy Box × BPC × Venda

> **Pergunta:** a queda de reputação de um seller prejudica o negócio? Vale a MELI **blindar** a reputação
> de sellers estratégicos?
> **Escopo:** 30 top sellers assessorados (ex-1P) de Home Electronics — Large Appliances + TV, **H&B**, MLB
> **Período:** principal YTD jan-mai/26 · extensão Q2/2025 → mai/2026 (14 meses) para o *event study*
> **Quando:** junho/2026

---

## A resposta curta

**Para top sellers assessorados, a reputação tem impacto de negócio limitado — e a justificativa de receita
para blindar é fraca com os dados disponíveis.**

- Reputação → Buy Box: só aparece em **dose severa** e é **fenômeno de pico**
- Buy Box → BPC: firme (+13 pp), mas **tautológico**
- Reputação → conversão/NMV: **sem penalidade nenhuma** — se algo, a conversão sobe
- Blindagem: já existe e é pesada no severo, mas **o efeito não é identificável** com dado observacional

**Para decidir de verdade, só um A/B test** — blindar aleatoriamente um grupo. É o único jeito de furar a
seleção.

---

## Por que a v1 estava errada (a lição metodológica)

A versão original, em Sheets, usava **"share de ganhos"** — ganhos em verde ÷ total de ganhos. Isso é
**confundido por exposição**: um seller que vive em amarelo terá a maioria dos ganhos em amarelo mesmo sem
efeito nenhum de reputação.

**A correção, em três movimentos:**

1. **Normalizar sempre, nunca usar share.**
   `taxa de ganho de BB na reputação R = item-dias com GANHADOR_BB=1 e reputação R ÷ item-dias na reputação R`

2. **Comparar cada seller consigo mesmo** (*within-seller*): dias verdes vs dias abaixo, e depois a média
   dos deltas. Sem isso, sellers grandes e agressivos em preço dominam o pooled — **paradoxo de Simpson**.

3. **Usar o grão certo para cada pergunta:**
   - reputação → **BB** é **item-dia** (ganhar ou perder o catálogo) → `DM_COM_COMPETENCIA`
   - reputação → **conversão/NMV** é **seller-dia** (a reputação é da loja) → base diária de rep + visitas + venda

> 🔑 **Transferível:** sempre que a métrica for "quantas vezes X aconteceu", pergunte **"dividido por
> quantas oportunidades de acontecer?"**. Share sem denominador de exposição é quase sempre exposição
> disfarçada de efeito.

**Reputação é gradiente ordinal**, não binário:
`green_platinum > green_gold > green_silver > green > light_green > yellow > orange > red`.
"Verde" = qualquer green-family + light_green. "Abaixo" = yellow/orange/red. **`newbie` se exclui.**

---

## Os achados

### A · Quem cai é efeito de perfil logístico, não de período
- Só **13 de 30 sellers** ficaram abaixo de verde em 14 meses (19 nunca caíram)
- **D2C: 6 de 7 caem** (média de 45% dos dias abaixo) vs **SELLER: 5 de 23** (5,5%)
- **ME1 (logística própria): 7 de 8** (47%) vs **ME2 (logística MELI): 4 de 22** (3%)
- Campeões de queda — MIDEA, Electrolux, BUD — todos **D2C + ME1**

> **ME1 acumula atritos e derruba reputação; ME2/Full se mantém verde.** Se houver plano de blindagem, o
> alvo natural é quem opera logística própria.

### B · Reputação → ganho de BB: escalona por cor
- Binário "verde vs abaixo" *within-seller* ≈ **0** — porque amarelo domina o "abaixo" e amarelo ≈ neutro
- **Gradiente (dose-resposta):** verde − amarelo **+0,6 pp** · verde − laranja **+2,8 pp** · verde − vermelho **+4,6 pp**
- **É fenômeno de pico:** o delta verde−amarelo foi **+4,0 pp no Q4/25** contra **−2,0 pp no YTD normal**
- Laranja e vermelho são **raros** — 3,5% dos item-dias, concentrados em ~6 sellers, quase todos ME1

### C · Buy Box → BPC: +13 pp, estável — **mas tautológico**
Ganhador de BB tem BPC 13 pp melhor. Só que, no proxy usado, ganhar BB **é** ter o menor preço MELI. É
quase a mesma coisa medida duas vezes.

### D · Reputação → conversão / NMV: **sem penalidade** (event study limpo, 14 meses)
Pré-tendência **plana** (desenho válido). Depois da queda pública: CVR **+0,18 a +0,25 pp** e NMV/visita
**+R$ 2,5 a 4,5**, significativos.

**Cair abaixo de verde não derruba a venda.** Se algo, a conversão sobe — o que aponta para **causalidade
reversa**: pico de demanda → mais pedidos → mais atritos → reputação cai *depois*.

### E · Blindagem: existe, é pesada no severo, e o efeito não é medível
- **14% dos seller-dias blindados** — no Q4/25, **20%**
- ~**75% do laranja** e ~**56% do vermelho** são mostrados como verdes → o comprador quase nunca vê severo
- Efeito medido de "mostrar verde" na conversão: **nulo a negativo**
- **Mas é seleção** — a MELI blinda os casos mais frágeis. Não dá para creditar nem descreditar a blindagem
  com dado observacional

---

## Ressalvas obrigatórias — declare sempre

1. **`GANHADOR_BB` é proxy de menor preço MELI** (`item == BEST_MELI_MIN_PRICE`), **não** o ganhador real
   do Buy Box (que pondera reputação, frete etc.). Por isso reputação → BB sai fraco: o proxy é dominado
   por preço.
2. **Tautologia BB ↔ BPC** — ganhar BB e ter BPC alto são quase a mesma coisa neste desenho.
3. **Causalidade reversa** — períodos degradados têm visitas e conversão altas. Não é a queda que melhora a venda.
4. **A blindagem "suja" a base** — o comprador vê o `Current` (público, possivelmente blindado) sobre um
   `Real` pior. E a blindagem é **seletiva**.
5. **A base de BB estava truncada** (25 mil linhas) no Sheets original — foi refeita completa.
6. **Não generalize** — são top sellers assessorados, grandes e agressivos em preço.

---

## Fontes e execução

| Tema | Tabela (`meli-bi-data.WHOWNER`) | Query |
|---|---|---|
| BB / BPC (item-dia) | `DM_COM_COMPETENCIA` | `queries-e-scripts/query.sql`, `_panel_template.sql` |
| Reputação diária (Real/Current/Blindado) | `BT_REP_SELLER_REPUTATION_LOG` | `_ext_A_rep.sql` |
| Visitas diárias (escopo H&B) | `BT_VISITS_MLB_UF` | `_ext_B_vis.sql` |
| Venda diária (NMV/NSI) | `DM_EFICIENCIA_MLB` | `_ext_C_venda.sql` |

**Fórmulas usadas:**
```
GANHADOR_BB = (item == BEST_MELI_MIN_PRICE.ITE_ITEM_ID)
BPC         = (VISITS_MATCH + VISITS_CHEAPER) / (VISITS_MATCH + VISITS_CHEAPER + VISITS_EXPENSIVE)
CVR%        = NSI / Visitas × 100
```

**Notas de execução que economizam tempo:**
- As tabelas estão em `meli-bi-data.WHOWNER`. Os projetos Fury (`pdme000107`/`000147`) deram **Access
  Denied** — não perca tempo tentando por lá.
- **`BT_VISITS_MLB_UF` é ultragranular** (UF × item × dia × device × plataforma × CEP) e **não é
  clusterizada por seller** → filtrar seller **não poda o scan**. São ~**690 GB / US$ 4,2** em 14 meses.
  Não existe tabela de visitas pré-agregada no WHOWNER.
- A base diária é montada em **Python**, com join por (seller_id, dia): A=reputação, B=visitas, C=venda.
  Dias sem atividade no escopo entram como 0.
- **Windows/encoding:** rode `cmd /c "bq query ... < query.sql > out.csv"` — o pipe do PowerShell 5.1
  corrompe acento.

📁 Scripts de análise em `queries-e-scripts/`: `_panel_analyze.py` · `_did.py` · `_did_event.py` ·
`_ext_event.py` · `_ext_shield.py` · `_corr.py` e outros.
📁 `METODOLOGIA 2.0.docx` — o método normalizado, referência canônica.
📁 `CONVERSA_completa_Reputacao_BB_BPC.md` — o histórico do raciocínio, incluindo o que foi descartado.
📁 `entregaveis/BB x BPC - Consolidado.xlsx` — consolidado executivo.

---

## Próximos passos, se alguém retomar

1. **Repetir com o ganhador real do Buy Box**, não o proxy de preço — é a correção que mais muda o resultado
2. **Recorte de sellers menores** — reputação provavelmente pesa mais fora do top assessorado
3. **Costurar BB/BPC (item-dia) resumido a seller-dia** com a base diária, para fechar a cadeia inteira
4. Considerar canais não medidos: confiança e recompra de longo prazo, churn, retenção do próprio seller
