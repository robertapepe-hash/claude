# Price Point — metodologia e as decisões que a sustentam

> Cada régua aqui foi escolhida contra uma alternativa razoável. Este documento registra **por que** —
> porque é isso que permite defender o número numa sala, e é isso que se perde quando alguém sai.
> Fonte completa: `originais/Metodologia_Price_Point.md` (16 seções, com o log de validações V1-V8).

---

## 1 · O que herdamos do time de Data, e o que é nosso

O ponto de partida foi o deck **BIDS - Price Point** (Commerce Business Insights & Data Science): uma
regressão **three-way fixed effects** sobre experimentos de rebate MLB 2025 cruzados com scraping
(9,9 mil itens), ponderada por visitas, com erros clusterizados por campanha.

| Elemento | Herdado? | O que é nosso |
|---|---|---|
| CVR, Treatment, `g`, `dist`, efeitos fixos | conceito | a fórmula operacional nas **nossas** tabelas |
| Limiares **4 / 5 / 10** | sim, como régua-padrão | testar se valem **por faixa de ASP** |
| Causalidade desconto → CVR para **> 70 USD** em MLB | sim, tomado como dado | — |
| Faixas de ASP | conceito, mas em USD | trocadas pelas do **Shield, em R$** |
| **Investimento em R$** | **não** — o deck não mede $ | inteiramente nosso |
| **Classificação da carteira viva** | não | inteiramente nosso |

> ⚠️ **O limite da herança causal.** Herdamos que **o mecanismo existe** acima de 70 USD. **Não** herdamos
> que o número exato seja 4/5/10 para Large — o "70+" deles é um balde aberto e não sabemos quanto dele é
> linha branca. Por isso existe a validação por faixa de ASP.

**Por que não reestimamos a causalidade:** não temos A/B próprio. Sem experimento, o honesto é aplicar o
veredito causal deles e assumir que o nosso é **associação ajustada**, não causa. Está declarado nas
limitações e sempre foi dito assim em apresentação.

---

## 2 · As decisões travadas (e a alternativa que foi descartada)

### 2.1 · Banda de posição = ±1%, não ±4%

O deck do Data usa ±4%. **Nós usamos ±1%** — a banda do BPC/Pricing.

**Por quê:** os ±4% servem para **correlacionar conversão** (abaixo disso o efeito não é detectável). Para
**classificar posição** — "estou caro ou barato?" — a régua que a casa inteira usa é ±1%. Misturar as duas
faz o funil deixar de conversar com o BPC.

### 2.2 · Grão = painel item-dia, com E sem rebate

**Alternativa descartada:** olhar só os dias com rebate.

**Por quê:** preço é por item e por dia, e **dias sem rebate carregam sinal** — podemos estar perdendo para
a concorrência sem ação nenhuma. Um recorte "só rebate" é cego para o problema mais barato de resolver.

### 2.3 · ASP de referência = preço MELI na **mesma janela**, não janela fixa anterior

Esta mudou no meio do caminho, e a mudança importa.

- **v1:** mediana do preço cheio numa janela fixa de 3 meses "normais" (fev/mar/abr 2026)
- **v2 (atual):** mediana da favorabilidade **na própria janela de análise** (Q2), com **fallback
  NMV/NSI** do `DM_EFICIENCIA` para cobrir todo item vendido

**Por quê:** com a janela fixa, itens novos ou de histórico curto ficavam **sem ASP** — R$ 40 Mi de gasto
não alocado. Com a janela própria + fallback, o "sem ASP" caiu para **R$ 0,1 Mi**. Buraco fechado.

> 🔑 **O que NÃO mudou, e não deve mudar: a faixa vem do preço CHEIO, não do praticado.** Usar o preço com
> rebate cria **circularidade** — o item mais rebatado cai numa faixa mais baixa por causa do próprio
> tratamento, e aí a faixa barata "parece" ter mais desconto por construção. Essa regra foi herdada do
> Shield e vale para qualquer análise que cruze preço com faixa.

### 2.4 · Investimento = só a porção MELI, sempre

O delta entre preço "de" e preço "por" é **cofinanciado** — parte MELI, parte seller. E o preço "de" pode
ter sido inflado pelo seller.

**Três regras que saem daí:**
1. **Investimento atribuído à MELI = só a porção MELI**, nunca o delta total
2. **Competitividade real = preço de chegada (POR)** — não é afetada por um "de" inflado, porque é o que o
   comprador efetivamente paga e compara
3. **A partida deve ser medida pelo preço em dias sem rebate**, não pelo `ORIGINAL_PRICE`

**A evidência que forçou a regra 3 (validação V8):** o "de" está inflado em mediana +3,5%, mas
**~49% dos itens acima de 5%** e **~25% acima de 20%** do preço real. Usar o "de" bruto distorceria a
partida de um quarto da base.

**Escala do cofinanciamento (HE, mai/26):** DXI MELI R$ 35,7 Mi contra R$ 249,1 Mi do seller — **a MELI
banca ~12,5%** do pré-acordo.

### 2.5 · Fonte primária = base validada do Pricing

**v1:** montar o painel do zero a partir de `DM_COM_COMPETENCIA` + `BT_COM_FAVORABILITY` + `DM_EFICIENCIA`.
**v2 (atual):** usar `SBOX_REVENUEMKPBR.SITUACAO_REBATE_TESTE` — a saída da query #7 do time de Pricing,
um pipeline de 7 etapas já chancelado.

**Por quê:** número que já foi validado pelo dono da métrica não precisa ser defendido duas vezes. E foi
auditado: `CP_INVESTMENTS_LC` em HE **é idêntico ao DXI** (35,65 = 35,65 Mi em mai/26).

⚠️ **O PIX (DXB-Pix) está FORA dessa base.** É camada nossa, à parte. Por isso o PIX é o passo 2 e não sai
de graça.

### 2.6 · Perímetro = 3P apenas

**1P tem DXI = DXB = 0.** Confirmado em HE mai/26: 1P fez R$ 530 Mi de GMV (~22% do total de HE) com
**R$ 0** de investimento auditado. O 1P move preço por margem interna, não por rebate rastreável.

**Consequência:** 1P entra como **contexto de competitividade**, nunca no denominador de eficiência de
investimento. A alavanca simplesmente não existe no dado.

### 2.7 · "Não vencedor" virou "com erro de leitura"

Renomeação deliberada. Item **sem preço de rival no dia** (`COMP_PRICE_RIVAL` nulo) **não é** um item que
continuou caro — é um item que não conseguimos avaliar.

**Por que a palavra importa:** chamar isso de "não venceu" inflava o desperdício aparente e levava a
conclusão errada — "gastamos mal" em vez de "não sabemos". São problemas diferentes, com donos diferentes.

---

## 3 · A estrutura do funil

### Camada 1 — partição de 100% do DXI

| Categoria | O que é |
|---|---|
| `exp→cheaper/match` ✅ | partiu caro e **virou** para barato ou empate |
| `exp→exp` ❌ | partiu caro e **continua caro** |
| `cheaper→cheaper` ⚠️ | **tóxico** — já era barato, o rebate não comprou posição |
| `fora do hound` | sem rival mapeado |
| `com erro de leitura` | rival mapeado mas sem preço capturado no dia |

**Transição:** partida = dia **antes** do rebate (`START_DATE_REBATE − 1`); chegada = durante.
⚠️ `exp→cheaper` **inclui empate** — o balde une cheaper + match. Separar exigiria ajuste no pipeline do
Pricing.

### Camada 2 — quebras por D1 / alavanca / faixa de ASP

**Só sobre os 3 baldes com status de preço.** Excluir `fora do hound` e `erro de leitura` aqui é
deliberado: eles são problema de **cobertura**, não de **competitividade**, e misturá-los contamina toda
comparação entre D1s ou alavancas.

**Alavancas (`DXI_CAMPAIGN_SUBTYPE`), composição HE mai/26:**
PRE_ACORDO **69,4%** · ON_DEMAND 15,0% · PRICING_MATCHING(_MELI_ALL) **~11,5%** · SMART_COFINANCED 4,2%

---

## 4 · Os três eixos de classificação (desenho completo, parcialmente executado)

O funil publicado implementa o **eixo 2**. Os eixos 1 e 3 estão desenhados e validados, mas não foram
executados — são o caminho natural de continuidade.

**Eixo 1 — Qualidade do investimento** (dias com rebate, caixas mutuamente exclusivas):

| Caixa | Regra | Leitura |
|---|---|---|
| Piso — já barato | `dist_partida ≤ −5%` | $ sem retorno |
| Gap pequeno | `0 < dist_partida < +4%` | fechar não move CVR |
| Landing alto | `dist_chegada > +10%` | aterrissou longe, uplift baixo |
| **Zona de uplift** ✅ | partida ≥ +4%, chegada ≤ +10%, partida > −5% | o bom |

**Eixo 2 — Transição** (é o funil publicado). A métrica-chave que eu queria:
`Σ $ de rebate cuja chegada NÃO é cheaper`, **vs Shopee**, aberto por faixa de ASP e lente box/PIX —
"dinheiro que não virou posição vencedora contra a Shopee". Revela o gasto que **ganha no box mas não no
PIX**, que é a tese do Shield quantificada em reais.

**Eixo 3 — Exposição** (dias **sem** rebate). Métrica = **visitas / % de SoV**, não R$ — não há gasto:

| Faixa | Leitura |
|---|---|
| `dist ≤ m` | **competitivo "de graça"** — ganhando sem gastar |
| match a +10% | ganho barato, rebate pequeno resolve |
| +10% até `teto_MELI` | recuperável **só com nosso lever** |
| `teto_MELI` a `teto_negociado` | recuperável **com deal cofinanciado** |
| acima disso | **estrutural** — fora do alcance de rebate (custo/sourcing) |

`teto_MELI` = p90 histórico da profundidade do rebate MELI por faixa · `teto_negociado` = p90 do desconto
total. **Use o p90 empírico, não palpite.**

> O eixo 3 é o que eu acho mais subaproveitado. Ele responde "onde estamos perdendo de graça" — e a
> resposta costuma ser mais acionável que o desperdício.

---

## 5 · Validações de dado — o que foi checado antes do primeiro número

Rodar número antes disso foi explicitamente proibido no desenho. Todas passaram:

| # | O que validou | Resultado |
|---|---|---|
| **V1** | `AMOUNT_REBATE_MELI` é por unidade? | ✅ sim — identidade MELI+seller = DE−POR, razão mediana 1,0 |
| **V1b** | Escala do cofinanciamento em HE | ✅ MELI ~12,5% do pré-acordo; DXB-Pix R$ 9,8 Mi, **fora** do `AMOUNT_REBATE_MELI` |
| **V2** | Cobertura de preço em box e PIX | ✅ **100%** para Shopee, Amazon e Magalu |
| **V3** | `DM_COM` × `BT_COM` batem? | ✅ **99,998%** dentro de 1%, mediana de diferença = 0, em ~1,05 Mi item-dias |
| **V4** | Rótulos exatos de D1 | ✅ do de-para oficial — **match exato, nunca `LIKE`** |
| **V7** | Excluir H&B? | ❌ **não** — consistente com o Shield |
| **V8** | O preço "de" é confiável? | ❌ **não** — inflado, ~25% dos itens acima de 20% |

---

## 6 · Limitações — declare sempre

1. **Sem A/B nosso, causalidade limpa não é reproduzível por nós.** O que fazemos é associação ajustada
   aplicando o veredito causal do Data.
2. Depende da **qualidade e cobertura do scraping** de preço — é exatamente o que os R$ 47 Mi de off-target
   revelam.
3. **Rebates bancados pelo seller ficam fora** do "$ MELI".
4. O *pooling* de HE assume efeito comparável entre subcategorias — por isso o ASP entra como **segmento**,
   não como premissa.
5. **CVR ainda não entrou.** O funil hoje mede posição, não conversão. Fechar essa ponte é o que
   transformaria o instrumento em medida de retorno de verdade.
