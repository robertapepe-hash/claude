# PRICE POINT BR — comece aqui

> **A pergunta:** de todo o rebate que investimos, **quanto virou posição vencedora de preço** — e quanto
> foi para itens que já estavam baratos, que continuaram caros, ou que nem tinham rival para comparar?

🔗 **Grid (funil do box):** https://grid.adminml.com/d/01KW89RWFKQ9YQQTJMSQRZYVEP/view
📄 **Metodologia completa:** `originais/Metodologia_Price_Point.md`
📄 **Runbook para replicar em outra vertical:** `originais/HANDOFF_Tech_PricePoint.md`

---

## O que é (e o que não é)

**Nasceu** como uma "foto do desperdício" — um número único de quanto rebate foi jogado fora.

**Virou** outra coisa, por decisão minha depois da pausa de junho/2026: **um instrumento perene de
inteligência de preço × conversão para Home Electronics.** Ele diagnostica onde nosso preço e nosso
investimento ganham ou perdem conversão, acompanha no tempo, gera plano e mede impacto — com foco em
**ganhar da Shopee**. A quantificação do desperdício virou **um dos outputs**, não o fim.

Isso importa para quem assumir: **não trate como análise encerrada.** A estrutura foi montada para rodar de
novo todo trimestre.

---

## O funil, em uma tela

Todo o investimento de rebate box (DXI) se parte em **5 categorias que somam 100%**:

```
                          R$ 113,8 Mi  (Q2 2026, HE, 3P)
                                 │
     ┌───────────────────────────┼───────────────────────────┐
     │  COM leitura de preço     │   SEM leitura de preço    │
     │  R$ 66,6 Mi               │   R$ 47,0 Mi  (off-target)│
     │                           │                           │
     ├─ exp→cheaper/match  ✅    │   ├─ fora do hound  16,2  │
     │     VIROU                 │   └─ erro de leitura 30,8 │
     ├─ exp→exp           ❌     │                           │
     │     continua caro         │   "problema de cobertura, │
     └─ cheaper→cheaper   ⚠️     │    não de competitividade"│
           tóxico: já era barato │                           │
```

**A separação entre as duas colunas é o coração do desenho.** Misturar "gastei e não virou" com "gastei e
não consigo nem saber se virou" produz um número de desperdício inflado e indefensável.

---

## Os quatro achados do Q2 2026 (box, HE, 3P)

1. **R$ 47 Mi (41% do gasto) é off-target** — sem rival mapeado no dia. Isso não é ineficiência de preço, é
   **buraco de cobertura de dado**. É a primeira coisa a atacar, e não custa verba nenhuma.

2. **PM (price matching) é a alavanca mais eficiente — vira ~55%.** É a campanha do time de Pricing, onde a
   MELI banca mais por causa do **PM100%** (cobrimos 100% do gap).

3. **Pré-acordo domina o gasto e vira só ~22%.** É onde mora a oportunidade de realocação: o balde grande é
   o menos eficiente.

4. 🔑 **O rival do box é a Amazon, não a Shopee.** A Shopee é só 5-8% do gasto de rebate no box.
   **Isso confirma, por um caminho totalmente independente, a tese do Shield: a briga com a Shopee é no
   PIX.** Duas análises diferentes, com fontes diferentes, chegando na mesma conclusão — foi o achado que
   mais me deu confiança no diagnóstico.

---

## Estado quando saí

| Camada | Status |
|---|---|
| **Box (DXI)** | ✅ **Fechado e publicado.** Base validada pelo Pricing, funil no Grid com seletor de período (Q2 · julho MTD · 07/07) |
| **PIX (DXB-Pix)** | 🔵 **Kickoff pronto, não executado.** É o passo 2 — e é onde deve morar a disputa com a Shopee |
| **CVR (conversão)** | ⏸️ **Adiado**, dependia de validação com o time de Data |
| **Replicação em Tech** | 📄 **Runbook escrito e entregue** para outro time rodar sozinho |

---

## Ordem de leitura

| Documento | Quando |
|---|---|
| **`01-Metodologia-e-decisoes.md`** | Antes de mexer em qualquer número — explica *por que* cada régua é o que é |
| **`02-Runbook-replicar.md`** | Quando quiser rodar em outra vertical ou outro período |
| `originais/Metodologia_Price_Point.md` | A fonte completa: 16 seções, todas as decisões travadas e as validações V1-V8 |
| `originais/HANDOFF_Tech_PricePoint.md` | O runbook original com as queries e o gerador de HTML, prontos para colar |

---

## O primeiro trabalho de quem assumir

**Fazer o PIX.** O kickoff está escrito (`originais/Metodologia_Price_Point.md` §16), as fontes estão
identificadas e todas são `WHOWNER` — não precisa do sandbox do Pricing:

- **Investimento PIX** = `DM_EFICIENCIA_MLB`, `DXB_INVESTMENT_LC` com `DXB_PAYMENT_METHOD='PIX'`
  (~R$ 9,8 Mi/mês em HE, ~27% do DXI)
- **Posição PIX** = `BT_COM_FAVORABILITY` com `FAVORABILITY_TYPE='BOX_ALL_ABC_PIX'`
- **ASP de referência** = mesma janela, mediana da favorabilidade PIX + fallback NMV/NSI

**A decisão que ficou para o próximo chat:** fazer o **PIX "leve"** (posição caro/empate/barato em ±1% +
gasto DXB-Pix, por ASP × alavanca × competidor, com foco no recorte Shopee-winner) — **é a minha
recomendação** — ou o **PIX "completo"** (replicar também a transição partida→chegada, bem mais caro,
porque o Pricing **não entrega PIX pronto** e teríamos que reconstruir).
