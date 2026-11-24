# Demais projetos — índice e destino

> Os três temas aprofundados deste pacote (Shield, BPC, Price Point) não são tudo o que eu tocava.
> Este índice existe para que **nada se perca por desconhecimento** — cada item diz o que é, onde está,
> em que estado ficou e quem deveria pegar.

⚠️ **Os caminhos abaixo são da minha máquina** (`C:\Users\bdacache\Documents\Claude\Projects\...`).
Os arquivos **não estão neste ZIP** — precisam ser transferidos à parte, por pasta compartilhada ou Drive.
**Peça isso antes que a máquina seja reprovisionada.**

---

## 1 · WBR-HE — Weekly Business Review de Home Electronics

**O que é:** o report semanal de HE, automatizado. Gera big numbers + highs & lows **decompostos**
(NMV por segmento / D2 / marca com contribuição, BPC, Delivery Promise) por D1 e o bloco Total HE, e
**publica no Grid** — sempre no mesmo documento, mesmo link.

| | |
|---|---|
| **Cadência** | toda segunda-feira |
| **Como roda** | plugin local `wbr-he` — comando: *"rodar o WBR de Home Electronics"* (ou por D1) |
| **Onde** | `Projects\Built-In\wbr-he-marketplace\` · skill em `plugins\wbr-he\skills\wbr-he\` |
| **Grid** | doc fixo `01KTQ0V4038G3ZPZQ8FHFEHQ3A` |
| **Motor** | `bq` CLI + `curl.exe` para o Grid (precisa de **VPN**) |
| **Estado** | ✅ funcionando |

⚠️ **Preenchimento manual, por ora:** **Investimentos (EF VC / ROAS)** e o bloco de **sellers**. O primeiro
depende de escopo de Drive; o segundo, de PII corporativa. Quem assumir precisa saber disso na primeira
segunda-feira.

📌 **Existe um plano de migração para n8n (Verdi) + Google Docs nativo**, para reduzir custo de token.
A planta está em `Projects\Built-In\WBR-n8n-SPEC.md` (e `WBR-n8n-BUILD.md`). Não foi executado.
Nota operacional herdada: dentro do Verdi Flows, a query BigQuery roda com credencial OAuth e
`Project = meli-bi-data` selecionado **por ID** — a credencial `bg-read` **nega `jobs.create`**.

**Sugestão de destino:** quem herdar a cadência semanal de HE.

---

## 2 · Data Dupla HE

**O que é:** report do **dia** da data dupla — TGMV (% da meta, Δ vs meta, 1P/3P) + quebra, BPC
`BOX_ALL_ABC` (ALL / 1P / 3P) e Market Share, comparando com a data dupla anterior, com o mesmo dia do ano
passado e com o mês fechado. Dois escopos: uma D1 específica com quebra por D2 em 3P, ou HE inteiro com
quebra por D1.

| | |
|---|---|
| **Como roda** | skill `data-dupla-he` — *"rodar o report de data dupla"* |
| **Onde** | `Projects\Built-In\data-dupla-he-skill.zip` |
| **Estado** | ✅ funcionando |

**Sugestão de destino:** o mesmo dono do WBR — são a mesma rotina em cadências diferentes.

---

## 3 · KIs Selection HE (Shopee)

**O que é:** curadoria mensal da base de Key Selection Items que o time de Selection traz da concorrência.
Itens **FOUND** (existem no MELI) eram minha frente; **NOT FOUND** é do Pedro Henrique. Para os FOUND, eu
mantinha um Grid interativo com o perfil dos itens — marca, seller, ASP, recorrência.

| | |
|---|---|
| **Onde** | `Projects\KIs-Selection\` |
| **Ler antes de tudo** | `PLAYBOOK_KSI_Selection.md` (fluxo mensal) e `KB_KSI_Regras_Aprendidas.md` (conhecimento acumulado) |
| **Base atual** | `Shopee\KSI_V18_GridReady.xlsx` (jan-jun/2026) |
| **Grid** | `01KS3ECPZVB6MS44T3KP00MFFS` · **doc de teste** `01KSNVEDM1H8Y8CZ41X0HE31FJ` |
| **Estado** | ✅ Shopee estabilizado até V18 · ⏳ **Amazon nunca foi iniciado** |

**Princípios não-negociáveis do pipeline** (valem para quem continuar):
1. **RAW é imutável** — é o histórico cru, nunca se altera
2. **REMOVIDOS é append-only** — toda remoção com `MOTIVO_REMOCAO` + `ROUND_REVISAO`
3. `SELLER_ORIG` e `BRAND_ANTES` são imutáveis; a curadoria vive em `SELLER_FINAL` e `BRAND`
4. **Nunca deletar sem aprovação** — fluxo é flag → sugestão pronta → aprovação → REMOVIDOS
5. **Herança entre versões:** BRAND por `MELI_ID` · `SELLER_FINAL` por (`MELI_ID` + `COMP_ID`) ·
   `D2_CORRIGIDO` por `MELI_ID`
6. **Sempre subir no doc de teste antes do oficial**

⚠️ **Códigos de competidor divergem entre bases:** Amazon é `AMZ` na base de Selection e **`AMB`** na
`BT_COM_FAVORABILITY`. Shopee é `SPE` nas duas.

**Pendências abertas:** scraping de ~45 sellers vazios · o item `3748114860` em HOLD ·
D2/D3/D4 de 3 itens corrigidos em junho · **Amazon do zero**.

**Sugestão de destino:** Pedro Henrique de Araujo Baldi já opera o outro lado do mesmo pipeline.

---

## 4 · Built In — categoria core

**O que é:** análises de KPI e performance da D2 **Built In** dentro de Large Appliances, mais análises da
D1 inteira (o WBR).

| | |
|---|---|
| **Onde** | `Projects\Built-In\` |
| **Tabela principal** | `WHOWNER.DM_EFICIENCIA_MLB` |
| **Estado** | análises pontuais, sem cadência fixa além do WBR |

🔑 **Convenção crítica, e contraintuitiva:**
**NMV = `SUM(F_NMV_LC)` SEM `NMV_FLG`.** Aplicar `NMV_FLG=TRUE` tira ~3,8% (cancelados, devoluções, combos
grátis) e **não bate com o número oficial** que a liderança usa.
*Exemplo validado: Large Appliances 1P+3P em mai/26 = R$ 609,4 Mi sem flag vs R$ 586,0 Mi com flag.*
Se o seu número vier ~4% abaixo do esperado, é isso.

⚠️ **Não use as colunas `_TEMP`** de domínio (taxonomia 2025) — estão remapeadas e bagunçadas.
Use `DOM_DOMAIN_AGG1/2/3`. E "BUILT IN PARTS" cai em `AGG1='HOUSEHOLD APPLIANCES PARTS'`, **fora** da D1.

**Divisão de responsabilidade que existia:** Built In era minha; **Laundry e Refrigeration são da Nicole
Freire Anjos**. A análise da D1 inteira era minha, mas o plano de ação de problemas em D2 não-Built In é
dela.

📌 **Existe um painel de handover de Built In** — app de Grid com 4 abas filtráveis (macro / lojas / marca /
BPC), com seller agrupado por grupo econômico, NMV + NSI. Foi desenhado justamente para passar a estratégia
da categoria adiante. **Spec travado, vale procurar antes de refazer qualquer coisa.**

**Sugestão de destino:** quem assumir a categoria.

---

## 5 · Análises de competição que não viraram pasta própria

Ficam registradas para que ninguém as reconstrua do zero.

| Análise | O que é | Onde procurar |
|---|---|---|
| **Combate HE — Data Dupla** | App de Grid de combate à concorrência em HE (espelho de 06/06). Base montada via `bq` CLI + `external_push` **porque `grid_sql` estoura o teto de 1 GB** | Grid |
| **Gap de sellers Shopee × MELI** | Método para validar base de "gap" de sellers de competidores por **match fuzzy de nome** (`DM_MKP_SELLERS_HIST`, `TOP_VERTICAL`, 2 passadas). Truque necessário: `bq` + `cmd` para UTF-8 | notas de projeto |
| **Gap por vertical (Shopee)** | Top 5.000 itens, `UNNEST` de competidores, gap por D1 e ASP. **Achado: HE tem gap de 20% das visitas; Tech, 35%** | notas de projeto |
| **MBR HE — BPC por ASP + cobertura** | Widget de Grid com BPC de HE por faixa de ASP / mês / data dupla em 3 lentes | Grid, doc `01KXPCDFV8…` |

---

## Checklist de transição — o que pedir antes que a máquina seja reprovisionada

- [ ] Cópia das pastas `Projects\Built-In\`, `Projects\KIs-Selection\`, `Projects\Ad-Hoc\` e
      `Projects\Shield Against Asians\` (inclui os cubos de dados que ficaram fora deste ZIP)
- [ ] Transferência de **propriedade dos documentos do Grid** listados acima
- [ ] Instalação do plugin local `wbr-he` na máquina de quem assumir
- [ ] Acessos de BigQuery reemitidos em nome de quem assumir (ver `../LEIA-ME.md`)
- [ ] Revisar a **visibilidade `public`** do Grid do Business Case (`01M0DSBDBHEAV3650Q913YSP6Y`)
