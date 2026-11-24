# Runbook — Price Point (box) para a vertical TECH · data dupla (07/07) + Julho MTD

> Cole este arquivo inteiro no seu Claude (ou anexe-o). Ele tem contexto, regras, as queries e o gerador do Grid. Roda ponta a ponta e publica **num doc NOVO seu**. Baseado na análise já feita para Home Electronics.

## Regras (importante)
- **NÃO suba em Grid de outra pessoa.** Crie um documento **NOVO** (sem `doc_id`). A referência de layout é `https://grid.adminml.com/d/01KW89RWFKQ9YQQTJMSQRZYVEP/view` (HE) — é só referência visual; **os seus dados vão pro seu doc.**
- Confirme o **valor exato de `VERTICAL`** (Passo 1) e troque em todas as queries.
- **Custo antes de rodar:** sempre `dry_run` primeiro; se passar de ~5 GB, mostre e confirme.
- **Acesso:** as tabelas do Pricing (`meli-sbox.REVENUEMKPBR.*`) e as `meli-bi-data.WHOWNER.*` abrem via **MCP bigquery-meli**. (bq CLI direto costuma ser negada no sandbox do Pricing.)
- A base do Pricing pode estar **congelada num dia recente** (a de HE congelou em 12/jul). O Passo 1 mostra a `MAX(ORD_CLOSED_DT)` — **ajuste a janela do MTD** pra terminar nesse dia.

## O que é a análise (contexto)
Funil de eficiência do **rebate de box (DXI)**: de todo o rebate investido, quanto **"virou"** nossa posição pra baixo do rival (exp→cheaper/match), quanto **continua caro** (exp→exp), quanto é **tóxico** (cheaper→cheaper = já era barato) e quanto é **off-target** (fora do hound / sem leitura de preço). Fonte = base validada do time de Pricing (`SITUACAO_REBATE_TESTE`). Banda de posição = **±1%**. ASP de referência = preço MELI na janela estável (favorability + fallback NMV/NSI). **Camada 1** = as 5 categorias (soma 100%). **Camada 2** = quebras por D1 / alavanca / faixa de ASP, só nos itens com status de preço.

---

## Passo 1 — Descobrir o VERTICAL de Tech + a frescor da base
Rode (via MCP, `dry_run` antes):
```sql
SELECT VERTICAL, MAX(ORD_CLOSED_DT) AS max_dt,
  COUNTIF(ORD_CLOSED_DT >= DATE '2026-07-01') AS rows_jul,
  COUNTIF(ORD_CLOSED_DT = DATE '2026-07-07') AS rows_0707
FROM `meli-sbox.REVENUEMKPBR.SITUACAO_REBATE_TESTE`
WHERE ORD_CLOSED_DT >= DATE '2026-06-01'
GROUP BY VERTICAL
ORDER BY rows_jul DESC
```
→ Anote o **nome exato do VERTICAL de Tech** (ex.: `TECHNOLOGY`) e a **`max_dt`**. Se `max_dt` < 12/jul, troque `'2026-07-12'` nas queries abaixo pela `max_dt`.

---

## Passo 2 — O cubo (Q2 + Julho MTD + 07/07)
⚠️ Troque **`'TECHNOLOGY'`** (3 lugares no `base` + 2 no ASP) pelo valor do Passo 1, e ajuste `'2026-07-12'` se preciso. `dry_run` primeiro (deve dar ~30 GB).
```sql
WITH asp_fav AS (
  SELECT ITE_ITEM_ID, APPROX_QUANTILES(PRICE_MELI,2)[OFFSET(1)] AS p
  FROM `meli-bi-data.WHOWNER.BT_COM_FAVORABILITY`
  WHERE SIT_SITE_ID='MLB' AND FAVORABILITY_TYPE='BOX_ALL_ABC' AND MELI_ID_TYPE='PRODUCT'
    AND VERTICAL='TECHNOLOGY' AND TIM_DAY BETWEEN DATE '2026-04-01' AND DATE '2026-06-30' AND PRICE_MELI>0
  GROUP BY ITE_ITEM_ID
),
asp_ef AS (
  SELECT ITE_ITEM_ID, SUM(F_NMV_LC)/NULLIF(SUM(F_NSI),0) AS p
  FROM `meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB`
  WHERE VERTICAL='TECHNOLOGY' AND ORD_CLOSED_DT BETWEEN DATE '2026-04-01' AND DATE '2026-07-12' AND F_NSI>0
  GROUP BY ITE_ITEM_ID
),
asp_ref AS (
  SELECT COALESCE(f.ITE_ITEM_ID,e.ITE_ITEM_ID) AS ITE_ITEM_ID, COALESCE(f.p,e.p) AS asp
  FROM asp_fav f FULL OUTER JOIN asp_ef e USING(ITE_ITEM_ID)
),
base AS (
  SELECT 'Q2' AS periodo, DOM_AGG_1, CAMPAIGN_SUBTYPE, ITE_ITEM_ID, rebates_total,
    REBATE_EXPENSIVE_CHEAPER, REBATE_EXPENSIVE_EXPENSIVE, REBATE_CHEAPER_CHEAPER, rebates_fora_hound
  FROM `meli-sbox.REVENUEMKPBR.SITUACAO_REBATE_TESTE`
  WHERE VERTICAL='TECHNOLOGY' AND ORD_CLOSED_DT BETWEEN DATE '2026-04-01' AND DATE '2026-06-30'
  UNION ALL
  SELECT 'MTD', DOM_AGG_1, CAMPAIGN_SUBTYPE, ITE_ITEM_ID, rebates_total,
    REBATE_EXPENSIVE_CHEAPER, REBATE_EXPENSIVE_EXPENSIVE, REBATE_CHEAPER_CHEAPER, rebates_fora_hound
  FROM `meli-sbox.REVENUEMKPBR.SITUACAO_REBATE_TESTE`
  WHERE VERTICAL='TECHNOLOGY' AND ORD_CLOSED_DT BETWEEN DATE '2026-07-01' AND DATE '2026-07-12'
  UNION ALL
  SELECT '0707', DOM_AGG_1, CAMPAIGN_SUBTYPE, ITE_ITEM_ID, rebates_total,
    REBATE_EXPENSIVE_CHEAPER, REBATE_EXPENSIVE_EXPENSIVE, REBATE_CHEAPER_CHEAPER, rebates_fora_hound
  FROM `meli-sbox.REVENUEMKPBR.SITUACAO_REBATE_TESTE`
  WHERE VERTICAL='TECHNOLOGY' AND ORD_CLOSED_DT = DATE '2026-07-07'
)
SELECT b.periodo, b.DOM_AGG_1, COALESCE(b.CAMPAIGN_SUBTYPE,'None') AS sub,
  CASE WHEN a.asp IS NULL THEN '0_SEM_ASP' WHEN a.asp<200 THEN '1_<200' WHEN a.asp<500 THEN '2_200-500' WHEN a.asp<1500 THEN '3_500-1500' WHEN a.asp<3000 THEN '4_1500-3000' ELSE '5_>3000' END AS asp_band,
  ROUND(SUM(b.rebates_total)/1e6,3) AS t,
  ROUND(SUM(b.REBATE_EXPENSIVE_CHEAPER)/1e6,3) AS ec,
  ROUND(SUM(b.REBATE_EXPENSIVE_EXPENSIVE)/1e6,3) AS ee,
  ROUND(SUM(b.REBATE_CHEAPER_CHEAPER)/1e6,3) AS cc,
  ROUND(SUM(b.rebates_fora_hound)/1e6,3) AS fh
FROM base b LEFT JOIN asp_ref a ON b.ITE_ITEM_ID=a.ITE_ITEM_ID
GROUP BY 1,2,3,4
```
> Obs. faixas de ASP (200/500/1500/3000) são as de HE (Shield). Tech tem ticket mais alto — se quiser, ajuste os cortes do `CASE`. Pra "mesmo formato", pode manter.

→ Salve as **linhas do resultado** num arquivo **`result.json`** (uma lista de objetos com `periodo, DOM_AGG_1, sub, asp_band, t, ec, ee, cc, fh`).

---

## Passo 3 — Gerar o HTML do Grid (parse + template)
Rode este Python (ajuste `RESULT`, `VERTICAL_NOME`, `OUT` no topo). Ele produz o HTML self-contained com **seletor de período (Q2 · Julho MTD · 07/07)**, Camada 1 (5 categorias) e Camada 2 (D1 / alavanca / ASP, com toggle Tabela/Barras). Layout idêntico ao de HE (sem a barra de competidor, que era específica de HE — dá pra adicionar depois).

```python
import json, io
RESULT = "result.json"        # arquivo com as linhas da Query 2
VERTICAL_NOME = "Tech"        # nome pra exibir no cabeçalho
OUT = "Funil_Box_Tech.html"

rows = json.load(open(RESULT, encoding="utf-8"))
if isinstance(rows, dict) and "rows" in rows: rows = rows["rows"]
asp_order=['0_SEM_ASP','1_<200','2_200-500','3_500-1500','4_1500-3000','5_>3000']
aspL=['Sem ASP','< 200','200–500','500–1.500','1.500–3.000','> 3.000']
subf={'commercial':'Pré-acordo','on_demand':'SAD (on demand)','price_matching':'PM (price matching)','price_matching_meli_all':'PM meli all','cofinanced':'Cofinanced','unhealthy_stock':'Unhealthy','lightning':'Lightning','None':'Sem campanha'}
d1s=sorted({r['DOM_AGG_1'] for r in rows}); subs=sorted({(r['sub'] or 'None') for r in rows})
di={v:i for i,v in enumerate(d1s)}; si={v:i for i,v in enumerate(subs)}; ai={v:i for i,v in enumerate(asp_order)}
def f(x): return round(float(x),3) if x is not None else 0.0
per={'Q2':[],'MTD':[],'0707':[]}
for r in rows:
    p=r['periodo']; per.setdefault(p,[])
    per[p].append([di[r['DOM_AGG_1']],si[r['sub'] or 'None'],ai[r['asp_band']],f(r['t']),f(r['ec']),f(r['ee']),f(r['cc']),f(r['fh'])])
P={"d1L":d1s,"subL":[subf.get(s,s) for s in subs],"aspL":aspL,"vert":VERTICAL_NOME,
   "Q2":per.get('Q2',[]),"MTD":per.get('MTD',[]),"0707":per.get('0707',[])}
DATA=json.dumps(P,ensure_ascii=False,separators=(',',':'))

TPL=r'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Price Point __VERT__ — Box</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#fff}
.wrap{font-family:system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;color:#21242b;max-width:1000px;margin:0 auto;padding:22px 22px 44px;line-height:1.45}
h1{font-size:23px;font-weight:600;margin:0 0 2px}.eye{font-size:12px;color:#6b7178;margin-bottom:14px}
.sec{font-size:11px;font-weight:600;letter-spacing:.5px;text-transform:uppercase;color:#2a78d6;margin:22px 0 10px}
.mgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px}
.mcard{background:#f7f8f9;border:1px solid #eceef1;border-radius:10px;padding:11px 13px}
.mcard .k{font-size:10.5px;font-weight:600;color:#6b7178;text-transform:uppercase}.mcard .v{font-size:13.5px;font-weight:600;margin-top:3px}.mcard .s{font-size:11.5px;color:#6b7178;margin-top:2px}
.ruler{display:flex;height:26px;border-radius:4px;overflow:hidden;margin:2px 0 4px;max-width:560px}.ruler div{display:flex;align-items:center;justify-content:center;color:#fff;font-size:12px;font-weight:500}
.note{font-size:12px;color:#6b7178}
.fork{display:flex;flex-wrap:wrap;align-items:center;gap:12px;margin-top:4px}
.fk-part{background:#fff;border:1px solid #e6e8eb;border-radius:10px;padding:8px 12px;text-align:center}.fk-lbl{font-size:10.5px;font-weight:600;color:#6b7178;text-transform:uppercase;margin-bottom:5px}
.fk-pill{color:#fff;font-size:12px;font-weight:500;border-radius:12px;padding:4px 14px;display:inline-block}.fk-arrow{font-size:13px;font-weight:600;color:#2a78d6}
.fk-branches{display:flex;flex-direction:column;gap:6px}.fk-b{color:#fff;font-size:12.5px;font-weight:500;border-radius:12px;padding:6px 14px}
.params{background:#f7f8f9;border:1px solid #eceef1;border-radius:10px;padding:11px 14px;font-size:12px;color:#4a4f57;line-height:1.7;margin-top:16px}
.perbar{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:24px 0 6px}.perbar .lbl{font-size:11px;font-weight:600;text-transform:uppercase;color:#2a78d6}
.per{border:1px solid #d7dade;background:#fff;color:#5a6068;font-size:12.5px;padding:7px 14px;cursor:pointer;border-radius:8px}.per.on{background:#2a78d6;color:#fff;border-color:#2a78d6}
.fl2{display:flex;flex-wrap:wrap;gap:12px 16px;align-items:flex-end;background:#f7f8f9;border:1px solid #eceef1;border-radius:10px;padding:12px 14px;margin-bottom:14px}
.fl2 label{font-size:11px;color:#6b7178;font-weight:600;display:block;margin-bottom:4px}.fl2 select{font-size:13px;padding:7px 9px;border:1px solid #d7dade;border-radius:8px;background:#fff;color:#21242b;min-width:150px}
.tot{font-size:34px;font-weight:600;font-variant-numeric:tabular-nums;line-height:1}.cap{font-size:12px;color:#8a8f96;margin-bottom:14px}
.cat{display:flex;align-items:center;gap:10px;margin-bottom:7px}.nm{width:190px;font-size:13px}.tr{flex:1;height:16px;background:#eef0f2;border-radius:4px;overflow:hidden}.fill{height:100%}.rv{width:160px;text-align:right;font-size:12px;color:#5a6068;font-variant-numeric:tabular-nums}
.dv{border-top:1px dashed #e0e2e6;margin:11px 0 8px;padding-top:3px;font-size:11px;color:#8a8f96}
.c2head{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px}.leg{font-size:11.5px;color:#5a6068}.leg .dot{display:inline-block;width:9px;height:9px;border-radius:2px;margin:0 4px 0 10px}
.tog{border:1px solid #d7dade;background:#fff;color:#5a6068;font-size:12px;padding:5px 12px;cursor:pointer}.tog:first-child{border-radius:8px 0 0 8px}.tog:last-child{border-radius:0 8px 8px 0;border-left:none}.tog.on{background:#2a78d6;color:#fff;border-color:#2a78d6}
.q{margin-bottom:16px}.qh{font-size:13px;font-weight:600;margin-bottom:6px}
table{width:100%;border-collapse:collapse;font-size:12px;table-layout:fixed}th{font-weight:600;color:#5a6068;text-align:right;padding:6px 7px;border-bottom:1px solid #e6e8eb}th:first-child{text-align:left}
td{padding:6px 7px;text-align:right;font-variant-numeric:tabular-nums;border-bottom:1px solid #eef0f2}td:first-child{text-align:left;color:#5a6068}.pctm{color:#9aa0a6;font-size:10.5px}.dot{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:4px}
.brow{display:flex;align-items:center;gap:10px;margin-bottom:8px}.bname{width:150px;font-size:12.5px}.btrack{flex:1;height:22px;background:#eef0f2;border-radius:4px;overflow:hidden}.bfill{height:100%;display:flex;gap:1.5px}.bval{width:150px;text-align:right;font-size:12px;color:#5a6068;font-variant-numeric:tabular-nums}
.foot{font-size:11.5px;color:#8a8f96;border-top:1px solid #eceef1;margin-top:24px;padding-top:12px}
</style></head><body><div class="wrap">
<div class="eye">Price Point __VERT__ · rebate de box (DXI) · base validada pelo time de Pricing</div>
<h1>Box — como lemos e para onde foi o investimento</h1>
<div class="sec">1 · Premissas</div>
<div class="mgrid">
<div class="mcard"><div class="k">Perímetro</div><div class="v">__VERT__ · 3P · MLB</div></div>
<div class="mcard"><div class="k">Períodos</div><div class="v">Q2 · Julho MTD · 07/07</div><div class="s">selecionável abaixo</div></div>
<div class="mcard"><div class="k">Lente</div><div class="v">Box (à vista)</div></div>
<div class="mcard"><div class="k">Régua</div><div class="v">empate = ±1%</div></div>
</div>
<div class="sec">2 · Régua de posição (vs melhor rival)</div>
<div class="ruler"><div style="width:42%;background:#1baf7a">Mais barato</div><div style="width:16%;background:#9aa0a6">Empate</div><div style="width:42%;background:#df6048">Mais caro</div></div>
<div class="note">empate = ±1% (banda BPC/Pricing)</div>
<div class="sec">3 · O que o rebate fez — partiu caro, e aí?</div>
<div class="fork">
<div class="fk-part"><div class="fk-lbl">Partida (sem rebate)</div><div class="fk-pill" style="background:#df6048">Mais caro</div></div>
<div class="fk-arrow">rebate ▶</div>
<div class="fk-branches"><div class="fk-b" style="background:#1baf7a">→ Mais barato / empate = VIROU ✓</div><div class="fk-b" style="background:#df6048">→ Continua mais caro = não virou</div></div>
</div>
<div class="params"><b>Parâmetros:</b> Empate = ±1% · Investimento só MELI (3P; box = DXI) · ASP = preço MELI de referência (janela estável) · "Inauditável" = rebate sem rival mapeado (fora do hound + sem leitura).</div>
<div class="perbar"><span class="lbl">Período</span><button class="per on" data-p="Q2">Q2 · Abr–Jun</button><button class="per" data-p="MTD">Julho MTD</button><button class="per" data-p="0707">07/07 · data dupla</button></div>
<div class="sec" style="margin-top:8px">Camada 1 · todo o investimento (soma 100%)</div>
<div class="fl2"><div><label>D1</label><select id="fnD1"></select></div><div><label>Faixa de ASP</label><select id="fnAsp"></select></div><div><label>Alavanca</label><select id="fnSub"></select></div></div>
<div class="tot" id="fnTot"></div><div class="cap" id="fnCap"></div><div id="fnCats"></div>
<div class="sec">Camada 2 · só itens com status de preço <span id="fnBase" style="text-transform:none;letter-spacing:0;color:#8a8f96;font-weight:400"></span></div>
<div class="c2head"><div class="leg"><span class="dot" style="background:#df6048"></span>exp→exp<span class="dot" style="background:#1baf7a"></span>exp→cheaper/match<span class="dot" style="background:#eaa15a"></span>cheaper→cheaper</div><div><button id="tgTab" class="tog on">Tabela</button><button id="tgBar" class="tog">Barras</button></div></div>
<div class="q"><div class="qh">por D1</div><div id="fnQD1"></div></div>
<div class="q"><div class="qh">por alavanca</div><div id="fnQSub"></div></div>
<div class="q"><div class="qh">por faixa de ASP</div><div id="fnQAsp"></div></div>
<div class="foot">Fonte: SITUACAO_REBATE (Pricing) — box/DXI, item×dia×campanha. "exp→cheaper" inclui empate. "com erro de leitura" = rebate sem preço de rival capturado no dia.</div>
</div>
<script>
var P=__DATA__;var PERIODS={'Q2':P.Q2,'MTD':P.MTD,'0707':P['0707']};
var PERCAP={'Q2':'Q2 · Abr–Jun 2026','MTD':'Julho MTD','0707':'07/07 · data dupla'};
var PER='Q2',VIEW='tab',d1L=P.d1L,subL=P.subL,aspL=P.aspL;
function money(x){return 'R$ '+(Math.round(x*10)/10).toFixed(1).replace('.',',')+' Mi';}
function amt(x){return (Math.round(x*10)/10).toFixed(1).replace('.',',');}
function pct(x,t){return t>0?(100*x/t).toFixed(1).replace('.',',')+'%':'0%';}
function val(id){return document.getElementById(id).value;}
function opts(id,l){var s=document.getElementById(id);var h='<option value="">Todos</option>';for(var i=0;i<l.length;i++)h+='<option value="'+i+'">'+l[i]+'</option>';s.innerHTML=h;}
function cur(){var fd=val('fnD1'),fa=val('fnAsp'),fs=val('fnSub');return PERIODS[PER].filter(function(r){return (fd===''||r[0]==+fd)&&(fa===''||r[2]==+fa)&&(fs===''||r[1]==+fs);});}
function sum(rs){var o={t:0,ec:0,ee:0,cc:0,fh:0};rs.forEach(function(r){o.t+=r[3];o.ec+=r[4];o.ee+=r[5];o.cc+=r[6];o.fh+=r[7];});o.er=o.t-o.ec-o.ee-o.cc-o.fh;return o;}
function catRow(nm,v,t,c){var w=t>0?(100*v/t):0;return '<div class="cat"><div class="nm">'+nm+'</div><div class="tr"><div class="fill" style="width:'+w.toFixed(1)+'%;background:'+c+'"></div></div><div class="rv">'+money(v)+' · '+pct(v,t)+'</div></div>';}
function items(dc,sb){var m={};cur().forEach(function(r){var k=r[dc];if(!m[k])m[k]={ee:0,ec:0,cc:0};m[k].ee+=r[5];m[k].ec+=r[4];m[k].cc+=r[6];});
var it=Object.keys(m).map(function(k){var g=m[k];return {k:+k,ee:g.ee,ec:g.ec,cc:g.cc,tot:g.ee+g.ec+g.cc};}).filter(function(x){return x.tot>0.02;});
if(sb)it.sort(function(a,b){return a.k-b.k;});else it.sort(function(a,b){return b.tot-a.tot;});return it;}
function tableHTML(dc,l,sb){var it=items(dc,sb);var lab=dc==0?'D1':dc==1?'alavanca':'ASP';
var h='<table><colgroup><col style="width:28%"><col><col><col><col style="width:15%"></colgroup><thead><tr><th>'+lab+'</th><th>exp→exp</th><th>exp→ch/m</th><th>ch→ch</th><th>total</th></tr></thead><tbody>';
it.forEach(function(x){h+='<tr><td>'+l[x.k]+'</td><td>'+amt(x.ee)+' <span class="pctm">'+(x.tot>0?Math.round(100*x.ee/x.tot):0)+'%</span></td><td>'+amt(x.ec)+' <span class="pctm">'+(x.tot>0?Math.round(100*x.ec/x.tot):0)+'%</span></td><td>'+amt(x.cc)+' <span class="pctm">'+(x.tot>0?Math.round(100*x.cc/x.tot):0)+'%</span></td><td>'+amt(x.tot)+'</td></tr>';});return h+'</tbody></table>';}
function barsHTML(dc,l,sb){var it=items(dc,sb);function seg(w,v,c,fx){var t=w>=9?(amt(v)+' · '+Math.round(w)+'%'):'';var ws=fx?'flex:1':'width:'+w.toFixed(1)+'%';return '<div style="'+ws+';background:'+c+';display:flex;align-items:center;justify-content:center;color:#fff;font-size:10.5px;white-space:nowrap;overflow:hidden">'+t+'</div>';}
var h='';it.forEach(function(x){var we=x.tot>0?100*x.ee/x.tot:0,wc=x.tot>0?100*x.ec/x.tot:0;h+='<div class="brow"><div class="bname">'+l[x.k]+'</div><div class="btrack"><div class="bfill" style="width:100%">'+seg(we,x.ee,'#df6048',0)+seg(wc,x.ec,'#1baf7a',0)+seg(100-we-wc,x.cc,'#eaa15a',1)+'</div></div><div class="bval">'+money(x.tot)+'</div></div>';});return h;}
function quad(dc,l,sb){return VIEW=='tab'?tableHTML(dc,l,sb):barsHTML(dc,l,sb);}
function render(){var s=sum(cur());document.getElementById('fnTot').textContent=money(s.t);document.getElementById('fnCap').textContent='investido no recorte · '+PERCAP[PER];
var h=catRow('exp→exp (continua caro)',s.ee,s.t,'#df6048')+catRow('exp→cheaper/match (virou)',s.ec,s.t,'#1baf7a')+catRow('cheaper→cheaper (tóxico)',s.cc,s.t,'#eaa15a')+'<div class="dv">sem leitura de preço — outra categoria de problema</div>'+catRow('fora do hound (sem rival)',s.fh,s.t,'#8f8d82')+catRow('com erro de leitura',s.er,s.t,'#6f6d64');
document.getElementById('fnCats').innerHTML=h;document.getElementById('fnBase').textContent='· base '+money(s.ee+s.ec+s.cc)+' (exclui fora do hound + erro de leitura)';
document.getElementById('fnQD1').innerHTML=quad(0,d1L,0);document.getElementById('fnQSub').innerHTML=quad(1,subL,0);document.getElementById('fnQAsp').innerHTML=quad(2,aspL,1);}
opts('fnD1',d1L);opts('fnAsp',aspL);opts('fnSub',subL);
['fnD1','fnAsp','fnSub'].forEach(function(id){document.getElementById(id).addEventListener('change',render);});
document.getElementById('tgTab').addEventListener('click',function(){VIEW='tab';this.classList.add('on');document.getElementById('tgBar').classList.remove('on');render();});
document.getElementById('tgBar').addEventListener('click',function(){VIEW='bar';this.classList.add('on');document.getElementById('tgTab').classList.remove('on');render();});
var pb=document.querySelectorAll('.per');pb.forEach(function(b){b.addEventListener('click',function(){PER=this.getAttribute('data-p');pb.forEach(function(x){x.classList.remove('on');});this.classList.add('on');render();});});
render();
</script></body></html>'''
html=TPL.replace("__DATA__",DATA).replace("__VERT__",VERTICAL_NOME)
io.open(OUT,"w",encoding="utf-8").write(html)
print("ok:",OUT,len(html),"chars")
```

---

## Passo 4 — Publicar no Grid (documento NOVO)
Peça ao seu Claude: **"publica o `Funil_Box_Tech.html` no Grid usando a skill grid-sharing, criando um documento NOVO (sem `doc_id`), título 'Price Point Tech — Box (funil)'."**
- ⚠️ **Não** informe `doc_id` de ninguém → o engine cria um doc **seu**.
- Se pedir atualização de skill, atualize o plugin oficial da Meli.
- O link que voltar (`grid.adminml.com/d/.../view`) é o **seu** doc.

## Ajustes finos (opcionais)
- **Faixas de ASP:** Tech tem ticket mais alto — pode mudar os cortes no `CASE` da Query 2.
- **Barra de competidor** (Amazon/Shopee/…): não incluí (era específica de HE). Se quiser, dá pra adicionar com um join na `BT_COM_FAVORABILITY` (`COMP_SITE_ID_WINNER`).
- **Janela do MTD:** ajuste conforme a `max_dt` do Passo 1.
