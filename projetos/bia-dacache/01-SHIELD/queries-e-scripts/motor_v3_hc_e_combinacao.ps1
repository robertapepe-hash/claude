# (1) H&C em 3 visoes: TOTAL / BASE (sem 500-1500) / CELULA 500-1500 isolada
# (2) Teste de combinacao de previsoes v1 (YoY) + v2 (decomposicao) — Bates & Granger
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
$hd = $out | Where-Object { $_ -like 'd1,*' } | Select-Object -First 1
$raw = $out[([Array]::IndexOf($out,$hd))..($out.Count-1)] | ConvertFrom-Csv | Where-Object { $_.d1 }

function TIdx($mes){ $y=[int]$mes.Substring(0,4); $mm=[int]$mes.Substring(5,2); return [int]((($y-2023)*12) + $mm) }
function CMon($mes){ return [int]$mes.Substring(5,2) }
function MesDe($tt){ $tt=[int]$tt; $y=2023+[math]::Floor(($tt-1)/12); $mm=(($tt-1)%12)+1; return "$y-$('{0:d2}' -f $mm)" }
function OLS($xs,$ys){
  $k=$xs.Count; if($k -lt 2){ return @(0.0,0.0) }
  $mx=($xs|Measure-Object -Average).Average; $my=($ys|Measure-Object -Average).Average
  $sxy=0.0; $sxx=0.0
  for($i=0;$i -lt $k;$i++){ $sxy += (($xs[$i]-$mx)*($ys[$i]-$my)); $sxx += [math]::Pow(($xs[$i]-$mx),2) }
  if($sxx -eq 0){ return @($my,0.0) }
  $b=$sxy/$sxx; return @(($my-$b*$mx),$b)
}
# serie: filtro por d1 + lista de faixas (incluir) ou 'ex' (excluir)
function Serie($d1,$campo,$incluir,$excluir){
  $h=@{}
  foreach($r in $raw){
    if($r.d1 -ne $d1){ continue }
    if($incluir -and ($incluir -notcontains $r.fx)){ continue }
    if($excluir -and ($excluir -contains $r.fx)){ continue }
    $tt=TIdx $r.mes
    if(-not $h.ContainsKey($tt)){ $h[$tt]=0.0 }
    $h[$tt] += [double]$r.$campo
  }
  return $h
}
function Sazonal($serie,$tIni,$tFim){
  $tIni=[int]$tIni; $tFim=[int]$tFim
  $ts=@(); $ly=@()
  foreach($tt in ($serie.Keys|Sort-Object)){ if($tt -ge $tIni -and $tt -le $tFim -and $serie[$tt] -gt 0){ $ts+=$tt; $ly+=[math]::Log($serie[$tt]) } }
  $sm=@{}; 1..12|ForEach-Object{ $sm[$_]=0.0 }
  for($pass=1;$pass -le 2;$pass++){
    $adj=@(); for($i=0;$i -lt $ts.Count;$i++){ $adj += ($ly[$i] - $sm[(CMon (MesDe $ts[$i]))]) }
    $ab=OLS $ts $adj
    $acc=@{}; 1..12|ForEach-Object{ $acc[$_]=@() }
    for($i=0;$i -lt $ts.Count;$i++){ $acc[(CMon (MesDe $ts[$i]))] += ($adj[$i] - ($ab[0]+$ab[1]*$ts[$i])) }
    $novo=@{}; foreach($mm in 1..12){ if($acc[$mm].Count -gt 0){ $novo[$mm]=$sm[$mm]+(($acc[$mm]|Measure-Object -Average).Average) } else { $novo[$mm]=$sm[$mm] } }
    $mu=((1..12|ForEach-Object{$novo[$_]})|Measure-Object -Average).Average
    foreach($mm in 1..12){ $sm[$mm]=$novo[$mm]-$mu }
  }
  $S=@{}; foreach($mm in 1..12){ $S[$mm]=[math]::Exp($sm[$mm]) }
  return $S
}
# v2: decomposicao. Se $gFixo nao for $null, usa esse g (ex.: 0 = nivel constante)
function ProjV2($serie,$S,$tIni,$tFim,$Njan,$phi,$alvos,$gFixo){
  $tIni=[int]$tIni; $tFim=[int]$tFim; $Njan=[int]$Njan; $phi=[double]$phi
  $D=@{}
  foreach($tt in ($serie.Keys|Sort-Object)){ if($tt -ge $tIni -and $tt -le $tFim -and $serie[$tt] -gt 0){ $D[$tt]=$serie[$tt]/$S[(CMon (MesDe $tt))] } }
  $l3=@(); foreach($tt in @(($tFim-2),($tFim-1),($tFim))){ if($D.ContainsKey($tt)){ $l3+=$D[$tt] } }
  $L=($l3|Measure-Object -Average).Average
  $g=0.0
  if($null -eq $gFixo){
    $ts=@(); $ly=@()
    foreach($tt in ($D.Keys|Sort-Object)){ if($tt -gt ($tFim-$Njan) -and $tt -le $tFim){ $ts+=$tt; $ly+=[math]::Log($D[$tt]) } }
    $ab=OLS $ts $ly; $g=[math]::Exp($ab[1])-1
  } else { $g=[double]$gFixo }
  $res=@{}
  foreach($ta in $alvos){
    $steps=[int]$ta-([int]$tFim-1)
    $f=1.0; for($j=1;$j -le $steps;$j++){ $f *= (1 + $g*[math]::Pow($phi,$j)) }
    $res[$ta]=$L*$f*$S[(CMon (MesDe $ta))]
  }
  return @{ g=$g; L=$L; fc=$res }
}
# v1: YoY do semestre final da janela de fit, aplicado ao mes real do ano anterior
function ProjV1($serie,$tFim,$phi,$alvos){
  $tFim=[int]$tFim; $phi=[double]$phi
  $a=0.0;$b=0.0
  for($i=5;$i -ge 0;$i--){ $tt=$tFim-$i; $tl=$tt-12
    if($serie.ContainsKey($tt) -and $serie.ContainsKey($tl) -and $serie[$tl] -gt 0){ $a+=$serie[$tt]; $b+=$serie[$tl] } }
  $yoy = if($b -gt 0){ $a/$b-1 } else { 0.0 }
  $res=@{}
  foreach($ta in $alvos){
    $k=[int]$ta-$tFim; $tl=[int]$ta-12
    $base = if($serie.ContainsKey($tl)){ $serie[$tl] } else { 0.0 }
    $res[$ta]=$base*(1+$yoy*[math]::Pow($phi,$k))
  }
  return @{ yoy=$yoy; fc=$res }
}
function Metricas($fcS,$fcM,$serS,$serM,$alvos){
  $abs=0.0;$act=0.0;$pt=0.0;$ape=0.0;$pp=0.0;$cnt=0
  foreach($ta in $alvos){
    if(-not ($serS.ContainsKey($ta) -and $serM.ContainsKey($ta))){ continue }
    if($serM[$ta] -le 0 -or $serS[$ta] -le 0){ continue }
    $abs+=[math]::Abs($fcS[$ta]-$serS[$ta]); $act+=$serS[$ta]; $pt+=$fcS[$ta]
    $rA=$serS[$ta]/$serM[$ta]; $rP=$fcS[$ta]/$fcM[$ta]
    $ape+=[math]::Abs($rP-$rA)/$rA; $pp+=[math]::Abs($rP-$rA)*100; $cnt++
  }
  return @{ wape=($abs/$act*100); vies=(($pt-$act)/$act*100); mape=($ape/$cnt*100); pp=($pp/$cnt) }
}

$tShpIni=[int](TIdx '2024-01'); $tMeliIni=[int](TIdx '2023-01')
$tFull=[int](TIdx '2026-06'); $tBT=[int](TIdx '2025-12')
$alvBT=@(); for($k=1;$k -le 6;$k++){ $alvBT += [int]($tBT+$k) }
$alvFC=@(); for($k=1;$k -le 6;$k++){ $alvFC += [int]($tFull+$k) }
$FX_HC_ALL=@('200 a 500','500 a 1500','1500 a 3000','+3000')
$FX_HC_BASE=@('200 a 500','1500 a 3000','+3000')
$FX_CELL=@('500 a 1500')

# ================= (1) H&C EM 3 VISOES =================
Write-Output "=== 1A) H&C 3 VISOES — parametros (fit ate jun/26, L3M) e backtest (fit dez/25 -> jan-jun/26) ==="
Write-Output "visao;g_shp_mensal_pct;nivel_shp_L3M_Mi;ratio_atual_nivel_pct;bt_WAPE;bt_MAPE_ratio;bt_vies"
$visoes=@( @('H_C_TOTAL',$FX_HC_ALL), @('H_C_BASE',$FX_HC_BASE), @('CELULA_500_1500',$FX_CELL) )
$store=@{}
foreach($v in $visoes){
  $nome=$v[0]; $fxs=$v[1]
  $serS=Serie 'H_C' 'shp' $fxs $null; $serM=Serie 'H_C' 'meli' $fxs $null
  # celula: empresta o perfil sazonal da BASE (serie propria e degrau, indice seria lixo)
  if($nome -eq 'CELULA_500_1500'){
    $sazS=Sazonal (Serie 'H_C' 'shp' $FX_HC_BASE $null) $tShpIni $tFull
    $sazM=Sazonal (Serie 'H_C' 'meli' $FX_HC_BASE $null) $tMeliIni $tFull
  } else {
    $sazS=Sazonal $serS $tShpIni $tFull; $sazM=Sazonal $serM $tMeliIni $tFull
  }
  $pS=ProjV2 $serS $sazS $tShpIni $tFull 3 0.9 $alvFC $null
  $pM=ProjV2 $serM $sazM $tMeliIni $tFull 3 0.9 $alvFC $null
  # backtest
  $sazSb=if($nome -eq 'CELULA_500_1500'){ Sazonal (Serie 'H_C' 'shp' $FX_HC_BASE $null) $tShpIni $tBT } else { Sazonal $serS $tShpIni $tBT }
  $sazMb=if($nome -eq 'CELULA_500_1500'){ Sazonal (Serie 'H_C' 'meli' $FX_HC_BASE $null) $tMeliIni $tBT } else { Sazonal $serM $tMeliIni $tBT }
  $bS=ProjV2 $serS $sazSb $tShpIni $tBT 3 0.9 $alvBT $null
  $bM=ProjV2 $serM $sazMb $tMeliIni $tBT 3 0.9 $alvBT $null
  $mt=Metricas $bS.fc $bM.fc $serS $serM $alvBT
  Write-Output "$nome;$([math]::Round($pS.g*100,2));$([math]::Round($pS.L/1e6,1));$([math]::Round($pS.L/$pM.L*100,1));$([math]::Round($mt.wape,1));$([math]::Round($mt.mape,1));$([math]::Round($mt.vies,1))"
  $store[$nome]=@{ pS=$pS; pM=$pM; serS=$serS; serM=$serM; sazS=$sazS; sazM=$sazM }
}

Write-Output ""
Write-Output "=== 1B) H&C FORECAST jul-dez/26 (phi=0.9) — 3 visoes + cenarios da celula ==="
Write-Output "visao;mes;shp_Mi;meli_Mi;ratio_pct"
# BASE
foreach($ta in $alvFC){ $x=$store['H_C_BASE']
  Write-Output "H_C_BASE;$(MesDe $ta);$([math]::Round($x.pS.fc[$ta]/1e6,1));$([math]::Round($x.pM.fc[$ta]/1e6,1));$([math]::Round($x.pS.fc[$ta]/$x.pM.fc[$ta]*100,1))" }
# CELULA — 2 cenarios: nivel constante (g=0) e tendencia estimada
$cS=Serie 'H_C' 'shp' $FX_CELL $null; $cM=Serie 'H_C' 'meli' $FX_CELL $null
$sazSc=$store['CELULA_500_1500'].sazS; $sazMc=$store['CELULA_500_1500'].sazM
$cel_flat=ProjV2 $cS $sazSc $tShpIni $tFull 3 0.9 $alvFC 0.0
$cel_tend=ProjV2 $cS $sazSc $tShpIni $tFull 3 0.9 $alvFC $null
$celM=ProjV2 $cM $sazMc $tMeliIni $tFull 3 0.9 $alvFC $null
foreach($ta in $alvFC){ Write-Output "CELULA_nivel_constante;$(MesDe $ta);$([math]::Round($cel_flat.fc[$ta]/1e6,1));$([math]::Round($celM.fc[$ta]/1e6,1));$([math]::Round($cel_flat.fc[$ta]/$celM.fc[$ta]*100,1))" }
foreach($ta in $alvFC){ Write-Output "CELULA_com_tendencia;$(MesDe $ta);$([math]::Round($cel_tend.fc[$ta]/1e6,1));$([math]::Round($celM.fc[$ta]/1e6,1));$([math]::Round($cel_tend.fc[$ta]/$celM.fc[$ta]*100,1))" }
# TOTAL recomposto (BASE + celula nivel constante) e TOTAL direto
foreach($ta in $alvFC){ $b=$store['H_C_BASE']
  $s=$b.pS.fc[$ta]+$cel_flat.fc[$ta]; $m=$b.pM.fc[$ta]+$celM.fc[$ta]
  Write-Output "H_C_TOTAL_recomposto;$(MesDe $ta);$([math]::Round($s/1e6,1));$([math]::Round($m/1e6,1));$([math]::Round($s/$m*100,1))" }
foreach($ta in $alvFC){ $x=$store['H_C_TOTAL']
  Write-Output "H_C_TOTAL_direto;$(MesDe $ta);$([math]::Round($x.pS.fc[$ta]/1e6,1));$([math]::Round($x.pM.fc[$ta]/1e6,1));$([math]::Round($x.pS.fc[$ta]/$x.pM.fc[$ta]*100,1))" }

# ================= (2) COMBINACAO v1 + v2 =================
Write-Output ""
Write-Output "=== 2) COMBINACAO DE PREVISOES (fit dez/25 -> jan-jun/26, phi=0.9) ==="
Write-Output "modelo;escopo;WAPE_shp;MAPE_ratio;erro_pp;vies"
$defs=@( @('H_C',$FX_HC_BASE), @('LARGE',@('200 a 500','500 a 1500','1500 a 3000','+3000')), @('SMALL',@('120 a 150','150 a 200','200 a 500','500 a 1500','+3000')) )
$tot=@{}
foreach($mdl in @('v1_yoy','v2_decomp','combo_50_50')){
  foreach($dd in $defs){
    $d=$dd[0]; $fxs=$dd[1]
    $serS=Serie $d 'shp' $fxs $null; $serM=Serie $d 'meli' $fxs $null
    $sazSb=Sazonal $serS $tShpIni $tBT; $sazMb=Sazonal $serM $tMeliIni $tBT
    $v2S=ProjV2 $serS $sazSb $tShpIni $tBT 3 0.9 $alvBT $null; $v2M=ProjV2 $serM $sazMb $tMeliIni $tBT 3 0.9 $alvBT $null
    $v1S=ProjV1 $serS $tBT 0.9 $alvBT; $v1M=ProjV1 $serM $tBT 0.9 $alvBT
    $fS=@{}; $fM=@{}
    foreach($ta in $alvBT){
      switch($mdl){
        'v1_yoy'      { $fS[$ta]=$v1S.fc[$ta]; $fM[$ta]=$v1M.fc[$ta] }
        'v2_decomp'   { $fS[$ta]=$v2S.fc[$ta]; $fM[$ta]=$v2M.fc[$ta] }
        'combo_50_50' { $fS[$ta]=($v1S.fc[$ta]+$v2S.fc[$ta])/2; $fM[$ta]=($v1M.fc[$ta]+$v2M.fc[$ta])/2 }
      }
    }
    $mt=Metricas $fS $fM $serS $serM $alvBT
    Write-Output "$mdl;$d;$([math]::Round($mt.wape,1));$([math]::Round($mt.mape,1));$([math]::Round($mt.pp,1));$([math]::Round($mt.vies,1))"
    $kk="$mdl"; if(-not $tot.ContainsKey($kk)){ $tot[$kk]=@{w=@();m=@();p=@();v=@()} }
    $tot[$kk].w+=$mt.wape; $tot[$kk].m+=$mt.mape; $tot[$kk].p+=$mt.pp; $tot[$kk].v+=$mt.vies
  }
}
Write-Output "--- MEDIA DAS 3 D1s ---"
foreach($mdl in @('v1_yoy','v2_decomp','combo_50_50')){ $e=$tot[$mdl]
  Write-Output "$mdl;MEDIA;$([math]::Round((($e.w)|Measure-Object -Average).Average,1));$([math]::Round((($e.m)|Measure-Object -Average).Average,1));$([math]::Round((($e.p)|Measure-Object -Average).Average,1));$([math]::Round((($e.v)|Measure-Object -Average).Average,1))" }
