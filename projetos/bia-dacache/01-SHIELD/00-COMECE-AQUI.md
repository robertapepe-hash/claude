# SHIELD — comece aqui

> **Owner até setembro/2026:** Beatriz Dacache · **Escopo dela:** Home Electronics (Tech era com Lucas Kotinda)

---

## O que "Shield" quer dizer aqui

O nome cobre **três coisas diferentes** que nasceram juntas e foram se separando. Confundir uma com a outra
é o erro mais comum de quem chega — cada uma tem fonte, régua e público próprios.

| # | O quê | Pergunta que responde | Produto |
|---|---|---|---|
| **1** | **Shield Against Asians** (o squad original) | *Nosso preço está pior que o da Shopee, onde?* | Deck/XLSX mensal para a liderança H&T |
| **2** | **Grid Shield por ASP** | *Como Large Appliances se comporta por faixa de preço — venda, competitividade e demanda?* | Dashboard perene no Grid, atualizado por script |
| **3** | **Forecast BC Shopee**<br>*(= "Plano de Combate BC")* | *Quanto a Shopee está tomando de nós em Home, e como estaremos daqui a alguns meses?* | Business Case com projeção, no Grid |

**O #1 é competitividade de preço (BPC). O #3 é faturamento e share.** Não são a mesma métrica e não se
somam. O #2 é a casa onde os dois se encontram, por faixa de ASP.

---

## Estado de cada um (setembro/2026)

### 1 · Shield Against Asians — **cadência viva, entregável não-fixo**

Acompanhamento mensal de BPC vs Shopee (`SPE`) e Amazon (`AMB`), vertical H&T, por 3 lentes
(**BOX** preço à vista · **SHP** frete · **PIX**) e 5 faixas de ASP. Entregável é um PPT no fim do mês.

⚠️ **Não existe template fixo — e isso é de propósito.** Cada mês ataca uma célula crítica diferente. Quem
assumir vai querer criar um template; minha recomendação é **não criar**, e sim manter o método
(3 lentes × 5 faixas × Winner/UNNEST) e deixar o recorte seguir a pergunta do mês.

📁 Contexto completo em `originais/Shield_Shopee_Contexto_Mestre.md` — inclui os templates de query
reutilizáveis (A a E), os faróis semafóricos e as 14 regras de negócio.
📁 Últimos entregáveis em `entregaveis/` (deck HE e Tech de mai/2026, XLSX v4 por D1).

### 2 · Grid Shield por ASP — **pipeline perene, roda quando você mandar**

🔗 https://grid.adminml.com/d/01KXKJP50WAQ314W1MVQXD4SRZ/view

É o ativo mais reaproveitável que deixo. Um único script reconstrói **tudo**: 5 cubos de venda,
6 cubos de BPC e 3 cubos de demanda/conversão, injeta num template HTML e sobe nova versão no Grid.
Custa ~**US$ 6** por refresh e leva alguns minutos.

📖 **`01-Ways-of-Working-Grid-Shield.md` é o documento mais importante desta pasta.** Leia antes de tocar
em qualquer coisa.

### 3 · Forecast BC Shopee — **congelado com pendências conhecidas** 🔴

🔗 https://grid.adminml.com/d/01M0DSBDBHEAV3650Q913YSP6Y/view (v12) ⚠️ *visibilidade `public`*

> ⚠️ **Três nomes, uma coisa só:** *Forecast BC Shopee* (como eu falava), *Plano de Combate BC* (o nome da
> pasta) e *BC Shopee* (o título dentro do Grid). Se alguém procurar por um e não achar, é isto aqui.

Business Case para frear a Shopee em Large, Small e Heating & Cooling na janela **set-dez/2026**.
Compara a performance dos mesmos grupos econômicos de seller **no MELI e na Shopee**, transforma isso num
**ratio** (`Shopee ÷ MELI`) e projeta onde o ratio chega no fim do ano — com e sem ação.
Tese, evidência e projeção estão de pé e validadas. **A camada de "quanto pedir de verba" não está.**

🔴 **Antes de apresentar qualquer número deste BC para a liderança, leia
`03-Business-Case-Shopee.md` §"O que está quebrado".** A auditoria que eu mesma pedi em 21/08 encontrou
três erros materiais e um problema de método que muda o número de capa. Está tudo documentado — mas
não foi corrigido.

---

## Se você tem 15 minutos

1. **A tese em uma frase:** os sellers não sumiram, mudaram de endereço. Os 10 grupos econômicos cotados
   faturam **R$ 256 Mi** conosco e **R$ 477 Mi** na Shopee (mai+jun/26) — 186% mais lá do que aqui.
   Electrolux é o caso emblemático: saiu de 100% MELI para 57% Shopee em 11 meses, e **105% do crescimento
   do grupo foi para a Shopee**.

2. **Por que substituição vale mais que venda nova:** trazer um real da Shopee move os *dois* lados do
   ratio. A eficiência é `1 + MELI/Shopee` — em Large dá **3,34x**. E, como a fórmula é `1 + 1/r`,
   **defender território onde ainda somos grandes é mais eficiente do que reagir onde já perdemos.**

3. **A regra de ouro do perímetro:** todo número de capa é **D1 cheia**, sem recorte de faixa de ASP. A
   faixa é eixo de *alocação*, nunca de composição do número de capa. Isso foi decidido em 21/08 porque a
   versão anterior escondia 8,6 pp de ratio em Small.

4. **O que não confie:** o motor **subestima a Shopee** (−14% em Large, −34% em Small no backtest). Os
   ratios projetados são **piso, não teto**.

---

## Ordem de leitura sugerida

| Documento | Quando |
|---|---|
| **`01-Ways-of-Working-Grid-Shield.md`** | Antes de rodar ou alterar o Grid do Shield |
| **`02-Como-eu-olhava-BPC-vs-Shopee.md`** | Antes de montar o deck mensal do squad |
| **`03-Business-Case-Shopee.md`** | Antes de citar qualquer número do BC · **é a documentação do Grid `01M0DSBDBHEAV3650Q913YSP6Y`** (o §11 mapeia cada aba ao arquivo que a gera) |
| **`04-Armadilhas-e-licoes.md`** | Antes de escrever a primeira query ou script |
| `originais/ESTADO_DO_BC.md` | Fonte da verdade do BC (o que vale hoje) |
| `originais/premissas_bc_shopee_asp_home.md` | Histórico completo, 1.100+ linhas, inclui caminhos abandonados |
| `originais/AUDITORIA_21ago.md` | A auditoria cruzada das abas — leia junto com o §"O que está quebrado" |
