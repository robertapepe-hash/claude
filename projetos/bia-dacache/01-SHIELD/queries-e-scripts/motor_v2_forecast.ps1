# MOTOR v2 — decomposicao multiplicativa em log + tendencia recente amortecida
# Etapas: (1) S_m via log-linear com sazonalidade deterministica (2 passes)
#         (2) dessazonaliza  (3) nivel = L3M  (4) tendencia = OLS em log(D) nos ultimos N meses
#         (5) projeta com amortecimento phi
$ErrorActionPreference = 'Stop'

$sql = @'
WITH r AS (
SELECT CASE DOM_DOMAIN_AGG1 WHEN 'LARGE APPLIANCES' THEN 'LARGE' WHEN 'SMALL APPLIANCES' THEN 'SMALL' ELSE 'H_C' END d1,
FAIXA_ASP_NOVA fx, DATA, CAST(GMV_SHOPEE AS FLOAT64) s, CAST(TGMV_MELI AS FLOAT64) m
FROM `meli-bi-data.SBOX_MKPBR.DM_MARKET_ASP_MONTHLY_VERTICAL_D1`
WHERE VERTICAL='HOME ELECTRONICS' AND DATA BETWEEN '2023-01-01' AND '2026-06-30'
AND ((DOM_DOMAIN_AGG1='LARGE APPLIANCES' AND FAIXA_ASP_NOVA IN ('200 a 500','500 a 1500','1500 a 3000','+3000'))
OR (DOM_DOMAIN_AGG1='HEATING, COOLING & AIR QUALITY' AND FAIXA_ASP_NOVA IN ('200 a 500','500 a 1500','1500 a 3000','+3000'))
OR (DOM_DOMAIN_AGG1='SMALL APPLIANCES' AND FAIXA_ASP_NOVA IN ('120 a 150','150 a 200','200 a 500','500 a 1500','+3000'))))
SELECT d1, fx, FORMAT_DATE('%Y-%m',DATA) mes, ROUND(SUM(s),4) shp, ROUND(SUM(m),4) meli FROM r GROUP BY 1,2,3
'@
$out = bq query --project_id=meli-bi-data --use_legacy_sql=false --format=csv --max_rows=2000 (($sql -replace "\s+"," ").Trim())
$hh = $out | Where-Object { $_ -like 'd1,*' } | Select-Object -First 1
$raw = $out[([Array]::IndexOf($out,$hh))..($out.Count-1)] | ConvertFrom-Csv | Where-Object { $_.d1 }

function TIdx($mes){ $y=[int]$mes.Substring(0,4); $m=[int]$mes.Substring(5,2); return [int](($y-2023)*12 + $m) }
function CMon($mes){ return [int]$mes.Substring(5,2) }
function MesDe($t){ $y=2023+[math]::Floor(($t-1)/12); $m=(($t-1)%12)+1; return "$y-$('{0:d2}' -f $m)" }

# serie por D1 (soma das faixas-foco), com opcao de excluir celula
function Serie($d1, $campo, $excluirFx){
  $h=@{}
  foreach($r in $raw){
    if($r.d1 -ne $d1){ continue }
    if($excluirFx -and $r.fx -eq $excluirFx){ continue }
    $t=TIdx $r.mes
    if(-not $h.ContainsKey($t)){ $h[$t]=0.0 }
    $h[$t] += [double]$r.$campo
  }
  return $h
}
function OLS($xs,$ys){
  $n=$xs.Count; if($n -lt 2){ return @(0.0,0.0) }
  $mx=($xs|Measure-Object -Average).Average; $my=($ys|Measure-Object -Average).Average
  $sxy=0.0; $sxx=0.0
  for($i=0;$i -lt $n;$i++){ $sxy += ($xs[$i]-$mx)*($ys[$i]-$my); $sxx += [math]::Pow($xs[$i]-$mx,2) }
  if($sxx -eq 0){ return @($my,0.0) }
  $b=$sxy/$sxx; $a=$my-$b*$mx; return @($a,$b)
}

# Estima S_m (indice sazonal multiplicativo) por decomposicao em log, 2 passes
function Sazonal($serie,$tIni,$tFim){
  $tIni=[int]$tIni; $tFim=[int]$tFim
  $ts=@(); $ly=@()
  foreach($t in ($serie.Keys|Sort-Object)){ if($t -ge $tIni -and $t -le $tFim -and $serie[$t] -gt 0){ $ts+=$t; $ly+=[math]::Log($serie[$t]) } }
  $sm=@{}; 1..12|ForEach-Object{ $sm[$_]=0.0 }
  for($pass=1; $pass -le 2; $pass++){
    $adj=@(); for($i=0;$i -lt $ts.Count;$i++){ $adj += ($ly[$i] - $sm[(CMon (MesDe $ts[$i]))]) }
    $ab=OLS $ts $adj
    $acc=@{}; 1..12|ForEach-Object{ $acc[$_]=@() }
    for($i=0;$i -lt $ts.Count;$i++){ $res = $adj[$i] - ($ab[0]+$ab[1]*$ts[$i]); $acc[(CMon (MesDe $ts[$i]))] += $res }
    $novo=@{}; foreach($m in 1..12){ if($acc[$m].Count -gt 0){ $novo[$m]=$sm[$m] + ($acc[$m]|Measure-Object -Average).Average } else { $novo[$m]=$sm[$m] } }
    $mu=(1..12|ForEach-Object{$novo[$_]}|Measure-Object -Average).Average
    foreach($m in 1..12){ $sm[$m]=$novo[$m]-$mu }
  }
  $S=@{}; foreach($m in 1..12){ $S[$m]=[math]::Exp($sm[$m]) }
  return $S
}

# Ajusta nivel L3M + tendencia g, e projeta
function Projeta($serie,$S,$tIni,$tFim,$N,$phi,$alvos){
  $tIni=[int]$tIni; $tFim=[int]$tFim; $N=[int]$N; $phi=[double]$phi
  # dessazonaliza
  $D=@{}
  foreach($t in ($serie.Keys|Sort-Object)){ if($t -ge $tIni -and $t -le $tFim -and $serie[$t] -gt 0){ $D[$t]=$serie[$t]/$S[(CMon (MesDe $t))] } }
  $keys=$D.Keys|Sort-Object
  # nivel L3M (centrado em tFim-1)
  $l3=@(); foreach($t in @(($tFim-2),($tFim-1),($tFim))){ if($D.ContainsKey($t)){ $l3+=$D[$t] } }
  $L=($l3|Measure-Object -Average).Average
  # tendencia nos ultimos N meses
  $ts=@(); $ly=@()
  foreach($t in $keys){ if($t -gt ($tFim-$N) -and $t -le $tFim){ $ts+=$t; $ly+=[math]::Log($D[$t]) } }
  $ab=OLS $ts $ly; $g=[math]::Exp($ab[1])-1
  $res=@{}
  foreach($ta in $alvos){
    $steps=$ta-($tFim-1)   # nivel L3M esta centrado em tFim-1
    $f=1.0; for($j=1;$j -le $steps;$j++){ $f *= (1 + $g*[math]::Pow($phi,$j)) }
    $res[$ta]=$L*$f*$S[(CMon (MesDe $ta))]
  }
  return @{ g=$g; L=$L; fc=$res }
}

$D1S=@('H_C','LARGE','SMALL')
$tShpIni=[int](TIdx '2024-01'); $tMeliIni=[int](TIdx '2023-01')
$tFimFull=[int](TIdx '2026-06'); $tFimBT=[int](TIdx '2025-12')

# ---------- A) INDICES SAZONAIS ----------
Write-Output "=== A) INDICE SAZONAL S_m (base: Shopee 2024-01..2026-06 | MELI 2023-01..2026-06) ==="
Write-Output "serie;jan;fev;mar;abr;mai;jun;jul;ago;set;out;nov;dez"
$Ssh=@{}; $Sme=@{}
foreach($d in $D1S){
  $Ssh[$d]=Sazonal (Serie $d 'shp' $null) $tShpIni $tFimFull
  $Sme[$d]=Sazonal (Serie $d 'meli' $null) $tMeliIni $tFimFull
  Write-Output "SHP_$d;$((1..12|ForEach-Object{ [math]::Round($Ssh[$d][$_],2) }) -join ';')"
  Write-Output "MELI_$d;$((1..12|ForEach-Object{ [math]::Round($Sme[$d][$_],2) }) -join ';')"
}

# ---------- B) BACKTEST v2 (fit ate dez/25 -> preve jan-jun/26) ----------
$alvosBT=@(); for($k=1;$k -le 6;$k++){ $alvosBT += ($tFimBT+$k) }
Write-Output ""
Write-Output "=== B) BACKTEST MOTOR v2 — fit ate dez/25, preve jan-jun/26 ==="
Write-Output "N_tend;phi;escopo;WAPE_shp_mes;erro_total_6m_shp;MAPE_ratio;erro_ratio_pp"
foreach($N in @(3,6)){
 foreach($phi in @(1.0,0.9,0.8)){
  $agg=@{}
  foreach($d in $D1S){
    $ss=Serie $d 'shp' $null; $mm=Serie $d 'meli' $null
    $Sb=Sazonal $ss $tShpIni $tFimBT; $Mb=Sazonal $mm $tMeliIni $tFimBT
    $ps=Projeta $ss $Sb $tShpIni $tFimBT $N $phi $alvosBT
    $pm=Projeta $mm $Mb $tMeliIni $tFimBT $N $phi $alvosBT
    $abs=0.0;$act=0.0;$pt=0.0;$ape=0.0;$pp=0.0;$cnt=0
    foreach($ta in $alvosBT){
      if(-not ($ss.ContainsKey($ta) -and $mm.ContainsKey($ta))){ continue }
      $abs+=[math]::Abs($ps.fc[$ta]-$ss[$ta]); $act+=$ss[$ta]; $pt+=$ps.fc[$ta]
      $rA=$ss[$ta]/$mm[$ta]; $rP=$ps.fc[$ta]/$pm.fc[$ta]
      $ape+=[math]::Abs($rP-$rA)/$rA; $pp+=[math]::Abs($rP-$rA)*100; $cnt++
    }
    foreach($sc in @($d,'TOTAL')){
      if(-not $agg.ContainsKey($sc)){ $agg[$sc]=@{abs=0.0;act=0.0;pt=0.0;ape=0.0;pp=0.0;n=0} }
      $agg[$sc].abs+=$abs; $agg[$sc].act+=$act; $agg[$sc].pt+=$pt; $agg[$sc].ape+=$ape; $agg[$sc].pp+=$pp; $agg[$sc].n+=$cnt
    }
  }
  foreach($sc in @('H_C','LARGE','SMALL','TOTAL')){
    $e=$agg[$sc]
    Write-Output "$N;$phi;$sc;$([math]::Round($e.abs/$e.act*100,1));$([math]::Round(($e.pt-$e.act)/$e.act*100,1));$([math]::Round($e.ape/$e.n*100,1));$([math]::Round($e.pp/$e.n,1))"
  }
 }
}

# ---------- C) H&C SEM A CELULA 500-1500 ----------
Write-Output ""
Write-Output "=== C) DIAGNOSTICO H&C — com vs sem a celula 500 a 1500 (N=6, phi=0.9) ==="
Write-Output "variante;WAPE_shp_mes;erro_total_6m;MAPE_ratio;erro_ratio_pp"
foreach($v in @('COM_500_1500','SEM_500_1500')){
  $ex = if($v -eq 'SEM_500_1500'){ '500 a 1500' } else { $null }
  $ss=Serie 'H_C' 'shp' $ex; $mm=Serie 'H_C' 'meli' $ex
  $Sb=Sazonal $ss $tShpIni $tFimBT; $Mb=Sazonal $mm $tMeliIni $tFimBT
  $ps=Projeta $ss $Sb $tShpIni $tFimBT 6 0.9 $alvosBT
  $pm=Projeta $mm $Mb $tMeliIni $tFimBT 6 0.9 $alvosBT
  $abs=0.0;$act=0.0;$pt=0.0;$ape=0.0;$pp=0.0;$cnt=0
  foreach($ta in $alvosBT){
    if(-not ($ss.ContainsKey($ta) -and $mm.ContainsKey($ta))){ continue }
    $abs+=[math]::Abs($ps.fc[$ta]-$ss[$ta]); $act+=$ss[$ta]; $pt+=$ps.fc[$ta]
    $rA=$ss[$ta]/$mm[$ta]; $rP=$ps.fc[$ta]/$pm.fc[$ta]
    $ape+=[math]::Abs($rP-$rA)/$rA; $pp+=[math]::Abs($rP-$rA)*100; $cnt++
  }
  Write-Output "$v;$([math]::Round($abs/$act*100,1));$([math]::Round(($pt-$act)/$act*100,1));$([math]::Round($ape/$cnt*100,1));$([math]::Round($pp/$cnt,1))"
}

# ---------- D) FORECAST PRE-REGISTRADO jul/26 -> dez/26 ----------
$alvosF=@(); for($k=1;$k -le 6;$k++){ $alvosF += ($tFimFull+$k) }
Write-Output ""
Write-Output "=== D) FORECAST PRE-REGISTRADO (fit ate jun/26; tendencia L3M N=3; nivel L3M=abr-jun/26) ==="
Write-Output "phi;d1;mes;shp_prev_Mi;meli_prev_Mi;ratio_prev_pct"
foreach($phi in @(1.0,0.9,0.8)){
  foreach($d in $D1S){
    $ss=Serie $d 'shp' $null; $mm=Serie $d 'meli' $null
    $ps=Projeta $ss $Ssh[$d] $tShpIni $tFimFull 3 $phi $alvosF
    $pm=Projeta $mm $Sme[$d] $tMeliIni $tFimFull 3 $phi $alvosF
    foreach($ta in $alvosF){
      Write-Output "$phi;$d;$(MesDe $ta);$([math]::Round($ps.fc[$ta]/1e6,1));$([math]::Round($pm.fc[$ta]/1e6,1));$([math]::Round($ps.fc[$ta]/$pm.fc[$ta]*100,1))"
    }
  }
}
Write-Output ""
Write-Output "=== E) PARAMETROS ESTIMADOS (fit completo ate jun/26, N=6) ==="
Write-Output "serie;g_mensal_pct;nivel_L3M_Mi"
foreach($d in $D1S){
  $ps=Projeta (Serie $d 'shp' $null) $Ssh[$d] $tShpIni $tFimFull 6 1.0 @($tFimFull+1)
  $pm=Projeta (Serie $d 'meli' $null) $Sme[$d] $tMeliIni $tFimFull 6 1.0 @($tFimFull+1)
  Write-Output "SHP_$d;$([math]::Round($ps.g*100,2));$([math]::Round($ps.L/1e6,1))"
  Write-Output "MELI_$d;$([math]::Round($pm.g*100,2));$([math]::Round($pm.L/1e6,1))"
}
