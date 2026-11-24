# O que é cada arquivo desta pasta

---

## Pipelines (rodam ponta a ponta)

| Arquivo | O que faz |
|---|---|
| **`refresh_shield_large.ps1`** | **O motor do Grid Shield por ASP** (`01KXKJP50WAQ314W1MVQXD4SRZ`). Reconstrói os 14 cubos, injeta no template e sobe nova versão no Grid. 📖 Documentado em `../01-Ways-of-Working-Grid-Shield.md` |
| **`motor_d1_cheia.ps1`** | **O motor do forecast do BC Shopee** (`01M0DSBDBHEAV3650Q913YSP6Y`), versão atual — em **D1 cheia**. Ajusta as duas regras, combina, projeta e roda a validação contra o realizado |

---

## Histórico do método de forecast

Ficam como registro de como o motor evoluiu. **Não use para gerar número novo** — o vigente é o
`motor_d1_cheia.ps1`.

| Arquivo | O que foi |
|---|---|
| `motor_v2_forecast.ps1` | decomposição multiplicativa (nível × tendência × sazonalidade). Foi onde se descobriu que **L3M (N=3) vence** como janela de nível |
| `motor_v3_hc_e_combinacao.ps1` | H&C em 3 visões + a **combinação de previsões** que virou caso-base |
| `estima_phi_backtest.ps1` | estima o amortecimento **φ** por D1 e roda o backtest (ajusta até dez/25, projeta jan-jun/26, mede o erro) |

---

## Queries do BC Shopee

| Arquivo | O que faz | Onde trocar para reusar |
|---|---|---|
| **`query_shopee_loja_x_asp.sql`** | Faturamento e peças **da Shopee por loja × faixa de ASP**, dos 3 últimos meses fechados da própria base. Fonte: `DM_YIPIT_SHOPEE_ITEMS` | **só o CTE `params`** — é o único lugar com nome de categoria |
| **`queries_replicar_aba_sellers.sql`** | Replica a **aba 3 (migração dos sellers)** em outras D1s. Escrita para TVs e Áudio | **só a lista de D1** nas queries A, B e C |
| `perfil_d1.sql` | Quais D1s existem na base do Planning e qual o TGMV/GMV de cada uma | — |
| `perfil_faixas.sql` | O de-para entre `FAIXA_ASP_NOVA` e `FAIXA_ASP`, com o GMV de mercado de cada | — |
| `perfil_tempo.sql` | **Até quando a base do Planning vai** e quando foi atualizada | — |

> 🔑 **Rode os três `perfil_*.sql` antes de qualquer janela nova.** A base do Planning tem lag de ~2 meses
> e o Yipit fecha um mês antes do DM Eficiência. Foi assumir frescor sem conferir que já me gerou uma
> comparação de 2 meses contra 3.

---

## Cubos de affordability e de capacidade de seller

| Arquivo | O que faz |
|---|---|
| **`q_afford_mon.sql`** | Cubo **mensal de affordability**: NMV por **faixa de ASP × grupo econômico × meio de pagamento**. Separa **Pix incentivado** (`DXB_PAYMENT_METHOD='PIX'`) de **Pix orgânico**, além de Crédito, Meli Saldo e Mercado Crédito |
| **`q_afford_dd.sql`** | O mesmo cubo, mas **por dia** — para ler datas duplas |
| **`q_sellercap.sql`** | Cubo **Seller-Helper**: capacidade dos sellers da Carteira Assessorada, agrupados por grupo econômico. É a base da pendência *"os grupos cotados conseguem entregar o que o BC promete?"* |

> 🔑 **Por que a separação Pix incentivado × orgânico importa:** é ela que permite ver se a competitividade
> em Pix está sendo **comprada** (incentivo) ou é **estrutural** (o comprador escolhe Pix sozinho). Isso
> conversa direto com a tese do Shield — que a briga com a Shopee é no Pix — e com o passo 2 do Price Point.

---

## Geradores e de-para

| Arquivo | O que faz |
|---|---|
| `gen_afford_sql.py` | Gera as `q_afford_*.sql` a partir do `grupos_economicos.csv` (monta o `STRUCT` do de-para dentro da query) |
| `gen_sellercap_sql.py` | Gera a `q_sellercap.sql` **a partir de uma planilha** e salva o de-para em CSV |
| `grupos_economicos.csv` | De-para `cust_id` → grupo econômico, versão ampla (inclui Casas Bahia, EFACIL, XCOMM, WEBFONES e outros) |
| `depara_grupos_economicos.csv` | De-para enxuto, **só os grupos cotados do BC** |

⚠️ **Os dois `gen_*.py` têm caminhos fixos da minha máquina** (incluindo uma pasta de scratchpad que não
existe mais). O `gen_sellercap_sql.py` lê de
`C:\Users\bdacache\Documents\grupos economicos - foco bc.xlsx`, que **não está neste pacote** — peça a
planilha junto com as pastas de projeto (ver `../../00-OUTROS/INDICE-DEMAIS-PROJETOS.md`).
Ajuste os caminhos no topo dos scripts antes de rodar.

⚠️ **Os dois CSVs de grupo econômico não são intercambiáveis.** Se você trocar um pelo outro, muda a
lista de grupos do BC — e foi exatamente uma lista de grupos desatualizada que gerou o erro mais grave da
auditoria de 21/08. Ver `../03-Business-Case-Shopee.md` §7.

---

## Antes de rodar qualquer coisa aqui

- **VPN corporativa** (para subir no Grid) e **`gcloud auth login`** (para o `bq`)
- **`dry_run` primeiro.** Acima de ~5 GB, confira antes
- `.ps1` está **bloqueado por SRP/GPO** nesta máquina — rode a lógica inline ou transforme em skill
- Force UTF-8 antes do `bq` e **achate o SQL em uma linha** (PS 5.1 trunca multi-linha como argumento de `.exe`)

📖 Os detalhes e as outras armadilhas estão em `../04-Armadilhas-e-licoes.md`.
