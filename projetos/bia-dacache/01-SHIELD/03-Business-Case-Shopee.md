# Forecast BC Shopee — frear a Shopee em Home

> Também chamado de **"Plano de Combate BC"** (é o nome da pasta de origem) e de **"BC Shopee"** (é o
> título dentro do Grid). São a mesma coisa. **Este é o documento que explica aquele Grid.**

🔗 **Grid (v12):** https://grid.adminml.com/d/01M0DSBDBHEAV3650Q913YSP6Y/view ⚠️ *visibilidade `public`*
📄 **Fonte da verdade:** `originais/ESTADO_DO_BC.md`
📄 **Histórico completo (inclui caminhos abandonados):** `originais/premissas_bc_shopee_asp_home.md`
📄 **Auditoria:** `originais/AUDITORIA_21ago.md`
🗂️ **Qual arquivo gera qual aba do Grid:** §11, no fim deste documento

> **Leia o §7 antes de citar qualquer número deste BC para a liderança.**

---

## 1 · A pergunta

Frear o avanço da Shopee em **Home Electronics** — Large Appliances, Small Appliances e
Heating & Cooling — trazendo sellers MELI para perto.

**KPI de compromisso:** `ratio = faturamento Shopee ÷ faturamento MELI` (↓ melhor).
**Horizonte:** jul-dez/2026, sendo **set-dez/26 a janela realmente acionável**.

---

## 2 · A regra de ouro do perímetro — D1 cheia, sempre

**Todo número de capa é D1 cheia, sem recorte de faixa de ASP.** Decidido em 21/08/2026, porque os números
macro precisam bater com os documentos oficiais. A faixa de ASP continua no BC, mas **só como eixo de
alocação** do incremental — nunca para compor o número de capa.

**A prova de que fecha** (jul-dez/25, Planning × DM Eficiência):

| D1 | Planning | DM Eficiência | gap |
|---|---|---|---|
| LARGE | 2.852,0 | 2.855 | **0,1%** |
| SMALL | 2.273,7 | 2.270 | **0,2%** |
| H&C | 1.693,5 | 1.694 | **0,03%** |

**Por que isso importa tanto:** no perímetro anterior (só faixas-foco), Small dava 1.789 contra 2.270 —
**27% de diferença**, e o ratio aparecia como 35,5% quando o real era 44,1%. **8,6 pp escondidos.** A
distorção acontecia porque o critério de faixa-foco exigia SoB MELI ≥5%, e a Shopee vive exatamente onde
nosso SoB é pequeno. Em Large e H&C a distorção era de meio ponto; em Small, era a conclusão inteira.

> 🔑 **Lição transferível:** um perímetro que filtra por "onde somos grandes" é cego justamente para onde o
> concorrente está crescendo. Se o recorte precisar existir, valide-o contra a base cheia antes de fechar.

---

## 3 · As três D1s — tratamento diferente para cada

| D1 | ratio H2'25 | ratio hoje (Q2'26) | jul-dez/26 | tratamento |
|---|---|---|---|---|
| **LARGE** | 20,7% | 30,0% | **42,7%** → 39,7% com camadas | ✅ projeção validada |
| **SMALL** | 29,2% | 44,1% | **45,2%** → 44,0% com camadas | ✅ projeção quantificada |
| **H&C** | 27,3% | 48,2% | **banda 45-70%** → 38-60% | 🔴 **sem projeção — banda + evidência** |

**Por que H&C não tem projeção:** quatro métodos deram 42%, 46%, 52% e 77%, e o motor em D1 cheia dá 67%.
Dispersão dessa ordem não é margem de erro — é a categoria dizendo que não é projetável. Causas: é a D1
mais sazonal (pico nov-jan, vale abr-jun, e o modelo ancora no vale para projetar no pico), há um degrau
de dado em out/25 que contamina qualquer YoY, e foi a pior no backtest.

**Para H&C usamos evidência medida, sem modelo:**
- o ratio saiu de **13% (jul/25) para 43-48% (Q2/26)** — triplicou em doze meses
- nossa **Carteira Assessorada encolhe** — e ela é **69% da categoria**
- **Frio Peças**, maior loja da Shopee em H&C, vende **9x mais lá** do que conosco (57,3 vs 6,5 Mi em mai+jun/26)
- **1P é só 5,5%** da categoria — essa alavanca não existe aqui

**Validação em D1 cheia (MELI de julho/26, um passo à frente do ajuste):**
LARGE projetado 642,4 vs realizado 641,3 (**+0,17%**) · SMALL 496,8 vs 513,8 (−3,3%) · H&C 224,8 vs 221,1 (+1,7%).

---

## 4 · A evidência central: a migração dos sellers

**Os grupos cotados vendem mais na Shopee do que conosco** (mai+jun/26, R$ Mi):

| D1 | MELI | Shopee | Shopee ÷ MELI |
|---|---|---|---|
| LARGE (10 grupos) | 147,3 | 236,0 | **160%** |
| SMALL (6 grupos) | 43,7 | 89,9 | **206%** |
| H&C (8 grupos) | 65,4 | 151,2 | **231%** |
| **TOTAL** | **256,4** | **477,1** | **186%** |

**Electrolux é o caso emblemático:** MELI 41,3 → 38,9 (**−6%**) enquanto a Shopee vai de 0 → 52,3 (abriu
loja oficial em ago/25). O grupo cresceu **+121%**, e **105% desse crescimento foi para a Shopee**. Saiu de
100% MELI para 57% Shopee em 11 meses. **Não é um seller fraco — é um seller forte cujo crescimento inteiro
perdemos.**

**Engage é a prova reversa:** cresceu +106% no MELI e ficou flat na Shopee. Único caso de migração na
nossa direção — e por isso o mais útil para entender o que funciona.

**Concentração:** os 6 grupos originais passaram de 24% (jul/25) para **57,3%** de tudo que a Shopee
fatura em Large. *(Este número tem uma ressalva de denominador — ver §7.)*

### A fórmula da substituição

Um real trazido da Shopee move **os dois lados** do ratio, então vale mais que um real de venda nova:

```
eficiência = (1 + r) / r = 1 + MELI/Shopee
```

Em Large (D1 cheia, jul-dez/26): **3,34x**. R$ 100 Mi de substituição valem R$ 334 Mi de venda nova, em
efeito sobre o ratio.

> 🔑 **A consequência estratégica é contraintuitiva:** como a eficiência é `1 + 1/r`, **a substituição vale
> mais onde a Shopee ainda é pequena** (r = 20% → 6x). **Defender território que ainda dominamos é mais
> eficiente do que reagir onde já perdemos.**

### A janela acionável são 4 meses, não 6

A base da Shopee fecha em jun/26, então o semestre inteiro aparece como pendente. Mas julho e agosto **já
passaram** — são meses que ainda não auditamos, não meses em que podemos agir. **Os dias acionáveis são
set, out, nov e dez/26.**

**Cenários em Large** — os 10 grupos faturam 115,2 Mi/mês na Shopee (jun/26):

| se trouxéssemos… | entra por mês | nos 4 meses | equivale a venda nova | ratio set-dez/26 |
|---|---|---|---|---|
| 20% | 23,0 Mi | 92 Mi | 299 Mi (×3,25) | 44,5% → 39,9% |
| 30% | 34,6 Mi | 138 Mi | 449 Mi (×3,25) | 44,5% → 37,8% |
| 50% | 57,6 Mi | 230 Mi | 748 Mi (×3,25) | 44,5% → **33,6%** |

---

## 5 · Como a projeção é feita

**Média de duas regras** — a média cancela viés (Bates & Granger, 1969): no perímetro, a primeira
subestimava 11% e a segunda superestimava 13%; a média ficou em +0,9%.

**Regra 1 — YoY sobre o mês real do ano anterior:**
`F = real(m−12) × (1 + YoY × φ^k)`, com o YoY dos últimos 6 meses fechados.

**Regra 2 — decomposição multiplicativa:**
`F = nível dessazonalizado × Π(1 + g·φ^j) × S_m`, onde `S_m` é o índice sazonal por mês-calendário
(log-linear; MELI 2023-26, Shopee 2024-26), o nível vem dos **últimos 3 meses fechados (L3M)** e `g` é a
tendência recente.

**Amortecimento φ = 0,9** (damped trend, Gardner & McKenzie 1985) — o crescimento continua, mas
desacelera, e a projeção não explode no horizonte longo.

📄 Scripts: `queries-e-scripts/motor_d1_cheia.ps1` (versão atual, D1 cheia) ·
`motor_v2_forecast.ps1` · `motor_v3_hc_e_combinacao.ps1` · `estima_phi_backtest.ps1`

### ⚠️ O motor subestima a Shopee

Backtest (ajuste até dez/25 → previsão de jan-jun/26), erro do ratio:
Large **10,9%** · Small **23,3%** · H&C **24,2%**.

Viés: **−14% em Large** e **−34% em Small**. Em D1 cheia as duas regras erram para o mesmo lado, então a
média **não cancela** o viés (em perímetro cancelava).

**Os ratios projetados são o piso, não o teto — o risco real é maior.** Na direção de um BC isso é
conservador: não há como acusar o número de estar inflado. Mas precisa estar declarado.

---

## 6 · Fontes e o papel de cada uma

| fonte | papel | observação |
|---|---|---|
| `SBOX_MKPBR.DM_MARKET_ASP_MONTHLY_VERTICAL_D1` | **nível de mercado** por D1 × faixa de ASP | Planning · defasagem ~2 meses (fecha jun/26) · **não tem 1P/3P nem seller** |
| `WHOWNER.DM_EFICIENCIA_MLB` | **acompanhamento**, segmento e seller | já tem jul/26 · `SUM(GMV_LC) WHERE NMV_FLG AND GMV_FLG`, por `ORD_CLOSED_DT` · **não tem faixa de ASP** |
| `WHOWNER.DM_YIPIT_SHOPEE_ITEMS` | **composição por loja** da Shopee | fecha jun/26 · nível item → loja |
| `depara_grupos_economicos.csv` | cust_id → grupo econômico | Elux tem loja oficial + Full; Shop EV = grupo Kill inteiro |

**Validação GMV × NMV:** o `TGMV_MELI` do Planning bate com o NMV líquido do DM Eficiência — gap de
**0,1%**. É isso que permite transitar entre as duas bases.

**Yipit e Planning são a MESMA fonte de Shopee** (verificado em 21/08/2026): `GMV_SHOPEE` do Planning ==
`NMV_LC` do Yipit agregado por D1 × mês, com erro de 0,00% a 0,15% em 18 combinações.
*Isso corrige uma instrução anterior de "nunca dividir uma pela outra" — **é válido dividir**, e portanto
o share do grupo dentro da Shopee da D1 é métrica legítima.* A **defasagem** continua real: Yipit/Planning
fecham em jun/26, o DM tem jul/26.

---

## 7 · 🔴 O que está quebrado — leia antes de apresentar

Em 21/08/2026 pedi uma auditoria cruzada de todas as abas do Grid. Ela encontrou o seguinte, e **nada
disso foi corrigido**. O detalhe completo está em `originais/AUDITORIA_21ago.md`.

### O que reconcilia ✅
Abas 1, 2 e 4 fecham exatamente entre si nos ratios realizados e na projeção. A aba 3 soma corretamente na
seleção múltipla.

### Os três erros materiais ❌

**7.1 — A lista de grupos da aba 2 está desatualizada.** Ela usa a lista de **antes** de Electrolux e
Philco entrarem: diz 8/3/5 grupos quando são **10/6/8**. Em Small a base está 30,7% errada; em H&C, 24,0%.

**7.2 — Com a lista certa, o gap do bloco BC cai de 296 para 121 Mi** — e vira **zero** em Small e H&C,
porque esses grupos crescem acima da própria categoria.

**7.3 — O gap de H&C conta o bloco BC duas vezes.** Os 314 Mi de "BAU" foram calculados sobre a Carteira
Assessorada **total**, que inclui os grupos do BC. Deveria ser sobre a carteira **menos** os grupos
cotados (≈235,6 em vez de 310,8).

### Inconsistências menores, mas visíveis 🟠

- **Duas taxas para a mesma coisa, na mesma aba:** em H&C, o banner diz que a Carteira Assessorada
  "encolhe −21,4%" e a tabela de diagnóstico diz **−7,4%**. É o número mais citado do caso de H&C.
  **Resolver antes de qualquer apresentação.**
- **Dois mecanismos diferentes de "com ação", sem rótulo na tela:** a aba 2 usa **incremental**
  (`ratio = Shopee / (MELI + camadas)`, a Shopee não muda); a aba 3 usa **substituição**
  (`ratio = (Shopee − recuperado) / (MELI + recuperado)`). A aba 3 parece mais eficiente **porque usa outro
  mecanismo**, não porque a ação seja melhor.
- **Janelas diferentes para a mesma métrica:** ratio projetado de Large aparece como 42,7% (semestre) e
  44,5% (janela set-dez).
- **O "57,3% da Shopee em Large" precisa ser reconferido na query original** — se o denominador vier do
  Planning, o número correto é 62,4%.

### 🔴 O problema de método — o mais grave

**A régua "gap vs ritmo da D1" mede a coisa errada quando aplicada ao bloco do BC.**

Com a lista certa, ela dá **BC = 0** em Small e H&C, porque os grupos cotados crescem mais rápido que a
categoria **do nosso lado**. Mas esses mesmos grupos vendem 145% (Small) e 210% (H&C) mais na Shopee do que
conosco.

> **A tese do BC é a segunda tabela, não a primeira. Um seller pode crescer 74% conosco e ainda estar dando
> o dobro do volume para a Shopee.** A régua do ritmo da D1 responde *"quanto deixamos na mesa por crescer
> devagar"* — pergunta certa para o **BAU**, errada para o **BC**.

**Recomendação registrada (a decisão é de quem assumir):**
1. **Bloco BC = substituição** — dimensionar pelo que os grupos dão para a Shopee, em cenários de
   recuperação na janela acionável. É a tese do BC e é o número que o farming negocia seller a seller.
2. **Bloco BAU = gap vs ritmo da D1** — mantém a régua, mas (a) excluindo os grupos do BC da base,
   (b) refazendo o gap de Small, (c) trocando o YoY de mês isolado por janela de 3 meses.
3. **Um só mecanismo no ratio** — ou tudo incremental, ou tudo substituição, ou as duas linhas lado a lado
   com rótulo explícito.
4. **Resolver o −21,4% vs −7,4%** de H&C.
5. **Alinhar a janela** — recomendo **set-dez** (é o acionável) e mover o semestre para nota de rodapé.

---

## 8 · Limitações que sempre declarei

1. **O GMV da Shopee é estimativa de painel**, não dado transacional. Use **tendência e ratio**, não nível absoluto.
2. **O motor subestima a Shopee** (§5).
3. **O YoY dos segmentos é medido em julho isolado** — mês único. Em H&C isso **muda o sinal** de uma
   conclusão: os grupos vinham de 79,7 Mi/mês em jan/26 e caíram para 30,3 em jun/26; jul/25 foi fraco,
   então o YoY de julho dá +40,7% enquanto a tendência de seis meses é de queda forte.
4. **As camadas entram integralmente já em julho**, sem rampa.
5. **Nada aqui prova causalidade.** A correlação entre a entrada dos sellers na Shopee e a estagnação aqui
   é forte, mas parte do crescimento lá pode ser demanda nova. Por isso a substituição entra como
   **cenário**, não como previsão.
6. **O incremental não é o pedido do BC.** É o tamanho do problema. Precisa ser rateado entre BAU, BC e 1P
   antes de virar pedido de verba.

---

## 9 · Pendências herdadas

1. **Corrigir o que está no §7** — precede tudo.
2. **Small e H&C: listas definitivas de sellers.** As atuais vieram de um print e foram confirmadas por nome.
3. **Rateio BAU × BC × 1P** — os 779 Mi precisam ser divididos. O farming entra aqui para estimar verba e eficiência.
4. **Capacidade de seller** — validar se os grupos cotados conseguem entregar, com os cubos do Shield
   (`seller_cap_cube`, `grupos_economicos`).
5. **Rampa de entrada** — as camadas hoje entram todas em julho; ajustar quando houver data de início.
6. **Faturamento dos grupos na Shopee por faixa de ASP** — para dimensionar a substituição por faixa.

---

## 10 · Regras de comunicação travadas do Grid

Valem para qualquer aba nova. Vieram de uma crítica de clareza em 20/08 e melhoraram muito a recepção:

- nenhum jargão sem tradução na tela
- unidade em todo cabeçalho
- período explícito em toda referência
- referência histórica sempre ao lado do alvo
- glossário na própria página
- o evolutivo mensal é peça central, não apêndice
- todo quadro com **colunas = histórico + projeção** e **linhas = KPIs** (faturamento, MoM, YoY de Shopee e
  MELI, ratio)

---

## 11 · Qual arquivo gera qual aba do Grid

O documento publicado (v12) é o **`grid_plano_combate_abas.html`** — o arquivo consolidado, com todas as
abas juntas. Os arquivos individuais abaixo são as abas construídas separadamente, e servem para editar uma
aba sem mexer nas outras.

| Aba no Grid | Conteúdo | Arquivo em `dashboards/` |
|---|---|---|
| **— (publicado)** | o documento inteiro, com as 4 abas | **`grid_plano_combate_abas.html`** |
| **1 · Diagnóstico por faixa** | evolutivo Shopee × MELI por D1 e faixa de ASP · **é a visão de alocação**; abre com as 11 faixas marcadas, então o default já é D1 cheia | `dashboard_evolutivo_shopee.html` |
| **2 · D1s consolidadas** | as três D1s com o tratamento de cada uma, o gap do semestre e as premissas | `consolidado_d1s.html` |
| **3 · Migração dos sellers** | MELI vs Shopee por grupo econômico · seleção múltipla (chips ou clique no ranking) · ranking atacar/proteger · cenários na janela de 4 meses | `migracao_sellers.html` |
| **4 · Realizado × Projetado** | gráfico contínuo com a fronteira em jun/26, em D1 cheia | `dashboard_realizado_projetado.html` |
| **5 · Simulador** ❌ | **apagada em 21/08/2026** — tinha sido construída no perímetro de faixas-foco e os valores não coincidiam mais com as demais abas | `simulador_desafio.html` *(preservado)* |

**Arquivos de apoio, na mesma pasta:**

| Arquivo | O que é |
|---|---|
| `dashboard_evolutivo_shopee_template.html` · `template_aba2_d1s.html` · `template_aba3_sellers.html` | os **templates** com placeholders — é onde se muda o layout |
| `dados-das-abas/` | os **payloads** que os templates consomem (`dados_d1cheia*.json`, `dados_aba3_5d1s.json`, os CSVs de TVs/Áudio e o `shopee_large_loja_x_asp.csv`) |
| `joystick_incremental.html` · `modo_reverso.html` | protótipos de simulação que **não** entraram no Grid final — ver o log de caminhos deprecados em `premissas_bc_shopee_asp_home.md` §13.2 antes de retomar |
| `consolidado_large.html` | versão anterior, só Large — **superada** pelo `consolidado_d1s.html` |

**Como regerar uma aba:** rodar a query parametrizada por data → gerar o JSON de dados → injetar no template
(o gerador injeta o JSON no placeholder via PowerShell) → subir no Grid. É o mesmo padrão do Shield por ASP,
descrito em `01-Ways-of-Working-Grid-Shield.md` §2.

**O motor do forecast que alimenta as abas 2 e 4:** `queries-e-scripts/motor_d1_cheia.ps1` (versão atual,
em D1 cheia). As anteriores — `motor_v2_forecast.ps1` e `motor_v3_hc_e_combinacao.ps1` — ficam como
histórico do método, e `estima_phi_backtest.ps1` é o que estima o amortecimento φ e roda o backtest.
