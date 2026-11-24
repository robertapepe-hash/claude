# Runbook — replicar o Price Point em outra vertical ou outro período

> O runbook completo, com as queries e o gerador de HTML prontos para colar, está em
> **`originais/HANDOFF_Tech_PricePoint.md`**. Ele foi escrito para que **outro time rodasse sozinho**, sem
> precisar falar comigo — e foi usado assim para Tech.
> Este documento é o mapa: o que fazer, em que ordem, e onde as pessoas costumam tropeçar.

---

## Antes de começar — três regras

**1. Crie um documento NOVO no Grid.** Nunca suba no Grid de outra pessoa. O layout de referência é o de HE
(`01KW89RWFKQ9YQQTJMSQRZYVEP`) — mas é **só referência visual**, os seus dados vão para o seu doc.
Não informe `doc_id` de ninguém: sem `doc_id`, o engine cria um documento seu.

**2. Custo antes de rodar.** `dry_run` sempre. O cubo principal dá **~30 GB** — acima de ~5 GB, mostre e
confirme antes de executar.

**3. Acesso.** As tabelas do Pricing (`meli-sbox.REVENUEMKPBR.*`) e as `meli-bi-data.WHOWNER.*` abrem via
**MCP `bigquery-meli`**. O `bq` CLI direto costuma ser **negado** no sandbox do Pricing — não insista.

---

## Passo 1 — Descobrir o `VERTICAL` e a frescor da base

⚠️ **Este passo não é burocracia.** A base do Pricing pode estar **congelada num dia recente** — a de HE
congelou em 12/jul. Se você assumir que ela tem o mês inteiro, seu MTD fica errado sem aviso nenhum.

```sql
SELECT VERTICAL, MAX(ORD_CLOSED_DT) AS max_dt,
  COUNTIF(ORD_CLOSED_DT >= DATE '2026-07-01') AS rows_jul
FROM `meli-sbox.REVENUEMKPBR.SITUACAO_REBATE_TESTE`
WHERE ORD_CLOSED_DT >= DATE '2026-06-01'
GROUP BY VERTICAL
ORDER BY rows_jul DESC
```

Anote o **nome exato** do `VERTICAL` e a `max_dt`. Ajuste a janela do MTD para terminar nesse dia.

---

## Passo 2 — O cubo

Uma query que devolve, por período × D1 × alavanca × faixa de ASP, os cinco valores do funil
(`total`, `exp→cheaper`, `exp→exp`, `cheaper→cheaper`, `fora do hound` — o "erro de leitura" é o resíduo).

**A estrutura tem três blocos:**
1. `asp_fav` — mediana do preço MELI na favorabilidade (box, produto), na janela de referência
2. `asp_ef` — fallback NMV/NSI do `DM_EFICIENCIA` (cobre item vendido sem favorabilidade)
3. `base` — a `SITUACAO_REBATE_TESTE` em `UNION ALL` de um período por seletor

**Os dois `asp_*` unidos por `FULL OUTER JOIN` são o que fecha o buraco do "sem ASP".** Não corte esse
pedaço para simplificar — foi ele que levou o não-alocado de R$ 40 Mi para R$ 0,1 Mi.

📄 SQL completo: `originais/HANDOFF_Tech_PricePoint.md` §Passo 2.

**O que trocar:**

| Trocar | Onde | Nota |
|---|---|---|
| `VERTICAL` | 3 lugares no `base`, 2 nos blocos de ASP | use o valor exato do Passo 1 |
| Datas | janelas do `UNION ALL` | ajuste o MTD à `max_dt` |
| Cortes de ASP | o `CASE` do `asp_band` | **veja abaixo** |

⚠️ **As faixas 200/500/1500/3000 são as de HE (Shield).** Verticais de ticket mais alto — Tech, por
exemplo — provavelmente precisam de cortes próprios. Manter as de HE dá comparabilidade entre verticais;
trocar dá resolução dentro da sua. **É uma escolha, faça conscientemente e declare qual usou.**

---

## Passo 3 — Gerar o HTML

Script Python que lê o resultado da query (`result.json`) e injeta num template, produzindo um HTML
autocontido com:
- **seletor de período** (Q2 · MTD · data dupla)
- **Camada 1** — as 5 categorias somando 100%, com filtros de D1 / ASP / alavanca
- **Camada 2** — quebras por D1, alavanca e faixa de ASP, com alternância entre tabela e barras

📄 Código completo: `originais/HANDOFF_Tech_PricePoint.md` §Passo 3.
📄 Exemplo do resultado: `dashboards/Funil_Box_Grid.html`.

**Ajuste no topo do script:** `RESULT`, `VERTICAL_NOME`, `OUT`.

---

## Passo 4 — Publicar

Peça ao Claude:

> *"publica o `Funil_Box_<vertical>.html` no Grid usando a skill `grid-sharing`, criando um documento NOVO
> (sem `doc_id`), título 'Price Point <Vertical> — Box (funil)'."*

O link que voltar é o seu documento.

---

## Onde as pessoas tropeçam

| Sintoma | Causa provável |
|---|---|
| Um pedaço grande do gasto cai em "Sem ASP" | os blocos `asp_fav`/`asp_ef` não foram unidos, ou a janela de referência não bate com a de análise |
| O MTD parece pequeno demais | a base do Pricing está congelada — você não conferiu a `max_dt` no Passo 1 |
| As categorias não somam 100% | o "erro de leitura" é resíduo (`total − ec − ee − cc − fh`), não uma coluna da query. Se der negativo, há duplicidade no join |
| A query passa de 30 GB | período largo demais, ou faltou filtrar `SIT_SITE_ID` / `MELI_ID_TYPE='PRODUCT'` nos blocos de ASP |
| Nada aparece no Grid | falta VPN, ou faltou `skill_version` no payload |

---

## O que o runbook de Tech **não** inclui

**A barra de competidor** (Amazon / Shopee / Magalu). Era específica de HE e foi deixada de fora para
simplificar. Para adicionar: um join com `BT_COM_FAVORABILITY` trazendo `COMP_SITE_ID_WINNER`.

**Vale a pena adicionar.** Foi essa barra que revelou que o rival do box é a Amazon e não a Shopee — o
achado mais importante da análise inteira.

---

## Para replicar na lente PIX (o passo 2 nunca executado)

Fontes, todas em `WHOWNER` — **não precisa do sandbox do Pricing**:

| Peça | Onde |
|---|---|
| Investimento | `DM_EFICIENCIA_MLB` · `DXB_INVESTMENT_LC` com `DXB_PAYMENT_METHOD='PIX'` · campanha em `DXB_CAMPAIGN_ID` |
| Posição | `BT_COM_FAVORABILITY` com `FAVORABILITY_TYPE='BOX_ALL_ABC_PIX'` · `MELI_ID_TYPE='PRODUCT'` |
| ASP de referência | mesma janela · mediana da favorabilidade PIX + fallback NMV/NSI |

**Mantenha a consistência com o box:** banda ±1% · mesmas faixas de ASP · mesmo funil (Camada 1 com 5
categorias somando 100%; Camada 2 só no hound) · a renomeação "erro de leitura" · foco no recorte
**Shopee-winner**.
