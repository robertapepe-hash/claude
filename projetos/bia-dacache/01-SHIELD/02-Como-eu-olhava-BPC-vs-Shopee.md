# Como eu olhava BPC vs Shopee

> A forma de leitura que virou padrão no squad Shield. Não é um template de slide — é a sequência de
> perguntas que eu fazia todo mês, e as armadilhas que aprendi a evitar no caminho.

---

## 1 · A sequência

Sempre nesta ordem. Pular etapa é como eu produzi as leituras erradas no começo.

```
   Onde estamos?          →  BPC total da D1, por faixa de ASP
        ↓
   De quem estamos        →  Share of Opportunity por competidor
   perdendo?                 (a Shopee é mesmo o problema?)
        ↓
   Em que lente?          →  BOX · SHP · PIX  (a resposta muda MUITO)
        ↓
   Onde exatamente?       →  faixa de ASP → D2 → marca → seller
        ↓
   Quanto vale mexer?     →  atribuição ponderada em pp
```

**A quarta etapa é onde mora o valor.** Dizer "o BPC de Large caiu 3 pp" não gera ação. Dizer "caiu 3 pp e
82% disso vem de duas marcas na faixa 500-1500, num único seller" gera.

---

## 2 · As três lentes — e por que a resposta muda entre elas

| Lente | `FAVORABILITY_TYPE` | O que compara |
|---|---|---|
| **BOX** | `BOX_ALL_ABC` | preço à vista |
| **SHP** | `SHP_ALL_ABC` | frete |
| **PIX** | `BOX_ALL_ABC_PIX` | preço com PIX aplicado |

⚠️ **PIX não é "BOX com desconto".** A metodologia aplica PIX **nos dois lados** — no nosso preço e no do
rival. Isso pode **trocar quem é o competitor winner** do item e, com isso, **inverter o sinal do MoM**.
Nunca leia um delta de PIX como se fosse o delta de BOX deslocado.

🔑 **A tese que fechou o Shield de Large:** a alavanca da Shopee **não é preço à vista nem sortimento — é
PIX, no premium, nas datas duplas.** Isso foi corroborado de forma independente pelo Price Point: no box,
o rival que aparece é a **Amazon**, e a Shopee é só 5-8% do gasto de rebate. Se você olhar só BOX, vai
concluir que a Shopee não é problema — e vai estar olhando a guerra errada.

---

## 3 · Winner view vs UNNEST view — a distinção que mais gera erro

São perguntas diferentes, não graus de precisão.

| | Winner view | UNNEST view |
|---|---|---|
| **Como** | `COMP_SITE_ID_WINNER = 'SPE'` (top-level) | `UNNEST(COMPETITORS) c WHERE c.COMP_SITE_ID = 'SPE'` |
| **Considera** | só quando a Shopee é o **melhor** rival do match | **todas** as visitas em que a Shopee aparece |
| **Responde** | "onde a Shopee está ganhando de nós e quanto custa reverter" | "qual a presença total da Shopee no universo" |
| **Use para** | **oportunidade**, SoO, War Room | dimensionamento, cobertura |

A Winner view é um **subconjunto** da UNNEST. Para leitura de oportunidade — que é 90% do que o squad
pede — **use Winner view**.

⚠️ Dentro do array `COMPETITORS`, o campo de preço chama **`COMP_ITEM_PRICE`**. No nível raiz chama
`COMP_PRICE_RIVAL`. Nomes diferentes para a mesma ideia; já me custou uma query silenciosamente errada.

---

## 4 · As métricas, e o que cada uma esconde

| Métrica | Fórmula | Cuidado |
|---|---|---|
| **BPC** | `(VISITS_CHEAPER + VISITS_EQUAL) / VISITS_MATCH` | ↑ melhor. É **ponderado por visita**, então um item de cauda longa não move nada |
| **Opportunity** | `VISITS_EXPENSIVE / VISITS_MATCH` = `1 − BPC` | — |
| **SoO** (Share of Opportunity) | `VISITS_EXPENSIVE do competidor X / VISITS_MATCH total da D1` | Soma dos SoO de todos os competidores = `1 − BPC` da D1. Serve de check |
| **MS Ratio** | `Market Share Shopee / Market Share Meli` | ↓ melhor. **É isso mesmo — não é NSI ratio** |
| **SOB** | Share of Business | Share **of Business**, não *of Bidding* |
| **Atribuição ponderada** | `Δbpc_unidade × (visits_unidade / visits_universo)` | É o que traduz "essa célula move quanto pp da vertical" |

**Cascata de impacto** — como eu dimensionava um movimento até a vertical:

```
+X pp de BPC numa célula, vs competidor C
  → impacto no agregado vs C  = X × (visits_célula / total_vs_C)
  → impacto na vertical       ≈ X × (visits_célula / total_vs_C) × (vs_C / total_vertical)
```

---

## 5 · Faróis semafóricos (o status competitivo do squad)

| Farol | Critério |
|---|---|
| 🔴 **Issue** | tendência MELI negativa **e** Shopee positiva |
| 🟡 **Attack** | tendências iguais, Shopee ganha MS Ratio **e** Ratio > 10% |
| ⚪ **Wait & See** | tendências iguais, Shopee ganha MS Ratio **e** Ratio < 10% |
| 🟢 **Controlled** | MELI melhor que Shopee, ou iguais e Shopee não ganha mais de +0,5 pp |

---

## 6 · Convenções de filtro do Shield (diferentes do War Room!)

Este é um ponto que confunde quem vem do War Room de PIX KMI.

| | Shield | War Room PIX KMI HE |
|---|---|---|
| `KMI` | **sem filtro** | `= 'true'` |
| H&B (`FLG_BULKY`) | **sem filtro** | sempre fora |
| Vertical | H&T (HE + Tech) | só HE |
| Faixa de ASP | eixo principal | secundário |

**No Shield, tudo entra na conta** — a menos que alguém peça explicitamente o contrário. Era convenção
minha e está documentada em `originais/Shield_Shopee_Contexto_Mestre.md`.

**Sempre presente, dos dois lados:**
- `SIT_SITE_ID = 'MLB'`
- `MELI_ID_TYPE = 'PRODUCT'` — é **cluster field**: corta 60-70% do scan e é o que salva quando a query
  bate no teto de 100 GB
- Marca: `UPPER(COALESCE(REAL_BRAND, BRAND))` — e **liste as duas grafias** de marcas com acento
  (`'BRITÂNIA','BRITANIA'`), porque a base tem as duas

---

## 7 · Armadilhas que me custaram retrabalho

1. **Scraper de frete perde competidor.** Em `SHP_ALL_ABC`, competidores somem em datas específicas —
   Magalu sumiu em maio inteiro, Shopee sumiu em 03/03 inteiro. **Sempre confira o volume de `VISITS_MATCH`
   antes de ler um delta de frete.** Um "ganho" gigante costuma ser ausência de rival, não vitória.
2. **`3P` não é a mesma coisa que "não-1P".** `ITEM_PARTY_TYPE='3P'` exclui CBT;
   `SEGMENTO_SELLER_DETAIL != 'FIRST PARTY'` inclui CBT, que **puxa o BPC para baixo**. Escolha conforme a
   pergunta e **declare qual usou**.
3. **`MELI_ID` é produto, `ITE_ITEM_ID` é anúncio do seller.** Quando alguém manda uma lista de IDs,
   quase sempre são `MELI_ID`. Agregue com `MELI_ID_TYPE='PRODUCT'`.
4. **`KMI`, `FLG_BULKY`, `FLG_COMP_1P` são STRING lowercase**, nunca booleano. Filtro canônico de "sem H&B":
   `COALESCE(FLG_BULKY,'false') != 'true'`.
5. **Americanas (`AMR`) está excluída** de todas as análises, por decisão minha — share irrelevante.
   Se alguém reintroduzir, as séries históricas deixam de ser comparáveis.
6. **MoM sempre em pp**, nunca em decimal. Ao escrever em XLSX/PPTX, multiplique por 100.

---

## 8 · Templates de query reutilizáveis

Estão prontos, comentados, em **`originais/Shield_Shopee_Contexto_Mestre.md` §8**:

| Template | O que faz |
|---|---|
| **A** | BPC por D1 × período × competidor (UNNEST view) |
| **B** | Bloco preto — Winner view + Share of Opportunity |
| **C** | Snippet de buckets de ASP |
| **D** | Filtro de marca com variações de acento |
| **E** | Agrupamento de sellers por `CUS_CUST_ID_SEL` |

O de-para completo de competidores, marcas analisadas, grupos de seller e os 16 `MELI_ID` do deep dive
item-level também estão lá.
