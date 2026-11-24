# Ways of working — Grid Shield por ASP

🔗 **Documento:** https://grid.adminml.com/d/01KXKJP50WAQ314W1MVQXD4SRZ/view
📄 **Motor:** `queries-e-scripts/refresh_shield_large.ps1`
🎨 **Template:** `dashboards/dashboard_template.html` → gera `dashboards/dashboard_shield_large.html` (~31 MB)

> Este é o documento central do Shield. Se você só puder ler uma coisa antes de mexer no Grid, leia isto.

---

## 1 · O que o Grid é

Um dashboard **autocontido** (um único HTML, sem backend, sem chamada de API em runtime) que lê
**Large Appliances em MLB por faixa de ASP** sob três ângulos ao mesmo tempo:

| Pilar | Pergunta | Fonte |
|---|---|---|
| **S&P** — Sales & Performance | Quanto vendemos, para quem, de que marca, em que faixa? | `WHOWNER.DM_EFICIENCIA_MLB` |
| **BPC** — Competitividade | Nosso preço está melhor ou pior que o do rival, nessa faixa? | `WHOWNER.BT_COM_FAVORABILITY` |
| **Demanda & Conversão** | Quantas visitas essa faixa recebe e quanto converte? | `WHOWNER.DM_MKP_VISITS` + `DM_EFICIENCIA_MLB` |

**O eixo-guia é sempre a faixa de ASP.** Foi uma decisão deliberada: em Large, a dinâmica competitiva muda
completamente entre o item de R$ 300 e o de R$ 3.000, e olhar a D1 inteira mistura duas guerras diferentes.

**Faixas (BRL, iguais em todo o Shield):** `<200` · `200-500` · `500-1500` · `1500-3000` · `>3000`

---

## 2 · A arquitetura, em uma passada

```
   BigQuery (bq CLI)                PowerShell                    HTML
┌────────────────────┐      ┌──────────────────────┐      ┌──────────────────┐
│ 10 queries         │─────>│ CSV/JSON intermediá- │─────>│ dashboard_       │
│ (S&P + BPC +       │      │ rios → derivação     │      │ template.html    │
│  Demanda)          │      │ local dos cubos      │      │ com placeholders │
└────────────────────┘      └──────────────────────┘      └────────┬─────────┘
                                                                    │ injeção
                                                                    ▼
                                                          dashboard_shield_large.html
                                                                    │ curl + VPN
                                                                    ▼
                                                          Grid MELI (nova versão)
```

**Por que essa arquitetura e não um dashboard conectado ao banco:** o Grid serve HTML estático. Um arquivo
único, com os dados dentro, abre em qualquer lugar, versiona sozinho e não quebra quando alguém perde
acesso ao BigQuery. O custo é que **o dado é uma foto** — a data do refresh precisa estar visível na tela.

**Por que a derivação é local e não no SQL:** os cubos de BPC e Demanda precisam de *bounding* (top-N por
faixa, resto vira "Outros") e de rótulo de seller. Fazer isso no BigQuery exigiria mais scans; fazer em
PowerShell sobre o CSV já baixado é de graça. O preço é ~3 minutos de `Import-Csv` nos masters grandes.

---

## 3 · Como rodar

```powershell
.\refresh_shield_large.ps1 -Through 2026-07
```

Sem `-Through`, ele assume o último mês completo. `-Through` define o fim da janela
(`ORD_CLOSED_DT <= último dia do mês`).

### Pré-requisitos
- **VPN corporativa** ligada (o upload para o Grid não sai sem ela)
- **Credencial gcloud** válida (`gcloud auth login`) para o `bq` CLI
- `grid_config2.json` presente na mesma pasta — é ele que carrega o `doc_id` e o `skill_version`

### ⚠️ O `.ps1` não roda direto nesta máquina
SRP/GPO corporativo bloqueia execução de `.ps1`. As duas saídas que funcionam:

1. **Rodar a lógica inline** — colar os blocos no terminal, na ordem do arquivo
2. **Transformar em skill** (recomendado) — foi o caminho que o WBR-HE seguiu e funcionou bem. Ver
   `00-OUTROS/INDICE-DEMAIS-PROJETOS.md` para o modelo do plugin `wbr-he`.

---

## 4 · Os três pilares em detalhe

### 4.1 · Pilar S&P — 5 cubos de `DM_EFICIENCIA_MLB`

| Cubo | Grão | Janela | Para quê |
|---|---|---|---|
| `cubo_large_18m` | mês × faixa × D2 × D4 × segmento | 2025-01 → | visão principal, sem bounding |
| `seller_cube` | + seller | 18 meses | ranking de seller por faixa |
| `growth_cube` | + seller | 30 meses | YoY e delta em pp |
| `brand_cube` | + marca | 30 meses | ranking de marca por faixa |
| `sb_cube` | marca × seller (sem D2) | 30 meses | drill "quais sellers vendem essa marca" |

**Filtro fixo:** `VERTICAL='HOME ELECTRONICS' AND DOM_DOMAIN_AGG1='LARGE APPLIANCES'`
**Faixa vem de:** `ITE_ITEM_FULL_UNIT_PRICE`
**De-para de segmento (`SEGMENTO_DETAIL`):** `CA` → *3P Assessorada* · `SD` → *3P Dev* · `PL` → *1P* ·
`1P`/`CBT` passam direto. Esse de-para foi **aterrado no dado real**, não deduzido da documentação.

### 4.2 · Pilar BPC — 6 cubos de `BT_COM_FAVORABILITY`

Duas queries (mensal e data-dupla), cada uma com **`GROUPING SETS`** para tirar três grãos
(estrutura + marca + seller) num **único scan** — é o que mantém o custo civilizado.

**As três lentes vêm como colunas, não como linhas:**

| Coluna | Lente | Como é calculada |
|---|---|---|
| `t_m` / `t_ce` | **Total** | todas as visitas com match |
| `w_m` / `w_ce` | **Shopee winner** | `COMP_RIVAL_NAME_WINNER='Shopee'` |
| `s_m` / `s_ce` | **vs Shopee** | subquery `UNNEST(COMPETITORS)` com `COMP_RIVAL_NAME='Shopee'` |

`BPC = ce / m` em qualquer uma delas. Ter as três lado a lado é o que permite responder
"a Shopee é o problema, ou só está ganhando onde já perdíamos de qualquer jeito?".

**Filtro fixo:** `SIT_SITE_ID='MLB' AND VERTICAL='HOME ELECTRONICS' AND DOM_AGG_1='LARGE APPLIANCES'`
e `FAVORABILITY_TYPE IN ('BOX_ALL_ABC','BOX_ALL_ABC_PIX','SHP_ALL_ABC')` — as três lentes de preço.

**Faixa vem de:** `PRICE_MELI` (com bucket `0_sem_preco` para nulo — não jogue fora, é diagnóstico).

**De-para de segmento no BPC é diferente do de S&P** (a taxonomia da tabela é outra):
`FIRST PARTY` → *1P* · `CBT%` → *CBT* · `ASESORADO PF` **e** `3P ASESORADO DIRECTO` → *3P Assessorada* ·
resto → *3P Dev*. Os dois valores caindo em "3P Assessorada" foi validação manual minha — não é óbvio.

**Datas duplas:** as datas são geradas como `M/M ± 1 dia`, de fevereiro até o mês do `-Through`.
Janeiro não tem data dupla. **Se o evento do mês for irregular, ajuste a lista à mão** — o script não sabe.

### 4.3 · Pilar Demanda & Conversão — 3 cubos item-level

Este é o pilar mais delicado. Ele cruza **visitas** (`DM_MKP_VISITS`) com **pedidos** (`DM_EFICIENCIA_MLB`)
por item × dia, via `FULL OUTER JOIN`, para que o CVR fique alinhado nos dois lados.

**Por que `FULL OUTER JOIN` e não `LEFT`:** item com visita e sem pedido, e item com pedido e sem visita
registrada, ambos existem. Um `LEFT JOIN` em qualquer direção enviesa o CVR.

**A ponte item → atributo (`bridge`):** as visitas não trazem faixa, marca nem seller. O script constrói um
de-para por item a partir do `DM_EFICIENCIA`, onde a **faixa vem da mediana do preço cheio do item**
(`APPROX_QUANTILES(ITE_ITEM_FULL_UNIT_PRICE,2)[OFFSET(1)]`), não do preço do dia.

> 🔑 **Esta é a lição mais transferível do Shield inteiro: a faixa de ASP é atributo do item, fixo, não do
> dia.** Se você usar o preço diário, o item "pula" de faixa toda vez que entra em promoção — e aí a faixa
> barata parece ter mais desconto por construção. O Price Point herdou essa regra (ver `03-PRICE-POINT/`).

**Calibração:** o CVR sai em ~1,3%, que bate com o COMMERCE/Looker. Se der muito diferente, o join quebrou.

**VIP entra como coluna** (`QTY_VISITS_VIP`), não como filtro — assim cruza com todos os outros cortes.

---

## 5 · Decisões de desenho que estão travadas

Não mude sem entender o motivo. Cada uma custou uma rodada de retrabalho.

| Decisão | Por quê |
|---|---|
| **Bounding top-N por faixa, resto = "Outros"** | Sem isso o HTML explode. Top-15 (NMV ∪ NSI) no S&P, top-6 no BPC, top-8 na Demanda. A união NMV∪NSI evita perder o seller que vende muita unidade barata. |
| **Ranking calculado em 2025-01+, aplicado a toda a série** | Se o top-N fosse recalculado por mês, o "Outros" mudaria de composição e a série ficaria incomparável. |
| **`SIT_SITE_ID='MLB'` sempre na FAVORABILITY** | Esquecer isso **infla o BPC** — a view tem outros sites. Foi um erro real, caro, e é a nota mais destacada no cabeçalho do script. |
| **Seller identificado por `CUS_CUST_ID_SEL`, nome vindo do `DM_EFICIENCIA`** | `CUS_NICKNAME` é **PII-bloqueado**. O ID é a chave; o nome legível vem de um de-para separado. |
| **Rótulo de seller e bounding feitos em PowerShell, não em SQL** | Reproduz exatamente os cubos já validados e não custa scan adicional. |
| **Janela começa em 2024-01 nos cubos de growth** | Para ter YoY de verdade nos 18 meses visíveis. |

---

## 6 · Sanity checks — rode sempre, antes de subir

O script já imprime os três. **Se algum destoar, pare e investigue — não suba.**

1. **NMV do mês por cubo.** Os 5 cubos de S&P precisam bater entre si no mês do `-Through`.
   *Referência validada:* jun/26 ≈ **R$ 584 Mi**.
2. **BPC Total ABC do mês.** *Referência validada:* jun/26 = **42,7%**.
3. **Placeholders restantes = 0.** O script conta os `/*__NOME__*/` que sobraram no HTML e **aborta** se
   houver algum. Placeholder sobrando = cubo faltando = gráfico vazio no Grid.

---

## 7 · Publicação no Grid

O script escolhe o caminho sozinho pelo tamanho do arquivo:

**≤ 10 MB — upload inline (1 passo)**
```
POST https://grid.melioffice.com/api/v1/engine/run   -F "config=<grid_config2.json" -F "file=@<html>"
```

**> 10 MB — presigned em 3 passos** (é o caso do Shield, que tem ~31 MB; teto real ~500 MB)
1. `POST /api/v1/engine/run/json` com `presigned_upload` → devolve o slot
2. `PUT /api/v1/documents/{slot}/upload-content` com `--data-binary`
3. `POST /api/v1/engine/run/json` com `confirm_presigned: true`

⚠️ **`skill_version` é obrigatório** no payload — o engine recusa sem ele. Está no `grid_config2.json`.
⚠️ **Sempre suba num doc de teste antes do oficial.** É princípio meu para qualquer publicação no Grid.
Para voltar atrás: `POST /api/v1/documents/{doc_id}/rollback {"version": N}`.

---

## 8 · Custo

| Bloco | Custo aproximado |
|---|---|
| S&P (5 cubos) | US$ 0,80 |
| BPC (2 masters + nomes) | US$ 4,34 |
| Demanda (master + nomes) | US$ 0,63 |
| **Total por refresh full** | **~US$ 5,80 – 6,60** |

**Otimização conhecida, não implementada:** congelar 2025 como baseline derrubaria para ~US$ 3,80. Não fiz
para manter a coerência do bridge e a simplicidade do script. Se o refresh virar semanal, vale fazer.
**Refresh incremental de BPC** (só o mês novo) sai por ~US$ 0,27 se você trocar a janela.

**Sempre `dry_run` antes** se mexer em qualquer query. Acima de ~5 GB, confira antes de rodar.

---

## 9 · O que eu faria diferente (pendências reais)

1. **Virar skill.** O bloqueio de `.ps1` é o maior atrito operacional deste pipeline. O plugin `wbr-he`
   resolve exatamente esse problema e é o molde a copiar.
2. **Congelar 2025** para cortar ~35% do custo.
3. **Trazer as outras duas D1s.** Hoje o Grid é só Large Appliances. Small e Heating & Cooling usam a mesma
   estrutura — o filtro `$FILT` é o único ponto de mudança, mas os sanity checks precisam de novos valores
   de referência.
4. **Consolidar o BC dentro deste Grid.** Ficou como pendência declarada. A recomendação registrada é
   **docs separados com link** (este HTML já tem 31 MB; embutir mais abas fica insustentável).
5. **Validar capacidade de seller** com os cubos `seller_cap_cube` / `grupos_economicos` — eu queria fazer
   e não deu tempo. É o que responde "os grupos cotados conseguem entregar o que o BC promete?".
