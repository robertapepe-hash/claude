# Premissas — Business Case: frear o avanço da Shopee em Home por faixa de ASP

**Projeto:** conter o ganho de faturamento/share da Shopee em Home Electronics nas **faixas de ASP nova**, via business case de aproximação de sellers MELI.
**Owner:** Beatriz Dacache · **Criado:** 2026-08-18 · **Status:** v5 (checks de integridade rodados · método do forecast travado)
**Casa:** `Shield Against Asians\Plano de Combate BC` · **Grid Shield por ASP (ref):** https://grid.adminml.com/d/01KXKJP50WAQ314W1MVQXD4SRZ/view
**Sheets de análise (origem da query):** https://docs.google.com/spreadsheets/d/1jpaRCTpgV3YUMBPcujU-UOT0slmSqf3LCt0HOQf3_do — aba `RATIO SHP - NEW ASP` = ratio `MS_Shopee/MS_MELI`, base valor (NMV), 6 faixas macro.
**Artefato série mensal:** https://docs.google.com/spreadsheets/d/1ST20McYZ2kflp1_J_t85iuacgfK3OrRync4LR-IjDR4
**Dashboard Grid — doc único com 3 abas (v2, 20/08):** https://grid.adminml.com/d/01M0DSBDBHEAV3650Q913YSP6Y/view (doc `01M0DSBDBHEAV3650Q913YSP6Y`) — ⚠️ **visibilidade `public` (todo o MELI)**, alterada em 20/08 16:43. Abas: **1 Diagnóstico** (evolutivo por faixa) · **2 Realizado × Projetado** · **3 Simulador do desafio**. Arquitetura: shell HTML com **iframes `srcdoc` em base64** — isola CSS/JS de cada painel (evita colisão de nomes) e carrega sob demanda. Fonte: `grid_plano_combate_abas.html`, montado de `dashboard_evolutivo_shopee.html` + `dashboard_realizado_projetado.html` + `simulador_desafio.html`. Para atualizar: regerar os painéis, rodar o build do shell e subir com `file_new_version:true` + `if_version`.
**Base primária:** `meli-bi-data.SBOX_MKPBR.DM_MARKET_ASP_MONTHLY_VERTICAL_D1` (mensal · física jan/23→jun/26 · lag ~2 meses)

---

## 0. Para que serve (vale mesmo se o BC não passar)
Mesmo sem verba extra aprovada, o estudo entrega o **norte de quanto a mais precisamos fazer em cada faixa/D1** — e esse delta é acompanhável mês a mês pelo **DM Eficiência** (validado apple-to-apple, §5). O BC é um caminho para financiar o delta; o delta existe de todo jeito.

---

## 1. Objetivo e horizonte
- **Frente Shopee:** medir faturamento por faixa → projetar **set–dez/26**.
- **Frente MELI:** medir ritmo (MoM/YoY) → derivar **quanto precisamos crescer** para conter o ratio.
- **Horizonte:** **2026 YTG apenas** (set–dez/26). 2027 fora de escopo por ora.
- **KPI de compromisso:** **ratio Shopee/MELI** (headline). **Share** (sobre mercado) aparece sempre como guarda.
- **Nível do compromisso:** **por D1**, com **alocação por faixa**. Modelar nas 11 faixas e **aglutinar depois** (nunca repartir).

---

## 2. Escopo — [FECHADO]
- `VERTICAL='HOME ELECTRONICS'`; D1s: `LARGE APPLIANCES`, `SMALL APPLIANCES`, `HEATING, COOLING & AIR QUALITY`.
- Régua: `FAIXA_ASP_NOVA` (11 faixas) · de-para p/ as 6 macro do Sheets.
- **Janela de dados: set/24 → jun/26** (22 meses; 2 passagens por Set-Dez). Análise 2025+; 2024 entra como base de YoY.
### 2.1 Faixas-foco — [FECHADO com critério objetivo, 19/08]
**Critério:** entra em FOCO se **SOB MELI ≥ 5%** (material para nós) **E** (**ratio ≥ 15%** OU **Δratio ≥ +4 pp**). Base: LTM jul/25–jun/26 vs jul/24–jun/25 (ciclo completo, sem viés sazonal). Faixas com ratio altíssimo mas SOB < 5% vão para **VIGIAR** (cabeça-de-ponte dela, defesa barata).

| D1 | faixa | SOB MELI | ratio | Δpp | Δ Shopee (Mi) | status |
|---|---|---|---|---|---|---|
| LARGE | 200 a 500 | 9,1% | **75,4%** | +51,5 | +331 | 🔴 FOCO |
| LARGE | 500 a 1500 | 29,0% | 31,2% | +21,0 | +408 | 🔴 FOCO |
| LARGE | 1500 a 3000 | 36,3% | 15,5% | +8,7 | +255 | 🔴 FOCO |
| LARGE | **+3000** | 24,3% | 8,6% | +5,7 | +102 | 🔴 FOCO *(promovida 20/08 por decisão da Beatriz — ratio **triplicou** de 2,9% p/ 8,6%, +102 Mi, e a faixa é 24,3% do nosso negócio em Large: eles avançam no premium)* |
| H&C | 200 a 500 | 19,4% | 15,9% | +4,7 | +38 | 🟡 FOCO |
| H&C | 500 a 1500 | 11,9% | **95,3%** | +89,9 | +345 | 🔴 FOCO ⚠️ (ver §8.2) |
| H&C | 1500 a 3000 | **42,3%** | 35,4% | +28,1 | **+417** | 🔴 FOCO |
| H&C | +3000 | 15,6% | 10,0% | +6,2 | +33 | 🟡 FOCO |
| SMALL | 120 a 150 | 6,1% | 41,6% | -3,8 | +26 | 🟡 FOCO |
| SMALL | 150 a 200 | 10,0% | 47,8% | +3,4 | +77 | 🔴 FOCO |
| SMALL | 200 a 500 | **32,8%** | 21,7% | +5,6 | +148 | 🔴 FOCO |
| SMALL | 500 a 1500 | 22,2% | 19,5% | +9,0 | +115 | 🔴 FOCO |
| SMALL | +3000 | 6,8% | 19,0% | +14,6 | +52 | 🟡 FOCO |
| SMALL | 19 a 49 / 49 a 79 | 1,8% / 3,6% | **236% / 128%** | melhorando | +72 / +52 | 👁️ VIGIAR |
| SMALL | 1500 a 3000 | 9,2% | 9,8% | **-10,0** | -20 | ⚪ FORA (ratio caindo) |

**Cobertura do perímetro (% do GMV MELI da D1):** LARGE 98,7% · H&C 89,2% · SMALL 77,9%.

**Confronto com a hipótese inicial:** H&C "acima de 200" ✅ confirmado · Small "quase todas" ✅ confirmado (ratio alto em toda a régua) · **Large "acima de 500" ❌ sub-escopa**: a faixa **200 a 500 tem o pior ratio de Large (75,4%, +51,5 pp)** e precisa entrar.
**Achados de leitura:** H&C 1500-3000 é a ameaça nº 1 em amount (+417 Mi, e concentra 42,3% do nosso negócio na D1) · em Small 19-79 a Shopee é **maior que o MELI**, mas o ratio está **melhorando** (reagimos) · Small 1500-3000 é a única faixa onde ganhamos terreno.

---

## 3. Métricas — [FECHADO]
- **GMV bruto** (como Planning reporta): MELI `TGMV_MELI` · Shopee `GMV_SHOPEE` · Mercado `GMV_MERCADO`.
- **SI** dos 3 players → **ASP = GMV/SI** (separa preço de volume).
- **Ratio** = `GMV_SHOPEE / TGMV_MELI` · **Share** = `GMV_x / GMV_MERCADO`.
- **Toda base é guardada em AMOUNT (R$)**; percentuais (share/ratio/MoM/YoY) são **recalculados a partir dos amounts** — é o que permite agregar qualquer combinação de faixas/D1s sem erro.

---

## 4. Decomposição 1P/3P, segmento e seller — [método]
- DM_MARKET_ASP **não tem** 1P/3P/segmento/seller (`TGMV_MELI` = MELI total).
- **1P/3P/seller → DM Eficiência / cubos do Shield** (`dem2_*`, `afford_*`, `seller_cube`, `seller_cap_cube`, `grupos_economicos`).
- **1P como parte da solução:** depois de fechado o incremental, avaliar o **potencial do 1P** antes/junto da divisão BAU vs BC — é fatia importante da resposta.

---

## 5. Validação GMV (Planning) × NMV (DM Eficiência) — [RESOLVIDA ✅ 18/08]
- Gap **~0,1%** (H1'26, 3 D1s) → **apple-to-apple**, sem fator de conversão. `TGMV_MELI` já é **líquido** (bate com NMV, não com bruto).
- **Metodologia DM:** `SUM(GMV_LC) WHERE NMV_FLG AND GMV_FLG`, data `ORD_CLOSED_DT` (partição obrigatória), sem `SIT_SITE`, sem filtro de segmento.
- Consequência: **acompanhamento mensal do BC roda no DM**, com quebra por seller, sem sair de bases correlatas.

---

## 6. Motor do forecast — [TRAVADO]

### 6.1 Motor v1 — YoY decaído sobre o mês do ano anterior [SUPERADO em 20/08, ver §6.1b]
$$\text{Shopee}_{\text{set/26}} = \text{Shopee}_{\text{set/25}}^{(\text{real})} \times (1 + \text{YoY}_{\text{set}}), \quad \text{YoY}_{m} = \text{YoY}_{\text{base}} \times \varphi^{\,k}$$
Ideia: o mês do ano anterior já contém a sazonalidade real, então bastaria modelar o decaimento φ do YoY.
**Por que foi superado:** o backtest (§10.5) mostrou que φ definido como razão de dois YoY (`YoY_S2/YoY_S1`) é uma **grandeza de 2ª ordem** — razão de razões — e amplifica variância. Instável entre períodos (11 de 13 células invertem de direção) e **piora** a previsão. Mantido no doc apenas como registro do caminho percorrido.

### 6.1b Motor v2 — decomposição multiplicativa (nível × tendência × sazonalidade) [ATUAL]
*Proposto pela Beatriz em 20/08 e formalizado: em vez de estimar o decaimento de uma taxa de crescimento, separar os componentes e estimar cada um a partir de **grandezas de 1ª ordem** (níveis), que têm variância muito menor.*

Para cada **D1** (não por faixa — ver §6.5):
1. **Índice sazonal** $S_m$ — perfil MoM observado, por mês-calendário: $S_m = \text{GMV}_m / \text{MM12}_{\text{centrada}}$, média entre os anos disponíveis, normalizado para $\frac{1}{12}\sum_m S_m = 1$. *(Shopee: 2024-2025. MELI/mercado: pode usar 2023-2025, 3 observações.)*
2. **Série dessazonalizada** $D_t = \text{GMV}_t / S_{m(t)}$.
3. **Tendência recente** $g$ = crescimento mensal médio da série **dessazonalizada** nos últimos N meses (slope de $\log D_t$, N≈6) — robusto porque não mistura sazonalidade.
4. **Amortecimento** $\varphi$ aplicado a $g$ (valor único por D1, ou definido por cenário).
5. **Projeção:** $F_{t+k} = D_{t} \times \prod_{j=1}^{k}\left(1 + g\,\varphi^{\,j}\right) \times S_{m(t+k)}$

**O que isso resolve (exemplo da Beatriz):** se ela vem crescendo MoM nos últimos meses **mas** no ano passado ficou flat de setembro em diante, o $g$ captura o crescimento subjacente e o $S_m$ captura o achatamento de Q4 — os dois se multiplicam, sem precisar chutar atenuação.
**Ligação com os dials:** $S_m$ da Shopee = **Dial B** (perfil próprio dela vs. perfil do mercado, §8.5) · $\varphi$ sobre $g$ = **Dial A**.
**Pendente:** backtest do Motor v2 no mesmo protocolo (fit 2025 → jan-jun/26), comparando com o benchmark de **~26%** já estabelecido (§10.6).

### 6.3 Validação cruzada obrigatória
O perfil **MoM Set→Dez** de 2024 e 2025 tem que confirmar a curva implícita do motor. Dois caminhos independentes convergindo = premissa sólida. Divergência ⇒ modelo errado, corrigir antes de apresentar.

### 6.4 Backtest
Ajustar até dez/25, projetar jan–jun/26 contra o real, medir **MAPE**. O erro histórico do método vai declarado no material.

### 6.5 Granularidade — forecast hierárquico (obrigatório)
Modelar no nível **D1** (robusto) + **mix de faixas**, e reconciliar para somar. Justificativa empírica em §8.1: ~25% das células (D1×sub-faixa) oscilam >±50% ao mês — projetar célula solta produz lixo.

---

## 7. Cenários e joystick — [desenho]
Dois eixos (a incerteza dela e a nossa ambição são coisas diferentes):
- **Eixo X — trajetória Shopee (φ):** desacelera rápido · mantém ritmo · acelera.
- **Eixo Y — resposta MELI:** (1) **inércia/baseline** (sem ação) · (2) **conter o ratio** (crescer proporcional a ela) · (3) **reduzir o ratio** para X pp.
Saída por D1 × faixa: **GMV incremental necessário (R$)**, ratio e share resultantes, e **selo de viabilidade** (compara com o maior crescimento já entregue naquela faixa — cenário acima do recorde nasce marcado inviável).

**Decomposição do incremental (obrigatória):**
`Incremental total = BAU (fomento/investimento nas faixas) + BC (verba extra)` — decompor para **cada faixa crítica e cada D1**. Avaliar antes o **potencial do 1P**.

---

## 8. Checks de integridade — [RODADOS 19/08] ⚠️ resultados que mudam o método

### 8.1 Quebra estrutural na fonte — SEM evidência de artefato global ✅ (mas ruído alto)
- Série agregada da Shopee cresce de forma contínua (44,9 Mi jan/24 → 473,4 Mi jun/26). **Nenhum mês concentra salto sistêmico** → não há indício de mudança de metodologia/cobertura da fonte.
- **Porém:** de 129 células (D1 × sub-faixa), **11 a 51 por mês (~25%) variam >+50% MoM**, todos os meses. Volatilidade estrutural de célula.
- **Consequência:** confirma §6.5 (hierárquico) e reforça a premissa "**tendência > valor absoluto**".

### 8.2 O +1.679% de H&C 500–1500 — NÃO usar como taxa de crescimento ❌
Série mensal (GMV Mi / SI mil / ASP R$):
| mês | GMV | SI | ASP |
|---|---|---|---|
| set/25 | 5,0 | 5,6 | 903 |
| **out/25** | **68,1** | **59,3** | **1.147** |
| nov/25 | 31,9 | 27,4 | 1.164 |
| mar/26 | 65,5 | 55,2 | 1.187 |
| abr/26 | 32,7 | 25,7 | 1.274 |
| **mai/26** | **6,0** | **6,7** | **894** |
| jun/26 | 16,6 | 14,4 | 1.152 |
- É um **degrau em out/25** (13x em um mês) seguido de oscilação extrema e **colapso em mai/26 (-82% MoM)**. O ASP sobe de ~900 para ~1.150-1.270 e volta a 894 no colapso → forte indício de **itens cruzando a fronteira da faixa** (migração), não de crescimento orgânico.
- **Premissa:** essa célula é **inutilizável** como taxa de crescimento. Tratar H&C acima de 200 de forma **agregada**, não por sub-faixa.

### 8.3 Migração de faixa / preço vs volume — maioria limpa ✅, 3 faixas com drift
ASP intra-faixa H1'25 → H1'26 e SI YoY vs GMV YoY (Shopee):
| faixa | ASP SHP 25→26 | SI YoY | GMV YoY | leitura |
|---|---|---|---|---|
| 79 a 100 | 92 → 92 | +181% | +181% | volume puro ✅ |
| 120 a 150 | 136 → 137 | +36% | +37% | volume puro ✅ |
| 150 a 200 | 173 → 175 | +48% | +50% | volume puro ✅ |
| 200 a 500 | 310 → 321 | +141% | +149% | drift leve |
| **500 a 1500** | **718 → 857 (+19%)** | +281% | **+354%** | mix subindo dentro da faixa ⚠️ |
| **1500 a 3000** | **2.243 → 1.945 (-13%)** | **+338%** | +280% | entrando por baixo ⚠️ |
| **+3000** | 4.057 → 3.800 (-6%) | +345% | +317% | entrando por baixo ⚠️ |
- **O ASP do MELI é estável em TODAS as faixas** (ex.: 500-1500: 753→765). O drift é **exclusivo da Shopee** (dado estimado).
- **Leitura:** na maioria das faixas o crescimento dela é **volume real**. Nas 3 altas há componente de preço/mix — usar **SI junto do GMV** ao ler essas faixas.
- Fragilidade de cesta não-fixa: conhecida e aceita pelo time/liderança; fica como **nota de premissa**, não como bloqueio.

### 8.4 Decaimento do YoY — a tese de atenuação vale só para LARGE ⚠️ (achado crítico)
YoY médio da Shopee por semestre:
| D1 | H1'25 | H2'25 | H1'26 | leitura |
|---|---|---|---|---|
| **LARGE** | 455% | 348% | 291% | **desacelerando** → φ<1 justificado (≈0,8 por semestre) |
| **H&C** | 302% | 305% | 289% | **estável** → φ≈1 |
| **SMALL** | 75% | 43% | **77%** | **RE-ACELERANDO** (mai/26 +149%, jun/26 +122%) → φ>1 |
- **Consequência:** **não existe um φ único.** φ estimado **por D1**. Assumir atenuação geral **subdimensionaria a ameaça em Small** — o erro mais perigoso possível para o BC.
- Contexto do mercado (YoY médio H1'26): Large mercado +22% / MELI +61% · Small mercado +27% / MELI +40% · **H&C mercado +2% / MELI +30%** → em H&C o ganho da Shopee é **pura transferência de share** num mercado parado.

### 8.5 Sazonalidade de Q4 da Shopee — perfil próprio, achatado (TESTADO em 14 D1s)
**Contexto do debate (19/08):** a observação inicial era que a BF é evento MELI (out→nov: MELI +45,9%/+66,3% vs Shopee +10,4%/+11,2%). **Beatriz contestou corretamente:** usar padrão histórico como preditivo ignora mudança de regime — em 2024/25 a Shopee não tinha a consolidação nem as parcerias com lojas que tem hoje, e ela é forte em BF em outras categorias. Subdimensionar a BF dela seria o erro mais caro do BC.

**Teste feito:** se consolidação explica amplitude de BF, então nas categorias onde a Shopee JÁ é consolidada o pico de novembro deveria ser grande. Medido o MoM out→nov da Shopee nas 14 D1s de HE+Tech, ordenado por ratio LTM:

**Como ler:** as colunas de nov são **MoM — novembro contra outubro DO MESMO ANO** (nov24/out24 e nov25/out25), não YoY. É o *degrau sazonal* da BF isolado do crescimento de tendência. "ratio LTM" = nível de consolidação da Shopee na D1 (GMV_SHP/TGMV_MELI, jul/25–jun/26).

| D1 | ratio LTM | SHP nov24/out24 | SHP nov25/out25 | MELI nov25/out25 |
|---|---|---|---|---|
| WEARABLES | 44% | +32% | +20% | +19% |
| H&C | 37% | **-33%** | **-9%** | +68% |
| SMALL APPL | 35% | +24% | +15% | +45% |
| HOUSEHOLD PARTS | 35% | +10% | +19% | +1% |
| CAMERAS & DRONES | 34% | +38% | +26% | +8% |
| LARGE APPL | 24% | +29% | +30% | +82% |
| CONSOLE GAMING | 24% | +18% | +16% | +104% |
| IT PERIPHERALS | 21% | +5% | +23% | +19% |
| TVs | 15% | +53% | +21% | +116% |
| SMARTPHONES | 14% | +23% | +21% | +46% |
| COMPUTERS | 7% | +36% | +16% | +53% |

**Resultado: NÃO existe relação entre consolidação e amplitude de BF.** A Shopee fica numa faixa estreita de **+15% a +30%** em novembro, independente de ter 7% ou 44% de ratio. Mesmo em Wearables (sua categoria mais consolidada) o nov é só +20%.

**Explicação estrutural:** o calendário comercial dela **não é BF-cêntrico** — é 9.9 / 10.10 / **11.11** / 12.12, distribuído mês a mês. O out dela já é alto (10.10), então o nov não dá salto. O MELI e os incumbentes de HE concentram tudo na semana de BF (mecânica de crediário e big ticket, que não é a dela). Em dezembro a Shopee cai menos que o MELI (SHP -11 a -35% vs MELI -22 a -50%) → **o Q4 dela é mais achatado e espalhado, não mais fraco**.

**Nota H&C:** nov é **negativo** para a Shopee nos dois anos (-33%, -9%) e dez é **+20%** — categoria de verão (ventilador/ar portátil), pico deslocado para dez-fev. O motor (§6.1) captura isso automaticamente ao usar o mês real do ano anterior.

**Premissas resultantes:**
1. **Caso-base:** perfil sazonal **próprio da Shopee** (uplift de nov ~+20%), não o do mercado. Crescimento dela em Q4 vem do **YoY de tendência**, não de um pico de BF.
2. **A BF da Shopee vira DIAL de cenário, não premissa.** Cenário agressivo = imputar a sazonalidade do **mercado** nela (~+50-60% em nov, ~3x o histórico dela) = "ela finalmente destrava a BF em HE". O BC **dimensiona o custo desse cenário** — protege sem inflar o caso-base.
3. Compromisso de ratio sempre **contra o mesmo mês do ano anterior** (higiene de medição, independente de cenário).
4. **Não aplicar a sazonalidade do mercado à Shopee no caso-base** — mas manter como teto de risco.

---

## 9. Higiene e premissas declaradas
- **Base da Shopee é estimada** (painel), não transacional. Premissa central: **apoiar-se em TENDÊNCIA e no ratio, não em valores absolutos**. Fluxo: crescimento nosso + crescimento dela → efeito no ratio → só então converter em amount.
- **Só meses fechados**; base vai até jun/26. **jul e ago/26 desconhecidos:** o lado MELI pode ser ancorado no DM Eficiência (mais fresco); o lado Shopee/mercado **não tem fonte** → assimetria declarada.
- **TikTok e demais players:** entram no denominador do cenário (se vencermos a Shopee e ela vencer os outros, ainda perdemos). Foco da decisão segue MELI vs SPE via ratio.
- Base zero → marcar "novo", não calcular %. Tipos mistos (`BIGNUMERIC`×`FLOAT`) → cast nas divisões.
- Refresh: query parametrizada por data + script gerador do HTML → regerar é reexecutar. VerdiFlow quando o layout estabilizar.

---

## 10. Pontos que entram depois (acordados, fora do escopo imediato)
- **Eficiência do investimento** (R$ investido por R$ de GMV incremental, via `DXI_*`/`DXB_*`/`CPN_*` do DM): trabalho do time de **farming**, que estará na mesa. Vira input, não output nosso.
- **Capacidade de oferta:** validar se os sellers supostos bastam — quanto vêm fazendo/mês na faixa, qual crescimento seria exigido; se muito acima do histórico, o BC precisa de **mais sellers**. Fonte: `seller_cap_cube` / `seller_names` / `grupos_economicos` do Shield. **Beatriz quer fazer essa validação.**
- **Consolidação no Grid do Shield por ASP:** avaliar subir as abas do BC no doc `01KXKJP50WAQ314W1MVQXD4SRZ` (opções: docs separados com link, HTML mestre com iframes, ou mesma pasta/workspace).

---

## 11. Log de decisões
- **18/08 (fundação)** — Escopo, GMV bruto, SI+ASP, share/ratio, `_LM`/`_LY`, higiene, 1P/3P via DM Eficiência. Doc em Shield\Plano de Combate BC.
- **18/08 (perfil + validação)** — Rótulos D1, 11 faixas, lag 2 meses. **GMV×NMV = 0,1% (apple-to-apple)**. Aba 1 do dashboard publicada no Grid.
- **19/08 (decisões)** — Horizonte **2026 YTG**; **ratio SPE = compromisso**, share como guarda; **compromisso por D1 com alocação por faixa**; janela desde **set/24**; modelar detalhado e aglutinar depois.
- **19/08 (checks)** — Sem quebra global na fonte ✅ · **+1.679% de H&C 500-1500 é degrau+migração, inutilizável** ❌ · ASP estável na maioria (volume real), drift em 500-1500 / 1500-3000 / +3000 só na Shopee · **φ por D1: Large desacelera, H&C estável, Small re-acelera**.
- **19/08 (debate BF)** — Beatriz contestou o uso preditivo do padrão histórico de BF da Shopee (mudança de regime: consolidação e parcerias novas). **Testado em 14 D1s: não há relação entre consolidação e amplitude de BF** — ela fica em +15/+30% em nov independente do ratio; calendário dela é 9.9/10.10/11.11/12.12, não BF-cêntrico; Q4 dela é achatado e espalhado, não fraco. **Resolução: caso-base = perfil próprio dela (~+20% nov); sazonalidade do mercado imputada nela vira CENÁRIO AGRESSIVO (dial), para dimensionar o custo do risco sem inflar o caso-base.**
- **19/08 (faixas-foco)** — Perímetro fechado com critério objetivo (§2.1). Hipótese de Large "acima de 500" corrigida: **200 a 500 entra** (pior ratio da D1: 75,4%). φ preliminar por D1 estimado.

---

## 10.5 BACKTEST — resultado e o que ele obriga a mudar [20/08] ⚠️ crítico

**Desenho:** fit **só com 2025**, prevê **jan–jun/26**, compara com o real. 3 variantes de base (YoY do Q4'25 / S2'25 / ano 2025) × 3 de φ (sem φ / φ por D1 / φ por célula) × 4 níveis de agregação. Script reutilizável: `estima_phi_backtest.ps1`.

### Erro (%) — fit 2025 → jan-jun/26
| base | φ | célula×mês | célula total | D1 total | total geral | viés |
|---|---|---|---|---|---|---|
| S2_25 | φ_D1 | 60,6 | 56,0 | 38,7 | **25,6** | +25,6 |
| Q4_25 | sem φ | 57,8 | 52,9 | 39,2 | 25,9 | +25,9 |
| S2_25 | sem φ | **55,0** | **47,4** | **29,9** | 29,9 | +29,9 |
| ANO_25 | φ_célula | 69,8 | 61,8 | 31,1 | 31,1 | +31,1 |
| Q4_25 | φ_célula | 81,1 | 78,1 | 40,7 | 29,8 | +29,8 |
| ANO_25 | sem φ | 58,8 | 51,3 | 42,8 | 42,8 | +42,8 |

### Erro do total de 6 meses por D1
`H&C previsto 913 Mi vs real 604 Mi → **+51,3%** · LARGE 1.042 vs 847 → **+23,0%** · SMALL 562 vs 602 → **-6,7%**`

### Cinco conclusões que viram premissa
1. **φ por faixa está DESCARTADO.** Testado como a Beatriz pediu — e o dado diz não: φ é instável entre períodos (H&C 500-1500: 3,56 → 0,62; Small 120-150: 0,07 → 2,24; Large 200-500: 2,36 → 0,45). φ estimado num período **não prevê** o seguinte. Nos backtests, φ por célula é o **pior** modelo em todos os níveis (célula×mês 81% vs 58% sem φ). Clássico overfitting.
2. **φ por D1 ajuda só no agregado** (reduz o viés de 29,9% para 25,6%), não na célula. Mantido apenas nesse papel.
3. **NUNCA comprometer número em célula×mês.** Erro de 55-82% nesse grão. A agregação faz o erro cair pela metade (D1 total ~30%, total geral ~26%). **O compromisso do BC tem que ser por D1 × período (set-dez), não por faixa × mês.** A alocação por faixa é *indicativa*, não compromisso.
4. **O método SUPERESTIMA a Shopee sistematicamente.** O viés é **positivo em todas as 9 configurações** (+25,6% a +42,8%). Aplicar o YoY recente aos meses futuros infla a ameaça — a desaceleração real é mais rápida que a modelada. Para um BC pedindo verba, superestimar a ameaça é a direção que a liderança questiona.
5. **H&C é o problema.** +51,3% de erro (vs Large +23%, Small -6,7%). Coerente com §8.2 — a célula 500-1500 (degrau out/25 + colapso mai/26) provavelmente domina o erro.

### Consequência de método — o erro medido VIRA a banda de cenário
Em vez de corrigir o viés com um fator (fitting numa única janela), o erro out-of-sample medido passa a ser a **banda de incerteza declarada**:
- **Caso-base:** motor com melhor config (base = YoY do **S2'25**, φ por **D1**).
- **Banda:** ±~26% no total geral (±30% no D1) — **é a acurácia medida do método**, não um chute. Os cenários conservador/agressivo passam a ter lastro estatístico.
- **H&C com banda própria e mais larga**, até resolver a célula 500-1500.

---

## 10.6 Testes de mix e de previsibilidade do ratio [20/08] ✅ resultados favoráveis

### Teste 1 — Estabilidade do mix de faixas dentro da D1 (18 meses, CV = desvio/média)
| D1 | faixa | mix Shopee (média) | **CV Shopee** | mix MELI (média) | CV MELI |
|---|---|---|---|---|---|
| SMALL | 200 a 500 | 34,1% | **11%** | 41,4% | 5% |
| SMALL | 500 a 1500 | 20,6% | **14%** | 29,6% | 7% |
| LARGE | 500 a 1500 | 38,5% | **18%** | 31,8% | 11% |
| LARGE | 1500 a 3000 | 24,3% | **18%** | 35,3% | 6% |
| SMALL | 150 a 200 | 25,5% | **20%** | 12,6% | 7% |
| LARGE | +3000 | 8,2% | 28% | 24,0% | 7% |
| H&C | 1500 a 3000 | 48,5% | 31% | 44,1% | 16% |
| SMALL | 120 a 150 | 14,4% | 35% | 7,7% | 7% |
| LARGE | 200 a 500 | 29,1% | 39% | 8,9% | 10% |
| SMALL | +3000 | 5,3% | 48% | 8,7% | 9% |
| H&C | +3000 | 8,0% | **60%** | 18,4% | 11% |
| H&C | 200 a 500 | 19,1% | **71%** | 23,2% | 23% |
| H&C | 500 a 1500 | 24,4% | **77%** | 14,4% | 15% |

**Conclusões:** o mix do **MELI é muito estável** (CV 5-23%) → alocação top-down confiável do nosso lado. O mix da **Shopee é estável em LARGE e SMALL** (CV 11-39%, a maioria ≤20%) → top-down viável com banda. **Em H&C o mix da Shopee é instável** (CV 60-77%) → nessa D1 a quebra por faixa é **indicativa**, com banda larga, nunca compromisso.
**Fragilidade aceita:** o efeito mix/migração de cesta atinge MELI e Shopee (item promocionado muda de faixa). Conhecido pelo time e liderança; **não bloqueia** — é sinalizado nas premissas. Nota analítica: como afeta numerador e denominador, **cancela parcialmente no ratio** — argumento a favor do ratio como métrica de compromisso.

### Teste 2 — Prever o RATIO é bem mais preciso que prever GMV no grão fino
Protocolo idêntico (fit 2025 → prevê jan-jun/26), nível **D1 × mês**:
| modelo | escopo | MAPE do ratio | erro médio (pp) |
|---|---|---|---|
| **A — via os 2 GMVs** (prevê Shopee e MELI, divide) | TOTAL | **25,7%** | **9,4 pp** |
| B — ratio direto (série do ratio) | TOTAL | 26,0% | 9,5 pp |
| C — naive (ratio = mesmo mês do ano anterior) | TOTAL | 55,1% | 20,7 pp |
| A | LARGE | **24,2%** | 6,4 pp |
| A | SMALL | **17,9%** | 6,1 pp |
| A | H&C | 35,1% | 15,7 pp |

**Quatro conclusões:**
1. **O ratio no grão D1 × MÊS tem o mesmo erro (~26%) que o GMV da Shopee tinha só no total de 6 meses.** Ganho grande de resolução: passamos a ter leitura **mensal** com a acurácia que antes só existia no agregado.
2. **A ≈ B** → não é preciso escolher. Usar a **rota A** (projetar os dois GMVs e dividir), que entrega o **ratio E os amounts** — e os amounts são necessários para o BC. A melhor precisão vem da **correlação de erros** entre Shopee e MELI (ambos seguem o mercado), que se cancela na divisão.
3. **O modelo bate o benchmark naive por ~2x** (26% vs 55%) → evidência objetiva de que há sinal real capturado. Ótimo argumento de validação para a liderança.
4. **Small é o mais previsível** (17,9% / 6,1 pp), Large sólido (24,2% / 6,4 pp), **H&C o pior** (35,1% / 15,7 pp) — coerente com todos os outros diagnósticos.

### Teste ainda pendente
- Refazer H&C **sem a célula 500-1500** (sabidamente quebrada, §8.2) e verificar se o erro converge para o nível de Large.
- **Backtest do Motor v2** (§6.1b) contra o benchmark de ~26%.

---

## 10.7 MOTOR v2 — resultados [20/08] · script `motor_v2_forecast.ps1`

**Recortes temporais usados (a declarar em todo output):**
- Índice sazonal $S_m$: **Shopee jan/24→jun/26** (2-3 obs/mês) · **MELI jan/23→jun/26** (3-4 obs/mês)
- Nível: **L3M dessazonalizado = abr-mai-jun/26** (centrado em mai/26)
- Tendência $g$: **OLS em log da série dessazonalizada nos últimos 3 meses (L3M)**
- Backtest: fit **até dez/25** → prevê **jan-jun/26**

### A) Índices sazonais estimados (média 1,00 = mês típico)
| série | jan | fev | mar | abr | mai | jun | jul | ago | **set** | **out** | **nov** | **dez** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SHP H&C | 1,22 | 1,08 | 1,36 | 0,79 | 0,80 | 0,59 | 0,69 | 0,70 | 1,19 | **1,65** | 1,26 | 1,26 |
| MELI H&C | 1,18 | 1,07 | 1,09 | 0,69 | 0,70 | 0,65 | 0,71 | 0,80 | 1,34 | 1,19 | **1,89** | 1,33 |
| SHP LARGE | 0,90 | 0,73 | 0,75 | 0,77 | 0,87 | 0,91 | 1,18 | 1,14 | 1,26 | 1,23 | **1,35** | 1,16 |
| MELI LARGE | 0,93 | 0,83 | 0,96 | 0,90 | 1,03 | 0,96 | 1,05 | 1,02 | 0,95 | 0,99 | **1,70** | 0,90 |
| SHP SMALL | 0,76 | 0,84 | 1,14 | 1,09 | 1,20 | 1,03 | 1,03 | 1,01 | 0,96 | 0,88 | 1,09 | 1,06 |
| MELI SMALL | 0,94 | 0,84 | 0,96 | 0,93 | 1,08 | 0,98 | 1,09 | 1,03 | 0,96 | 0,97 | **1,31** | 0,98 |

**Achado quantificado (vai para o Grid):** em Large, MELI nov = **1,70** vs Shopee **1,35**. Em Small, MELI 1,31 vs Shopee 1,09. Confirma numericamente, por D1, que **os calendários são diferentes**: a BF é nosso pico, o dela é mais distribuído.

> ⚠️ **CORREÇÃO (20/08, ver §10.8):** a leitura inicial de que "em H&C o pico da Shopee é outubro (1,65) — o 10.10" estava **ERRADA**. Aquele 1,65 é **artefato**: o degrau de out/25 na célula 500-1500 foi absorvido pelo índice sazonal de outubro de toda a D1 (com só 2 observações de outubro, uma delas contaminada). É o watch-out #4 (confundimento tendência × sazonalidade) se materializando. Não usar esse número no material.

### B) Backtest do Motor v2 — **L3M (N=3) vence**
| N | φ | escopo | WAPE shp/mês | viés total 6m | MAPE ratio | erro ratio (pp) |
|---|---|---|---|---|---|---|
| **3** | 1,0 | TOTAL | 38,2 | **+3,8** | 27,6 | 10,4 |
| **3** | 0,9 | TOTAL | 30,1 | -9,4 | **25,0** | 9,6 |
| **3** | 0,8 | TOTAL | 27,7 | -17,6 | **24,3** | 9,3 |
| 6 | 0,9 | TOTAL | 34,0 | +5,3 | 34,1 | 13,0 |
| 6 | 0,8 | TOTAL | 28,2 | -8,1 | 24,5 | 8,7 |
| **3** | **0,9** | **LARGE** | 12,7 | -12,7 | **8,6** | **2,5** |
| 3 | 1,0 | LARGE | 10,1 | +0,4 | 12,8 | 3,6 |
| 3 | 0,8 | H&C | 17,1 | +17,1 | 24,0 | 12,5 |
| 3 | 0,9 | SMALL | 49,3 | **-49,3** | 41,9 | 13,5 |

**Conclusões:**
1. **N=3 (L3M) é melhor que N=6** em praticamente toda a grade → a escolha da Beatriz é validada empiricamente.
2. **LARGE fica excelente com v2**: MAPE do ratio **8,6%** e erro de **2,5 pp** (v1 dava 24,2%). Grande ganho.
3. **SMALL falha no v2**: viés de **-49%** (subestima sistematicamente), MAPE 42% — porque a aceleração de Small virou no fim de 2025 e a tendência dessazonalizada de H2'25 estava plana. **Aqui o v1 (via YoY) é melhor: 17,9% / 6,1 pp.**
4. **H&C melhora muito ao segregar a célula 500-1500** (§C abaixo).
5. φ funciona como dial de viés: φ=1 → viés +3,8% (quase nulo, mas MAPE maior); φ=0,8 → MAPE menor, mas subestima 17,6%.

### C) H&C — com vs sem a célula 500 a 1500 (N=6, φ=0,9)
| variante | WAPE shp/mês | viés 6m | MAPE ratio | erro pp |
|---|---|---|---|---|
| COM 500-1500 | 62,5 | +62,5 | 52,4 | 23,3 |
| **SEM 500-1500** | **30,9** | +21,8 | **29,2** | **10,0** |

**Diagnóstico confirmado:** segregar a célula **reduz o erro de H&C à metade**. Justifica o tratamento em regime separado (§8.2). A célula segue no BC como diagnóstico e com premissa própria — só sai da estimação de parâmetros.

### D) ⚠️ PREVISÃO PRÉ-REGISTRADA — versão v2 apenas · **SUPERADA pela versão COMBO em §10.9-B** (usar aquela)
*(Motor v2, N=3/L3M, fit até jun/26. Valores em R$ Mi, perímetro = faixas-foco.)*

| mês | D1 | Shopee (φ=0,8 / **0,9** / 1,0) | MELI (φ=0,9) | ratio (φ=0,9) |
|---|---|---|---|---|
| **jul/26** | H&C | 104,7 / **109,2** / 114,1 | 195,7 | 55,8% |
| **jul/26** | LARGE | 251,8 / **256,5** / 261,6 | 634,5 | 40,4% |
| **jul/26** | SMALL | 134,2 / **138,3** / 142,8 | 386,0 | 35,8% |
| **jul/26** | **TOTAL** | **490,7 / 504,0 / 518,5** | 1.216,2 | **41,4%** |
| ago/26 | H&C | 115,9 / **125,1** / 136,2 | 221,8 | 56,4% |
| ago/26 | LARGE | 252,4 / **261,0** / 271,1 | 625,4 | 41,7% |
| ago/26 | SMALL | 138,9 / **146,8** / 156,2 | 370,0 | 39,7% |
| ago/26 | **TOTAL** | **507,2 / 532,9 / 563,5** | 1.217,2 | **43,8%** |

**Julho é o teste limpo** (mês fechado, dado ainda não existe na base → sem viés retrospectivo). Agosto fecha em 31/08.

### E) Parâmetros estimados (fit até jun/26)
| série | g mensal | nível L3M (Mi) |
|---|---|---|
| SHP H&C | **+9,98%** | 120,3 |
| MELI H&C | +4,16% | 267,8 |
| SHP LARGE | **+9,54%** | 193,0 |
| MELI LARGE | +4,41% | 583,8 |
| SHP SMALL | **+7,04%** | 109,4 |
| MELI SMALL | +3,11% | 344,8 |

**Diferencial de crescimento mensal Shopee − MELI: H&C +5,8 pp · Large +5,1 pp · Small +3,9 pp.** É esse diferencial composto que faz o ratio subir — e é exatamente o que o BC precisa neutralizar.

### F) 🚩 ALERTA DE IMPLAUSIBILIDADE — não usar set-dez de H&C ainda
A projeção de H&C dá **ratio > 100% em out/26** (129% com φ=1; 108% com φ=0,9), ou seja, Shopee faturando mais que o MELI nas faixas-foco de H&C. Causas: **(i)** a célula 500-1500 quebrada está dentro da série (inflando nível e tendência) e **(ii)** composição de um diferencial de 5,8 pp/mês por 6 meses somada à assimetria sazonal de outubro (SHP 1,65 vs MELI 1,19). **Ação obrigatória:** refazer H&C com a célula segregada antes de usar set-dez. Large e Small não têm esse problema.

### G) Encaminhamento metodológico recomendado
Em vez de escolher motor por D1 (o que caracteriza *model shopping* e infla otimismo — watch-out #9), adotar **combinação de previsões** (Bates & Granger, 1969): média das previsões v1 (YoY) e v2 (decomposição). A literatura mostra que combinar reduz variância e é robusto a má-especificação — e resolve o caso Small (v2 subestima, v1 acerta) sem escolher a dedo. **A testar no mesmo protocolo.**

---

## 10.8 H&C em 3 visões + combinação de previsões [20/08] · `motor_v3_hc_e_combinacao.ps1`

**Decisão da Beatriz:** H&C entra **junto E separado**, explicando os fatores. Três visões entregues: **TOTAL** · **BASE** (sem a célula) · **CÉLULA 500-1500** isolada. A célula **empresta o perfil sazonal da BASE**, porque a série própria dela é um degrau e o índice sazonal sairia lixo.

### A) Parâmetros e backtest das 3 visões (L3M, φ=0,9)
| visão | g mensal Shopee | nível L3M (Mi) | ratio no nível | bt WAPE | bt MAPE ratio | bt viés |
|---|---|---|---|---|---|---|
| H&C TOTAL | +17,6% | 120,3 | 44,9% | 35,2 | 24,4 | +35,2 |
| H&C BASE | +24,3% | 82,9 | 35,7% | **100,6** | 27,4 | **+100,6** |
| **CÉLULA 500-1500** | **−26,1%** | 24,4 | 58,4% | 33,3 | 58,2 | −17,2 |

**Achado 1 — a célula já passou do pico e está CAINDO:** tendência de **−26,1%/mês**. Ela saltou em out/25, e desde mar/26 desce (65,5 → 32,7 → 6,0 → 16,6 Mi). Não é uma ameaça crescente; é um evento em dissipação.

**Achado 2 — 🔴 o pico de outubro de H&C era ARTEFATO.** O índice sazonal de outubro da Shopee em H&C (1,65) foi inflado pelo **degrau de out/25 da célula** — com apenas 2 observações de outubro (2024 normal, 2025 contaminada), o evento entrou no índice como se fosse sazonalidade. **Isso invalida a leitura "o pico dela é o 10.10" em H&C** e era a causa do ratio > 100% em out/26 (§10.7-F). Corrigido em §10.7-A.

**Achado 3 — a tendência de H&C é instável com qualquer recorte.** BASE com L3M dá viés de **+100%** no backtest (a tendência de out-dez/25 extrapolou demais); TOTAL dá +35%. Com N=6 (§10.7-C) o padrão se invertia. **Conclusão: H&C exige a banda mais larga e o tratamento por cenário, não por ponto.**

### B) Forecast H&C jul-dez/26 (φ=0,9) — recomposto vs direto
| visão | jul | ago | set | out | nov | dez |
|---|---|---|---|---|---|---|
| BASE — Shopee (Mi) | 94,8 | 114,7 | 226,2 | 206,1 | 252,0 | 269,2 |
| CÉLULA — nível constante | 19,1 | 19,7 | 33,5 | 26,7 | 28,9 | 27,6 |
| CÉLULA — com tendência (−26%/mês) | 11,5 | 9,6 | 13,5 | 9,1 | 8,5 | 7,1 |
| **TOTAL recomposto — ratio** | **55,0%** | **55,0%** | **61,0%** | **59,1%** | **41,2%** | **62,4%** |
| TOTAL direto — ratio | 55,8% | 56,4% | 63,1% | **107,8%** ❌ | 56,2% | 86,0% |

**O recomposto elimina a anomalia de outubro** e entrega uma trajetória plausível (41-62%). **Adotar o recomposto** (BASE + cenário de célula) como caso-base de H&C; o direto fica como referência.

### C) 🎯 Combinação de previsões — VENCE (adotar como caso-base)
Protocolo idêntico (fit dez/25 → jan-jun/26), φ=0,9, média das 3 D1s:
| modelo | WAPE Shopee | **MAPE ratio** | **erro pp** | **viés** |
|---|---|---|---|---|
| v1 (YoY) | 28,7 | 23,2 | 8,0 | −11,1 |
| v2 (decomposição) | 54,2 | 26,0 | 8,5 | +12,8 |
| **combo 50/50** | 36,8 | **22,2** | **7,5** | **+0,9** |

Por D1 (combo): LARGE 10,2% / 2,8 pp · H&C 26,0% / 9,7 pp · SMALL 30,3% / 10,1 pp.

**Por que adotar a combinação:** ela ganha nas duas métricas que importam (MAPE do ratio e erro em pp) **e** os viéses se cancelam (v1 subestima −11,1%, v2 superestima +12,8% → combo **+0,9%, praticamente sem viés**). É o resultado clássico de Bates & Granger (1969), e resolve o problema de *model shopping*: não escolhemos motor por D1, usamos os dois. Para um BC, ausência de viés sistemático vale mais que o menor erro absoluto — significa que não estamos inflando nem desinflando a ameaça.

**Ressalva honesta:** o combo não é o melhor em cada D1 isoladamente (v2 é melhor em Large: 8,6% vs 10,2%; v1 é melhor em Small: 22,3% vs 30,3%). Reportar essas alternativas como **sensibilidade**, mantendo o combo como número central.

### D) Banda de incerteza a declarar (do backtest do combo)
**±22% no ratio (≈ ±7,5 pp)** como banda geral · **Large ±3 pp** (mais confiável) · **Small ±10 pp** · **H&C ±10 pp com ressalva de instabilidade de tendência**.

### E) Pendências desta etapa
1. Recalcular os **índices sazonais de H&C BASE** (sem a célula) para substituir o perfil contaminado no material.
2. Regerar a **previsão pré-registrada de jul/ago** com o **combo** (a de §10.7-D usou só v2).

---

## 10.9 NÚMEROS OFICIAIS — sazonalidade limpa + previsão pré-registrada (COMBO) [20/08]

### A) Índices sazonais de H&C — a prova do artefato e o perfil corrigido
| série | jan | fev | mar | abr | mai | jun | jul | ago | **set** | **out** | **nov** | dez |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SHP H&C TOTAL *(contaminado)* | 1,22 | 1,08 | 1,36 | 0,79 | 0,80 | 0,59 | 0,69 | 0,70 | 1,19 | **1,65** | 1,26 | 1,26 |
| **SHP H&C BASE** *(limpo)* | 1,17 | 1,01 | 1,29 | 0,75 | 0,98 | 0,70 | 0,78 | 0,81 | **1,37** | **1,09** | 1,18 | 1,13 |
| **MELI H&C BASE** | 1,19 | 1,08 | 1,10 | 0,69 | 0,69 | 0,62 | 0,70 | 0,80 | 1,34 | 1,19 | **1,99** | 1,34 |
| SHP CÉLULA 500-1500 | 1,41 | 1,57 | 1,82 | 1,26 | 0,32 | 0,34 | 0,36 | 0,37 | 0,72 | **3,95** ❌ | 2,19 | 2,21 |

**Prova do artefato:** o índice de outubro da **célula isolada é 3,95** — impossível como sazonalidade recorrente (é o degrau de out/25 lido como padrão). Ele arrastava o outubro da D1 inteira de **1,09 (limpo) para 1,65 (contaminado)**.

**Leitura CORRIGIDA de H&C (usar esta):** o pico da Shopee é **setembro (1,37)** — entrada da temporada de calor —, e **outubro é neutro (1,09)**. O nosso pico é **novembro (1,99)**, o mais forte de todas as séries medidas. O perfil da Shopee é **bem mais achatado** (0,70–1,37) que o nosso (0,62–1,99): reforça, agora com dado limpo, que **Q4 concentrado é evento MELI**.

### B) ⚠️ PREVISÃO PRÉ-REGISTRADA OFICIAL — **registrada em 2026-08-20**, antes de jul/26 existir na base
*Motor: **combinação v1+v2 (50/50)**, L3M, fit até jun/26. H&C = BASE + célula a nível constante. Shopee em R$ Mi.*

| escopo | jul/26 (φ 0,8 / **0,9** / 1,0) | ago/26 (φ 0,8 / **0,9** / 1,0) |
|---|---|---|
| LARGE | 234,6 / **246,7** / 259,0 | 237,8 / **262,0** / 289,3 |
| SMALL | 117,3 / **122,1** / 127,1 | 115,4 / **124,0** / 133,9 |
| H&C recomposto | 99,3 / **104,9** / 110,9 | 103,2 / **114,3** / 127,3 |
| **TOTAL 3 D1s** | **451,2 / 473,8 / 497,0** | **456,3 / 500,2 / 550,6** |

MELI (φ=0,9): jul **1.225,0** · ago **1.214,3** → **ratio previsto jul = 38,7% · ago = 41,2%**.
*Julho é o teste limpo (mês fechado, dado ainda inexistente na base). Banda estreita em jul (±5%), mais larga em ago (±10%).*

### C) Forecast jul-dez/26 (COMBO, φ=0,9) — ratio mensal
| escopo | jul | ago | set | out | **nov** | dez |
|---|---|---|---|---|---|---|
| LARGE | 39,0% | 42,5% | 52,2% | 50,5% | **33,9%** | 55,8% |
| SMALL | 32,5% | 34,6% | 36,9% | 33,5% | **30,6%** | 41,5% |
| H&C recomposto | 48,6% | 47,9% | 56,7% | 47,7% | **35,4%** | 47,5% |
| **TOTAL** | 38,7% | 41,2% | 49,5% | 45,2% | **33,6%** | 49,3% |

**Padrão relevante para o storytelling:** o ratio **cai em novembro em todas as D1s** — é a nossa Black Friday empurrando o ratio para baixo. Novembro é o mês em que naturalmente ganhamos terreno; o problema é dezembro e o pós-BF.

### D) Banda do período jul-dez/26 (o tamanho da ameaça)
| escopo | Shopee (φ 0,8 / 0,9 / 1,0) | MELI baseline (φ=0,9) | ratio do período |
|---|---|---|---|
| LARGE | 1.533 / **1.792** / 2.170 | 4.066 | 39,9% / **44,1%** / 49,5% |
| SMALL | 699 / **785** / 914 | 2.267 | 32,0% / **34,6%** / 38,3% |
| H&C recomposto | 888 / **1.081** / 1.399 | 2.360 | 40,9% / **45,8%** / 52,0% |
| **TOTAL 3 D1s** | **3.120 / 3.657 / 4.482** | **8.692** | 38,1% / **42,1%** / 47,4% |

### E) Mecânica do joystick — está tudo pronto
- **Dial A (φ)** = trajetória Shopee → a banda de §D
- **Dial B** = perfil sazonal da Shopee (próprio ✅ estimado) vs do mercado (a implementar)
- **Dial C** = ambição MELI: dado um **ratio-alvo r\***, resolve-se
  $$\text{MELI}_{\text{necessário}} = \frac{\text{Shopee}_{\text{forecast}}}{r^*} \qquad\Rightarrow\qquad \textbf{Incremental} = \text{MELI}_{\text{necessário}} - \text{MELI}_{\text{baseline}}$$
- O **MELI baseline** (coluna de §D) é a projeção inercial — exatamente o "sem ação" que o BC precisa como contrafactual.
- **DECISÃO PENDENTE (Beatriz):** qual é o **ratio de referência** a conter? Opções: (a) Q2'26 realizado, (b) H1'26 realizado, (c) LTM, (d) nível dessazonalizado L3M (Large 33,1% · Small 31,7% · H&C 44,9%). Cada escolha muda o tamanho do incremental.

---

## 10.10 Por que o ratio SOBE na projeção + escolha do ratio de referência [20/08]

### A) Esclarecimento conceitual — desaceleração ≠ parar de perder espaço
Dúvida legítima da Beatriz: *"vamos perder espaço na projeção? a Shopee não desacelerava?"*
**Sim, ela desacelera — e mesmo assim o ratio sobe.** O φ amortece a **taxa de crescimento**, não transforma crescimento em queda. Enquanto o crescimento dela superar o nosso, o ratio sobe; a desaceleração só faz subir mais devagar.

⚠️ **Correção (20/08):** a tabela abaixo estava com as taxas estimadas em **N=6**, mas o motor adotado usa **L3M (N=3)**. Taxas corretas (janela abr-jun/26, dessazonalizada) — as que efetivamente dirigem o forecast:

| D1 | g mensal Shopee | g mensal MELI | **diferencial** |
|---|---|---|---|
| LARGE | **+7,25%** | +2,07% | **+5,18 pp** |
| SMALL | **+12,33%** | +1,84% | **+10,49 pp** |
| H&C | **+24,29%** | +0,10% | **+24,19 pp** |
| *ponderado (3 D1s)* | *+13,1%* | *+1,6%* | *+11,5 pp* |

*(As de N=6 eram: Large 9,54/4,41 · Small 7,04/3,11 · H&C 9,98/4,16 — mantidas aqui só como registro.)* Nota: o diferencial de H&C (+24,19 pp/mês) é extremo e reflete a instabilidade de tendência já documentada em §10.8 — reforça a banda larga para essa D1.

**Validação visual (artefato `dashboard_realizado_projetado.html`):** o ratio realizado subiu de **~11% (jan/25) para ~34% (jun/26)** de forma contínua. A projeção até 49,3% (dez/26) é a **continuação da mesma inclinação** — não é um salto nem uma descontinuidade. Mesmo no cenário conservador (φ=0,8) o ratio sobe. **É essa continuidade que justifica o BC.**

### B) Ratios de referência realizados (perímetro faixas-foco)
| D1 | Q2'26 | H1'26 | LTM | nível L3M dessaz. | **projetado jul-dez** |
|---|---|---|---|---|---|
| LARGE | 29,6% | 27,4% | 23,9% | 33,1% | **44,1%** |
| SMALL | 35,5% | 31,5% | 25,7% | 31,7% | 34,6% |
| H&C | 47,8% | 46,4% | 34,7% | 39,1% | 45,8% |

### C) Incremental necessário (R$ Mi) por escolha de referência — φ=0,9
| D1 | ref = **Q2'26** | ref = H1'26 | ref = LTM | ref = L3M dessaz |
|---|---|---|---|---|
| **LARGE** | **+1.997** (+49,1%) | +2.481 (+61,0%) | +3.420 (+84,1%) | +1.357 (+33,4%) |
| SMALL | **−58** (−2,6%) | +220 (+9,7%) | +782 (+34,5%) | +207 (+9,1%) |
| H&C | **−97** (−4,1%) | −32 (−1,4%) | +754 (+32,0%) | +403 (+17,1%) |
| **TOTAL** | **≈ 1,8 Bi** | ≈ 2,7 Bi | ≈ 5,0 Bi | ≈ 2,0 Bi |

**Achado central: com Q2'26 como referência, TODO o desafio é LARGE.** Small e H&C já estão projetados para segurar (incremental negativo = não precisa de ação para manter o nível atual). Large sozinho responde por **+1,997 Bi**, porque é onde o ratio mais deteriora (29,6% → 44,1%, +14,5 pp).
*Ressalva: os negativos valem no caso-base (φ=0,9). Com φ=1,0 (Shopee acelerando) Small e H&C voltam a exigir incremental — a interação aparece no joystick.*

### D) Recomendação de framing (decisão da Beatriz)
- **Referência principal = Q2'26** (trimestre realizado mais recente): significa *"congelar a deterioração a partir de hoje"*. É a mais difícil de contestar e a menos inflada.
- **LTM como cenário ambicioso**: significa *"recuperar um ano de perdas"* → 5,0 Bi.
- O joystick ganha assim um intervalo com significado de negócio: **conter (1,8 Bi) → recuperar (5,0 Bi)**.

**Artefato:** `dashboard_realizado_projetado.html` — gráfico contínuo realizado→projetado (barras hachuradas, ratio tracejado, divisória em jun/26), filtro por D1/Total, com a tabela do diferencial de crescimento. Já implementa a spec visual de §11.5-4b.

---

## 10.11 ⚠️ CORREÇÃO da referência: o Q2'26 é sazonalmente inválido como alvo [20/08]

### A) Esclarecimento de leitura (dúvida da Beatriz)
As colunas Q2'26 / H1'26 / LTM **não são série temporal** — são **janelas encaixadas terminando todas em jun/26** (3, 6 e 12 meses). Andar para a direita é andar **para trás** no tempo. Como o ratio subiu, quanto mais passado se inclui, mais baixa a média. Logo `LTM 23,9% < H1 27,4% < Q2 29,6%` **é a assinatura de um ratio em alta**, não de queda. Ordem correta de leitura: 23,9% → 27,4% → 29,6% → 44,1%.

### B) 🔴 Achado: o fator sazonal do ratio (S_shopee / S_meli) distorce em direções OPOSTAS por D1
| D1 | fator médio abr-jun (Q2) | fator médio jul-dez (H2) | distorção H2/Q2 |
|---|---|---|---|
| **LARGE** | **0,891** (ratio deprimido) | **1,149** (ratio inflado) | **1,29x** |
| SMALL | 1,114 (inflado) | 0,958 (deprimido) | 0,86x |
| H&C | 1,215 (inflado) | 0,917 (deprimido) | 0,755x |

**Consequência grave:** comparar o Q2'26 realizado com uma projeção de **jul-dez** não é *like-for-like*. Em Large o Q2 é sazonalmente **ruim** para o ratio (fator 0,891) e o H2 é **bom** (1,149) — então parte do "salto" de 29,6% → 44,1% é **calendário, não Shopee**. Em Small e H&C ocorre o **inverso**, o que torna o alvo artificialmente **fácil** (daí os incrementais negativos).

> **Isso invalida a conclusão anterior de que "todo o desafio é Large".** Aquela concentração era, em boa parte, artefato de desalinhamento sazonal entre a janela de referência e a janela projetada.

### C) Referências sazonalmente válidas
| D1 | Q2'26 (❌ inválido p/ H2) | **H2'25** (like-for-like) | **nível L3M dessaz.** (neutro) | projetado H2'26 | Δ YoY do ratio |
|---|---|---|---|---|---|
| LARGE | 29,6% | 20,2% | 33,1% | 44,1% | **+23,9 pp** |
| SMALL | 35,5% | 19,5% | 31,7% | 34,6% | **+15,1 pp** |
| H&C | 47,8% | 24,8% | 39,1% | 45,8% | **+21,0 pp** |

**Statement sazonalmente limpo da ameaça:** na comparação H2 vs H2, **o ratio praticamente dobra nas três D1s**.

### D) Incremental por referência (R$ Mi, φ=0,9)
| D1 | ref Q2'26 ❌ | ref **H2'25** (zero deterioração YoY) | ref **L3M dessaz** ✅ |
|---|---|---|---|
| LARGE | +1.997 (+49%) | +4.820 (+119%) | **+1.357 (+33%)** |
| SMALL | −58 | +1.751 (+77%) | **+207 (+9%)** |
| H&C | −97 | +1.996 (+85%) | **+403 (+17%)** |
| **TOTAL** | **1.842** | **8.567** | **1.966** |

### E) RECOMENDAÇÃO REVISADA
1. **Referência de compromisso = nível dessazonalizado L3M** → **≈ R$ 2,0 Bi**. É o único candidato **neutro de sazonalidade** por construção (mesmo conceito de "dado dessazonalizado" usado em desemprego e PIB). Significado: *"manter a posição competitiva atual, medida limpa de calendário"*. E distribui o esforço de forma crível: **Large 69% · H&C 20% · Small 11%**.
2. **Cenário ambicioso = H2'25** → **≈ R$ 8,6 Bi** = *"zero deterioração YoY"*. Provavelmente **infactível** (exigiria +119% em Large sobre a projeção inercial) — entra como teto da régua e para dimensionar o custo da recuperação total.
3. **Q2'26 só como número de comunicação**, sempre com a ressalva de que Q2 vs H2 não é sazonalmente comparável. **Não usar para alocar entre D1s.**
4. **Régua do joystick (Dial C):** conter no nível atual (**2,0 Bi**) → recuperar o ano (**8,6 Bi**).

---

## 10.12 JOYSTICK — resultado com referência = nível atual (L3M dessaz) [20/08]
**Artefato:** `joystick_incremental.html` — 3 dials (escopo · φ · ratio de referência + ajuste fino em pp), KPIs, selo de viabilidade, tabela mensal e alocação por faixa.

### Caso-base: Total 3 D1s · φ=0,9 · alvo = nível atual (34,3% equivalente)
| | valor |
|---|---|
| Shopee jul-dez/26 (projetado) | **3.657 Mi** (ratio inercial **42,1%**) |
| MELI baseline inercial | **8.692 Mi** (+41,4% YoY vs H2'25) |
| MELI necessário | **10.658 Mi** |
| **INCREMENTAL NECESSÁRIO** | **1.966 Mi (+22,6% sobre o baseline)** |
| Crescimento YoY exigido do MELI | **73,4%** |
| Recorde histórico (maior YoY em 6 meses) | **75,6%** (janela terminando ago/24) |
| **Selo de viabilidade** | 🟡 **NO LIMITE** — exequível, sem folga |

### Selo de viabilidade — metodologia
Compara o **crescimento YoY exigido** do MELI (MELI necessário ÷ MELI realizado em H2'25) com o **maior crescimento YoY em 6 meses já entregue** na série histórica da mesma D1/perímetro. Régua: ≤80% do recorde = 🟢 viável · 80-105% = 🟡 no limite · >105% = 🔴 infactível. Recordes: **Large 98,2%** (set/24) · **H&C 85,1%** (ago/24) · **Small 56,1%** (jun/24) · **Total 75,6%** (ago/24).
*Confirma §10.11: com referência H2'25 o exigido vira 2-3x o recorde → **infactível**, como previsto.*

### Distribuição mensal do incremental (Total, caso-base)
| jul | ago | **set** | out | **nov** | **dez** |
|---|---|---|---|---|---|
| +175 | +261 | **+562** | +422 | **−53** | **+598** |

**Achado operacional relevante:** **novembro tem incremental NEGATIVO** — o ratio inercial de nov (33,6%) já fica **abaixo** do alvo (34,3%) por conta da nossa Black Friday. Ou seja, **a BF resolve novembro sozinha**; o esforço do BC precisa se concentrar em **setembro, outubro e dezembro** (1.582 dos 1.966 Mi = **80% do incremental**). Isso tem implicação direta de execução: o plano de sellers tem que estar operando **antes de setembro**.

### Alocação por faixa
Feita pelo **mix LTM do MELI** dentro da D1 (o incremental é GMV nosso a entregar). Em H&C a alocação é **indicativa** (mix da Shopee com CV 60-77%, §10.8).

---

## 10.13 Simulador v2 — refeito após crítica de clareza [20/08]
**Feedback da Beatriz sobre a v1 (`joystick_incremental.html`):** *"algumas coisas estão escritas bonitas mas não dá pra entender"*. Problemas concretos apontados — **todos válidos**: (i) jargão sem tradução (φ, "inercial", "zero YoY", L3M, LTM); (ii) **sem unidade** nas tabelas; (iii) **sem referencial histórico** ao lado do alvo → impossível julgar se é ambicioso; (iv) **período não explícito** em "nível atual" e "baseline"; (v) faltava o **evolutivo mensal** realizado→projetado.

**Regras de comunicação adotadas para todo artefato deste projeto (LOCKED):**
1. **Nenhum jargão sem tradução na própria tela.** φ → "como a Shopee deve crescer"; baseline inercial → "MELI se não fizermos nada"; ratio → explicado como "quanto ela fatura para cada R$ 100 nossos".
2. **Unidade em todo cabeçalho** ("R$ Milhões").
3. **Período explícito em toda referência** ("média abr-jun/26, sem calendário", "realizado jul-dez/25").
4. **Referência histórica sempre visível ao lado do alvo** (um ano atrás · hoje · sem ação) — sem isso não se julga ambição.
5. **Glossário na própria página.**
6. **Evolutivo mensal é peça central**, não a tabela.

**Artefato:** `simulador_desafio.html` — blocos numerados (1 categoria · 2 onde estamos · 3 ritmo da Shopee · 4 ratio-alvo), KPIs em linguagem natural, selo de viabilidade explicado, **gráfico com o incremental empilhado em verde sobre a barra do MELI** (mostra visualmente o pedaço a entregar), tabela mensal com unidades e glossário.

### Números do caso-base (Total 3 D1s · desacelera devagar · alvo = ratio de hoje 34,1%)
| | |
|---|---|
| Ratio um ano atrás (jul-dez/25) | **21,1%** |
| Ratio hoje (abr-jun/26, sem calendário) | **34,1%** → **+61% de avanço dela em 12 meses** |
| Ratio projetado sem ação (jul-dez/26) | **42,1%** |
| Shopee vai faturar | **3.657 Mi** |
| MELI se não fizermos nada | **8.692 Mi** (+41,4% vs jul-dez/25) |
| MELI precisa faturar | **10.757 Mi** (+75,0%) |
| **Desafio (incremental)** | **2.065 Mi** (+23,8%) |
| Selo | 🟡 **NO LIMITE** — exige +75,0% vs recorde de +75,6% |

**Mês a mês (falta entregar, Mi):** jul +188 · ago +273 · **set +581** · out +431 · **nov −35** · **dez +627**.

---

## 10.14 Cascata do incremental por faixa × mês × D1 [20/08]
**Método (definido pela Beatriz):** distribuir o incremental de cada D1 entre as faixas pelo **SoB realizado** — participação da faixa no faturamento do MELI na D1 — **sem fator de projeção**. Justificativa empírica: o SoB é **muito estável** entre janelas, logo não precisa ser projetado.

### SoB do MELI por faixa (validação de estabilidade)
| D1 · faixa | L3M | L6M | LTM | **ratio da faixa hoje** (abr-jun/26) |
|---|---|---|---|---|
| Large · 200 a 500 | 10,1% | 10,0% | 9,2% | 38,7% |
| Large · 500 a 1500 | 29,5% | 28,9% | 29,4% | **46,3%** |
| Large · 1500 a 3000 | 37,4% | 37,8% | 36,8% | 23,0% |
| Large · +3000 | 23,0% | 23,3% | 24,6% | 14,8% |
| Small · 120 a 150 | 7,8% | 8,0% | 7,8% | **72,2%** |
| Small · 150 a 200 | 11,6% | 12,4% | 12,8% | **64,3%** |
| Small · 200 a 500 | 43,6% | 42,4% | 42,2% | 29,2% |
| Small · 500 a 1500 | 28,0% | 28,1% | 28,5% | 27,5% |
| Small · +3000 | 9,0% | 9,0% | 8,8% | 22,6% |
| H&C · 200 a 500 | 24,2% | 24,7% | 21,8% | 23,1% |
| H&C · 500 a 1500 | 15,1% | 13,7% | 13,4% | **66,8%** |
| H&C · 1500 a 3000 | 44,4% | 44,8% | 47,4% | **67,4%** |
| H&C · +3000 | 16,3% | 16,8% | 17,5% | 13,3% |

Maior deriva: H&C 1500-3000 (44,4 → 47,4). Todas as outras variam ≤1,6 pp. **Cascata por SoB validada.**

### Matriz do incremental (caso-base: total, desacelera devagar, alvo = ratio de hoje 34,0%) — R$ Mi
| D1 · faixa | jul | ago | set | out | nov | dez | **jul-dez** |
|---|---|---|---|---|---|---|---|
| Large · 1500 a 3000 | 22 | 44 | 101 | 95 | −20 | 118 | **362** |
| Large · 500 a 1500 | 18 | 35 | 80 | 75 | −15 | 93 | **285** |
| H&C · 1500 a 3000 | 30 | 31 | 89 | 48 | −12 | 63 | **249** |
| Small · 200 a 500 | 26 | 37 | 48 | 30 | 20 | 74 | **235** |
| Large · +3000 | 14 | 27 | 62 | 59 | −12 | 72 | 222 |
| Small · 500 a 1500 | 17 | 24 | 31 | 19 | 13 | 48 | 151 |
| H&C · 200 a 500 | 16 | 17 | 49 | 26 | −7 | 34 | 136 |
| Large · 200 a 500 | 6 | 12 | 27 | 26 | −5 | 32 | 97 |
| H&C · +3000 | 11 | 11 | 33 | 17 | −4 | 23 | 91 |
| H&C · 500 a 1500 | 10 | 11 | 30 | 16 | −4 | 22 | 85 |
| Small · 150 a 200 | 7 | 10 | 13 | 8 | 5 | 20 | 62 |
| Small · +3000 | 5 | 8 | 10 | 6 | 4 | 15 | 49 |
| Small · 120 a 150 | 5 | 7 | 8 | 5 | 4 | 13 | 42 |
| **TOTAL** | **188** | **273** | **581** | **431** | **−35** | **627** | **2.065** |

### ⚠️ Observação estratégica sobre a lógica de alocação
A cascata por SoB distribui **proporcionalmente ao tamanho do nosso negócio**, não à gravidade da ameaça. Efeito visível: **Large 1500-3000 recebe o maior valor (362 Mi) apesar de ter o ratio mais confortável (23,0%)**, enquanto **H&C 500-1500 (ratio 66,8%) recebe só 85 Mi** por ser 15% da D1.
- **Prós do SoB:** é onde temos escala e sellers para entregar — mais executável.
- **Alternativa disponível (a pedido):** alocar por **gravidade** (peso pelo gap de ratio), concentrando onde ela está mais perto do nosso tamanho.
Registrado como opção; **o método vigente é SoB**, conforme decidido.

---

## 10.15 CONSOLIDAÇÃO — Large com três camadas [21/08] ⭐ versão sustentável
**Grid v3, aba 1:** https://grid.adminml.com/d/01M0DSBDBHEAV3650Q913YSP6Y/view · fonte `consolidado_large.html`

### Decisão de arquitetura (Beatriz)
O incremental é dividido em **três camadas por grau de controlabilidade**, cada uma com **uma regra medida**:
| camada | regra | valor H2'26 | controlabilidade |
|---|---|---|---|
| **BAU mais forte** | manter o ritmo YoY atual dos segmentos **em vez de desacelerar** (diferença entre projeção amortecida top-down e bottom-up dos segmentos no próprio ritmo) | **+380 Mi** | alta — é execução |
| **BC** | **os 6 grupos cotados entram** (ver §10.16). Quantificado: os 3 que ficaram atrás crescem no ritmo da CA | **+195 Mi** + substituição a quantificar | alta — negociada |
| **SD / fatia móvel** | a cauda longa `3P - SELLER DEV` (cresce só **+16,7%**) vai ao ritmo da carteira | **+120 Mi** | **baixa** — sellers pequenos, massivos, não assessorados; orientamos mas não garantimos execução |
| **TOTAL** | | **+696 Mi** | |

**A "fatia móvel" é o buffer:** se o BC for considerado subdimensionado, traz-se fatia do SD para dentro dele. Beatriz: *"mexer SD é igualmente difícil de mexer 1P — não temos ação sobre o dia a dia"*.

**1P fica fora:** cresce **+64,4% YoY**, acima da carteira. Não há catch-up a fazer — pedir "ritmo da carteira" seria pedir menos. *(YoY de um mês só — confirmar em janela de 3 meses.)*

### Resultado (Large, faixas prioritárias)
| | |
|---|---|
| Ratio um ano atrás (jul-dez/25) | **20,2%** |
| Ratio hoje (abr-jun/26, s/ calendário) | **33,1%** |
| Ratio sem ação (jul-dez/26) | **44,1%** → piora de **11,0 pp** |
| **Ratio com as 3 camadas** | **37,6%** → **evita 6,4 pp = 59% da piora** |
| Gap remanescente | **653 Mi** — risco declarado |

### A justificativa que sustenta o número (exigência da Beatriz)
Dizer "o ratio vai de 33% para 37,6% e isso é bom" só se sustenta mostrando os **crescimentos exigidos vs. realizados**:
| | jul | ago | set | out | nov | dez |
|---|---|---|---|---|---|---|
| Shopee — YoY projetado | +304% | +258% | +232% | +210% | +181% | +172% |
| MELI — YoY da tendência | +55% | +51% | +47% | +43% | +37% | +38% |
| **MELI — YoY exigido com as 3 camadas** | **+82%** | **+77%** | **+72%** | **+67%** | **+61%** | **+63%** |
| *(referência: YoY realizado jan-jun/26)* | *+60%* | *+57%* | *+77%* | *+66%* | *+60%* | *+48%* |

**O exigido (+61% a +82%) está dentro da faixa que já entregamos (+48% a +77%)** — no topo dela, mas dentro. É esse confronto que torna o pedido defensável.

### Estrutura do Grid (v3)
Aba 1 **Large consolidado** (a história) · Aba 2 Diagnóstico por faixa · Aba 3 Realizado × Projetado · Aba 4 Simulador (**anexo metodológico** — os dials saem da conversa principal).

### Regra de comunicação adicional (LOCKED)
Todo quadro deve ter **colunas = histórico + projeção** e **linhas = os KPIs principais** (faturamento, MoM, YoY de Shopee, do MELI, e o ratio). E **embaixo do gráfico, as premissas técnicas da projeção** — as duas regras, o amortecimento, as janelas, a validação de julho e o backtest.

### ⚠️ Ressalva a tratar
As três camadas entram **integralmente já em julho** no modelo. Na prática haveria uma rampa (julho e agosto já passaram). Ajustar a curva de entrada quando o plano tiver data de início.

---

## 10.16 CORREÇÃO — os 6 grupos entram no BC; e o mecanismo de substituição [21/08]

**Erro meu, corrigido:** eu havia excluído do BC os 3 grupos que já crescem acima da carteira (Engage, 3 Green, Philco), inferindo que "crescer bem" dispensa o BC. **Errado.** Beatriz: *"eles vão entrar, mesmo crescendo, porque eles estão crescendo na Shopee, então vamos tentar trazê-los pra mais perto"*.

**Razão de ser da seleção:** os 6 grupos cotados são **os sellers mais relevantes da Shopee em Large Appliances hoje**. Foram escolhidos por isso. Logo o BC tem **dois mecanismos**:

1. **Recuperação (quantificada): +195 Mi** — os 3 que ficaram atrás da carteira voltam ao ritmo dela. Ataca o **denominador** do ratio.
2. **Substituição (declarada, a quantificar)** — os 6 vendendo mais aqui tendem a vender menos lá. Ataca o **numerador**.

### 🔑 A substituição é 2,27x mais eficiente que o crescimento
Como o ratio é SHP/MELI, a derivada em relação a cada termo dá:
$$\frac{\partial r/\partial \text{SHP}}{|\partial r/\partial \text{MELI}|}=\frac{\text{MELI}}{\text{SHP}}=\frac{4.066}{1.792}=\mathbf{2{,}27}$$
**Cada R$ 1 retirado da Shopee vale R$ 2,27 somados ao MELI, em efeito sobre o ratio.** Isso reordena a prioridade do BC: tirar volume de lá vale mais que crescer aqui. **Pendência:** obter o faturamento desses 6 grupos **na Shopee** para dimensionar (fontes candidatas: base KSI Shopee / análise de gap de sellers do Shield).

### Períodos de cada medida — declarados (exigência da Beatriz)
| medida | janela |
|---|---|
| Crescimento próprio de cada grupo | **mai-jul/2026 vs mai-jul/2025** (mesmos 3 meses, ano contra ano) |
| Carteira Assessorada (referência +57,1%) | mesma janela · **+57,7%** em julho isolado |
| Base de projeção dos grupos | **jul-dez/2025 realizado** |
| SD (+16,7%) e 1P (+64,4%) | **jul/2026 vs jul/2025** (mês isolado) |

**Consistência validada:** a CA cresceu **+57,1%** na janela de 3 meses e **+57,7%** em julho isolado — as janelas praticamente coincidem, o que legitima comparar SD e 1P (medidos em julho) contra a carteira.

**Crescimento por grupo (mai-jul/26 vs mai-jul/25):** abaixo da carteira → Electrolux **−5,0%**, Infoar **−34,4%**, Outlet das Fábricas **+5,2%** · acima → Engage **+67,7%**, 3 Green **+136,5%**, Philco/Britânia **+210,1%**.

---

## 10.17 ⭐ A MIGRAÇÃO — a evidência central do BC [21/08] · `migracao_sellers.html` (Grid v5, aba 2)

### A fórmula da substituição (documentada a pedido da Beatriz)
Seja $r = S/M$ o ratio (Shopee ÷ MELI). Para R$ 1:
- **Real incremental** (venda nova; só o denominador se move): $|\Delta r| \approx r/M$
- **Real de substituição** (migra da Shopee; **os dois** lados se movem, $S{-}1$ e $M{+}1$): $|\Delta r| \approx (1+r)/M$

$$\boxed{\text{eficiência da substituição} \;=\; \frac{1+r}{r} \;=\; 1+\frac{1}{r} \;=\; 1+\frac{M}{S}}$$

Large (M=4.066, S=1.792, r=44,1%) → **3,27x**. *(Correção: eu havia dito 2,27x — esse é o efeito de apenas **retirar** da Shopee; a substituição também **soma** do nosso lado, daí 1 + M/S.)*

**Duas consequências para estruturar o BC:**
1. **Cada real deve ser pesado pela origem.** R$ 100 Mi de substituição = R$ 327 Mi de venda nova, em efeito sobre o ratio.
2. Como a eficiência é $1+1/r$, **a substituição vale mais onde a Shopee ainda é pequena**: r=44% → 3,3x · r=20% → **6x**. Defender território que ainda dominamos é mais eficiente que reagir onde já perdemos.

### 🔴 O achado: o faturamento não desapareceu, mudou de endereço
**Os 6 grupos cotados, jul/25 → jun/26:**
| | MELI | Shopee | total do grupo | % na Shopee |
|---|---|---|---|---|
| jul/25 | 60,7 | 19,5 | 80,2 | 24% |
| **jun/26** | **75,2** | **105,9** | **181,1** | **58%** |
| variação | **+24%** | **+443%** | +126% | |

**86% de todo o crescimento dos 6 grupos foi para a Shopee.** Eles ultrapassaram o MELI em **fev/26** e em jun/26 faturam **141% do que faturam aqui**.

**Electrolux — o caso emblemático:** MELI **41,3 → 38,9 (−6%)** enquanto Shopee **0 → 52,3** (abriu loja oficial em ago/25). Total do grupo **+121%**, e **105% desse crescimento foi para a Shopee** (mais que todo, porque o MELI encolheu). Ela saiu de **100% MELI para 57% Shopee em 11 meses**.
> Aquele "−5% YoY" que eu tratei como estagnação é **substituição de canal em curso**. Não é um seller fraco; é um seller cujo crescimento inteiro perdemos.

**Concentração:** os 6 grupos passaram de **24%** (jul/25) para **57,3%** (jun/26) de tudo que a Shopee fatura em Large. **Mais da metade do Large da Shopee são os sellers que estamos cotando.** A seleção estava certa por uma razão maior do que parecia.

**Engage — a prova reversa:** cresceu **+106% no MELI** (3,4 → 7,0) enquanto ficou flat na Shopee. É o único caso de migração na nossa direção — demonstra que a alavanca funciona.

### Dimensionamento da substituição (base: 105,9 Mi/mês na Shopee em jun/26)
| recuperar | Shopee recuperada/mês | 6 meses | equivalente incremental (×3,27) | ratio de Large |
|---|---|---|---|---|
| **20%** | 21,2 | 127 | **415** | 44,1% → **39,7%** (−4,4 pp) |
| **30%** | 31,8 | 191 | **623** | 44,1% → **37,6%** (−6,5 pp) |
| **50%** | 53,0 | 318 | **1.039** | 44,1% → **33,6%** (−10,4 pp) |

**Recuperar 50% do que os 6 grupos vendem na Shopee levaria o ratio a 33,6% — praticamente congelando no nível de hoje (33,1%).** A substituição sozinha neutralizaria toda a deterioração projetada. É de longe a alavanca mais potente do BC.

### Notas metodológicas travadas
- **Duas fontes, dois papéis (decisão da Beatriz):** **Yipit** (`DM_YIPIT_SHOPEE_ITEMS`) para **composição por loja** · **Planning** (`DM_MARKET_ASP`) para **nível de mercado**. Metodologias diferentes, **não reconciliam** — não somar nem dividir entre elas.
- **Defasagem:** Yipit fecha em **jun/26**; DM Eficiência já tem **jul/26**. ⚠️ *Erro que cometi e corrigi: minha primeira janela "mai-jul/26" no Yipit somou só mai+jun (2 meses) e comparei contra 3 meses de 2025, inflando os YoY. Sempre conferir a última competência disponível na fonte.*
- **De-para de loja Shopee → grupo econômico, confirmado pela Beatriz:** Electrolux→ELECTROLUX · Belmicro Oficial→3 GREEN · Webcontinental (×3)→INFOAR · ENGAGE-ELETRO→ENGAGE · Philco+Britânia Oficial→PHILCO/BRITANIA · REDE|marketplace→OUTLET DAS FABRICAS.
- **O que o quadro NÃO prova:** causalidade. A correlação temporal é forte, mas parte do crescimento lá pode ser demanda nova. Por isso a substituição entra como **cenário** (20/30/50%), não como previsão.

### Query base da Shopee (ajustada da original da Beatriz)
Nível **item→loja**: classifica a faixa de ASP no item (`NMV/NSI`) e depois agrega por loja e mês, preservando a atribuição de faixa. Filtros: `VERTICAL_CATEGORIZADOR='HOME ELECTRONICS'`, `D1_CATEGORIZADOR_D1='LARGE APPLIANCES'`. Custo baixo (~0,3-0,9 GB) — muito mais barato que o DM Eficiência.

---

## 10.18 ⭐ AS 3 D1s CONSOLIDADAS — regra única de catch-up [21/08] · `consolidado_d1s.html` (Grid v8, aba 2)

### Régua adotada (decisão da Beatriz, 21/08): **cada bloco cresce como a própria D1 cresce**
Referência = crescimento da D1 (jul/26 vs jul/25): **Large +54,6% · Small +43,9% · H&C +19,1%**.
Bloco que cresce **abaixo** entra com o valor para chegar lá; bloco que já cresce **acima não entra** (não há atraso a recuperar).
**Por que não "ritmo da carteira"** (a régua anterior): em H&C a Carteira Assessorada **encolhe 7,4%** — usá-la como referência seria pedir que os sellers encolhessem.

### Composição por segmento (H2'25 e YoY de julho)
| D1 | 1P | Carteira Assessorada | Seller Dev |
|---|---|---|---|
| LARGE | 920 · **+64,4%** | 1.634 · **+57,7%** | 301 · **+16,8%** 🔴 |
| SMALL | 598 · +47,0% | 696 · **+54,8%** | **976** · **+36,3%** 🔴 |
| H&C | 93 · +19,6% | **1.173** · **−7,4%** 🔴🔴 | 428 · **+75,2%** |

**H&C está invertida:** o segmento que mais controlamos (CA, 69% da D1) **encolhe**, e a cauda longa é o que cresce. Excluindo os grupos do BC, **o resto da CA de H&C cai −21,4%**.

### Cascata das camadas (perímetro-foco, R$ Mi)
| bloco | controlabilidade | LARGE | SMALL | H&C | **TOTAL** |
|---|---|---|---|---|---|
| **BC — grupos cotados** | alta, negociada | 208 | 23 | 65 | **296** |
| **Resto da Carteira Assessorada** | alta, gestão diária | 0 | 0 | **314** | **314** |
| **Seller Dev (fatia móvel)** | **baixa** | 112 | 57 | 0 | **169** |
| **1P** | média | 0 | 0 | 0 | **0** |
| **TOTAL a recuperar** | | **320** | **80** | **379** | **779** |

**🔑 A maior alavanca de todo o HE não está em Large: é o resto da Carteira Assessorada de H&C (+314 Mi)** — nosso próprio portfólio gerido, encolhendo 21%. É alta controlabilidade e ninguém estava olhando.
**1P não entra em nenhuma D1:** cresce acima da referência nas três (+64,4% / +47,0% / +19,6%). Encerra a hipótese "acionar 1P" com dado.

### Efeito no ratio
| D1 | Shopee | baseline | com camadas | ratio s/ ação | com camadas | evita |
|---|---|---|---|---|---|---|
| LARGE | 1.792 | 4.066 | 4.386 | 44,1% | **40,9%** | 3,2 pp |
| SMALL | 785 | 2.267 | 2.347 | 34,6% | **33,4%** | 1,2 pp |
| H&C | 1.081 | 2.360 | 2.739 | 45,8% | **39,5%** | **6,3 pp** |
| **TOTAL HE** | **3.658** | **8.693** | **9.472** | **42,1%** | **38,6%** | **3,5 pp** |

### 🚩 RISCO ABERTO — o baseline de H&C provavelmente está otimista
A projeção top-down dá **2.360 Mi** para H&C (+53% YoY), mas o **bottom-up dos segmentos aos próprios ritmos dá só 1.700 Mi (+10%)** — diferença de **39%**. Se o bottom-up estiver certo, o ratio de H&C sem ação não é 45,8% e sim **~63%**. Causa provável: a instabilidade de tendência de H&C já documentada (viés de +51% no backtest, célula 500-1500 com degrau, mercado parado). **Recomendação: revisar o baseline de H&C para o bottom-up antes de fechar o BC.** Alerta embutido no painel.

### Nota de mudança de enquadramento
A camada "BAU mais forte = não desacelerar" (+380 em Large) **saiu**. Ela vinha de comparar top-down vs bottom-up — um artefato de modelagem, não uma regra de negócio. Substituída pelo catch-up do "Resto da CA", que é medido e acionável. O total de Large caiu de 696 para 320 Mi: **mais conservador e mais defensável**.

### Armadilha técnica recorrente (3 ocorrências nesta sessão)
**PowerShell não diferencia maiúsculas em nomes de variável.** Colisões que causaram bugs silenciosos: `$n` × `$N` (contador × parâmetro), `$sS` × `$SS` (série × sazonal), `$h2` × `$H2` (soma × array de meses — este destruiu o array e zerou os resultados). **Regra: nunca usar nomes que difiram só por caixa.** Também: `continue` em `foreach` aninhado pode escapar os dois loops — preferir `if`.

---

## 11.5 Estrutura narrativa do Grid — [DEFINIDO 20/08]
**Princípio:** o Grid é **simulador E apresentação**. Toda premissa que sustenta uma escolha precisa estar **evidenciada com o dado ao lado** — não afirmada. Cada bloco leva uma legenda curta de "o que isso mostra". A história tem que seguir um fluxo coerente, do diagnóstico à decisão.

**Aba 1 · Diagnóstico** *(o problema, em evidências)*
1. Evolutivo Shopee × MELI (colunas + YoY + ratio na barra + tabela transposta) — *já publicado*
2. **Onde perdemos mais em amount** — matriz D1 × faixa (SOB MELI, ratio, Δpp, Δ R$) com faixas-foco destacadas (§2.1)
3. **Como ela cresce** — YoY por D1 (§8.4) + decomposição **preço vs volume** (ASP intra-faixa e SI vs GMV, §8.3)
4. **Sazonalidade** — tabela das **14 categorias** (degrau de BF vs consolidação, §8.5) + perfil de Q4 dela vs MELI

**Aba 2 · Forecast & Simulador**
4b. **Gráfico contínuo realizado → projetado** (decisão da Beatriz, 20/08): mesmo combo da aba 1, **estendido** com os meses de forecast. Convenções: barras do forecast com **hachura/opacidade reduzida**, **linha vertical divisória** marcando "último dado real (jun/26)", linhas de YoY **tracejadas** no trecho projetado, e **faixa de incerteza sombreada** (a banda de §10.8-D). O forecast **não deve ter o mesmo peso visual** do realizado. Bônus: quando jul/26 chegar, sobrepor **previsto vs realizado** nesses meses — é o argumento de credibilidade mais forte do material.
5. O motor e as 2 fórmulas explicadas em linguagem simples (§6.1 e §6.2)
6. **φ medido por D1 × faixa** + **backtest (MAPE/WAPE)** declarado
7. **Joystick 3 dials** (φ · BF · ambição MELI) → incremental necessário (R$), ratio/share resultante, selo de viabilidade
8. Decomposição **BAU vs BC**, com potencial de **1P** avaliado antes

**Aba 3 · Premissas & Método**
9. Todas as premissas em lista auditável · fragilidades declaradas (base estimada, cesta não-fixa/migração, célula H&C 500-1500, lag de 2 meses, assimetria jul-ago) · fontes · **validação GMV×NMV (0,1%)**

---

## 12. ONDE PARAMOS — retomada (pausa em 19/08/2026)

### Fechado e documentado
Escopo · métricas · validação GMV×NMV (0,1%) · motor do forecast (§6) · cenários/joystick (§7) · 3 checks de integridade (§8) · **faixas-foco com critério objetivo (§2.1)** · **debate da BF resolvido como dial (§8.5)** · φ preliminar por D1 (§8.4) · aba 1 do dashboard publicada no Grid.

### Próximos passos (na ordem)
1. **φ por D1 × faixa-foco** — agora viável: só as ~13 faixas do perímetro, não as 33. (Beatriz pediu explicitamente φ também por ASP.)
2. **Backtest** — ajustar até dez/25, projetar jan–jun/26 contra o real, medir **MAPE** por D1/faixa. Número vai declarado no material da liderança.
3. **Aba 2 do Grid — forecast com joystick de 3 dials:**
   - **Dial A — φ (trajetória Shopee):** desacelera · mantém · acelera (por D1)
   - **Dial B — BF da Shopee:** perfil próprio (~+20%) · intermediário · sazonalidade do mercado (~+50-60%)
   - **Dial C — ambição MELI:** inércia/baseline · conter o ratio · reduzir o ratio em X pp
   - Saída por D1 × faixa: **GMV incremental necessário (R$)**, ratio/share resultante, **selo de viabilidade** (vs. maior crescimento já entregue na faixa)
4. **Decompor o incremental** em **BAU** vs **BC**, avaliando antes o **potencial do 1P**.
5. **Validar capacidade de sellers** com os cubos do Shield (`seller_cap_cube`, `grupos_economicos`): quanto fazem/mês na faixa, qual crescimento seria exigido; se muito acima do histórico → BC precisa de mais sellers.
6. **Consolidação no Grid do Shield por ASP** (doc `01KXKJP50WAQ314W1MVQXD4SRZ`) — opções: docs separados com link (recomendado, o do Shield tem ~31 MB), HTML mestre com iframes, ou mesma pasta.
7. **Eficiência do investimento** (R$ investido por R$ incremental) — input do time de **farming**, não output nosso.

### Como executar (ambiente)
- BigQuery: acesso ao `SBOX_MKPBR` **liberado** (após `gcloud auth login`). Rodar via **bq CLI** (`--format=csv`, query em 1 linha, sem acento em literal para evitar mojibake) ou MCP `bigquery-insight`.
- Google Sheets/Docs: exige `create_meli_session` + aprovar a URL do iam-token-vault no browser.
- Grid: engine via `curl` (`skill_version` obrigatório); doc da aba 1 = `01M0DSBDBHEAV3650Q913YSP6Y`.
- Regenerar o dashboard: query parametrizada por data + script gerador (injeta JSON no template via PowerShell). Fontes em `dashboard_evolutivo_shopee_template.html`.

---

## 13. FECHAMENTO DA SESSÃO (21/08/2026) — o que virou estado, o que foi deprecado

> **§12 acima está encerrado.** A partir daqui, a fonte da verdade do que vale é
> **`ESTADO_DO_BC.md`** (mesma pasta). Este arquivo passa a ser **trilha de auditoria**:
> guarda o histórico, as correções e os caminhos que testamos e abandonamos.

### 13.1 Grid v9 — as três decisões implementadas

Publicado em `01M0DSBDBHEAV3650Q913YSP6Y` (v9). Cada D1 passou a ter **tratamento próprio**,
declarado na tela (linha "Tratamento") em vez de um método único aplicado às três:

| D1 | tratamento | jul-dez/26 |
|---|---|---|
| LARGE | projeção do motor combo, como estava | 44,1% → 40,9% com camadas |
| SMALL | **refeita** com o YoY realizado de H1'26 (MELI ×1,34 · Shopee ×1,97) | 28,7% → 27,8% |
| H&C | **projeção anulada** (`proj:false`, forecast = `null` na série) | banda 45-70% → 38-60% |

Implementação: flag `proj:true/false` por D1 no `META`; chip "Large + Small" para a soma
das duas quantificadas; bloco de evidência de 5 fatos em H&C; **banner de sazonalidade em
Small** ("o alívio de H2 não é vitória, é sazonalidade").

### 13.2 Caminhos deprecados — não retomar

1. **Motor v1 puro** (só YoY sobre o mês do ano anterior) — subestimava ~11% no backtest.
   Sobrevive apenas como uma das duas metades do combo.
2. **Motor v2 puro** (decomposição multiplicativa) — superestimava ~13%. Idem.
3. **φ estimado por D1 × faixa de ASP** — rejeitado empiricamente: com ~13 faixas-foco o
   ruído por célula superou o ganho. φ = 0,9 global.
4. **Projeção de ratio para H&C** — 4 métodos deram 42% / 46% / 52% / 77%. Dispersão dessa
   ordem não é margem de erro. Substituído por banda + evidência de seller.
5. **Baseline recomposto de H&C** (somar as faixas-foco recompostas) — inflava o MELI
   (+53% vs +24% real) e suprimia a Shopee (+183% vs +454% real); os dois erros empurravam
   o ratio para baixo, subdimensionando a ameaça em ~31 pp.
6. **Fator agregado de 77% para H&C** — contaminado pelo degrau de out/25.
7. **"Outubro é o pico da Shopee em H&C (1,65)"** — ARTEFATO. O degrau de out/25 foi
   absorvido pelo índice sazonal. Índice limpo: **1,37** dentro do perímetro, 1,09 fora.
8. **Classificação atacar/proteger vinda do print** — era arbitrária (preenchimento manual).
   Substituída por regra derivada do dado: Shopee > MELI ⇒ atacar.
9. **Ritmo da carteira como referência das camadas** — em H&C a carteira encolhe 7,4%;
   seria pedir que os sellers encolhessem. Substituído por **ritmo da própria D1**.
10. **Aba 5 (Simulador/joystick)** — mantida no doc como **anexo metodológico**, mas
    **fora da apresentação**. Motivo: "não gostei, não tá claro, tá bem confuso" — não dava
    para ver por mês, evolutivo, projetado.
11. **Hipótese "1P é alavanca"** — encerrada com dado: cresce acima da referência nas três D1s.

### 13.3 Erros meus, registrados

- **Afirmei acesso ao SBOX antes de testar** (metadata do MCP ≠ permissão de leitura).
  Regra: só declarar acesso depois de um `SELECT` que retorna linha.
- **Janela do Yipit**: comparei mai+jun/26 (base fecha em jun) contra 3 meses de 2025 —
  inflou todos os YoY. "Engage −39% na Shopee" era artefato; ela está flat.
- **Fórmula da substituição**: publiquei 2,27x; o correto é **3,27x** (2,27 é só retirar da
  Shopee — a substituição também **adiciona** ao MELI).
- **Taxas de crescimento publicadas com N=6** enquanto o motor rodava com N=3 (L3M).
- **Validação de julho citada como 0,13%** — a faixa real é **−0,9% a +1,0%**; eu havia
  escolhido o ponto mais favorável.
- **"Erro de −5,2% em Small"** era ininteligível: comparava a projeção de 5 das 11 faixas
  contra uma *estimativa* (514 × 77%), não contra o realizado de 514 Mi.

### 13.4 Regra travada de comunicação (origem: crítica de 20/08)

Nada de jargão sem tradução na tela · unidade em todo cabeçalho · período explícito em toda
referência · referência histórica sempre ao lado do alvo · glossário na página · evolutivo
mensal é peça central, não anexo · quadro sempre com **colunas = histórico + projeção** e
**linhas = KPIs** (faturamento, MoM, YoY de Shopee e MELI, ratio).

---

## 14. Grid v10 (21/08/2026) — agregação dos blocos e medição do perímetro

### 14.1 Pergunta da Beatriz: de onde vem o ratio de 35,5% em Small (Q2'26)?

Resposta verificada em query (`job mcp_job_bb74897b`, 10,7 MB, US$ 0,00005):
soma de **abr+mai+jun/26** nas **faixas-foco de Small** (120-150, 150-200, 200-500, 500-1500, +3000)
= MELI **1.029,2** · Shopee **365,7** → **35,53%**. Bate com o `d1cons2.json` do painel.

**Ela não reconhecia o número porque ele não é o de Small — é o do perímetro.**
Na **D1 cheia** (11 faixas): MELI **1.341,3** · Shopee **591,6** → **44,11%**.

**Medição do efeito do perímetro (Q2'26, ratio faixas-foco vs D1 cheia):**

| D1 | faixas-foco | D1 cheia | distorção |
|---|---|---|---|
| LARGE | 29,56% | 30,02% | +0,5 pp |
| H&C | 47,75% | 48,21% | +0,5 pp |
| **SMALL** | **35,53%** | **44,11%** | **+8,6 pp** 🔴 |

**Correção do que eu havia escrito antes:** a limitação estava enunciada como "cobertura do
perímetro" (98,7% / 87,3% / 77,1% do MELI). Cobertura baixa **não implica** ratio distorcido —
o que importa é se ela é **proporcional entre os dois lados**. Em H&C a cobertura é baixa (87%)
mas o ratio quase não muda. **O problema é só de Small**, e o número certo é **8,6 pp**, não "~9 pp
contra 40,3%" (aquele 40,3% vinha de outra janela).

**Causa:** as faixas excluídas de Small são exatamente as que a Shopee domina —
até 19 (ratio 1.053%) · 19-49 (148%) · 49-79 (199%) · 79-100 (62%) · 100-120 (74%).
O critério de faixa-foco exigia **SOB MELI ≥5%**, e em Small a Shopee vive onde nosso SOB é pequeno.
O filtro removeu o pior do quadro.

**Recomendação registrada (aguardando decisão):** virar o headline das três D1s para **D1 cheia**.
Large e H&C não mudam (meio ponto), Small é corrigida, e o conceito "perímetro" sai da apresentação.
A faixa de ASP permanece como eixo de **alocação** do incremental. Exige re-rodar a projeção de Small
sobre a série cheia (H2'25 cheio = **29,2%**, não 19,5%).

### 14.2 Agregação dos blocos — "Demais segmentos — BAU"

Pedido dela: juntar Resto da Carteira + Seller Dev + 1P em um bloco único, **sem dar direção**
de quem entrega. Motivo declarado: *"não quero assumir que carteira não vai poder colaborar
porque já cresce mais que a média da categoria, e nem 1P."*

**Armadilha evitada — não recalcular o gap sobre o bloco agregado.** O crescimento ponderado
dos três em Large é `(1195×0,688 + 301×0,168 + 920×0,644)/2416` = **60,7%**, acima da referência
de 54,6% → o gap viraria **zero** e o total de Large cairia de **320 para 208**. Isso é o oposto
da intenção dela. O total continua vindo da **soma dos gaps medidos por segmento**; a agregação
é **só de apresentação**.

| bloco | LARGE | SMALL | H&C | TOTAL |
|---|---|---|---|---|
| BC — grupos cotados | 208 | 23 | 65 | **296** |
| Demais segmentos — BAU | 112 | 57 | 314 | **483** |
| **TOTAL** | **320** | **80** | **379** | **779** |

Os totais publicados na v9 **não mudaram**.

### 14.3 O que mudou na aba 2 (v10)

- tabela de camadas → **"Quanto precisamos recuperar — e onde isso está hoje"**, 2 blocos,
  colunas `Base H2'25` · `Referência (ritmo da D1)` · `Gap medido` · `Como será endereçado`
- nota explícita: *"o gap fora dos grupos cotados não está alocado… é decisão do time,
  não premissa do modelo"*
- **nova tabela de diagnóstico** por segmento (1P / Carteira Assessorada total / Seller Dev)
  com H2'25, % da D1, YoY de julho e delta vs ritmo da D1 — **informativa, não aloca nada**.
  Oculta no chip "Large + Small" (somar segmentos de D1s com referências diferentes não faz sentido).
  Rodapé declara que a fonte é o **DM Eficiência (D1 cheia, NMV)** e o gráfico é o **Planning
  (faixas-foco, GMV)** — níveis não idênticos (Large 2.855 vs 2.817 · Small 2.270 vs 1.789).
- gráfico e quadro de KPIs: as barras `Resto CA` e `Seller Dev` viraram **uma só**, `Demais segmentos — BAU`
- limitação nº 3 reescrita com a medição de §14.1
- decimais com vírgula no "evita X pp" e YoY do diagnóstico com uma casa

Build: base64 da aba 2 substituído dentro do `var SRC=[...]` de `grid_v9.html` (as outras 4 abas
preservadas byte a byte e reconferidas por `<title>`), gravado como `grid_v10.html` e subido com
`if_version:9` → **v10**.

---

## 15. Grid v11 (21/08/2026) — **virada para D1 CHEIA** em todo o BC

### 15.1 A decisão

Beatriz, textual: *"tudo tem que ser na D1, sem premissas de olhar só as faixas mais relevantes e
depois ter que explicar. os numeros macro precisam bater com os numeros dos documentos oficiais.
por favor, retorne para TOTAL D1, sem quebrar nenhum asp."*

**Regra travada:** todo número de capa é **D1 cheia**. A faixa de ASP continua no BC, mas **só como
eixo de alocação** do incremental (aba 1) — nunca para compor o headline.

### 15.2 A prova de que fecha com o oficial

MELI, semestre jul-dez/25, Planning (D1 cheia) × DM Eficiência (soma dos segmentos):

| D1 | Planning | DM Eficiência | gap |
|---|---|---|---|
| LARGE | 2.852,0 | 2.855 | **0,1%** |
| SMALL | 2.273,7 | 2.270 | **0,2%** |
| H&C | 1.693,5 | 1.694 | **0,03%** |

No perímetro isso **não fechava**: Small dava 1.789 contra 2.270 — 27%.

E a checagem de julho/26 confirma pelo outro lado: o realizado de Small em D1 cheia dá **513,8 Mi**,
que é o **514 Mi** que ela já conhecia do relatório oficial.

### 15.3 Motor re-rodado — `motor_d1_cheia.ps1`

Novo script na pasta do projeto. Mesmos parâmetros do anterior (combo v1+v2, φ=0,9, nível L3M, Njan=3),
sem filtro de faixa. **A série mensal está congelada dentro do .ps1** (job `mcp_job_4757fcaf`) para não
depender do bq CLI. Fonte: `SBOX_MKPBR.DM_MARKET_ASP_MONTHLY_VERTICAL_D1`, jan/23–jun/26.

**Checagem de julho/26 (1 passo à frente, MELI):**

| D1 | jul/25 Planning | cresc. DM | jul/26 realizado | jul/26 projetado | erro |
|---|---|---|---|---|---|
| LARGE | 414,8 | +54,6% | 641,3 | 642,4 | **+0,17%** |
| SMALL | 357,1 | +43,9% | 513,8 | 496,8 | **−3,31%** |
| H&C | 185,6 | +19,1% | 221,1 | 224,8 | **+1,69%** |

**Ratios em D1 cheia:**

| D1 | H2'25 | Q2'26 | jul-dez/26 projetado | com camadas |
|---|---|---|---|---|
| LARGE | 20,7% | 30,0% | **42,7%** | 39,7% (−3,1 pp) |
| SMALL | 29,2% | 44,1% | **45,2%** | 44,0% (−1,2 pp) |
| H&C | 27,3% | 48,2% | 66,7% → **banda 45-70%** | 38-60% |
| Large+Small | 24,5% | 36,2% | 43,8% | 41,4% (−2,3 pp) |

### 15.4 Dois achados da virada

**(a) O "alívio sazonal" de Small era artefato do perímetro.** Na v10 o ratio de Small caía de 35,5%
para 28,7% no semestre e era preciso explicar em banner que aquilo era sazonalidade, não vitória.
**Em D1 cheia a queda não existe:** 44,1% → 45,2%, estável. O banner foi removido — não há nada a
explicar. Causa: a faixa 200-500, muito favorável a nós em H2, dominava o perímetro de Small.

**(b) A média de previsões deixou de cancelar viés.** No perímetro, v1 subestimava 11% e v2
superestimava 13% → combo +0,9% (o argumento Bates & Granger). **Em D1 cheia as duas erram para o
mesmo lado:**

| D1 | viés v1 | viés v2 | viés combo |
|---|---|---|---|
| LARGE | −13,4% | −14,8% | **−14,1%** |
| SMALL | −27,6% | −39,8% | **−33,7%** |
| H&C | −11,2% | +29,7% | +9,2% |

Ou seja: **o motor subestima a Shopee em D1 cheia.** Mantivemos o combo (uma regra só para todas,
validada out-of-sample em julho com +0,17% em Large) e **declaramos o viés no painel**: os ratios
projetados são o **piso**, não o teto. Na direção de um BC isso é conservador — não há como acusar o
número de estar inflado. *Não* fizemos seleção de modelo por D1 (v2 puro seria melhor em Large,
v1 puro em Small) para não trocar simplicidade por 2-3 pontos de MAPE.

### 15.5 Janela acionável: 4 meses, não 6

Beatriz: *"não podemos estimar 6 meses. tem 6 meses pendentes na base shopee. mas de dias acionaveis
temos apenas setembro, outubro, novembro e dezembro. o resto é mes que ainda não auditamos, mas ja
passou."*

A base da Shopee fecha em jun/26, então jul-dez/26 aparece inteiro como pendente — mas **jul e ago já
passaram**. Os cenários de recuperação da aba 3 passaram a ser dimensionados em **set-dez/26 (4 meses)**,
com nota explícita na tela. O ratio de referência dessa janela é **44,5%** em Large (não os 42,7% do
semestre) — declarado no rodapé da tabela.

### 15.6 Aba 3 (migração) — números soltos corrigidos

Crítica dela: *"aqui é um exemplo perfeito disso. na aba migração dos sellers voce bota numeros soltos,
% soltos. isso não é executivo."* Os cards mostravam `65 → 83` com `28%` embaixo, sem unidade, sem
período e sem dizer o que o percentual era. E o último card dizia `84%` / `parcial`.

Reescritos com unidade, período e leitura em português. O card de crescimento passou de "84% · parcial"
para: **"o grupo cresceu 110 Mi/mês — 92 Mi disso foi na Shopee e 18 Mi com a gente"**. Em Electrolux:
**"o grupo cresceu 50 Mi/mês — 52 Mi disso foi na Shopee e −2 Mi com a gente"**.

E o "Oportunidade se recuperar 30%" — que ela pediu para explicar — virou coluna autoexplicativa
(**"Se trouxéssemos 30% do que ele vende lá (R$ Mi/mês)"**) mais uma legenda dinâmica: *"hoje esse grupo
fatura X Mi/mês na Shopee (jun/26); se 20% disso passasse a ser vendido com a gente, entrariam Y Mi por
mês — Z Mi nos quatro meses acionáveis."* A leitura que ela deduziu estava certa.

### 15.7 Período do gap — a lacuna que ela apontou

Crítica: *"nessa parte, quanto falta em R$ voce se refere em qual periodo? de novo voce ta dando numeros
sem dizer em quanto tempo isso tem que ser realizado, ou qual o periodo base."*

O gap é **do semestre jul-dez/26 inteiro**, com base de comparação em **jul-dez/25**. Fórmula agora
escrita na tela: `base H2'25 × (referência − crescimento próprio do bloco)`. A tabela ganhou cabeçalhos
"Faturou em jul-dez/25" e "Gap no semestre jul-dez/26", e o rodapé mostra a média mensal
(Large ≈ 53 · Small ≈ 13 · H&C ≈ 63 Mi/mês). Os totais **não mudaram** (320 / 80 / 379).

### 15.8 Estado das 5 abas na v11

| aba | estado |
|---|---|
| 1 · Diagnóstico por faixa | **inalterada** — já tinha as 11 faixas e abre com todas marcadas, então o default dela já era D1 cheia. É a visão de alocação. |
| 2 · D1s consolidadas | **refeita em D1 cheia** |
| 3 · Migração dos sellers | cards reescritos, janela 4 meses, `PROJ` em D1 cheia (set-dez/26) |
| 4 · Realizado × Projetado | **série trocada para D1 cheia**, título ajustado |
| 5 · Simulador | **banner vermelho de depreciação** — construída no perímetro, valores não coincidem com as abas 1-4. Mantida como registro do método (não apagada, sem aprovação para isso). |

### 15.9 Deprecado nesta virada

- **Todo o conceito de "faixas-foco" como perímetro de headline** e o critério que o gerava (SOB MELI ≥5%
  E [ratio ≥15% ou Δ≥+4pp]). Sobrevive só como critério de priorização dentro da aba 1.
- **A projeção de Small "corrigida com YoY realizado"** (28,7%) — era correção de um artefato do perímetro.
- **O banner de sazonalidade de Small** — o fenômeno não existe em D1 cheia.
- **O argumento Bates & Granger como justificativa do combo** — não vale em D1 cheia (§15.4b). O combo
  continua, mas justificado por *simplicidade + validação out-of-sample*, não por cancelamento de viés.
- **3,27x** de eficiência de substituição em Large → **3,34x** em D1 cheia.

---

## 16. Grid v12 (21/08/2026) — aba 5 removida e seleção múltipla de sellers

### 16.1 Aba 5 (Simulador) apagada

Aprovação explícita da Beatriz: *"pode apagar a aba 5."* Motivo: foi construída sobre as faixas-foco
e os valores deixaram de coincidir com as abas 1-4 depois da virada para D1 cheia (§15).

**Não se perdeu nada:** o método está descrito na §7 deste documento e o HTML original continua na
pasta do projeto como `simulador_desafio.html`. O que saiu foi a aba do Grid.

O shell foi **reescrito para 4 abas** (antes tinha 5 botões, 5 iframes, `SRC` de 5 posições e loops
com `5` fixo). Agora usa `var N=4` e o loop é derivado de `N`, para a próxima remoção/adição não
exigir caçar números mágicos. Os payloads das abas 1, 2 e 4 foram reaproveitados **byte a byte** da
v11 (base64 extraído e reinserido, conferido por `<title>`).

Doc caiu de 246,3 KB para 211,5 KB.

### 16.2 Seleção múltipla de grupos na aba 3

Pedido: *"queria que voce adicionasse seleção multipla dos sellers na aba sellers... o botão todos
deve permanecer, mas ele não é suficiente."*

**Antes:** `selG` era uma string; `'TODOS'` somava tudo, qualquer outro valor mostrava **um** grupo.
**Agora:** `selG` é um `Set`. **Conjunto vazio = Todos** — assim o estado inicial e o botão "Todos"
usam o mesmo caminho de código, sem caso especial.

- chip **"Todos (10)"** limpa o conjunto
- cada chip de grupo **alterna** (marcado ganha `✓` e destaque)
- chip **"limpar seleção"** aparece só quando há algo marcado
- **clicar em qualquer linha do ranking** também alterna o grupo (a linha marcada fica com fundo
  amarelo e barra lateral) — o ranking virou seletor, não só leitura
- ao **trocar de D1**, grupos que não existem na nova categoria são descartados do conjunto
- o texto de apoio se adapta: *"Somando 2 de 10 grupos: ELECTROLUX · 3 GREEN"*, e a legenda dos
  cenários passa a dizer *"os 2 grupos marcados faturam X Mi/mês"* com a concordância certa

`serie()` perdeu o parâmetro de grupo (lê `listaSel(d)` direto) e unificou os dois caminhos: soma os
valores não nulos dos grupos selecionados, devolve 0 quando nenhum tem valor no mês, e **sempre `null`
para Shopee em jul/26** (Yipit fecha em jun/26) — antes essa regra existia só no caminho de grupo único.

**Conferência:** Electrolux sozinha = 52,3 Mi/mês na Shopee (jun/26); somando 3 GREEN = 82,9;
MELI 38,9 → 51,8. Soma, não substitui. "Todos" volta para 115,2 / 82,5.

### 16.3 Armadilha de teste registrada

Ao verificar pelo browser, meu matcher de chip usava `/lux/` minúsculo contra o texto `ELECTROLUX` —
não casou, os passos do teste foram silenciosamente pulados e o resultado *pareceu* válido (só faltavam
chaves no objeto). **Ao testar chips por texto, usar regex com flag `i`** e conferir se todas as chaves
esperadas voltaram no resultado.

---

## 17. CORREÇÃO IMPORTANTE (21/08/2026) — Yipit e Planning são a MESMA fonte

### 17.1 O que eu afirmei errado durante toda a análise

Repeti em vários lugares — nas notas metodológicas da aba 3, na §8 do `ESTADO_DO_BC.md` e
na §11.x deste documento — que:

> *"As duas bases de Shopee (Planning e Yipit) NÃO reconciliam — metodologias diferentes;
> não somar nem dividir entre elas."*

**Isso está errado.** Verificado com query direta (`job mcp_job_bc7185e8`):

`SBOX_MKPBR.DM_MARKET_ASP_MONTHLY_VERTICAL_D1.GMV_SHOPEE`
**==** `WHOWNER.DM_YIPIT_SHOPEE_ITEMS.NMV_LC` agregado por D1 × mês.

| D1 | jan/26 | fev/26 | mar/26 | abr/26 | mai/26 | jun/26 |
|---|---|---|---|---|---|---|
| LARGE | +0,004% | +0,002% | 0,000% | −0,005% | −0,002% | −0,008% |
| SMALL | +0,079% | +0,025% | +0,006% | −0,044% | −0,127% | −0,153% |
| TVs | +0,004% | +0,053% | +0,003% | +0,058% | 0,000% | −0,035% |

18 combinações testadas, **erro máximo de 0,15%**. E no Planning `GMV_SHOPEE` == `NMV_SHOPEE`
(idênticos ao centavo) — para a Shopee aquela base não tem distinção bruto/líquido.

A própria descrição da tabela Yipit já dizia: *"Source: Planning MLB"* e *"GMV_OBSERVED_LC
renamed to NMV_LC"*. Eu não li.

### 17.2 O que isso libera

1. **É válido dividir Yipit por Planning.** Portanto a afirmação *"os grupos cotados são 62,4%
   de tudo que a Shopee fatura em Large (jun/26)"* — que eu havia marcado como *a verificar* na
   auditoria (§2.9 de `AUDITORIA_21ago.md`) — **é legítima**. `115,2 / 184,65 = 62,4%`.
   *(O 57,3% que aparece em textos anteriores era com os 6 grupos originais; com os 10 é 62,4%.)*
2. **Cai uma limitação declarada** do material. Uma ressalva menos para explicar na liderança.
3. **Dá uma métrica nova e forte para a aba 3:** o *share do grupo dentro da Shopee daquela D1*.
   É o número que mostra concentração — e em TVs ele é brutal (ver §17.4).
4. **O Yipit pode substituir o Planning** para o lado Shopee quando se quer nível de loja e
   nível de D1 na mesma query, sem defasagem entre as duas.

**A defasagem continua real e não muda:** Yipit/Planning fecham em **jun/26**, o DM Eficiência
tem **jul/26**. Isso é sobre competência disponível, não sobre metodologia.

### 17.3 Onde corrigir
- nota metodológica da aba 3 no Grid (texto "não reconciliam")
- `ESTADO_DO_BC.md` §8 (tabela de fontes) e §9 (limitações)
- `AUDITORIA_21ago.md` §2.9 → resolvido, é legítimo

### 17.4 Ranking de lojas Shopee em TVs e Áudio (para replicação por outro time)

Pedido: replicar a aba 3 para TVs e Áudio. Rodei o ranking (`job mcp_job_0c2dc43d`).
Queries completas em `queries_replicar_aba_sellers.sql`.

**TELEVISIONS & STREAMING DEVICES** — Shopee mai+jun/26 = **257,7 Mi**. Concentração extrema:

| # | loja | mai+jun/26 (Mi) | SoB da D1 | acum. | grupo já mapeado? |
|---|---|---|---|---|---|
| 1 | **Shop.EV** | **121,4** | **47,1%** | 47,1% | ✅ SHOP EV (KILL) |
| 2 | Philco Oficial | 25,2 | 9,8% | 56,9% | ✅ PHILCO/BRITANIA |
| 3 | Mercado Fácil | 19,4 | 7,5% | 64,4% | ❓ |
| 4 | TNTinfoLoja | 10,3 | 4,0% | 68,4% | ❓ |
| 5 | REP Store | 9,5 | 3,7% | 72,1% | ❓ |
| 6 | Belmicro Oficial | 7,4 | 2,9% | 74,9% | ✅ 3 GREEN |

**Uma loja é metade da categoria.** Três das seis maiores já estão no de-para de HE.
⚠️ Philco Oficial tem 25,2 Mi em mai+jun mas **0,0 em jun/26** — tudo em maio. Ou parou de
vender ou é falha de coleta; conferir antes de usar.

**AUDIO & GENERAL ELECTRONICS** — Shopee mai+jun/26 = **142,0 Mi**. Fragmentada (3.334 lojas):

| # | loja | mai+jun/26 (Mi) | SoB da D1 | acum. |
|---|---|---|---|---|
| 1 | REP Store | 16,9 | 11,9% | 11,9% |
| 2 | TNTinfoLoja | 8,3 | 5,8% | 17,7% |
| 3 | NegociuN | 7,6 | 5,3% | 23,1% |
| 4 | Outubro_acessoriodelojaonline | 6,9 | 4,9% | 27,9% |
| 5 | mxf36nvesb | 6,1 | 4,3% | 32,3% |
| 7 | Casas Bahia Oficial | 4,4 | 3,1% | 38,9% |

**Top 20 = 59,8% da D1.** Áudio **não** tem o mesmo caso de negociação seller a seller que
Large/TVs têm: aqui é cauda longa. A tese do BC de HE (poucos grupos grandes migrando) **não
se transfere para Áudio** — vale dizer isso ao time antes de eles montarem o material.

### 17.5 Adaptação da Beatriz ao cenário de 30% (adotar)

Ela converteu o amount de "trazer 30%" em **% de uplift sobre o BAU mensal do próprio seller**
(mai+jun/26 ÷ 2) e aplica esse fator a cada mês da meta.

**Por que é melhor que o valor absoluto — e isso é um defeito da minha versão:** R$ 14,9 Mi de
incremental segura o ratio contra uma base de maio/junho, mas **não muda quase nada** contra a
base de novembro, que é muito maior. Em percentual o alvo fica proporcional ao mês.

É o **mesmo problema de sazonalidade** que apareceu (a) no ratio de Small em H2, (b) na
referência de crescimento medida em julho isolado. Terceira aparição do mesmo padrão: **valor
absoluto fixo aplicado a meses de tamanhos muito diferentes**. Vale virar regra do projeto.

---

## 18. TVs e Áudio — preparação da replicação (21/08/2026)

Lado Shopee já puxado (`job mcp_job_0fc45d2f`, série mensal jul/25–jun/26 por `SHOP_ID`, top 12
de cada D1). Falta o de-para `SHOP_ID → CUS_CUST_ID` das lojas novas, que a Beatriz vai mandar.
Query B do `queries_replicar_aba_sellers.sql` reproduz a série em ~0,9 GB.

### 18.1 Contexto de D1 (Planning, D1 cheia) — o que cada categoria é

| D1 | ratio jun/25 | ratio jun/26 | Q2'26 MELI | Q2'26 Shopee | ratio Q2'26 | eficiência da substituição |
|---|---|---|---|---|---|---|
| **TELEVISIONS & STREAMING** | 9,2% | **20,9%** | 1.356,4 | 296,2 | **21,8%** | **5,58x** |
| **AUDIO & GENERAL ELECTRONICS** | 19,8% | **29,0%** | 827,5 | 196,0 | **23,7%** | **5,22x** |

*(Eficiência = `1 + MELI/Shopee` sobre o realizado de Q2'26. Não há projeção para essas D1s — elas
não estão no BC de HE. Na aba 3 o ratio delas entra como "sem projeção", igual a H&C.)*

**A eficiência aqui é quase o dobro de Large (3,3x).** Coerente com a fórmula `1+1/r`: quanto menor
o ratio, mais vale cada real trazido de volta. **Defender TVs agora custa menos do que reagir em
Large depois** — é o melhor argumento disponível para essas duas D1s.

### 18.2 TVs — a Shopee entrou em escala em maio/26

Shopee em TVs, mensal (R$ Mi): jul/25 35,4 · ago 32,5 · set 33,2 · out 39,9 · nov 48,1 · dez 66,5 ·
jan/26 46,9 · fev 59,1 · mar 56,2 · abr **38,3** · mai **152,2** · jun **105,7**.

**O ratio saiu de 8-12% em quase todo 2025 para 21-31% em mai-jun/26.** Não é tendência gradual: é
um degrau. E o degrau tem nome — **Shop.EV**, que foi de 3,1 Mi em abr/26 para **69,6 em mai** e
51,8 em jun. Sozinha, 47,1% da Shopee em TVs.

### 18.3 Áudio — estável por 18 meses, um mês fora da curva

Ratio de Áudio: 19-22% de jan/25 a mai/26, **sem tendência**. Em jun/26 salta para **29,0%**
(Shopee 59,2 → 82,8, +40% MoM).

Cinco das maiores lojas multiplicam por 4-6x **no mesmo mês** de jun/26: REP Store 3,6→13,3 ·
NegociuN 0,9→6,7 · mxf36nvesb 0,85→5,3 · Casas Bahia 0,9→3,5 · UNIVERSO 0,2→2,3.
**O total da D1 confirma o salto**, então não é artefato de uma loja — mas é **um mês só**.
Não construir tese em cima disso antes de ver jul/26. Pode ser campanha (6.6) ou mudança de
cobertura do painel.

### 18.4 Avisos de qualidade de dado (dar ao time antes de eles usarem)

1. 🔴 **Philco Oficial em TVs:** 25,159 Mi em mai/26 e **0,039 em jun/26**, contra 0,005-0,5 nos
   meses anteriores. Um mês isolado com 25 Mi. Conferir antes de citar — pode ser recategorização.
2. 🟠 **Shop.EV em TVs tem buracos** (sem mar/26) e série muito instável: 1,7 → 8,3 → 0,9 → 13,5 →
   (vazio) → 3,1 → 69,6 → 51,8. Usar nível recente, nunca taxa de crescimento.
3. 🟠 **Mercado Fácil em TVs só existe desde abr/26** (0,1 → 15,6 → 3,8). Entrante.
4. 🟢 **Multi Oficial é o caso reverso:** 8,8 Mi/mês em jul/25 → **1,1 em jun/26** (−87%). Ou saiu
   da Shopee ou nós recuperamos. Vale investigar — é o único "ganhamos" da lista.

### 18.5 Recado sobre Áudio (importante para o time que vai replicar)

**A tese do BC de HE não se transfere para Áudio.** Em Large e TVs poucos grupos grandes explicam a
maior parte (Shop.EV sozinha = 47% de TVs). Em Áudio são **3.334 lojas**, o top 20 dá 59,8% e o #1
tem 11,9%. Não existe a negociação seller a seller que sustenta o BC de HE. A mesma aba vai rodar,
mas a conclusão vai apontar para outra alavanca — não para um BC de sellers.

---

## 19. Grid v13 e v14 (21/08/2026) — aba 2 corrigida e TVs/Áudio na aba 3

### 19.1 v13 — aba 2 com duas réguas

Aprovado por ela ("pode subir o ajuste na aba de D1 mesmo"). Correções da auditoria aplicadas:
lista de grupos 8/3/5 → **10/6/8**, bases 439/75/284 → **448,5/108,3/373,5**, e o **duplo-contagem de
H&C** resolvido (o gap do BAU agora sai de 799,5 = carteira total menos os grupos cotados, não dos
1.173 cheios).

**Mudança de método:** o bloco BC deixou de ser dimensionado pela régua do ritmo da D1.

| bloco | régua | LARGE | SMALL | H&C | total |
|---|---|---|---|---|---|
| BC — grupos cotados | **substituição**: 30% do que vendem na Shopee (nível jun/26), 4 meses | 138,2 | 35,8 | 76,6 | **250,6** |
| Demais segmentos — BAU | **gap medido** vs ritmo da D1, escalado para set-dez | 80,7 | 51,1 | 166,4 | **298,2** |
| **total set-dez/26** | | **218,9** | **86,9** | **243,0** | **548,8** |

*Escala para set-dez = participação de set-dez no semestre da própria D1 (Large 70,9% · Small 68,9% ·
H&C 78,5%). Assume que o segmento tem a mesma sazonalidade intra-semestre da D1 — declarado na tela.*

**Mecanismo agora é o correto por bloco:** BC sai da Shopee e entra no MELI
(`(Shopee−X)/(MELI+X)`); BAU é incremental (`Shopee/(MELI+X)`).

| D1 | set-dez sem ação | com ação | evita |
|---|---|---|---|
| LARGE | 44,5% | **36,8%** | 7,7 pp |
| SMALL | 45,6% | **42,0%** | 3,6 pp |
| Large+Small | 44,9% | **38,9%** | 6,0 pp |
| H&C | banda 45-70% | *não quantificável* — sem projeção de MELI, não há denominador |

**Adaptação dela aplicada:** trazer 30% do que os grupos vendem na Shopee é um **uplift de 46,9% em
Large, 40,9% em Small e 58,5% em H&C** sobre o que esses grupos faturam com a gente hoje. Está na tela
ao lado da tabela — é o número que o farming negocia.

**Ganho visual não planejado:** como o BC virou substituição, a barra da Shopee nos meses projetados se
divide e o pedaço verde é o volume que muda de lado. Vê-se o volume migrando, em vez de só a nossa
barra crescer.

Mantidos **dois KPIs de ratio** — o do semestre (42,7% Large, que bate com abas 1 e 4) e o da janela
acionável (44,5%) — cada um rotulado, para não cruzarem.

### 19.2 v14 — TVs e Áudio na aba 3 (5 chips de D1)

De-para dela + os 3 custs do Shop EV encontrados em `Shield Against Asians\grupos_economicos.csv`
(**KILL E-COMMERCE = 1212138371, 703236581, 750553953**; o `750553953` aparece como "SHOP EV" em
`seller_names.csv`). Todos os custs dela validaram — os 8 grupos retornaram dado.

**Os 8 grupos são ~100% `3P - VERTICALES`** (Carteira Assessorada) nas duas D1s novas, então o
perímetro MELI é o mesmo das 3 D1s de HE. Não há inconsistência de segmento entre os chips.

**A cobertura é o número que decide a alavanca:**

| D1 | grupos mapeados | total Shopee da D1 | cobertura | lojas na D1 |
|---|---|---|---|---|
| **TVS** | 201,8 | 257,9 | **78,2%** | 303 |
| **AUDIO** | 32,5 | 142,2 | **22,8%** | 838 |

### 19.3 TVs é o caso mais grave do portfólio

Os 8 grupos, jul/25 → jun/26: **com a gente 28 → 17 Mi/mês (−38%)**, na Shopee **13 → 77 (+503%)**.
O grupo cresceu 132% no total e **nós encolhemos**.

**Todos os 8 estão em ATACAR** — todos vendem mais na Shopee que com a gente. Shopee ÷ MELI do
conjunto = **663%**, contra 140% em Large. Destaques (mai+jun/26, R$ Mi):

| grupo | com a gente | na Shopee | Shopee÷MELI |
|---|---|---|---|
| SHOP EV (KILL) | 9,4 | **121,4** | 1.288% |
| PHILCO/BRITANIA | 0,7 | 25,2 | 3.624% |
| MERCADO FACIL | 0,2 | 19,4 | 8.486% |
| TNTINFOLOJA | 9,9 | 10,3 | 105% |
| **total** | **30,4** | **201,8** | **663%** |

Eficiência da substituição em TVs = **5,58x** (ratio 21,8%), quase o dobro de Large (3,34x).

### 19.4 Áudio — nota de hunting publicada na aba

Banner vermelho, a pedido dela: as mesmas 8 lojas cobrem 78,2% em TVs e só **22,8% em Áudio**, logo
**77% do faturamento da Shopee em Áudio vem de sellers fora da carteira assessorada**. 838 lojas, maior
player 11,9%, top 20 = 59,8%.
**Consequência escrita na tela:** negociar com quem já é nosso resolve pouco; o caminho é trazer seller
novo, que é **hunting** — outro time, outro custo, outro prazo. A tese do BC de HE não se transfere.

Um contraste dentro de Áudio: **REP STORE vende 19x mais na Shopee** (0,9 vs 16,9) enquanto
**TNTINFOLOJA é PROTEGER** (12,9 com a gente vs 8,3 lá).

### 19.5 Custo e armadilha de ambiente

- **O MCP `bigquery-insight` não alcança `DM_EFICIENCIA_MLB` nem `DM_MKP_SELLERS_HIST`** — roda em
  outro projeto (`melic-6bkba4`). Para o DM Eficiência é **bq CLI**, obrigatoriamente.
- **Scan do DM Eficiência: ~3,6 GB por mês de partição** com 6 colunas, ~5,1 GB com `SEGMENTO`.
  Filtrar D1 ou cust **não reduz**. 13 meses com SEGMENTO = **66,75 GB** (~US$ 0,42). Aprovado por ela.
  *A nota antiga de "1,2-1,4 GB por mês" está desatualizada — corrigir onde aparecer.*
- 🔴 **O scratchpad da sessão é efêmero e foi limpo no meio do trabalho.** Recuperei as 4 abas
  baixando o próprio doc do Grid (`GET $GRID_HOST/d/{doc_id}`) e extraindo os payloads base64.
  **Regra nova: todo artefato que não seja descartável vai para a pasta do projeto na hora.**
  Agora persistidos lá: `template_aba2_d1s.html`, `template_aba3_sellers.html`,
  `dados_d1cheia_camadas.json`, `dados_aba3_5d1s.json`, `dados_meli_tvs_audio.csv`,
  `dados_shopee_tvs_audio.csv`, `grid_plano_combate_abas.html`.
- **Grid skill exigiu `skill_version` 3.6.8** (426 com 3.6.6).
- Armadilha de template: usei `f1()` no `d1v2_template.html`, onde ela **não existia** (é do template
  da aba 3). O `render()` abortava silenciosamente e a aba ficava em branco. **Ao portar trecho de um
  template para outro, conferir os helpers.**
