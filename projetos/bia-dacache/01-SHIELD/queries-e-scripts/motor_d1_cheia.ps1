# Motor de forecast em D1 CHEIA (sem recorte de faixa de ASP)
# Fonte: SBOX_MKPBR.DM_MARKET_ASP_MONTHLY_VERTICAL_D1, VERTICAL='HOME ELECTRONICS'
# Serie agregada por D1 (job mcp_job_4757fcaf), congelada aqui para nao depender do bq CLI.
# Parametros identicos ao motor anterior: combo v1(YoY)+v2(decomposicao), phi=0.9, nivel L3M, Njan=3.
$ErrorActionPreference = 'Stop'

$dados = @'
d1,mes,meli,shp
LARGE,2023-01,92.45,0
LARGE,2023-02,85.19,0
LARGE,2023-03,104.62,0
LARGE,2023-04,92.19,0
LARGE,2023-05,108.26,0
LARGE,2023-06,110.53,0
LARGE,2023-07,127.71,0
LARGE,2023-08,136.16,0
LARGE,2023-09,132.19,0
LARGE,2023-10,140.62,0
LARGE,2023-11,267.55,0
LARGE,2023-12,148.48,0
LARGE,2024-01,158.02,4.34
LARGE,2024-02,154.23,4.34
LARGE,2024-03,172.28,5.44
LARGE,2024-04,191.70,7.74
LARGE,2024-05,241.08,11.52
LARGE,2024-06,217.82,13.13
LARGE,2024-07,250.21,15.66
LARGE,2024-08,246.64,15.76
LARGE,2024-09,245.13,19.24
LARGE,2024-10,276.18,22.57
LARGE,2024-11,452.62,29.16
LARGE,2024-12,271.90,30.73
LARGE,2025-01,285.16,33.67
LARGE,2025-02,269.91,30.32
LARGE,2025-03,314.39,36.96
LARGE,2025-04,313.91,36.89
LARGE,2025-05,377.04,35.28
LARGE,2025-06,391.06,51.78
LARGE,2025-07,414.84,64.58
LARGE,2025-08,413.92,76.47
LARGE,2025-09,401.08,95.06
LARGE,2025-10,430.17,103.35
LARGE,2025-11,784.33,134.43
LARGE,2025-12,407.64,116.78
LARGE,2026-01,453.34,116.57
LARGE,2026-02,421.61,117.20
LARGE,2026-03,556.93,127.52
LARGE,2026-04,519.98,135.68
LARGE,2026-05,604.17,191.08
LARGE,2026-06,579.43,184.65
SMALL,2023-01,126.27,0
SMALL,2023-02,115.93,0
SMALL,2023-03,138.20,0
SMALL,2023-04,128.74,0
SMALL,2023-05,161.83,0
SMALL,2023-06,150.39,0
SMALL,2023-07,173.15,0
SMALL,2023-08,175.62,0
SMALL,2023-09,164.61,0
SMALL,2023-10,174.58,0
SMALL,2023-11,243.82,0
SMALL,2023-12,189.52,0
SMALL,2024-01,199.86,30.06
SMALL,2024-02,183.05,42.80
SMALL,2024-03,202.60,65.78
SMALL,2024-04,220.96,66.31
SMALL,2024-05,257.32,77.00
SMALL,2024-06,242.99,72.49
SMALL,2024-07,276.20,73.02
SMALL,2024-08,263.89,71.13
SMALL,2024-09,262.01,72.42
SMALL,2024-10,265.24,71.90
SMALL,2024-11,338.96,88.84
SMALL,2024-12,277.55,94.43
SMALL,2025-01,277.50,86.64
SMALL,2025-02,250.83,92.95
SMALL,2025-03,284.85,97.75
SMALL,2025-04,289.13,97.62
SMALL,2025-05,337.41,97.36
SMALL,2025-06,325.43,89.99
SMALL,2025-07,357.07,112.07
SMALL,2025-08,348.99,112.19
SMALL,2025-09,339.90,113.82
SMALL,2025-10,353.60,102.68
SMALL,2025-11,513.84,118.19
SMALL,2025-12,360.33,105.62
SMALL,2026-01,361.28,122.33
SMALL,2026-02,342.04,115.49
SMALL,2026-03,431.84,169.49
SMALL,2026-04,410.02,149.88
SMALL,2026-05,477.04,242.03
SMALL,2026-06,454.31,199.71
H_C,2023-01,81.64,0
H_C,2023-02,87.11,0
H_C,2023-03,97.77,0
H_C,2023-04,54.96,0
H_C,2023-05,60.13,0
H_C,2023-06,64.21,0
H_C,2023-07,57.80,0
H_C,2023-08,71.95,0
H_C,2023-09,181.34,0
H_C,2023-10,147.12,0
H_C,2023-11,265.31,0
H_C,2023-12,160.05,0
H_C,2024-01,153.30,10.52
H_C,2024-02,126.92,7.02
H_C,2024-03,171.77,10.24
H_C,2024-04,101.90,8.28
H_C,2024-05,119.36,8.28
H_C,2024-06,91.86,6.32
H_C,2024-07,110.60,6.52
H_C,2024-08,131.19,7.53
H_C,2024-09,223.14,21.52
H_C,2024-10,194.57,31.47
H_C,2024-11,282.13,21.02
H_C,2024-12,205.61,25.44
H_C,2025-01,257.71,27.99
H_C,2025-02,290.97,43.41
H_C,2025-03,210.63,58.18
H_C,2025-04,139.18,25.64
H_C,2025-05,144.40,21.38
H_C,2025-06,153.85,24.86
H_C,2025-07,185.64,27.43
H_C,2025-08,178.12,27.42
H_C,2025-09,228.00,58.89
H_C,2025-10,251.47,115.98
H_C,2025-11,423.42,105.58
H_C,2025-12,426.81,127.00
H_C,2026-01,333.29,130.21
H_C,2026-02,255.42,125.99
H_C,2026-03,271.75,170.76
H_C,2026-04,210.83,94.89
H_C,2026-05,204.58,119.41
H_C,2026-06,213.81,89.07
'@

$raw = $dados | ConvertFrom-Csv

function TIdx($mes){ $yy=[int]$mes.Substring(0,4); $mm=[int]$mes.Substring(5,2); return [int]((($yy-2023)*12) + $mm) }
function CMon($mes){ return [int]$mes.Substring(5,2) }
function MesDe($tt){ $tt=[int]$tt; $yy=2023+[math]::Floor(($tt-1)/12); $mm=(($tt-1)%12)+1; return "$yy-$('{0:d2}' -f $mm)" }
function OLS($xs,$ys){
  $kk=$xs.Count; if($kk -lt 2){ return @(0.0,0.0) }
  $mx=($xs|Measure-Object -Average).Average; $my=($ys|Measure-Object -Average).Average
  $sxy=0.0; $sxx=0.0
  for($i=0;$i -lt $kk;$i++){ $sxy += (($xs[$i]-$mx)*($ys[$i]-$my)); $sxx += [math]::Pow(($xs[$i]-$mx),2) }
  if($sxx -eq 0){ return @($my,0.0) }
  $bb=$sxy/$sxx; return @(($my-$bb*$mx),$bb)
}
function SerieOf($cat,$campo){
  $hh=@{}
  foreach($rr in $raw){
    if($rr.d1 -ne $cat){ continue }
    $tt=TIdx $rr.mes
    if(-not $hh.ContainsKey($tt)){ $hh[$tt]=0.0 }
    $hh[$tt] += [double]$rr.$campo
  }
  return $hh
}
function Sazonal($serie,$tIni,$tFim){
  $tIni=[int]$tIni; $tFim=[int]$tFim
  $ts=@(); $ly=@()
  foreach($tt in ($serie.Keys|Sort-Object)){ if($tt -ge $tIni -and $tt -le $tFim -and $serie[$tt] -gt 0){ $ts+=$tt; $ly+=[math]::Log($serie[$tt]) } }
  $idx=@{}; 1..12|ForEach-Object{ $idx[$_]=0.0 }
  for($pass=1;$pass -le 2;$pass++){
    $adj=@(); for($i=0;$i -lt $ts.Count;$i++){ $adj += ($ly[$i] - $idx[(CMon (MesDe $ts[$i]))]) }
    $ab=OLS $ts $adj
    $acc=@{}; 1..12|ForEach-Object{ $acc[$_]=@() }
    for($i=0;$i -lt $ts.Count;$i++){ $acc[(CMon (MesDe $ts[$i]))] += ($adj[$i] - ($ab[0]+$ab[1]*$ts[$i])) }
    $novo=@{}; foreach($mm in 1..12){ if($acc[$mm].Count -gt 0){ $novo[$mm]=$idx[$mm]+(($acc[$mm]|Measure-Object -Average).Average) } else { $novo[$mm]=$idx[$mm] } }
    $mu=((1..12|ForEach-Object{$novo[$_]})|Measure-Object -Average).Average
    foreach($mm in 1..12){ $idx[$mm]=$novo[$mm]-$mu }
  }
  $fat=@{}; foreach($mm in 1..12){ $fat[$mm]=[math]::Exp($idx[$mm]) }
  return $fat
}
function ProjV2($serie,$fat,$tIni,$tFim,$Njan,$phi,$alvos,$gFixo){
  $tIni=[int]$tIni; $tFim=[int]$tFim; $Njan=[int]$Njan; $phi=[double]$phi
  $des=@{}
  foreach($tt in ($serie.Keys|Sort-Object)){ if($tt -ge $tIni -and $tt -le $tFim -and $serie[$tt] -gt 0){ $des[$tt]=$serie[$tt]/$fat[(CMon (MesDe $tt))] } }
  $l3=@(); foreach($tt in @(($tFim-2),($tFim-1),($tFim))){ if($des.ContainsKey($tt)){ $l3+=$des[$tt] } }
  $nivel=($l3|Measure-Object -Average).Average
  $gg=0.0
  if($null -eq $gFixo){
    $ts=@(); $ly=@()
    foreach($tt in ($des.Keys|Sort-Object)){ if($tt -gt ($tFim-$Njan) -and $tt -le $tFim){ $ts+=$tt; $ly+=[math]::Log($des[$tt]) } }
    $ab=OLS $ts $ly; $gg=[math]::Exp($ab[1])-1
  } else { $gg=[double]$gFixo }
  $res=@{}
  foreach($ta in $alvos){
    $steps=[int]$ta-([int]$tFim-1)
    $ff=1.0; for($j=1;$j -le $steps;$j++){ $ff *= (1 + $gg*[math]::Pow($phi,$j)) }
    $res[$ta]=$nivel*$ff*$fat[(CMon (MesDe $ta))]
  }
  return @{ g=$gg; L=$nivel; fc=$res }
}
function ProjV1($serie,$tFim,$phi,$alvos){
  $tFim=[int]$tFim; $phi=[double]$phi
  $aa=0.0;$bb=0.0
  for($i=5;$i -ge 0;$i--){ $tt=$tFim-$i; $tl=$tt-12
    if($serie.ContainsKey($tt) -and $serie.ContainsKey($tl) -and $serie[$tl] -gt 0){ $aa+=$serie[$tt]; $bb+=$serie[$tl] } }
  $yoy = if($bb -gt 0){ $aa/$bb-1 } else { 0.0 }
  $res=@{}
  foreach($ta in $alvos){
    $kk=[int]$ta-$tFim; $tl=[int]$ta-12
    $base = if($serie.ContainsKey($tl)){ $serie[$tl] } else { 0.0 }
    $res[$ta]=$base*(1+$yoy*[math]::Pow($phi,$kk))
  }
  return @{ yoy=$yoy; fc=$res }
}
function Metricas($fcS,$fcM,$serS,$serM,$alvos){
  $abs=0.0;$act=0.0;$pt=0.0;$ape=0.0;$dpp=0.0;$cnt=0
  foreach($ta in $alvos){
    if(-not ($serS.ContainsKey($ta) -and $serM.ContainsKey($ta))){ continue }
    if($serM[$ta] -le 0 -or $serS[$ta] -le 0){ continue }
    $abs+=[math]::Abs($fcS[$ta]-$serS[$ta]); $act+=$serS[$ta]; $pt+=$fcS[$ta]
    $rA=$serS[$ta]/$serM[$ta]; $rP=$fcS[$ta]/$fcM[$ta]
    $ape+=[math]::Abs($rP-$rA)/$rA; $dpp+=[math]::Abs($rP-$rA)*100; $cnt++
  }
  return @{ wape=($abs/$act*100); vies=(($pt-$act)/$act*100); mape=($ape/$cnt*100); pp=($dpp/$cnt) }
}

$tIniS=[int](TIdx '2024-01'); $tIniM=[int](TIdx '2023-01')
$tFim=[int](TIdx '2026-06');  $tBT=[int](TIdx '2025-12')
$alvos=@(); for($k=1;$k -le 6;$k++){ $alvos += [int]($tFim+$k) }
$alvBT=@(); for($k=1;$k -le 6;$k++){ $alvBT += [int]($tBT+$k) }

# ---------- (1) BACKTEST em D1 cheia: fit ate dez/25 -> jan-jun/26 ----------
Write-Output "=== 1) BACKTEST D1 CHEIA (fit dez/25 -> jan-jun/26, phi=0.9) ==="
Write-Output "d1;modelo;WAPE_shp;MAPE_ratio;erro_pp;vies"
foreach($cat in @('LARGE','SMALL','H_C')){
  $serS=SerieOf $cat 'shp'; $serM=SerieOf $cat 'meli'
  $sazSb=Sazonal $serS $tIniS $tBT; $sazMb=Sazonal $serM $tIniM $tBT
  $v2S=ProjV2 $serS $sazSb $tIniS $tBT 3 0.9 $alvBT $null; $v2M=ProjV2 $serM $sazMb $tIniM $tBT 3 0.9 $alvBT $null
  $v1S=ProjV1 $serS $tBT 0.9 $alvBT;  $v1M=ProjV1 $serM $tBT 0.9 $alvBT
  foreach($mdl in @('v1_yoy','v2_decomp','combo')){
    $fcS=@{}; $fcM=@{}
    foreach($ta in $alvBT){
      switch($mdl){
        'v1_yoy'    { $fcS[$ta]=$v1S.fc[$ta]; $fcM[$ta]=$v1M.fc[$ta] }
        'v2_decomp' { $fcS[$ta]=$v2S.fc[$ta]; $fcM[$ta]=$v2M.fc[$ta] }
        'combo'     { $fcS[$ta]=($v1S.fc[$ta]+$v2S.fc[$ta])/2; $fcM[$ta]=($v1M.fc[$ta]+$v2M.fc[$ta])/2 }
      }
    }
    $mtr=Metricas $fcS $fcM $serS $serM $alvBT
    Write-Output "$cat;$mdl;$([math]::Round($mtr.wape,1));$([math]::Round($mtr.mape,1));$([math]::Round($mtr.pp,1));$([math]::Round($mtr.vies,1))"
  }
}

# ---------- (2) FORECAST jul-dez/26 em D1 cheia (combo) ----------
Write-Output ""
Write-Output "=== 2) FORECAST D1 CHEIA jul-dez/26 (combo v1+v2, phi=0.9) ==="
Write-Output "d1;mes;shp_Mi;meli_Mi;ratio_pct"
$guardar=@{}
foreach($cat in @('LARGE','SMALL','H_C')){
  $serS=SerieOf $cat 'shp'; $serM=SerieOf $cat 'meli'
  $sazS=Sazonal $serS $tIniS $tFim; $sazM=Sazonal $serM $tIniM $tFim
  $v2S=ProjV2 $serS $sazS $tIniS $tFim 3 0.9 $alvos $null; $v2M=ProjV2 $serM $sazM $tIniM $tFim 3 0.9 $alvos $null
  $v1S=ProjV1 $serS $tFim 0.9 $alvos;  $v1M=ProjV1 $serM $tFim 0.9 $alvos
  $fcS=@{}; $fcM=@{}
  foreach($ta in $alvos){ $fcS[$ta]=($v1S.fc[$ta]+$v2S.fc[$ta])/2; $fcM[$ta]=($v1M.fc[$ta]+$v2M.fc[$ta])/2 }
  $guardar[$cat]=@{ fcS=$fcS; fcM=$fcM; serS=$serS; serM=$serM; g=$v2S.g; yoyS=$v1S.yoy; yoyM=$v1M.yoy }
  foreach($ta in $alvos){
    Write-Output "$cat;$(MesDe $ta);$([math]::Round($fcS[$ta],1));$([math]::Round($fcM[$ta],1));$([math]::Round($fcS[$ta]/$fcM[$ta]*100,1))"
  }
}

# ---------- (3) RESUMO por D1: ratios de referencia ----------
Write-Output ""
Write-Output "=== 3) RESUMO D1 CHEIA ==="
Write-Output "d1;shp_H2_25;meli_H2_25;ratio_H2_25;shp_Q2_26;meli_Q2_26;ratio_Q2_26;shp_H2_26p;meli_H2_26p;ratio_H2_26p;yoy_shp_L6M;yoy_meli_L6M"
foreach($cat in @('LARGE','SMALL','H_C')){
  $gg=$guardar[$cat]
  $h2s=0.0;$h2m=0.0; for($k=7;$k -le 12;$k++){ $tt=[int](TIdx "2025-$('{0:d2}' -f $k)"); $h2s+=$gg.serS[$tt]; $h2m+=$gg.serM[$tt] }
  $q2s=0.0;$q2m=0.0; for($k=4;$k -le 6;$k++){ $tt=[int](TIdx "2026-$('{0:d2}' -f $k)"); $q2s+=$gg.serS[$tt]; $q2m+=$gg.serM[$tt] }
  $pjs=0.0;$pjm=0.0; foreach($ta in $alvos){ $pjs+=$gg.fcS[$ta]; $pjm+=$gg.fcM[$ta] }
  Write-Output "$cat;$([math]::Round($h2s,1));$([math]::Round($h2m,1));$([math]::Round($h2s/$h2m*100,1));$([math]::Round($q2s,1));$([math]::Round($q2m,1));$([math]::Round($q2s/$q2m*100,1));$([math]::Round($pjs,1));$([math]::Round($pjm,1));$([math]::Round($pjs/$pjm*100,1));$([math]::Round($gg.yoyS*100,1));$([math]::Round($gg.yoyM*100,1))"
}

# ---------- (4) CHECAGEM out-of-sample de julho/26 ----------
# Realizado de jul/26 nao existe no Planning (fecha jun/26). Reconstruido do DM Eficiencia:
# jul/25 do Planning (D1 cheia) x crescimento medido no DM (jul/26 vs jul/25).
Write-Output ""
Write-Output "=== 4) CHECAGEM jul/26 MELI (1 passo a frente, D1 cheia) ==="
Write-Output "d1;jul25_planning;cresc_DM_pct;jul26_realizado_est;jul26_projetado;erro_pct"
$crescDM=@{ LARGE=54.6; SMALL=43.9; H_C=19.1 }
foreach($cat in @('LARGE','SMALL','H_C')){
  $gg=$guardar[$cat]
  $tJul25=[int](TIdx '2025-07'); $tJul26=[int](TIdx '2026-07')
  $real=$gg.serM[$tJul25]*(1+$crescDM[$cat]/100)
  $proj=$gg.fcM[$tJul26]
  Write-Output "$cat;$([math]::Round($gg.serM[$tJul25],1));$($crescDM[$cat]);$([math]::Round($real,1));$([math]::Round($proj,1));$([math]::Round(($proj/$real-1)*100,2))"
}
