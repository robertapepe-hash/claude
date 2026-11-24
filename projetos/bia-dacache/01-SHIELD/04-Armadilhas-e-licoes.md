# Armadilhas e lições

> Tudo aqui custou pelo menos uma rodada de retrabalho, e várias custaram um número errado que só apareceu
> na auditoria. Vale para o Shield, mas quase tudo vale para qualquer análise em `meli-bi-data`.

---

## 1 · BigQuery — custo e escopo

**O scan do `DM_EFICIENCIA_MLB` é dirigido pelas COLUNAS, não pelas linhas.**
São ~1,2-1,4 GB por mês de partição. **Filtrar por D1 ou por `cust_id` não reduz o scan** — só reduz o
resultado. Para cortar custo de verdade: reduza a janela de datas ou o número de colunas referenciadas.
Esse é o erro de intuição mais caro da casa.

**Teto de 100 GB por query na `BT_COM_FAVORABILITY`.** Quando bater, adicione
`MELI_ID_TYPE = 'PRODUCT'` — é cluster field e tipicamente corta **60-70%** do scan.

**`BOC_BENEFITS_ITEM_DAY_DASHBOARD` é a tabela mais cara da casa** (~89-117 GB). Nunca rode sem filtro de
data explícito. E ela usa **`DAY_MONTH_YEAR`**, não `TIM_DAY`.

**Sempre `dry_run` antes.** Acima de ~5 GB, mostre o custo e confirme antes de executar. Era regra minha e
evitou muita conta desnecessária.

**Segunda de manhã o `bq` CLI estoura a fila do `meli-bi-data`.** Quando acontecer, o caminho é o MCP
`bigquery-insight` (`execute_query`) — não adianta insistir no CLI.

**Sempre confira a última competência disponível na fonte antes de definir a janela.** O Yipit fecha um mês
antes do DM. Isso já me gerou uma comparação de 2 meses contra 3 meses, silenciosamente.

---

## 2 · BigQuery — semântica que engana

**`SIT_SITE_ID = 'MLB'` sempre na `BT_COM_FAVORABILITY`.** A view tem outros sites, e esquecer o filtro
**infla o BPC**. É a nota mais destacada no cabeçalho do script de refresh, por motivo.

**`KMI`, `FLG_BULKY`, `FLG_COMP_1P`, `COMP_FLAG_FIRST_PARTY` são STRING lowercase** — `'true'`/`'false'`,
nunca booleano.

**`CUS_NICKNAME` é PII-bloqueado.** Use `CUS_CUST_ID_SEL` como chave e traga o nome legível de um de-para
separado a partir do `DM_EFICIENCIA` (`SELLER_NAME`).

**Campos com nomes diferentes para a mesma coisa:**
- `MELI_ID` (na FAVORABILITY) ≡ `ITE_ITEM_ID` (nas outras)
- dentro do array `COMPETITORS` o preço é **`COMP_ITEM_PRICE`**; no nível raiz é `COMP_PRICE_RIVAL`
- datas: `TIM_DAY` (favorabilidade) · `ORD_CLOSED_DT` (eficiência) · `DAY_MONTH_YEAR` (benefits)

**As colunas `_TEMP` de domínio (taxonomia 2025) estão remapeadas e bagunçadas — não use.** Use
`DOM_DOMAIN_AGG1/2/3` estáveis.

**Tipos mistos (`BIGNUMERIC` × `FLOAT`)** quebram divisão — faça cast explícito.

**Base zero:** marque como "novo", não calcule variação percentual. Um `∞` num quadro executivo destrói a
credibilidade da tabela inteira.

---

## 3 · PowerShell — quatro bugs silenciosos que me pegaram

**1. PowerShell NÃO diferencia maiúsculas em nomes de variável.**
Três bugs silenciosos numa sessão só: `$n`×`$N`, `$sS`×`$SS`, `$h2`×`$H2` — o último destruiu um array e
zerou resultados sem erro nenhum. **Nunca use nomes que difiram só por caixa.**

**2. `continue` dentro de `foreach` aninhado pode escapar os dois loops.** Use `if` em vez de `continue`.

**3. Precedência da vírgula:** `@($x-2, $x-1, $x)` é lido como `$x - (2, $x-1, $x)`. **Parentize.**

**4. PS 5.1 trunca SQL multi-linha passado como argumento de `.exe`.** Antes de chamar o `bq`, achate a
query em uma linha:
```powershell
$flat = ($sql -replace '\r?\n',' ').Trim()
```

**Encoding:** leia `.sql` com `[System.IO.File]::ReadAllText` (remove BOM) e force UTF-8 antes de chamar o `bq`:
```powershell
$env:PYTHONIOENCODING = "utf-8"; chcp 65001 > $null; [Console]::OutputEncoding = [Text.Encoding]::UTF8
```
Sem isso, acento vira mojibake (`COLORVISÃO` e afins). Em alguns casos o pipe do PS 5.1 corrompe mesmo
assim — a saída é `cmd /c "bq query ... < query.sql > out.csv"`.

**`.ps1` está bloqueado por SRP/GPO corporativo nesta máquina.** Rode a lógica inline ou transforme em
skill (modelo: plugin `wbr-he`).

---

## 4 · JavaScript nos dashboards

**Arrays esparsos:** `map` **pula buracos** e o `join` os transforma em vazio, desalinhando as células da
tabela. Use `new Array(n).fill(null)` em vez de deixar o array crescer com buracos.

---

## 5 · Grid MELI

- **`skill_version` é obrigatório** no payload do engine — sem ele, recusa.
- **≤ 10 MB:** upload inline. **> 10 MB:** presigned em 3 passos (reserva slot → PUT → confirm). Teto real ~500 MB.
- **Sempre suba num doc de teste antes do oficial.** Princípio não-negociável meu.
- **Rollback:** `POST /api/v1/documents/{doc_id}/rollback {"version": N}`.
- **Precisa de VPN corporativa** para o upload.
- **Confira a visibilidade do doc.** O Grid do BC está como `public` — pode não ser o desejado.

---

## 6 · Método — as três que mais mudaram conclusões

**1. Perímetro que filtra por "onde somos grandes" é cego para onde o concorrente cresce.**
Foi o que escondeu 8,6 pp do ratio de Small. Se precisar de recorte, valide contra a base cheia antes de fechar.

**2. Faixa de ASP é atributo do item, fixo — não do dia.**
Se a faixa vier do preço praticado, o item promocionado "cai" de faixa por causa do próprio tratamento, e
a análise fica circular. Use a **mediana do preço cheio** numa janela estável.

**3. YoY de mês isolado pode inverter o sinal de uma conclusão.**
Em H&C, `jul/26 vs jul/25` deu +40,7% enquanto a tendência de seis meses era queda forte, só porque
jul/25 tinha sido um mês fraco. Prefira janelas de 3 meses.

---

## 7 · Checklist antes de publicar qualquer coisa

- [ ] `dry_run` rodado e custo confirmado
- [ ] `SIT_SITE_ID='MLB'` presente (se for favorabilidade)
- [ ] última competência da fonte conferida — todas as bases na mesma janela
- [ ] sanity check batendo com a referência conhecida (NMV do mês, BPC do mês)
- [ ] nenhum placeholder sobrando no HTML
- [ ] unidade e período explícitos em todo cabeçalho e toda referência
- [ ] limitações declaradas na própria peça, não só no documento
- [ ] subido primeiro no doc de teste
