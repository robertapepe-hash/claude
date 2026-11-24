# Handover — Beatriz Dacache · Pricing & Selection HE

> Pacote de transferência de conhecimento dos projetos que desenvolvi como analista sênior de categoria em
> **Home Electronics (MLB)**, focal de **Pricing** e **Selection**.
> Montado em **setembro/2026**, na minha saída do time.

---

## Para que serve este pacote

Não é um arquivo morto. É o **manual de operação** dos três projetos que mais consumiram tempo e que
deixam método reaproveitável: como as análises foram construídas, quais decisões foram travadas e por quê,
quais armadilhas custaram caro, e o que precisa ser refeito antes de a próxima pessoa apresentar qualquer
número para a liderança.

Cada pasta tem um **`00-COMECE-AQUI.md`**. Se você só tem 15 minutos, leia os três e pare.

---

## Como navegar

| Pasta | Tema | Leia se você… |
|---|---|---|
| **[01-SHIELD](01-SHIELD/)** | Shield Against Asians — MELI vs Shopee em Home | …vai tocar o Grid do Shield por ASP, o **Forecast BC Shopee** (ratio MELI × Shopee e projeção), ou precisa entender a leitura por faixa de ASP |
| **[02-BPC](02-BPC/)** | Buyer Price Competitiveness — canon, War Room e análises ad hoc | …vai escrever qualquer query de BPC, tocar o War Room PIX KMI, ou reaproveitar as análises de reputação/Buy Box e da entrada da Casas Bahia |
| **[03-PRICE-POINT](03-PRICE-POINT/)** | Price Point BR — funil de eficiência do rebate | …vai medir para onde vai o investimento de rebate, ou quer replicar o funil em outra vertical |
| **[00-OUTROS](00-OUTROS/)** | Índice dos demais projetos | …procura WBR-HE, KIs Selection ou Built In e quer saber onde está e quem deveria pegar |

Dentro de cada pasta:

- **`00-COMECE-AQUI.md`** — resumo executivo: o que é, estado, o que herdar, o que refazer
- **documentos numerados** — método, decisões, armadilhas (escritos para este handover)
- **`originais/`** — os documentos-fonte como eu os mantinha, sem edição
- **`queries-e-scripts/`** — SQL, PowerShell e Python que rodam de verdade
- **`dashboards/`** e **`entregaveis/`** — os produtos finais (HTML, PPTX, XLSX)

---

## Tem um link de Grid e não sabe onde ele está documentado?

Os documentos do Grid MELI são identificados por um código na URL
(`grid.adminml.com/d/`**`<código>`**`/view`). Procure o código aqui:

| Código do Grid | O que é | Documentado em |
|---|---|---|
| `01KXKJP50WAQ314W1MVQXD4SRZ` | **Shield por ASP** — venda, competitividade e demanda de Large por faixa de preço | [`01-SHIELD/01-Ways-of-Working-Grid-Shield.md`](01-SHIELD/01-Ways-of-Working-Grid-Shield.md) |
| `01M0DSBDBHEAV3650Q913YSP6Y` | **Forecast BC Shopee** — ratio MELI × Shopee por grupo de seller e projeção | [`01-SHIELD/03-Business-Case-Shopee.md`](01-SHIELD/03-Business-Case-Shopee.md) *(o §11 mapeia cada aba ao arquivo que a gera)* |
| `01KW89RWFKQ9YQQTJMSQRZYVEP` | **Price Point — funil do box** | [`03-PRICE-POINT/`](03-PRICE-POINT/) |
| `01KTQ0V4038G3ZPZQ8FHFEHQ3A` | **WBR-HE** — report semanal (doc fixo, mesmo link toda semana) | [`00-OUTROS/`](00-OUTROS/INDICE-DEMAIS-PROJETOS.md) §1 |
| `01KS3ECPZVB6MS44T3KP00MFFS` | **KIs Selection Shopee** — perfil dos itens FOUND | [`00-OUTROS/`](00-OUTROS/INDICE-DEMAIS-PROJETOS.md) §3 |
| `01KSNVEDM1H8Y8CZ41X0HE31FJ` | KIs Selection — **doc de teste** (rascunho, não é o oficial) | idem |
| `01KS5XRQ9BY2VSX5W46EWBDF2T` | Deck Shield **HE** mai/26 | `01-SHIELD/entregaveis/` |
| `01KS5XRZEWWNM3T7QVHAKHBF3M` | Deck Shield **Tech** mai/26 | `01-SHIELD/entregaveis/` |
| `01KXPCDFV8…` | **MBR HE** — BPC por ASP + cobertura Shopee | [`02-BPC/02-Analises-que-eu-fiz.md`](02-BPC/02-Analises-que-eu-fiz.md) §C |

⚠️ **Cuidado com os apelidos.** O mesmo projeto costuma ter três nomes — o que eu falava, o nome da pasta e
o título dentro do Grid. O caso mais confuso é o `01M0DSBDBHEAV3650Q913YSP6Y`: **Forecast BC Shopee** =
**Plano de Combate BC** = **BC Shopee**. São a mesma coisa.

---

## Três coisas que valem para os três projetos

**1. O documento-fonte manda, não o slide.** Toda análise aqui tem um `.md` de premissas que é a fonte da
verdade. Quando o slide e o documento divergirem, o documento está certo — o slide envelhece mais rápido.

**2. Nada aqui é causal.** Nenhuma dessas análises teve teste A/B. São diagnósticos correlacionais bem
construídos, com limitações declaradas. Sempre que forem apresentadas como prova de causa, alguém vai
perguntar e a resposta honesta é "não é". As limitações estão escritas em cada projeto — use-as.

**3. Convenções de output que a liderança de HE já espera.** Absolutos em K/Mi/Bi · percentuais com 1 casa
e vírgula (47,1%) · deltas sempre em **pp** com sinal (+8,3 pp) · visitas em % de SoV com o absoluto
abreviado entre parênteses · insight primeiro, suporte depois.

---

## O que este pacote NÃO tem

- **Bases de dados brutas.** Os cubos (`.csv`/`.json`) ficaram de fora — juntos passam de 400 MB e a maioria
  vira dado velho em um mês. Todos são **regeneráveis** pelos scripts em `queries-e-scripts/`.
- **Acessos.** BigQuery (`meli-bi-data.WHOWNER`, `SBOX_*`), Grid e o sandbox do time de Pricing precisam ser
  pedidos em nome de quem assumir. Ver o bloco "Acessos necessários" abaixo.
- **Os decks apresentados à liderança H&T.** Estão no Drive do squad, não comigo.

---

## Acessos necessários para dar continuidade

| O quê | Para quê | Como conseguir |
|---|---|---|
| BigQuery `meli-bi-data.WHOWNER` | Praticamente tudo (favorabilidade, eficiência, visitas) | Ticket Shield / skill `bigquery-meli` |
| BigQuery `SBOX_MKPBR.DM_MARKET_ASP_*` | Base de mercado do Planning (Shield/BC) | Pedir ao time de Planning · leitura só via MCP em conta pessoal |
| BigQuery `meli-sbox.REVENUEMKPBR.*` | Base validada do Pricing (Price Point) | Pedir ao time de Pricing · `bq` CLI direto costuma ser negado, usar MCP |
| Grid MELI (`grid.adminml.com`) | Publicar e versionar os dashboards | Já é padrão MELI · precisa de **VPN corporativa** para o upload |
| Skill `bpc-reader` | Canon oficial de BPC do time de Pricing | Plugin oficial MELI |

---

## Quem procurar

| Assunto | Pessoa |
|---|---|
| Squad Shield / War Room H&T | Julia de Cassia Arcoverde (organiza o squad) |
| Liderança Large Appliances | Maira Fanchin Garcia |
| Brands / marcas prioritárias | Sebah Marques |
| Farming / carteira Asesorado PF | Felipe Lopardo |
| BPC Tech (o par do meu escopo em HE) | Lucas Kotinda |
| Laundry & Refrigeration (D2s vizinhas) | Nicole Freire Anjos |
| KIs Selection — NOT FOUND | Pedro Henrique de Araujo Baldi |

---

*Beatriz Dacache · beatriz.dacache@mercadolivre.com · setembro/2026*
