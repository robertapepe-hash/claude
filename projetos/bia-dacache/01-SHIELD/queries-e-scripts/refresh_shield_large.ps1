# =====================================================================
#  refresh_shield_large.ps1  —  Pipeline PERENE do dashboard Shield/Large
#  Reconstruido jul/2026. Queries dry_run-validadas; de-para de segmento
#  aterrado no dado real (SEGMENTO_DETAIL: CA->'3P Assessorada',
#  SD->'3P Dev', PL->'1P', 1P/CBT diretos). Reconcilia jun/26 = ~584 Mi.
#  Constroi TUDO num refresh: 5 cubos S&P (DM_EFICIENCIA) + pilar BPC (6 cubos de
#  BT_COM_FAVORABILITY) + pilar DEMANDA (3 cubos ITEM-LEVEL: DM_MKP_VISITS + DM_EFICIENCIA via bridge).
#
#  USO:  .\refresh_shield_large.ps1 -Through 2026-07
#        (sem -Through = ultimo mes completo)
#
#  Motor: bq CLI (os cubos passam de 3.000 linhas -> MCP nao serve).
#  Custo full (janela 25x26 p/ YoY): S&P ~US$0,80 + BPC ~US$4,34 + Demanda ~US$0,63 = ~US$5,8-6,6/refresh.
#  (Freeze de 2025 como baseline = otimizacao futura p/ cair a ~US$3,8; nao feito p/ manter simplicidade+coerencia do bridge.)
#  (BPC incremental de 1 mes ~US$0,27 se trocar a janela -> ver nota no bloco.)
#  Faca dry_run se em duvida. NAO roda direto (.ps1 bloqueado por SRP/GPO
#  corporativo) -> rodar a logica INLINE ou virar SKILL (a la wbr-he).
#  Depende de VPN corporativa (upload Grid) e credencial gcloud (bq).
# =====================================================================
param([string]$Through = "")

$ErrorActionPreference = "Stop"
$sp  = $PSScriptRoot                                   # kit vive junto do script
$tpl = Join-Path $sp "dashboard_template.html"
$out = Join-Path $sp "dashboard_shield_large.html"
$cfg = Join-Path $sp "grid_config2.json"

# ---- janela: START fixo por cubo; END = ultimo dia do mes -Through ----
if (-not $Through) { $lm = (Get-Date).AddDays(-(Get-Date).Day); $Through = $lm.ToString("yyyy-MM") }
$END = ([datetime]::ParseExact("$Through-01","yyyy-MM-dd",$null)).AddMonths(1).AddDays(-1).ToString("yyyy-MM-dd")
Write-Host "== Refresh Shield/Large ate $Through (ORD_CLOSED_DT <= $END) =="

# ---- UTF-8 p/ o bq nao comer acento (COLORVISAO etc.) ----
$env:PYTHONIOENCODING = "utf-8"; chcp 65001 > $null; [Console]::OutputEncoding = [Text.Encoding]::UTF8

$FILT = "VERTICAL='HOME ELECTRONICS' AND DOM_DOMAIN_AGG1='LARGE APPLIANCES'"
$FAIXA = "CASE WHEN ITE_ITEM_FULL_UNIT_PRICE<200 THEN '1_<200' WHEN ITE_ITEM_FULL_UNIT_PRICE<500 THEN '2_200-500' WHEN ITE_ITEM_FULL_UNIT_PRICE<1500 THEN '3_500-1500' WHEN ITE_ITEM_FULL_UNIT_PRICE<3000 THEN '4_1500-3000' ELSE '5_>3000' END"
$SEG = "CASE SEGMENTO_DETAIL WHEN 'CA' THEN '3P Assessorada' WHEN 'SD' THEN '3P Dev' WHEN 'PL' THEN '1P' ELSE SEGMENTO_DETAIL END"

# ---- 1) MAIN (mes x faixa x d2 x d4 x segmento) — sem bounding, 2025-01+ ----
$qMain = @"
SELECT FORMAT_DATE('%Y-%m',ORD_CLOSED_DT) AS mes, $FAIXA AS faixa, DOM_DOMAIN_AGG2 AS d2,
  REPLACE(DOM_DOMAIN_ID,'MLB-','') AS d4, $SEG AS segmento,
  ROUND(SUM(F_NMV_LC)/1e6,4) AS nmv_mi, ROUND(SUM(F_NSI),4) AS nsi,
  COUNT(DISTINCT ORD_ORDER_ID) AS pedidos, COUNT(DISTINCT CUS_CUST_ID) AS compradores,
  COUNT(DISTINCT IF(NEW_BUYER_FLG,CUS_CUST_ID,NULL)) AS novos
FROM ``meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB``
WHERE $FILT AND ORD_CLOSED_DT BETWEEN '2025-01-01' AND '$END'
GROUP BY 1,2,3,4,5
"@

# ---- template do cubo com BOUNDING (top-15 NMV U NSI por faixa + Outros; rank em 2025-01+) ----
function BoundedCube([string]$entExpr,[string]$entAlias,[string]$start) {
@"
WITH base AS (
  SELECT FORMAT_DATE('%Y-%m',ORD_CLOSED_DT) AS mes, $FAIXA AS faixa, DOM_DOMAIN_AGG2 AS d2,
    $SEG AS segmento, $entExpr AS ent, F_NMV_LC AS nmv, F_NSI AS nsi
  FROM ``meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB``
  WHERE $FILT AND ORD_CLOSED_DT BETWEEN '$start' AND '$END' ),
rk AS ( SELECT faixa, ent, SUM(nmv) snmv, SUM(nsi) snsi FROM base WHERE mes>='2025-01' GROUP BY 1,2 ),
named AS ( SELECT faixa, ent FROM (
    SELECT faixa, ent, ROW_NUMBER() OVER(PARTITION BY faixa ORDER BY snmv DESC) rn,
           ROW_NUMBER() OVER(PARTITION BY faixa ORDER BY snsi DESC) rs FROM rk ) WHERE rn<=15 OR rs<=15 )
SELECT b.mes, b.faixa, b.d2, b.segmento, IF(n.ent IS NULL,'Outros',b.ent) AS $entAlias,
  ROUND(SUM(b.nmv)/1e6,4) AS nmv_mi, ROUND(SUM(b.nsi),4) AS nsi
FROM base b LEFT JOIN named n ON b.faixa=n.faixa AND b.ent=n.ent
GROUP BY 1,2,3,4,5
"@
}
$qSeller = BoundedCube "SELLER_NAME" "seller" "2025-01-01"                       # 18m
$qGrowth = BoundedCube "SELLER_NAME" "seller" "2024-01-01"                       # 30m (YoY/Dpp)
$qBrand  = BoundedCube "COALESCE(NULLIF(ITE_ITEM_BRAND,''),'(sem marca)')" "marca" "2024-01-01"  # 30m

# ---- 5) SB = cruzamento marca x seller (marca-first, SEM d2, 30m) — drill "sellers da marca" ----
$qSB = @"
WITH base AS ( SELECT FORMAT_DATE('%Y-%m',ORD_CLOSED_DT) AS mes, $FAIXA AS faixa, $SEG AS segmento, COALESCE(NULLIF(ITE_ITEM_BRAND,''),'(sem marca)') AS marca, SELLER_NAME AS seller, F_NMV_LC AS nmv, F_NSI AS nsi FROM ``meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB`` WHERE $FILT AND ORD_CLOSED_DT BETWEEN '2024-01-01' AND '$END' ),
mrk AS (SELECT faixa,marca,SUM(nmv) n,SUM(nsi) s FROM base WHERE mes>='2025-01' GROUP BY 1,2),
mnamed AS (SELECT faixa,marca FROM (SELECT faixa,marca,ROW_NUMBER() OVER(PARTITION BY faixa ORDER BY n DESC) rn,ROW_NUMBER() OVER(PARTITION BY faixa ORDER BY s DESC) rs FROM mrk) WHERE rn<=15 OR rs<=15),
b2 AS (SELECT base.*, IF(m.marca IS NULL,'Outros',base.marca) AS marca_b FROM base LEFT JOIN mnamed m ON base.faixa=m.faixa AND base.marca=m.marca),
srk AS (SELECT faixa,segmento,marca_b,seller,SUM(nmv) n FROM b2 WHERE marca_b<>'Outros' AND mes>='2025-01' GROUP BY 1,2,3,4),
snamed AS (SELECT faixa,segmento,marca_b,seller FROM (SELECT faixa,segmento,marca_b,seller,ROW_NUMBER() OVER(PARTITION BY faixa,segmento,marca_b ORDER BY n DESC) rn FROM srk) WHERE rn<=8)
SELECT b2.mes, b2.faixa, b2.segmento, b2.marca_b AS marca, IF(b2.marca_b='Outros','Outros', IF(s.seller IS NULL,'Outros', b2.seller)) AS seller, ROUND(SUM(b2.nmv)/1e6,4) AS nmv_mi, ROUND(SUM(b2.nsi),4) AS nsi
FROM b2 LEFT JOIN snamed s ON b2.faixa=s.faixa AND b2.segmento=s.segmento AND b2.marca_b=s.marca_b AND b2.seller=s.seller
GROUP BY 1,2,3,4,5
"@

# =====================================================================
#  PILAR COMPETITIVIDADE / BPC  (BT_COM_FAVORABILITY, MLB, Large)
#  1 scan por grao (mensal + data-dupla) via GROUPING SETS: struct(+KMI+D2)
#  / marca / seller. 3 lentes como colunas (t=Total, w=Shopee winner,
#  s=vs Shopee via UNNEST(COMPETITORS)). Bounding top-6/faixa + rotulo de
#  seller = LOCAL (BpcDerive) -> reproduz os cubos validados (jun26 ABC=42,7%).
#  Custo full-2026 ~US$2,7; incremental (so o mes novo) ~US$0,27 (ver nota).
#  LICAO: SEMPRE SIT_SITE_ID='MLB' nesta view (all-sites infla o BPC).
# =====================================================================
$BPC_FILT  = "SIT_SITE_ID='MLB' AND VERTICAL='HOME ELECTRONICS' AND DOM_AGG_1='LARGE APPLIANCES' AND FAVORABILITY_TYPE IN ('BOX_ALL_ABC','BOX_ALL_ABC_PIX','SHP_ALL_ABC')"
$BPC_FAIXA = "CASE WHEN PRICE_MELI IS NULL THEN '0_sem_preco' WHEN PRICE_MELI<200 THEN '1_<200' WHEN PRICE_MELI<500 THEN '2_200-500' WHEN PRICE_MELI<1500 THEN '3_500-1500' WHEN PRICE_MELI<3000 THEN '4_1500-3000' ELSE '5_>3000' END"
# de-para segmento BPC (taxonomia SEGMENTO_SELLER_DETAIL 2026; Bia validou: ASESORADO PF=CA E 3P ASESORADO DIRECTO=CA -> 3P Assessorada)
$BPC_SEG   = "CASE WHEN SEGMENTO_SELLER_DETAIL='FIRST PARTY' THEN '1P' WHEN SEGMENTO_SELLER_DETAIL LIKE 'CBT%' THEN 'CBT' WHEN SEGMENTO_SELLER_DETAIL IN ('ASESORADO PF','3P ASESORADO DIRECTO') THEN '3P Assessorada' ELSE '3P Dev' END"
$BPC_SPE   = "(SELECT AS STRUCT SUM(c.VISITS_MATCH) AS m, SUM(c.VISITS_CHEAPER)+SUM(c.VISITS_EQUAL) AS ce FROM UNNEST(COMPETITORS) c WHERE c.COMP_RIVAL_NAME='Shopee')"
$BPC_MEAS  = "GROUPING(marca) AS gm, GROUPING(seller_id) AS gs, ROUND(SUM(vm),1) AS t_m, ROUND(SUM(vce),1) AS t_ce, ROUND(SUM(IF(crw='Shopee',vm,0)),1) AS w_m, ROUND(SUM(IF(crw='Shopee',vce,0)),1) AS w_ce, ROUND(SUM(spe.m),1) AS s_m, ROUND(SUM(spe.ce),1) AS s_ce"

# datas de data-dupla = M/M +/- 1 dia (Fev..mes-Through; Jan sem DD). Ajuste manual se o evento for irregular.
$ddList = @(); $yBpc = [int]$Through.Substring(0,4); $mThru = [int]$Through.Substring(5,2)
for($mm=2; $mm -le $mThru; $mm++){ $b=Get-Date -Year $yBpc -Month $mm -Day $mm; $ddList += $b.AddDays(-1).ToString('yyyy-MM-dd'); $ddList += $b.ToString('yyyy-MM-dd'); $ddList += $b.AddDays(1).ToString('yyyy-MM-dd') }
$DD_IN = ($ddList | ForEach-Object { "'$_'" }) -join ","

$qBpcMon = @"
WITH base AS (SELECT FORMAT_DATE('%Y-%m',TIM_DAY) AS mes, FAVORABILITY_TYPE AS favtype, CAST(KMI AS STRING) AS kmi, $BPC_FAIXA AS faixa, $BPC_SEG AS segmento, DOM_AGG_2 AS d2, REAL_BRAND AS marca, CUS_CUST_ID_SEL AS seller_id, VISITS_MATCH AS vm, (VISITS_CHEAPER+VISITS_EQUAL) AS vce, COMP_RIVAL_NAME_WINNER AS crw, $BPC_SPE AS spe FROM ``meli-bi-data.WHOWNER.BT_COM_FAVORABILITY`` WHERE $BPC_FILT AND TIM_DAY BETWEEN '2025-01-01' AND '$END')
SELECT mes,favtype,kmi,faixa,segmento,d2,marca,seller_id, $BPC_MEAS FROM base GROUP BY GROUPING SETS ((mes,favtype,kmi,faixa,segmento,d2),(mes,favtype,faixa,segmento,marca),(mes,favtype,faixa,segmento,seller_id))
"@
$qBpcDD = @"
WITH base AS (SELECT CAST(TIM_DAY AS STRING) AS dia, FAVORABILITY_TYPE AS favtype, CAST(KMI AS STRING) AS kmi, $BPC_FAIXA AS faixa, $BPC_SEG AS segmento, DOM_AGG_2 AS d2, REAL_BRAND AS marca, CUS_CUST_ID_SEL AS seller_id, VISITS_MATCH AS vm, (VISITS_CHEAPER+VISITS_EQUAL) AS vce, COMP_RIVAL_NAME_WINNER AS crw, $BPC_SPE AS spe FROM ``meli-bi-data.WHOWNER.BT_COM_FAVORABILITY`` WHERE $BPC_FILT AND TIM_DAY IN ($DD_IN))
SELECT dia,favtype,kmi,faixa,segmento,d2,marca,seller_id, $BPC_MEAS FROM base GROUP BY GROUPING SETS ((dia,favtype,kmi,faixa,segmento,d2),(dia,favtype,faixa,segmento,marca),(dia,favtype,faixa,segmento,seller_id))
"@
# id->nome do seller (CUS_CUST_ID_SEL = mesma chave da FAVORABILITY; CUS_NICKNAME e' PII-bloqueado)
$qBpcNames = @"
SELECT CAST(CUS_CUST_ID_SEL AS STRING) AS id, ANY_VALUE(SELLER_NAME) AS nome FROM ``meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB`` WHERE VERTICAL='HOME ELECTRONICS' AND DOM_DOMAIN_AGG1='LARGE APPLIANCES' AND ORD_CLOSED_DT BETWEEN '2025-01-01' AND '$END' AND CUS_CUST_ID_SEL IS NOT NULL GROUP BY 1
"@

# =====================================================================
#  PILAR DEMANDA & CONVERSAO  (ITEM-LEVEL: DM_MKP_VISITS + DM_EFICIENCIA_MLB via bridge item->atributo)
#  Bridge item->{faixa(mediana preco gross), d2, segmento(2 taxonomias), marca, seller, modal, picking, frete}.
#  Visitas FULL OUTER JOIN pedidos (GMV_FLG) por item x dia -> CVR alinhado, calibra ~1,3% (bate COMMERCE/Looker).
#  GROUPING SETS: struct (faixa x d2 x seg x modal x picking x frete) + marca + seller (bounded top-8/faixa).
#  Derivacao local pre-agrega mes+semana (campo g + mo). VIP = coluna (vip), cruza tudo. Custo ~US$0,25/refresh.
# =====================================================================
$qDem2 = @"
WITH it AS (SELECT ITE_ITEM_ID iid, APPROX_QUANTILES(ITE_ITEM_FULL_UNIT_PRICE,2)[OFFSET(1)] med, ANY_VALUE(DOM_DOMAIN_AGG2) d2, ANY_VALUE(SEGMENTO_SELLER_DETAIL) sraw, COALESCE(NULLIF(ANY_VALUE(ITE_ITEM_BRAND),''),'(sem marca)') marca, CAST(ANY_VALUE(CUS_CUST_ID_SEL) AS STRING) seller, LOWER(ANY_VALUE(SHIPPING_MODE)) modal, ANY_VALUE(PICKING_TYPE) picking, IF(ANY_VALUE(FREE_SHIPPING_BUYER_FLG),'gratis','pago') frete FROM ``meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB`` WHERE VERTICAL='HOME ELECTRONICS' AND DOM_DOMAIN_AGG1='LARGE APPLIANCES' AND ORD_CLOSED_DT BETWEEN '2025-01-01' AND '$END' AND ITE_ITEM_FULL_UNIT_PRICE>0 GROUP BY 1), br AS (SELECT iid, CASE WHEN med<200 THEN '1_<200' WHEN med<500 THEN '2_200-500' WHEN med<1500 THEN '3_500-1500' WHEN med<3000 THEN '4_1500-3000' ELSE '5_>3000' END faixa, d2, CASE WHEN sraw IN ('FIRST PARTY','PRIVATE LABEL') THEN '1P' WHEN sraw LIKE 'CBT%' THEN 'CBT' WHEN sraw IN ('ASESORADO PF','3P ASESORADO DIRECTO') THEN '3P Assessorada' ELSE '3P Dev' END seg, marca, seller, modal, picking, frete FROM it), vv AS (SELECT ITE_ITEM_ID iid, TIM_DAY dia, SUM(QTY_VISITS) v, SUM(QTY_VISITS_VIP) vip FROM ``meli-bi-data.WHOWNER.DM_MKP_VISITS`` WHERE SIT_SITE_ID='MLB' AND VERTICAL_DOMAIN='HOME ELECTRONICS' AND DOM_DOMAIN_AGG1='LARGE APPLIANCES' AND TIM_DAY BETWEEN '2025-01-01' AND '$END' GROUP BY 1,2), oo AS (SELECT ITE_ITEM_ID iid, ORD_CLOSED_DT dia, COUNT(DISTINCT ORD_ORDER_ID) ped FROM ``meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB`` WHERE VERTICAL='HOME ELECTRONICS' AND DOM_DOMAIN_AGG1='LARGE APPLIANCES' AND ORD_CLOSED_DT BETWEEN '2025-01-01' AND '$END' AND GMV_FLG GROUP BY 1,2), j AS (SELECT COALESCE(vv.iid,oo.iid) iid, COALESCE(vv.dia,oo.dia) dia, IFNULL(vv.v,0) v, IFNULL(vv.vip,0) vip, IFNULL(oo.ped,0) ped FROM vv FULL OUTER JOIN oo ON vv.iid=oo.iid AND vv.dia=oo.dia), jb AS (SELECT CAST(j.dia AS STRING) dia, COALESCE(br.faixa,'0_sem_faixa') faixa, COALESCE(br.d2,'(s/d2)') d2, COALESCE(br.seg,'(s/seg)') seg, COALESCE(br.marca,'(s/marca)') marca, COALESCE(br.seller,'0') seller, COALESCE(br.modal,'(s/mod)') modal, COALESCE(br.picking,'(s/pick)') picking, COALESCE(br.frete,'(s/frete)') frete, j.v, j.vip, j.ped FROM j LEFT JOIN br ON j.iid=br.iid), mn AS (SELECT faixa,marca FROM (SELECT faixa,marca,ROW_NUMBER() OVER(PARTITION BY faixa ORDER BY SUM(v) DESC) rn FROM jb WHERE marca!='(s/marca)' GROUP BY 1,2) WHERE rn<=8), sn AS (SELECT faixa,seller FROM (SELECT faixa,seller,ROW_NUMBER() OVER(PARTITION BY faixa ORDER BY SUM(v) DESC) rn FROM jb WHERE seller!='0' GROUP BY 1,2) WHERE rn<=8), b2 AS (SELECT jb.*, IF(mn.marca IS NULL,'Outros',jb.marca) mb, IF(sn.seller IS NULL,'Outros',jb.seller) sb FROM jb LEFT JOIN mn ON jb.faixa=mn.faixa AND jb.marca=mn.marca LEFT JOIN sn ON jb.faixa=sn.faixa AND jb.seller=sn.seller) SELECT dia,faixa,d2,seg,modal,picking,frete,mb AS marca,sb AS seller,GROUPING(mb) gm,GROUPING(sb) gs,SUM(v) v,SUM(vip) vip,SUM(ped) ped FROM b2 GROUP BY GROUPING SETS ((dia,faixa,d2,seg,modal,picking,frete),(dia,faixa,d2,seg,mb),(dia,faixa,d2,seg,sb))
"@
$qDem2Names = @"
SELECT CAST(CUS_CUST_ID_SEL AS STRING) id, ANY_VALUE(SELLER_NAME) nome FROM ``meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB`` WHERE VERTICAL='HOME ELECTRONICS' AND DOM_DOMAIN_AGG1='LARGE APPLIANCES' AND ORD_CLOSED_DT BETWEEN '2025-01-01' AND '$END' AND CUS_CUST_ID_SEL IS NOT NULL GROUP BY 1
"@

# ---- roda no bq -> CSV ----
function RunBQ([string]$sql,[string]$file) {
  $flat = ($sql -replace '\r?\n',' ').Trim()   # PS5.1 trunca SQL multi-linha como arg de .exe -> achatar em 1 linha
  $p = Join-Path $sp $file
  Write-Host "  bq -> $file ..."
  bq --project_id=meli-bi-data query --use_legacy_sql=false --format=csv --max_rows=1000000 --quiet $flat > $p
}
RunBQ $qMain   "cubo_large_18m.csv"
RunBQ $qSeller "seller_cube.csv"
RunBQ $qGrowth "growth_cube.csv"
RunBQ $qBrand  "brand_cube.csv"
RunBQ $qSB     "sb_cube.csv"
RunBQ $qBpcMon   "bpc_master.csv"
RunBQ $qBpcDD    "bpc_dd_master.csv"
RunBQ $qBpcNames "seller_names.csv"
RunBQ $qDem2      "dem2_master.csv"
RunBQ $qDem2Names "dem2_names.csv"

# ---- deriva os 6 cubos BPC dos masters (split gm/gs + bounding top-6/faixa + rotulo seller). ~3min (Import-Csv dos masters grandes) ----
$invBpc=[Globalization.CultureInfo]::InvariantCulture; $anyBpc=[Globalization.NumberStyles]::Any
function nzn($v){ $d=0.0; if([double]::TryParse("$v",$anyBpc,$invBpc,[ref]$d)){$d}else{0.0} }   # parse decimal '.' do bq independe da cultura
$bpcMets='t_m','t_ce','w_m','w_ce','s_m','s_ce'
$SNM=@{}; Import-Csv (Join-Path $sp "seller_names.csv") -Encoding UTF8 | ForEach-Object { $SNM[$_.id]=$_.nome }
function BpcDerive([string]$csv,[string]$keyCol,[string]$fStruct,[string]$fMarca,[string]$fSeller){
  $rows=Import-Csv (Join-Path $sp $csv) -Encoding UTF8
  $struct=New-Object System.Collections.ArrayList; $wM=@{}; $wS=@{}
  foreach($r in $rows){
    if($r.gm -eq '1' -and $r.gs -eq '1'){ $o=[ordered]@{}; $o[$keyCol]=$r.$keyCol;$o.favtype=$r.favtype;$o.kmi=$r.kmi;$o.faixa=$r.faixa;$o.segmento=$r.segmento;$o.d2=$r.d2; foreach($m in $bpcMets){$o[$m]=[math]::Round((nzn $r.$m),1)}; [void]$struct.Add([pscustomobject]$o) }
    elseif($r.gm -eq '0'){ if(-not $wM[$r.faixa]){$wM[$r.faixa]=@{}}; $wM[$r.faixa][$r.marca]=(nzn $wM[$r.faixa][$r.marca])+(nzn $r.t_m) }
    elseif($r.gs -eq '0'){ if(-not $wS[$r.faixa]){$wS[$r.faixa]=@{}}; $wS[$r.faixa][$r.seller_id]=(nzn $wS[$r.faixa][$r.seller_id])+(nzn $r.t_m) }
  }
  $topM=@{}; foreach($f in $wM.Keys){ $hh=@{}; ($wM[$f].GetEnumerator()|Sort-Object Value -Descending|Select-Object -First 6 -ExpandProperty Key)|ForEach-Object{$hh["$_"]=$true}; $topM[$f]=$hh }
  $topS=@{}; foreach($f in $wS.Keys){ $hh=@{}; ($wS[$f].GetEnumerator()|Sort-Object Value -Descending|Select-Object -First 6 -ExpandProperty Key)|ForEach-Object{$hh["$_"]=$true}; $topS[$f]=$hh }
  $accM=@{}; $accS=@{}
  foreach($r in $rows){
    if($r.gm -eq '0'){ $mk= if($topM[$r.faixa] -and $topM[$r.faixa].ContainsKey("$($r.marca)")){$r.marca}else{'Outros'}; $k="$($r.$keyCol)|$($r.favtype)|$($r.faixa)|$($r.segmento)|$mk"; if(-not $accM[$k]){$accM[$k]=@{key=$r.$keyCol;favtype=$r.favtype;faixa=$r.faixa;segmento=$r.segmento;e=$mk;t_m=0.0;t_ce=0.0;w_m=0.0;w_ce=0.0;s_m=0.0;s_ce=0.0}}; foreach($m in $bpcMets){$accM[$k][$m]+=(nzn $r.$m)} }
    elseif($r.gs -eq '0'){ $sid=$r.seller_id; $keep=($topS[$r.faixa] -and $topS[$r.faixa].ContainsKey("$sid")); $snm= if($keep){ if($SNM[$sid]){$SNM[$sid]}else{$sid} }else{'Outros'}; $k="$($r.$keyCol)|$($r.favtype)|$($r.faixa)|$($r.segmento)|$snm"; if(-not $accS[$k]){$accS[$k]=@{key=$r.$keyCol;favtype=$r.favtype;faixa=$r.faixa;segmento=$r.segmento;e=$snm;t_m=0.0;t_ce=0.0;w_m=0.0;w_ce=0.0;s_m=0.0;s_ce=0.0}}; foreach($m in $bpcMets){$accS[$k][$m]+=(nzn $r.$m)} }
  }
  $mk2=$accM.Values|ForEach-Object{ $o=[ordered]@{};$o[$keyCol]=$_.key;$o.favtype=$_.favtype;$o.faixa=$_.faixa;$o.segmento=$_.segmento;$o.marca=$_.e; foreach($m in $bpcMets){$o[$m]=[math]::Round($_.$m,1)}; [pscustomobject]$o }
  $sl2=$accS.Values|ForEach-Object{ $o=[ordered]@{};$o[$keyCol]=$_.key;$o.favtype=$_.favtype;$o.faixa=$_.faixa;$o.segmento=$_.segmento;$o.seller=$_.e; foreach($m in $bpcMets){$o[$m]=[math]::Round($_.$m,1)}; [pscustomobject]$o }
  ($struct|ConvertTo-Json -Depth 3 -Compress)|Out-File (Join-Path $sp $fStruct) -Encoding utf8
  (@($mk2)|ConvertTo-Json -Depth 3 -Compress)|Out-File (Join-Path $sp $fMarca) -Encoding utf8
  (@($sl2)|ConvertTo-Json -Depth 3 -Compress)|Out-File (Join-Path $sp $fSeller) -Encoding utf8
  Write-Host ("  BPC {0}: struct={1} marca={2} seller={3}" -f $csv,$struct.Count,@($mk2).Count,@($sl2).Count)
}
BpcDerive "bpc_master.csv"    "mes" "bpc_struct.json"    "bpc_marca.json"    "bpc_seller.json"
BpcDerive "bpc_dd_master.csv" "dia" "bpc_dd_struct.json" "bpc_dd_marca.json" "bpc_dd_seller.json"

# ---- deriva os 3 cubos de Demanda do master item-level: split gm/gs + pre-agrega mes+semana+data-dupla (g + mo) ----
# g='d' (data-dupla) so nos dias do $ddList (M/M+/-1, mesmas 18 datas do bloco BPC); per=dia, mo=mes p/ o filtro de mes agrupar no CVR.
$demNm=@{}; Import-Csv (Join-Path $sp "dem2_names.csv") -Encoding UTF8 | ForEach-Object { $demNm[$_.id]=$_.nome }
$dinv=[Globalization.CultureInfo]::InvariantCulture; $dcal=$dinv.Calendar
$ddSet=@{}; $ddList | ForEach-Object { $ddSet[$_]=$true }
$wkc=@{}
function DWkMo($s){ if($wkc.ContainsKey($s)){return $wkc[$s]}; $d=[datetime]::ParseExact($s,'yyyy-MM-dd',$dinv); $dw=[int]$d.DayOfWeek; $thu=$d.AddDays(3-(($dw+6)%7)); $r=@(("{0}-W{1:D2}" -f $thu.Year,$dcal.GetWeekOfYear($thu,[Globalization.CalendarWeekRule]::FirstFourDayWeek,[DayOfWeek]::Monday)),$thu.ToString('yyyy-MM')); $wkc[$s]=$r; return $r }
$dm=Import-Csv (Join-Path $sp "dem2_master.csv") -Encoding UTF8; $daS=@{}; $daM=@{}; $daL=@{}
foreach($x in $dm){ $mth=$x.dia.Substring(0,7); $w=DWkMo $x.dia; $v=[double]$x.v;$vp=[double]$x.vip;$p=[double]$x.ped
  $grains=@( ,@('m',$mth,$mth) ); $grains+=,@('w',$w[0],$w[1]); if($ddSet.ContainsKey($x.dia)){ $grains+=,@('d',$x.dia,$mth) }
  foreach($gp in $grains){
    if($x.gm -eq '1' -and $x.gs -eq '1'){ $k="$($gp[0])|$($gp[1])|$($x.faixa)|$($x.d2)|$($x.seg)|$($x.modal)|$($x.picking)|$($x.frete)"; if(-not $daS[$k]){$daS[$k]=@{g=$gp[0];per=$gp[1];mo=$gp[2];fx=$x.faixa;d2=$x.d2;sg=$x.seg;md=$x.modal;pk=$x.picking;fr=$x.frete;v=0.0;vp=0.0;p=0.0}}; $daS[$k].v+=$v;$daS[$k].vp+=$vp;$daS[$k].p+=$p }
    elseif($x.gm -eq '0'){ $k="$($gp[0])|$($gp[1])|$($x.faixa)|$($x.d2)|$($x.seg)|$($x.marca)"; if(-not $daM[$k]){$daM[$k]=@{g=$gp[0];per=$gp[1];mo=$gp[2];fx=$x.faixa;d2=$x.d2;sg=$x.seg;mc=$x.marca;v=0.0;vp=0.0;p=0.0}}; $daM[$k].v+=$v;$daM[$k].vp+=$vp;$daM[$k].p+=$p }
    elseif($x.gs -eq '0'){ $s=$x.seller; $lbl= if($s -eq 'Outros'){'Outros'}elseif($demNm.ContainsKey($s)){$demNm[$s]}else{$s}; $k="$($gp[0])|$($gp[1])|$($x.faixa)|$($x.d2)|$($x.seg)|$lbl"; if(-not $daL[$k]){$daL[$k]=@{g=$gp[0];per=$gp[1];mo=$gp[2];fx=$x.faixa;d2=$x.d2;sg=$x.seg;sl=$lbl;v=0.0;vp=0.0;p=0.0}}; $daL[$k].v+=$v;$daL[$k].vp+=$vp;$daL[$k].p+=$p }
  } }
function DDump($h,$fields,$file){ $arr=$h.Values|ForEach-Object{ $o=[ordered]@{}; foreach($f in $fields){ $o[$f]= if($f -in 'v','vp','p'){[int]$_.$f}else{$_.$f} }; [pscustomobject]$o }; ($arr|ConvertTo-Json -Compress)|Out-File (Join-Path $sp $file) -Encoding utf8; $arr.Count }
$null=DDump $daS @('g','per','mo','fx','d2','sg','md','pk','fr','v','vp','p') "dem2_struct.json"
$null=DDump $daM @('g','per','mo','fx','d2','sg','mc','v','vp','p') "dem2_marca.json"
$null=DDump $daL @('g','per','mo','fx','d2','sg','sl','v','vp','p') "dem2_seller.json"
Write-Host ("  Demanda item-level: struct {0} / marca {1} / seller {2}" -f $daS.Count,$daM.Count,$daL.Count)

# ---- reconciliacao rapida (sanity) ----
foreach ($f in "cubo_large_18m.csv","seller_cube.csv","growth_cube.csv","brand_cube.csv","sb_cube.csv") {
  $rows = Import-Csv (Join-Path $sp $f) -Encoding UTF8
  $tot  = ($rows | Where-Object {$_.mes -eq $Through} | Measure-Object nmv_mi -Sum).Sum
  Write-Host ("  {0}: {1} linhas | NMV {2} = {3} Mi" -f $f,$rows.Count,$Through,[math]::Round($tot,1))
}
# sanity BPC (Total ABC do mes -Through; jun/26 validado = 42,7%)
$bs = Get-Content (Join-Path $sp "bpc_struct.json") -Raw | ConvertFrom-Json | Where-Object { $_.favtype -eq 'BOX_ALL_ABC' -and $_.mes -eq $Through }
$sm=($bs|ForEach-Object{nzn $_.t_m}|Measure-Object -Sum).Sum; $sce=($bs|ForEach-Object{nzn $_.t_ce}|Measure-Object -Sum).Sum
if($sm -gt 0){ Write-Host ("  BPC {0} ABC Total = {1}% (match {2:N0})" -f $Through,[math]::Round($sce/$sm*100,1),$sm) }

# ---- injeta nos placeholders do template ----
function J([string]$csv) { Import-Csv (Join-Path $sp $csv) -Encoding UTF8 | ConvertTo-Json -Depth 3 -Compress }
function JF([string]$f) { [IO.File]::ReadAllText((Join-Path $sp $f),[Text.Encoding]::UTF8) }   # cubo BPC ja e' JSON; ReadAllText UTF8 tira BOM
$html = [IO.File]::ReadAllText($tpl,[Text.Encoding]::UTF8)
$html = $html.Replace('/*__DATA__*/[]',(J "cubo_large_18m.csv")).Replace('/*__SELLERS__*/[]',(J "seller_cube.csv")).Replace('/*__GROWTH__*/[]',(J "growth_cube.csv")).Replace('/*__BRAND__*/[]',(J "brand_cube.csv")).Replace('/*__SB__*/[]',(J "sb_cube.csv"))
$html = $html.Replace('/*__BPC_STRUCT__*/[]',(JF "bpc_struct.json")).Replace('/*__BPC_MARCA__*/[]',(JF "bpc_marca.json")).Replace('/*__BPC_SELLER__*/[]',(JF "bpc_seller.json")).Replace('/*__BPC_DD_STRUCT__*/[]',(JF "bpc_dd_struct.json")).Replace('/*__BPC_DD_MARCA__*/[]',(JF "bpc_dd_marca.json")).Replace('/*__BPC_DD_SELLER__*/[]',(JF "bpc_dd_seller.json")).Replace('/*__SELLER_NAMES__*/{}','{}')   # SELLER_NAMES nao e' usado pelo JS (nome ja vem no cubo) -> nao inflar
$html = $html.Replace('/*__DEM_STRUCT__*/[]',(JF "dem2_struct.json")).Replace('/*__DEM_MARCA__*/[]',(JF "dem2_marca.json")).Replace('/*__DEM_SELLER__*/[]',(JF "dem2_seller.json"))
[IO.File]::WriteAllText($out,$html,(New-Object System.Text.UTF8Encoding($false)))
$bytes=(Get-Item $out).Length; $left=([regex]::Matches($html,'/\*__[A-Z_]+__\*/')).Count
Write-Host ("  template injetado -> {0:N0} bytes = {1} MB | placeholders restantes: {2}" -f $bytes,[math]::Round($bytes/1MB,2),$left)
if($left -gt 0){ Write-Host "  !! ABORTAR: placeholder nao substituido (cubo faltando?)"; return }
# ---- sobe nova versao no Grid: inline (<=10 MB) ou PRESIGNED 3-passos (>10 MB; teto real=500 MB) ----
$cfgO = Get-Content $cfg -Raw | ConvertFrom-Json; $docId=$cfgO.doc_id; $sv=$cfgO.skill_version
if($bytes -le 10485760){
  $resp = curl.exe -sS -X POST "https://grid.melioffice.com/api/v1/engine/run" -F "config=<$cfg" -F "file=@$out"
} else {
  Write-Host "  > 10 MB -> upload PRESIGNED (Flow B: reserva slot -> PUT -> confirm)"
  $j1="{`"skill_version`":`"$sv`",`"doc_id`":`"$docId`",`"presigned_upload`":{`"filename`":`"dashboard_shield_large.html`",`"content_type`":`"text/html`",`"file_size`":$bytes}}"
  [IO.File]::WriteAllText((Join-Path $sp "step1.json"),$j1,(New-Object System.Text.UTF8Encoding($false)))
  $slot=((curl.exe -sS -X POST "https://grid.melioffice.com/api/v1/engine/run/json" -H "Content-Type: application/json" -d ("@"+(Join-Path $sp "step1.json")))|ConvertFrom-Json).doc_id
  curl.exe -sS -o NUL -X PUT "https://grid.melioffice.com/api/v1/documents/$slot/upload-content" -H "Content-Type: text/html" --data-binary ("@"+$out) | Out-Null
  $j3="{`"skill_version`":`"$sv`",`"doc_id`":`"$slot`",`"confirm_presigned`":true,`"file_size`":$bytes}"
  [IO.File]::WriteAllText((Join-Path $sp "step3.json"),$j3,(New-Object System.Text.UTF8Encoding($false)))
  $resp = curl.exe -sS -X POST "https://grid.melioffice.com/api/v1/engine/run/json" -H "Content-Type: application/json" -d ("@"+(Join-Path $sp "step3.json"))
}
Write-Host $resp
Write-Host "== Refresh concluido =="
