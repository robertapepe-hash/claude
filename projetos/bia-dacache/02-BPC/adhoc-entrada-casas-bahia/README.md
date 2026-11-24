# Entrada da Casas Bahia no MELI — Incrementalidade Regional

> Análise ad-hoc | Iniciada: 2026-05-28 | Owner: Beatriz Dacache
> Stakeholder: liderança HE (Maira Fanchin Garcia)

## Pergunta de negócio

Em nov/2025 a Loja Oficial da Casas Bahia (CBH) entrou no 3P do MELI. Proposta de valor: **competitividade de preço + capilaridade logística** (frete grátis e SLA bom em regiões antes mal servidas pelo MELI — N, NE, CO, S).

A pergunta principal é dupla:
1. **(Ponto 1 — outro time)** A entrada da CBH canibalizou sellers já existentes ou o 1P? Em quanto? Quais sellers foram prejudicados?
2. **(Ponto 2 — FOCO DESTE ESTUDO)** Quanto a CBH contribuiu pro crescimento do MELI nas regiões antes pouco competitivas? Trouxe sortimento incremental? Ou canibalizou sellers regionais que eram únicos mesmo sendo fracos?

Este estudo **prioriza o Ponto 2**. Estrutura modular pra ativar o Ponto 1 se o outro time não entregar.

## Escopo

- **Universo**: Vertical Home Electronics (HE). Technology fica fora — CBH tem share ≤0,4% em qualquer D1 de Tech, sem materialidade. Tech entra apenas como nota de rodapé / big numbers no fechamento.
- **D1 esperadas com insight**: LARGE APPLIANCES, TELEVISIONS & STREAMING DEVICES, SMALL APPLIANCES (CBH com 13-17% share em 1 semana de abril/26).
- **Seller CBH**: `CUS_CUST_ID_SEL = 1046986303` / `SELLER_NAME = LOJAOFICIALCASASBAHIA` (único ID).
- **Período pós-CBH**: nov/2025 → abr/2026 (6 meses cheios).
- **Comparações temporais** (3 lentes combinadas):
  - **Lente 1 (núcleo)**: fev-abr/2026 vs fev-abr/2025 — sem BF, CBH consolidada, mesmo período do ano
  - **Lente 2 (robustness)**: ago-out/2025 (pré-CBH) vs fev-abr/2026 (pós-CBH consolidada) — mesmo macro recente
  - **Lente 3 (contexto)**: série mensal jan/2024 → abr/2026 — revela inflexão

## Metodologia em 5 etapas

### Etapa 0 — Setup ✅
Confirmação de schema, valores de VERTICAL/D1, presença CBH, volume de bytes.

### Etapa 1 — Caracterização CBH
Quem é a CBH no MELI hoje. NMV/NSI/ASP/SKUs/catálogos por mês, share no HE, distribuição UF e por região, breakdown D1/D2.

### Etapa 2 — Crescimento regional com vs sem CBH
- NMV HE por região, YoY e nas 3 lentes temporais
- NMV HE **ex-CBH** por região
- Δ = contribuição bruta CBH ao growth regional
- Cruzamento BPC favorability pré-entrada (backup)

### Etapa 3 — Sortimento incremental e Buy Box
- ITEM_ID da CBH classificados em:
  - **Tipo A**: catálogo (CAT_PRODUCT_ID) já existia em MELI
  - **Tipo B**: catálogo novo em MELI (incremental puro)
- Por catálogo: quem era BB winner pré-CBH, quem perdeu/manteve espaço
- Recorte regional: CBH ganhou BB em quais UFs

### Etapa 4 — Canibalização regional (hipótese, DiD leve)
- Top sellers HE por região pré-CBH
- Diff-in-diff leve: queda em regiões "alvo CBH" vs SE (controle)
- Identificação de sellers prejudicados regionalmente
- **Declarado abertamente como correlacional, não causal**

### Etapa 5 — Síntese executiva
Doc final pra liderança com:
- Contribuição CBH ao growth regional (números diretos)
- Heatmap UF × D2
- Sortimento: % incremental vs replicado
- Canibalização estimada (com disclaimer)
- O que não conseguimos responder (limitações)
- Big numbers Tech (escopo de fechamento)

## Limitações metodológicas declaradas

1. **Sem contrafactual real** — não houve teste A/B de entrada. Tudo é correlacional, não causal.
2. **Sazonalidade BF 2025** — entrada em nov/25 = mês de pico. Comparações YoY clássicas sofrem; mitigado com Lente 1.
3. **Crescimento orgânico MELI 24→25** foi alto — pode enviesar baselines YoY. Mitigado com Lente 1 (períodos recentes).
4. **War Room PIX** — sem campanha ativa atualmente, ruído baixo. Documentado.
5. **Canibalização inferida ≠ comprovada** — Etapa 4 é hipótese, não prova.

## Schema relevante (DM_EFICIENCIA_MLB)

| Campo | Uso |
|---|---|
| `CUS_CUST_ID_SEL` | Seller ID (CBH = 1046986303) |
| `SELLER_NAME` | Nome do seller |
| `ITE_ITEM_ID` | Item ID (anúncio do seller) |
| `MELI_ID` | ID do anúncio MELI |
| `ITE_ITEM_CATALOG_PRODUCT_ID` | Product ID / Buy Box ⭐ |
| `BUYBOX_FLG` | Flag BB |
| `DOM_DOMAIN_AGG1` / `_AGG2` / `_AGG3` | D1 / D2 / D3 |
| `VERTICAL` | Vertical (filtro HE) |
| `RECEIVER_STATE` | UF do buyer |
| `SENDER_STATE` | UF do seller |
| `CUS_PARTY_TYPE_ID` | 1P / 3P / PL |
| `CLUSTER_NAME` | Segmentação seller |
| `GMV_LC` | Valor em BRL |
| `SI` | Itens vendidos |
| `NMV_FLG` | TRUE = entra no NMV (sem combo free / cancelado / devolvido) |
| `ORD_CLOSED_DT` | Data de fechamento (referência) |

## Estrutura da pasta

```
2026-05-entrada-cbh-incrementalidade-regional/
├── README.md                       # Este arquivo
├── queries/                        # SQL de cada etapa
├── outputs/                        # CSVs/XLSX resultantes
└── notas/                          # Notas de reunião e contexto adicional
```

## Status

| Etapa | Status |
|---|---|
| 0 — Setup | ✅ Completa |
| 1 — Caracterização CBH | 🔵 Em andamento |
| 2 — Crescimento regional | ⏳ Pendente |
| 3 — Sortimento / Buy Box | ⏳ Pendente |
| 4 — Canibalização regional (DiD) | ⏳ Pendente |
| 5 — Síntese | ⏳ Pendente |
| Ponto 1 (stand-by) | ⏳ Stand-by |
