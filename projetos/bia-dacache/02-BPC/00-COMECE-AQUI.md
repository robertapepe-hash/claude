# BPC — comece aqui

> **BPC = Buyer Price Competitiveness.** Mede em quantas visitas com match de catálogo o MELI está com
> preço **menor ou igual** ao do competidor. Quanto maior, melhor.
>
> Fui focal de BPC da vertical **Home Electronics em MLB** de 2025 a setembro/2026.

---

## O que tem nesta pasta

| Documento | O que é |
|---|---|
| **`01-Manual-BPC.md`** | O canon: fórmulas, tabelas, filtros e as 16 regras que não estão no catálogo de dados |
| **`02-Analises-que-eu-fiz.md`** | Inventário do que foi produzido, com o achado de cada uma e onde está |
| `adhoc-bb-bpc-reputacao/` | Ad hoc jun/2026 — reputação → Buy Box → BPC → venda |
| `adhoc-entrada-casas-bahia/` | Ad hoc mai/2026 — a entrada da Casas Bahia no 3P foi incremental? |
| `originais/` | Os documentos-fonte, sem edição |
| `entregaveis/` | `Guia_BPC_Time.docx` — o guia que escrevi para o time |

---

## Antes de escrever a primeira query

**1. Consulte a skill `bpc-reader` primeiro.** É o canon oficial do time de Pricing — tabelas, fórmulas e
o mapa de `FAVORABILITY_TYPE` por site. Uma cópia local está em `originais/bpc-reader_SKILL.md`, mas
**use a skill instalada, não a cópia** (a cópia envelhece).

**2. A fórmula é sempre esta:**
```sql
BPC = SAFE_DIVIDE(SUM(VISITS_CHEAPER + VISITS_EQUAL), SUM(VISITS_MATCH))
```
Tudo o mais é recorte.

**3. Saiba em qual das duas frentes você está.** Elas têm convenções *opostas* de filtro:

| | **War Room PIX KMI HE** | **Shield vs Shopee** |
|---|---|---|
| Metodologia | `BOX_ALL_ABC_PIX` | as 3 lentes (BOX · SHP · PIX) |
| `KMI` | `= 'true'` (obrigatório) | **sem filtro** |
| H&B (`FLG_BULKY`) | sempre fora | **sem filtro** |
| Vertical | só HE | H&T (HE + Tech) |
| Eixo principal | D1 → D2 → marca → seller | **faixa de ASP** |
| Público | War Room / liderança HE | squad Shield / liderança H&T |

Rodar um número do Shield com os filtros do War Room (ou o contrário) produz um resultado que parece
plausível e está errado. **Sempre declare qual convenção usou.**

---

## As duas frentes, em uma frase cada

### A · War Room BPC PIX KMI HE
Fechar o gap de competitividade em PIX KMI de Home Electronics, atacando o ofensor estrutural do momento.
Filtros travados (PIX + KMI true + sem H&B + vertical HE + 6 D1s), drill de
**D1 → D2 → marca → seller** e cascata de impacto ponderado até a vertical.

⚠️ **A hipótese de foco é móvel, não dogma.** Quando saí, era **MGL Winner → Small Appliances → Kitchen →
Mondial**. A liderança redireciona; o *método* é que é estável.

### B · Shield vs Shopee
Apoio analítico ao squad, com leitura por faixa de ASP e as 3 lentes.
📁 Está documentado em **`../01-SHIELD/`** — inclusive os templates de query.

---

## O insight que eu levaria comigo

**A lente PIX pode inverter o sinal do que você lê no BOX.** `BOX_ALL_ABC_PIX` aplica PIX **nos dois
lados** — no nosso preço e no do rival — e isso **troca quem é o competitor winner** do item. Um MoM
positivo em BOX pode ser negativo em PIX, sobre o mesmo universo.

No Brasil, **PIX é o preço-âncora**. Por isso MLB usa `BOX_ALL_ABC_PIX` para BOX, KMI, KC e Vertical —
enquanto o allMeli usa `BOX_ALL_ABC` (para não duplicar entre sites).

Isso não é detalhe técnico: foi o que sustentou a tese de que **a briga com a Shopee é no PIX, não no
preço à vista** — confirmada de forma independente pelo Price Point, onde o rival do box aparece sendo a
**Amazon** e a Shopee é só 5-8% do gasto de rebate. Ver `../03-PRICE-POINT/`.

---

## Contexto de negócio herdado (setembro/2026)

O estado abaixo é de mai-jun/2026 e **envelhece rápido** — trate como ponto de partida, não como verdade.

- BPC HE PIX KMI sem H&B ≈ **47%**
- BPC vs MGL Winner em HE = **32,8%** — MGL Winner pesa ~20% das visitas de HE
- **D1 foco:** Small Appliances (50% do universo vs MGL) → **D2:** Kitchen (74% de Small) → **marca:**
  Mondial (97% das visitas Mondial-em-Small estão em Kitchen, BPC vs MGL de 17,8%)
- **Próxima onda de marca:** Electrolux
- **Quick wins de paridade em aberto:** `LOJAGAZIN` (BPC ~8%) e `VGSHOPOFICIAL` (BPC ~5%) — BPC baixo
  demais para ser real, provável **erro sistêmico de catálogo**. Vale auditar antes de tratar como
  problema comercial.

---

## Pendências que deixo

1. Auditoria de paridade de `LOJAGAZIN` / `VGSHOPOFICIAL` (provável erro de catálogo, não de preço)
2. Elegibilidade de PIX Match dos sellers prioritários — precisa do time de Pricing
3. Confirmar em produção o valor exato de `COMP_RIVAL_NAME_WINNER` para Casas Bahia
4. Onda Electrolux (2ª marca prioritária depois de Mondial)
