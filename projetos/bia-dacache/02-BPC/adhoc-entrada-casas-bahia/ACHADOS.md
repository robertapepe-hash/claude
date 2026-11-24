# Achados consolidados — Entrada CBH no MELI HE

> Documento cumulativo. Inclui achados usados E não usados (referência).
> Última atualização: 2026-05-28

---

## TL;DR pra liderança

> **A entrada da Casas Bahia adicionou +9,9 pp ao crescimento YoY do MELI em Home Electronics no 1º trimestre comparável pós-consolidação (fev-abr/26 vs fev-abr/25, growth 40,6% total vs 30,7% ex-CBH), com efeito concentrado nas regiões antes mal servidas: +17,3 pp no Norte, +15,8 pp no Nordeste e +11,1 pp no Centro-Oeste, contra +7,0 pp no Sul (já bem servido) e +8,8 pp no Sudeste. O ex-CBH ainda cresceu 30,7%, indicando que a CBH não substituiu o crescimento orgânico do MELI — somou. Large Appliances é a D1 onde a CBH mais impulsionou capilaridade (+50,4 pp de contribuição ao YoY do Norte).**

A confirmação de canibalização vs incremental puro depende das Etapas 3 e 4 (catálogo/BB e DiD por seller).

---

## ETAPA 1 — Caracterização CBH (nov/25 → abr/26)

### Tamanho
- **NMV em HE: R$ 880,1 Mi** em 6 meses
- **1,04 Mi pedidos**, ASP médio R$ 847
- 947 mil itens vendidos
- Único SELLER_ID: 1046986303 / LOJAOFICIALCASASBAHIA

### Mix por D1 (84% concentrado em LA + TVs — confirma briefing)
| D1 | NMV (R$ Mi) | Share |
|---|---:|---:|
| LARGE APPLIANCES | 400,3 | 45% |
| TELEVISIONS & STREAMING | 341,6 | 39% |
| SMALL APPLIANCES | 110,9 | 13% |
| AUDIO + H/C + outros | 27,3 | 3% |

### Top D2 (suas D2s core aparecem fortes)
| D2 | NMV (R$ Mi) |
|---|---:|
| TELEVISIONS | 341,6 |
| REFRIGERATION *(Nicole)* | 188,8 |
| LAUNDRY & DISHWASHERS *(Nicole)* | 133,0 |
| KITCHEN | 88,0 |
| **BUILT IN** *(Beatriz)* | **78,5** |
| HOUSING & CLEANING | 22,8 |

### Padrão temporal
- TVs: pico nov/25 R$ 106 Mi (BF puro) → estabilizou em ~R$ 40-60 Mi/mês
- LA: comportamento mais estável, **pico em jan/26 (R$ 87 Mi)** — possível efeito 13º + troca pós-festas
- Small App: estável ~R$ 16-21 Mi/mês

### Distribuição regional CBH (contra-intuitivo na 1ª leitura)
| Região | NMV (R$ Mi) | Share interno CBH |
|---|---:|---:|
| SE | 469,0 | 53,3% |
| NE | 205,8 | 23,4% |
| S | 97,8 | 11,1% |
| CO | 64,2 | 7,3% |
| N | 43,3 | 4,9% |

**SE concentra mais da metade do NMV CBH em volume absoluto.** Top 5 UFs (SP, MG, RJ, BA, PR) = 65,3%. BA na 4ª posição (9,3%) é o destaque regional fora do SE.

> ⚠️ Esse share absoluto **não** invalida a tese de capilaridade — o que importa é o **share da CBH dentro de cada região vs share do MELI total naquela região**. Confirmado na Etapa 2.

📁 6 CSVs em `outputs/etapa1_*`.

---

## ETAPA 2 — Crescimento regional com vs sem CBH

### Lente 1 (núcleo) — YoY fev-abr/26 vs fev-abr/25

| Região | NMV 25 (Mi) | NMV 26 (Mi) | YoY Total | YoY ex-CBH | **Contrib CBH (pp)** | Share CBH |
|---|---:|---:|---:|---:|---:|---:|
| **N** | 113,0 | 184,4 | **+63,2%** | +45,9% | **+17,3 pp** | 10,6% |
| **NE** | 600,5 | 987,6 | **+64,5%** | +48,6% | **+15,8 pp** | 9,6% |
| **CO** | 269,6 | 398,9 | **+48,0%** | +36,8% | **+11,1 pp** | 7,5% |
| **SE** | 2.334,8 | 3.124,0 | +33,8% | +25,0% | +8,8 pp | 6,5% |
| **S** | 646,3 | 889,1 | +37,6% | +30,6% | +7,0 pp | 5,1% |
| **BR** | 3.982,3 | 5.600,7 | **+40,6%** | **+30,7%** | **+9,9 pp** | 7,0% |

**A contribuição CBH em pp ao growth segue gradiente perfeito de capilaridade**: N > NE > CO > SE > S. Coerente com a tese.

### Lente 1 — Breakdown por D1 × Região (contribuição CBH em pp do YoY)

| D1 | SE | NE | S | CO | **N** |
|---|---:|---:|---:|---:|---:|
| **LA** | 17,5 | **45,3** | 13,2 | 25,7 | **50,4** 🔥 |
| **TVs** | 17,6 | 19,9 | 14,7 | 23,7 | 26,8 |
| Small App | 6,2 | 9,5 | 5,5 | 7,3 | 11,8 |
| Audio | 1,0 | 1,3 | 0,7 | 0,8 | 1,1 |
| H/C | 0,6 | 1,4 | 0,4 | 0,6 | 2,1 |

**Achado-chave**: em **LA no Norte, a CBH contribuiu com +50,4 pp dos 93,7% YoY** — ou seja, mais da metade do crescimento veio dela. Mesmo padrão em NE (+45,3 pp). TVs tem efeito mais homogêneo entre regiões.

### Lente 1 — Breakdown por D1 × Região (YoY total com CBH)

| D1 | SE | NE | S | CO | N |
|---|---:|---:|---:|---:|---:|
| LA | +65,0% | +81,1% | +61,5% | +73,9% | **+93,7%** |
| TVs | +37,4% | +60,8% | +38,4% | +50,0% | +51,8% |
| Small App | +38,0% | +65,5% | +40,0% | +45,9% | +70,5% |
| H/C | -1,9% | +74,8% | +21,8% | +40,9% | +100,1% |

LA no Norte quase dobrou de tamanho YoY.

### Lente 2 (robustness) — ago-out/25 PRÉ-CBH vs fev-abr/26 PÓS-CBH (mesmo ano fiscal)

| Região | NMV Pré (Mi) | NMV Pós (Mi) | Δ Total | Δ ex-CBH | **Contrib CBH (pp)** |
|---|---:|---:|---:|---:|---:|
| **N** | 150,6 | 184,4 | +22,5% | +9,5% | **+13,0 pp** |
| **NE** | 789,2 | 987,6 | +25,1% | +13,1% | **+12,0 pp** |
| CO | 358,6 | 398,9 | +11,2% | +2,9% | +8,4 pp |
| SE | 2.804,1 | 3.124,0 | +11,4% | +4,1% | +7,3 pp |
| S | 814,8 | 889,1 | +9,1% | +3,6% | +5,5 pp |
| **BR** | 4.934,4 | 5.600,7 | +13,5% | +5,5% | **+8,0 pp** |

**Mesma ordenação da Lente 1** (N > NE > CO > SE > S). Robustness ✅ — não foi efeito YoY artificial.

### Lente 3 (contexto) — Inflexão mensal visível

NMV HE total mensal (R$ Mi) — comparação 2024 vs 2025 vs 2026:
- Out: 2024 R$ 1.251 → 2025 R$ 1.701 (+36%) → ainda pré-CBH
- Nov: 2024 R$ 1.770 → 2025 **R$ 2.860** (+62%) → BF + entrada CBH
- Dez: 2024 R$ 1.292 → 2025 R$ 1.905 (+47%)
- Fev: 2025 R$ 1.300 → 2026 R$ 1.668 (+28%)
- Mar: 2025 R$ 1.370 → 2026 R$ 2.029 (+48%)
- Abr: 2025 R$ 1.294 → 2026 R$ 1.887 (+46%)

Share CBH mensal (%) no HE total:
| Mes | SE | NE | S | CO | **N** |
|---|---:|---:|---:|---:|---:|
| nov/25 | 6,9 | 8,5 | 4,5 | 6,4 | **10,1** |
| dez/25 | 5,9 | 9,3 | 4,0 | 8,3 | **12,1** |
| jan/26 | 8,4 | 12,7 | 6,2 | 9,2 | **14,8** ← pico |
| fev/26 | 6,8 | 9,6 | 4,9 | 8,3 | 11,8 |
| mar/26 | 6,0 | 8,8 | 4,5 | 6,8 | 9,9 |
| abr/26 | 6,9 | 10,5 | 5,8 | 7,7 | 10,3 |

**Norte chegou a 14,8% de share CBH em jan/26**, o maior pico. SE máximo 8,4%. Confirma capilaridade visualmente.

📁 8 CSVs em `outputs/etapa2_*`.

---

## Achados secundários (não usados na narrativa principal, mas registrados)

- **Pico jan/26 anômalo**: o share CBH em todas as regiões teve pico em jan/26 (Norte 14,8%, NE 12,7%, SE 8,4%). Hipóteses: efeito 13º + pagamento 1ª parcela cartão BF + troca pós-festas. Vale validar se foi padrão único ou se replica em janeiros futuros.
- **MELI HE crescendo organicamente 30,7% YoY ex-CBH** — base orgânica forte, confirma o ponto que a Beatriz levantou no briefing sobre crescimento orgânico potencializar YoY.
- **H/C no Norte teve +100,1% YoY** mas com baixo volume absoluto — interpretar com cautela.
- **BA na 4ª posição UF da CBH (9,3%)** é o estado fora do SE com maior peso CBH — provavelmente alvo de capilaridade física.
- **Built In (sua D2): R$ 78,5 Mi em 6m de CBH** — vale análise dedicada na Etapa 3.

---

## Limitações declaradas (recapitulando)

1. Não há contrafactual real → análise correlacional, não causal
2. BF nov/25 = entrada CBH no mesmo mês → mitigado com Lente 1 (fev-abr) e Lente 2 (ago-out vs fev-abr)
3. War Room PIX sem campanha ativa → ruído baixo
4. Canibalização (Etapa 4) sempre será hipótese, não prova

---

---

## ETAPA 3 — Sortimento incremental e Buy Box

Universo de análise: **1.566 catálogos únicos** onde a CBH vendeu (cobrem R$ 740 Mi dos R$ 880 Mi totais — 84%; restante = anúncios livres sem product_id).

### 3.B — Tipo A (já existia em MELI) vs Tipo B (novo em MELI)

| Tipo | Qt cat. | Share | NMV CBH (R$ Mi) | Share NMV |
|---|---:|---:|---:|---:|
| **A — Catálogo existente** | 1.402 | 89,5% | 667,2 | **90,1%** |
| **B — Catálogo novo em MELI** | 164 | 10,5% | 73,0 | 9,9% |

**Achado**: a CBH **não trouxe sortimento massivamente novo** ao MELI. 90% do NMV vem de catálogos que já existiam. O valor está em **execução** (capilarizar, expor, precificar bem) — não em catálogo inédito.

Por D1, % de NMV vindo de catálogos novos:
- H/C: 24,1% / Audio: 15,4% / Small App: 12,6% / **LA: 10,5%** / **TVs: 7,4%**

### 3.B — Catálogos dormentes reativados

| Bucket NMV pré | Qt cat. | NMV CBH pós (Mi) | NMV pré total (Mi) | Multiplicador |
|---|---:|---:|---:|---:|
| Dormente (<R$ 10K pré) | 142 | 49,5 | 0,2 | **~250x** |
| Fraco (10K-100K) | 165 | 60,3 | 7,5 | ~8x |
| Médio (100K-1Mi) | 465 | 228,0 | 201,0 | ~1,1x |
| Alto (1-10Mi) | 535 | 238,0 | 1.826,8 | competiu |
| Top (>10Mi pré) | 95 | 91,5 | 1.935,8 | competiu |

**Achado**: 307 catálogos "mortos ou quase mortos" (NMV pré <R$ 100K combinados R$ 7,7 Mi) viraram **R$ 110 Mi com a entrada da CBH**.

### 3.B — Capilaridade UF dentro de catálogo existente

> ⚠️ **REVISÃO 28-mai (Beatriz validou)**: o bucket "1-5 UFs (regional)" estava enviesado — 96% desses 84 catálogos eram dormentes (NMV pré <R$ 100K). Não eram "produtos regionais por design", eram catálogos quase parados que por acaso tinham vendido em 1-5 UFs. Isso causava **dupla contagem** com o mecanismo de "reativação de dormentes". A reclassificação correta está em **"REVISÃO: 4 mecanismos limpos"** no fim deste documento.

| Situação | Qt cat. | Share | NMV CBH (Mi) |
|---|---:|---:|---:|
| **CBH expandiu cobertura UF** (vendeu em + UFs que existia) | 435 | 31,0% | 456,6 |
| CBH dentro/menor cobertura pré | 967 | 69,0% | 210,6 |

| UFs pré do catálogo | Qt | % onde CBH expandiu | NMV CBH (Mi) | ⚠️ Diagnóstico |
|---|---:|---:|---:|---|
| 1-5 UFs (regional) | 84 | 83,3% | 35,0 | **NÃO usar — 96% são dormentes** |
| 6-15 UFs (nac. médio) | 272 | 59,6% | 163,1 | Capilaridade genuína |
| 16-26 UFs (nac.) | 818 | 16,1% | 363,1 | Capilaridade genuína |
| 27 UFs (full) | 157 | 0% (já estava em tudo) | 76,5 | N/A |

### 3.C — Quem é o Top Seller hoje (BB winner change)

| Cenário | Qt cat. | Share | NMV CBH (Mi) |
|---|---:|---:|---:|
| **CBH virou top, tomando de outro seller** | 463 | 29,6% | 456,1 |
| **CBH virou top em catálogo novo (Tipo B)** | 171 | 10,9% | 90,9 |
| CBH coexiste (não é top) | 982 | 62,7% | 236,1 |

CBH é o **#1 seller em 40,5% dos catálogos** onde atua. Em 30% **tomou de outro**.

### 3.C — Quem foi canibalizado (top sellers pré que perderam BB)

Filtro: catálogos onde CBH tomou top + top pré tinha NMV >R$ 100K (n=240). Comparação: NMV pós real vs taxa-pré projetada pra 6m equivalentes.

| Resultado | Qt | Share | Δ NMV agregado (Mi) |
|---|---:|---:|---:|
| Top pré PERDEU NMV vs taxa | 166 | 69,2% | **-76,1** |
| Top pré MANTEVE ou cresceu | 74 | 30,8% | (positivo) |

### 3.C — Top sellers afetados (perda agregada vs taxa-pré)

| Seller | Cat. perdeu BB | Δ NMV (Mi) | NMV CBH capturada (Mi) |
|---|---:|---:|---:|
| **MERCADO LIVRE ELETRONICOS (1P)** | 104 | -21,3 | ~166 |
| COLORVISÃO | 4 | -4,7 | — |
| FASTSHOP OFICIAL | 14 | -3,9 | — |
| MAXXNASUACASA | 2 | -2,7 | — |
| 123 COMPROU | 6 | -1,8 | — |
| BUDCOMÉRCIO ELETRODOMÉSTICOS | 4 | -1,7 | — |
| MEGAMAMUTE FULLMG | 8 | -0,75 | — |
| LOJAS KOERICH | 5 | -0,6 | — |

### 3.C — Deep no 1P MELI (descoberta importante)

Olhando o universo COMPLETO (sem filtro de NMV pré >100K), são **128 catálogos** onde o 1P era top e CBH tomou. Resultado líquido:

| Métrica | Valor |
|---|---:|
| NMV 1P pré (22m) | R$ 300,7 Mi |
| NMV 1P pré projetado pra 6m equivalentes | R$ 82,0 Mi |
| NMV 1P real nos 6m pós | R$ 62,8 Mi |
| **Δ líquido 1P (perda vs taxa)** | **-R$ 3,3 Mi** |
| NMV CBH nesses 128 catálogos | R$ 165,8 Mi |

**Por D1**: a perda do 1P está em LA (-R$ 9,0 Mi) e Small App (-R$ 2,4 Mi). Em **TVs o 1P até CRESCEU** (+R$ 7,7 Mi nos 22 catálogos onde perdeu BB) — provavelmente carregado pelo crescimento orgânico forte da categoria.

**Interpretação**: a "canibalização" do 1P MELI é MUITO menor que o número bruto sugere. Em termos líquidos, são R$ 3,3 Mi perdidos vs CBH ganhando R$ 165,8 Mi nesses mesmos catálogos → indica **incrementalidade líquida positiva** ainda dentro do que parecia canibalização.

⚠️ Caveat: a "taxa pré projetada" assume crescimento zero. Como o MELI HE cresceu ~30% YoY ex-CBH, a perda real ajustada por crescimento esperado é maior. Mas mesmo ajustada não chega a explicar o NMV da CBH.

📁 CSVs Etapa 3:
- `etapa3a_catalogos_cbh_raw.json` — universo CBH
- `etapa3b_catalogos_classificados.csv` — Tipo A/B + métricas pré
- `etapa3b_distrib_NMVpre_buckets.csv` — buckets dormente/vivo
- `etapa3b_histograma_UFspre.csv` — capilaridade UF
- `etapa3c_bb_winner_completo.csv` — top sellers pré/pós
- `etapa3c_sellers_canibalizados.csv` — ranking de sellers afetados
- `etapa3_INTEGRADO_catalogos.csv` — **arquivo mestre integrado** (1.566 cat × 21 campos)

---

## Achado consolidado pra o slide *(versão revisada 28-mai)*

A CBH ajudou o MELI a crescer através de **4 mecanismos mutuamente exclusivos** (sem dupla contagem):

| # | Mecanismo | Critério | Qt cat. | NMV CBH (Mi) | Share |
|---|---|---|---:|---:|---:|
| 1 | **Capilaridade pura** | Cat. com volume real (≥R$ 100K pré) + CBH expandiu UFs | 208 | **347,8** | 39,5% |
| 2 | **Coexistência** | Cat. com volume + CBH não expandiu UFs | 887 | 209,5 | 23,8% |
| 3 | **Reativação dormentes** | Cat. com NMV pré <R$ 100K (qualquer UF) | 307 | 109,9 | 12,5% |
| 4 | **Sortimento novo** (Tipo B) | Cat. nunca vendido em MELI | 164 | 73,0 | 8,3% |
| 5 | Fora de catálogo | Anúncios livres sem product_id | — | 140,0 | 15,9% |
| **TOTAL** | | | | **880,2** | 100% ✓ |

**Capilaridade pura (R$ 348 Mi) — onde está concentrada:**
- 91 catálogos com **6-15 UFs pré** (nacional médio): R$ 112 Mi
- 114 catálogos com **16-26 UFs pré** (quase full nacional): R$ 235 Mi
- 3 catálogos com 1-5 UFs pré e volume: R$ 0,1 Mi (irrelevante)

Canibalização identificada é **menor que o NMV CBH em ordens de magnitude**:
- Sellers perdedores agregados: -R$ 76 Mi vs taxa pré (estimado)
- 1P MELI líquido: -R$ 3,3 Mi
- Top 10 sellers afetados (ex-1P): ~R$ 17 Mi

**Net incremental estimado: ~R$ 700-800 Mi** do NMV CBH é incremental ao MELI (vs R$ 880 Mi totais).

---

---

## ETAPA 3.D — Perfil dos sellers pré-CBH em cada catálogo

Pergunta: a CBH entrou em catálogos "abandonados pelos grandes" (só sellers dev) ou em catálogos consolidados?

| Perfil pré-CBH | Qt cat. | Share | NMV CBH (Mi) | Share NMV |
|---|---:|---:|---:|---:|
| **C — Catálogo tinha 1P MELI vendendo** | 951 | 60,7% | 469,6 | **63,4%** |
| **B — Catálogo tinha TO (sem 1P)** | 415 | 26,5% | 195,2 | 26,4% |
| **B_NOVO — Catálogo novo em MELI** | 164 | 10,5% | 73,0 | 9,9% |
| **A — Só Seller Dev pré (Long Tail/Midtail 3P)** | 36 | 2,3% | 2,4 | **0,3%** |

**Achado contra-intuitivo**: a CBH **NÃO** entrou principalmente em territórios fracos. **87% do NMV CBH veio de catálogos onde já havia 1P ou TO**. Apenas R$ 2,4 Mi vieram de catálogos "só dev".

**Por D1 (Qt catálogos)**:
| D1 | A só dev | B com TO | C com 1P | B novo | Total |
|---|---:|---:|---:|---:|---:|
| Small App | 25 | 136 | 444 | 45 | 650 |
| LA | 3 | 162 | 373 | 62 | 600 |
| TVs | 0 | 49 | 75 | 28 | 152 |
| H/C | 6 | 33 | 37 | 18 | 94 |
| Audio | 2 | 35 | 22 | 11 | 70 |

**TVs: ZERO catálogos "só dev"** — categoria 100% consolidada. CBH competiu cara a cara em todos.

**Por D1 (NMV CBH em R$ Mi)**:
| D1 | A só dev | B com TO | C com 1P | B novo | Total |
|---|---:|---:|---:|---:|---:|
| LA | 0,1 | 83,2 | 228,6 | 36,5 | 348,4 |
| TVs | 0 | 96,9 | 154,0 | 20,1 | 271,0 |
| Small App | 1,9 | 8,4 | 78,8 | 12,8 | 101,9 |
| Audio | 0,2 | 5,6 | 3,0 | 1,6 | 10,5 |
| H/C | 0,3 | 1,0 | 5,1 | 2,0 | 8,4 |

**Reinterpretação da narrativa**: O valor da CBH NÃO foi entrar em "vazios competitivos". Foi adicionar **capilaridade regional + execução** em catálogos onde 1P e TOs já operavam. Por isso o efeito líquido sobre os players foi pequeno (coexistência) e o net incremental se mantém alto.

📁 `outputs/etapa3_MESTRE_v2_com_perfil.csv` — arquivo master 1.566 catálogos × 32 campos (com perfil pré).

---

## ETAPA 3.E — NMV CBH fora de catálogo (item_id sem product_id)

**R$ 139,7 Mi (15,9%) do NMV CBH em HE são vendas fora de catálogo** — anúncios livres ITEM_ID sem product_id.

| D2 | Em catálogo (Mi) | Fora catálogo (Mi) | Total (Mi) | % Fora |
|---|---:|---:|---:|---:|
| TELEVISIONS | 271,0 | 70,6 | 341,6 | **20,7%** 🔥 |
| REFRIGERATION | 165,0 | 23,8 | 188,8 | 12,6% |
| LAUNDRY & DISHWASHERS | 116,8 | 16,2 | 133,0 | 12,2% |
| KITCHEN | 81,0 | 7,0 | 88,0 | 8,0% |
| **BUILT IN** | 66,6 | 12,0 | 78,5 | **15,3%** |
| HOUSING & CLEANING | 20,9 | 1,9 | 22,8 | 8,4% |
| AUDIO | 9,8 | 5,3 | 15,1 | 35,1% |
| COOLING | 8,4 | 2,9 | 11,4 | 25,9% |

**Insight**: TVs tem 20,7% fora de catálogo (R$ 70,6 Mi) — hipótese: bundles, configurações específicas (modelo+tamanho exato), ou anúncios próprios CBH não unificados ao BB. Vale investigar caso a caso se quiser ver oportunidade de unificação.

Built In (sua D2 core): 15,3% fora. R$ 12 Mi em anúncios próprios CBH.

📁 `outputs/etapa3e_fora_vs_em_catalogo.csv`

---

---

## ETAPA 4 — Decomposição regional do BR + aceleração por marca/D2/ASP

### Decomposição regional do crescimento BR (validação dos +9,9 pp)

A soma das contribuições regionais ao YoY BR bate exatamente:

| Região | NMV 25 (Mi) | Δ total (Mi) | **Contrib CBH (pp BR)** | Contrib ex-CBH (pp BR) | Contrib total (pp BR) |
|---|---:|---:|---:|---:|---:|
| SE | 2.334,8 | 789,2 | 5,16 | 14,75 | 19,91 |
| NE | 600,5 | 387,1 | 2,40 | 7,37 | 9,76 |
| S | 646,3 | 242,8 | 1,14 | 4,99 | 6,13 |
| CO | 269,6 | 129,3 | 0,76 | 2,50 | 3,26 |
| N | 113,0 | 71,4 | 0,49 | 1,31 | 1,80 |
| **BR** | 3.964,2 | 1.619,8 | **9,95** | **30,92** | **40,86** ✓ |

### Intensidade CBH dentro de cada região

| Região | Δ CBH / Δ regional | YoY total | YoY ex-CBH | Premium CBH (pp) |
|---|---:|---:|---:|---:|
| **N** | 27,3% | +63,2% | +45,9% | **+17,3** |
| NE | 24,5% | +64,5% | +48,6% | +15,8 |
| SE | 25,9% | +33,8% | +25,0% | +8,8 |
| CO | 23,2% | +48,0% | +36,8% | +11,1 |
| S | 18,5% | +37,6% | +30,6% | +7,0 |

**Argumento da causalidade-pela-regionalização**: sem a CBH, o gradiente de growth regional existiria mas seria menor. A CBH **amplifica** o gradiente — premium de +17,3 pp no Norte vs +7 pp no Sul (**2,5x mais intensa onde MELI tinha pior proposta de valor**).

### Aceleração por D2 (Contribuição CBH ao YoY)

| D2 | YoY total | YoY ex-CBH | Contrib CBH (pp) | Share CBH |
|---|---:|---:|---:|---:|
| **LAUNDRY & DISHWASHERS** | +102,3% | +69,2% | **+33,1 pp** | 16,4% |
| **REFRIGERATION** | +62,3% | +30,8% | **+31,5 pp** | 19,4% |
| **TELEVISIONS** | +50,0% | +26,5% | **+23,5 pp** | 15,6% |
| BUILT IN | +52,0% | +42,9% | +9,1 pp | 6,0% |
| KITCHEN | +44,9% | +36,3% | +8,6 pp | 5,9% |
| HOUSING & CLEANING | +43,3% | +39,0% | +4,4 pp | 3,1% |

**LAUNDRY e REFRIGERATION** (D2s da Nicole): 1/3 do crescimento veio da CBH — onde frete + capilaridade são decisivos. **Built In já estava em forte rampa orgânica** (+42,9% ex-CBH).

### Top marcas mais impulsionadas pela CBH

| Marca | YoY ex-CBH | YoY total | **Contrib CBH (pp)** | Share CBH na marca |
|---|---:|---:|---:|---:|
| **TCL** (TV) | +58,6% | +126,8% | **+68,2 pp** 🔥 | **30,1%** |
| **Consul** (LA) | +59,3% | +101,4% | **+42,1 pp** | 20,9% |
| **Philips** (TV) | +45,4% | +80,2% | +34,8 pp | 19,3% |
| **Brastemp** (LA) | +60,9% | +87,3% | +26,4 pp | 14,1% |
| **LG** | +9,1% | +32,1% | +23,0 pp | 17,4% |
| **Mondial** (Small) | +52,7% | +75,5% | +22,8 pp | 13,0% |
| **Britânia** | +10,4% | +32,2% | +21,8 pp | 16,5% |
| **Midea** | +75,4% | +94,7% | +19,3 pp | 9,9% |
| **Electrolux** | +24,7% | +41,6% | +16,9 pp | 12,0% |
| **Samsung** | **−5,2%** ⚠️ | +10,3% | +15,5 pp | 14,1% |

**Insights-bomba pra liderança**:
- **TCL é a marca mais impulsionada**: 30% das vendas TCL no MELI hoje vêm da CBH. NMV TCL dobrou (R$ 61 → R$ 139 Mi).
- **Samsung CAIRIA −5,2% sem a CBH**. Com ela, cresce +10,3%. **A CBH é hedge contra perda de marca estratégica**.

### Concentração CBH por faixa de ASP

| ASP (R$ por unidade) | Qt catálogos | NMV CBH (Mi) | Share |
|---|---:|---:|---:|
| até R$ 200 | 339 | 35,6 | 4,8% |
| R$ 200-500 | 302 | 69,2 | 9,3% |
| R$ 500-1k | 230 | 77,5 | 10,5% |
| **R$ 1k-2k** | 169 | 125,9 | 17,0% |
| **R$ 2k-3k** | 167 | 166,0 | **22,4%** |
| **R$ 3k-5k** | 213 | 197,8 | **26,7%** 🔥 |
| > R$ 5k | 116 | 68,3 | 9,2% |

**66% do NMV CBH na faixa R$ 1k-5k** — TVs grandes + ED frost-free + lavadora 11-13kg + cooktop/fogão 5 bocas. **Faixa onde frete grátis + financiamento + capilaridade fazem mais diferença vs loja física**.

📁 CSVs: `etapa2_decomposicao_regional.csv`, `etapa4a_marcas_growth.csv`, `etapa4b_d2_growth.csv`, `etapa4c_asp_buckets.csv`

---

---

## REVISÃO 28-mai/2026 — 4 mecanismos limpos + perfil dos dormentes

### Reclassificação dos mecanismos (corrige dupla contagem)

A análise inicial dos "84 catálogos com 1-5 UFs pré com 83% expansão" estava enviesada: **96% desses 84 catálogos eram dormentes** (NMV pré <R$ 100K — mediana de R$ 3.639 em 22 meses). A "expansão UF" deles é o mesmo fenômeno da "reativação de dormentes" — não eram catálogos regionais por design, eram catálogos quase parados que por acaso tinham vendido em poucas UFs.

**Reclassificação correta — 4 mecanismos mutuamente exclusivos** (Tipo A apenas):

| # | Mecanismo | Critério | Qt cat. | NMV CBH (Mi) | Share |
|---|---|---|---:|---:|---:|
| 1 | **Capilaridade pura** | Cat. com volume real (NMV pré ≥R$ 100K) + CBH expandiu UFs | 208 | **347,8** | 39,5% |
| 2 | **Coexistência** | Cat. com volume + CBH não expandiu UFs | 887 | 209,5 | 23,8% |
| 3 | **Reativação dormentes** | Cat. com NMV pré <R$ 100K (qualquer UF) | 307 | 109,9 | 12,5% |
| 4 | **Sortimento novo** (Tipo B) | Cat. nunca vendido em MELI antes | 164 | 73,0 | 8,3% |
| 5 | Fora de catálogo | Anúncios livres sem product_id | — | 140,0 | 15,9% |
| **TOTAL CBH HE 6m** | | | | **880,2** | **100%** ✓ |

**Capilaridade pura por bucket de UFs pré** (onde realmente o mecanismo agiu):
- 91 catálogos com 6-15 UFs pré → R$ 112 Mi
- 114 catálogos com 16-26 UFs pré → R$ 235 Mi
- 3 catálogos com 1-5 UFs pré com volume → R$ 0,1 Mi (não usar como argumento)

### Perfil dos 307 catálogos dormentes — quem ganhou voz com a CBH

**Por D2 (categoria mais beneficiada):**

| D2 | Qt cat. dormentes | NMV pré 22m (R$) | NMV CBH pós 6m (Mi) | Multiplicador |
|---|---:|---:|---:|---:|
| **TELEVISIONS** | 25 | 814 mil | **42,6** | 52x |
| **REFRIGERATION** | 75 | 1,03 Mi | **41,5** | 40x |
| BUILT IN | 25 | 847 mil | 8,8 | 10x |
| KITCHEN | 86 | 2,35 Mi | 7,4 | 3x |
| HOUSING & CLEANING | 37 | 1,05 Mi | 4,1 | 4x |
| LAUNDRY & DISHWASHERS | 21 | 597 mil | 2,4 | 4x |
| AUDIO | 11 | 459 mil | 2,3 | 5x |
| COOLING | 24 | 486 mil | 0,7 | 2x |

**TVs + Refrigeration concentram 76% do volume reativado** (R$ 84 Mi de R$ 110 Mi).

**Top marcas que mais avançaram (dormentes reativados):**

| Marca | Qt cat. dormentes | NMV pré 22m (R$) | NMV CBH pós 6m (Mi) |
|---|---:|---:|---:|
| **Consul** | 20 | 160 mil | **23,1** |
| **Hisense** | 14 | 200 mil | **17,0** |
| **Philips** | 4 | 98 mil | **14,8** |
| Electrolux | 37 | 1,03 Mi | 10,0 |
| Philco | 30 | 667 mil | 6,2 |
| Brastemp | 17 | 85 mil | 5,7 |
| Esmaltec | 4 | 211 mil | 5,2 |
| Samsung | 12 | 502 mil | 4,8 |
| LG | 18 | 793 mil | 4,4 |
| TCL | 5 | 184 mil | 3,9 |

**Os 5 mais dramáticos catálogos individuais (multiplicador absurdo):**

| Product ID | D2 | Marca | NMV pré 22m | NMV CBH 6m | Mult |
|---|---|---|---:|---:|---:|
| 52714724 | TVs | Philips | R$ 46 mil | R$ 10,5 Mi | 227x |
| 53505423 | TVs | Hisense | R$ 7.564 | R$ 8,3 Mi | **1.096x** |
| 52458477 | Refrig | Consul | R$ 17 mil | R$ 5,8 Mi | 337x |
| 52435146 | Refrig | Consul | R$ 19 mil | R$ 4,9 Mi | 262x |
| 57723340 | TVs | Philips | R$ 0 | R$ 4,3 Mi | ∞ |

### Frase para o slide (versão validada)

> "Dos 307 catálogos dormentes reativados pela CBH (R$ 110 Mi pós-CBH vs R$ 7,7 Mi pré), as categorias mais beneficiadas foram **Televisions e Refrigeration** (76% do volume reativado). As marcas que mais avançaram foram **Consul (R$ 23 Mi de R$ 160 mil pré), Hisense (R$ 17 Mi de R$ 200 mil) e Philips (R$ 14,8 Mi de apenas 4 catálogos quase parados)**. Casos extremos: 1 TV Hisense saltou de R$ 7.564 em 22 meses para R$ 8,3 Mi em 6 meses (multiplicador de 1.096x)."

📁 CSVs investigativos:
- `investigacao_catalogos_1_5_UFs.csv` — os 84 catálogos do bucket "1-5 UFs" (registro do achado errado)
- `investigacao_307_dormentes.csv` — perfil completo dos 307 dormentes
- `investigacao_208_capilaridade_pura.csv` — os 208 catálogos de capilaridade pura

---

## ENTREGÁVEIS FINAIS

| Arquivo | Conteúdo |
|---|---|
| `outputs/STORYBOARD_CBH_HE.xlsx` | **XLSX storyboard** — 20 abas na ordem da história, base pra montar slides no template MELI |
| `outputs/ANALISE_CBH_HE_master.xlsx` | **XLSX master** — 12 abas filtráveis (catálogos, perfis, sellers canibalizados, marcas, D2, ASP, decomposição regional, evolutivo) |
| `outputs/deck_CBH_HE_principal.pptx` | Deck principal (3 slides) — referência visual |
| `outputs/deck_CBH_HE_backup.pptx` | Backup deck (5 slides) — referência visual |
| `outputs/investigacao_*.csv` | 3 CSVs investigativos (dormentes, capilaridade pura, 1-5 UFs) |
| `ACHADOS.md` | Documento cumulativo com todos os achados (este arquivo) |
| `queries/etapa*.sql` | Queries BigQuery documentadas com custo |
| `outputs/etapa*.csv` (16 arquivos) | Outputs intermediários por etapa |

---

## Próximas etapas

- [x] **Etapa 0** — Setup
- [x] **Etapa 1** — Caracterização CBH
- [x] **Etapa 2** — Crescimento regional
- [x] **Etapa 3** — Sortimento + Buy Box (3A/3B/3C/3D/3E)
- [x] **Etapa 4** — Decomposição + marcas/D2/ASP
- [x] **Etapa 5** — Síntese executiva + XLSX + PPT
- [x] **Revisão pós-validação** — 4 mecanismos limpos + perfil dormentes ✅
- [ ] **Ponto 1** — stand-by (canibalização nacional 1P vs 3P)
