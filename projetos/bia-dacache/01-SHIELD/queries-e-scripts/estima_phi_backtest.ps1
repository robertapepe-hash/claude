# Estima phi (decaimento do YoY) por D1 x faixa-foco e roda backtest out-of-sample.
# Fit: apenas 2025. Teste: jan-jun/2026. Compara 3 modelos: phi por celula, phi por D1, sem decaimento.
$ErrorActionPreference = 'Stop'

$sql = @'
WITH r AS (
SELECT CASE DOM_DOMAIN_AGG1 WHEN 'LARGE APPLIANCES' THEN 'LARGE' WHEN 'SMALL APPLIANCES' THEN 'SMALL' ELSE 'H_C' END d1,
FAIXA_ASP_NOVA fx, DATA,
CAST(GMV_SHOPEE AS FLOAT64) s, CAST(GMV_SHOPEE_LY AS FLOAT64) sly
FROM `meli-bi-data.SBOX_MKPBR.DM_MARKET_ASP_MONTHLY_VERTICAL_D1`
WHERE VERTICAL='HOME ELECTRONICS' AND DATA BETWEEN '2025-01-01' AND '2026-06-30'
AND ((DOM_DOMAIN_AGG1='LARGE APPLIANCES' AND FAIXA_ASP_NOVA IN ('200 a 500','500 a 1500','1500 a 3000','+3000'))
OR (DOM_DOMAIN_AGG1='HEATING, COOLING & AIR QUALITY' AND FAIXA_ASP_NOVA IN ('200 a 500','500 a 1500','1500 a 3000','+3000'))
OR (DOM_DOMAIN_AGG1='SMALL APPLIANCES' AND FAIXA_ASP_NOVA IN ('120 a 150','150 a 200','200 a 500','500 a 1500','+3000'))))
SELECT d1, fx, FORMAT_DATE('%Y-%m',DATA) mes, ROUND(SUM(s),3) shp, ROUND(SUM(sly),3) shp_ly
FROM r GROUP BY 1,2,3 ORDER BY 1,2,3
'@

$sql1 = ($sql -replace "\s+", " ").Trim()
$out = bq query --project_id=meli-bi-data --use_legacy_sql=false --format=csv --max_rows=1000 $sql1
$hdrLine = $out | Where-Object { $_ -like 'd1,*' } | Select-Object -First 1
if (-not $hdrLine) { Write-Output "ERRO: bq nao retornou dados"; $out; exit 1 }
$start = [Array]::IndexOf($out, $hdrLine)
$data = $out[$start..($out.Count - 1)] | ConvertFrom-Csv

# ---- indexacao ----
$cell = @{}
foreach ($r in $data) {
  if (-not $r.d1) { continue }
  $k = "$($r.d1)|$($r.fx)"
  if (-not $cell.ContainsKey($k)) { $cell[$k] = @{} }
  $cell[$k][$r.mes] = [pscustomobject]@{ s = [double]$r.shp; sly = [double]$r.shp_ly }
}
$d1agg = @{}
foreach ($k in $cell.Keys) {
  $d = $k.Split('|')[0]
  if (-not $d1agg.ContainsKey($d)) { $d1agg[$d] = @{} }
  foreach ($m in $cell[$k].Keys) {
    if (-not $d1agg[$d].ContainsKey($m)) { $d1agg[$d][$m] = [pscustomobject]@{ s = 0.0; sly = 0.0 } }
    $d1agg[$d][$m].s += $cell[$k][$m].s
    $d1agg[$d][$m].sly += $cell[$k][$m].sly
  }
}

$S1 = @('2025-01','2025-02','2025-03','2025-04','2025-05','2025-06')
$S2 = @('2025-07','2025-08','2025-09','2025-10','2025-11','2025-12')
$Q4 = @('2025-10','2025-11','2025-12')
$Q2 = @('2026-04','2026-05','2026-06')
$H1 = @('2026-01','2026-02','2026-03','2026-04','2026-05','2026-06')

function YoY($h, $months) {
  $a = 0.0; $b = 0.0
  foreach ($m in $months) { if ($h.ContainsKey($m)) { $a += $h[$m].s; $b += $h[$m].sly } }
  if ($b -le 0) { return $null }
  return ($a / $b - 1)
}
function PhiSem($h) {
  $y1 = YoY $h $S1; $y2 = YoY $h $S2
  if ($null -eq $y1 -or $null -eq $y2 -or $y1 -le 0 -or $y2 -le 0) { return 1.0 }
  return ($y2 / $y1)
}
function P($v) { if ($null -eq $v) { return 'n/d' } return [math]::Round($v * 100, 0) }

# ---- tabela de phi ----
Write-Output "=== PHI E YoY POR CELULA (fit so em 2025) ==="
Write-Output "d1;faixa;yoy_s1_25;yoy_s2_25;yoy_h1_26;yoy_q2_26(base);phi_25(s2/s1);phi_26(h1_26/s2)"
foreach ($k in ($cell.Keys | Sort-Object)) {
  $h = $cell[$k]; $p = $k.Split('|')
  $y1 = YoY $h $S1; $y2 = YoY $h $S2; $y3 = YoY $h $H1; $y4 = YoY $h $Q2
  $p25 = if ($y1 -and $y2 -and $y1 -gt 0 -and $y2 -gt 0) { [math]::Round($y2 / $y1, 2) } else { 'n/d' }
  $p26 = if ($y2 -and $y3 -and $y2 -gt 0 -and $y3 -gt 0) { [math]::Round($y3 / $y2, 2) } else { 'n/d' }
  Write-Output "$($p[0]);$($p[1]);$(P $y1);$(P $y2);$(P $y3);$(P $y4);$p25;$p26"
}
Write-Output ""
Write-Output "=== PHI E YoY POR D1 (agregado das faixas-foco) ==="
Write-Output "d1;yoy_s1_25;yoy_s2_25;yoy_h1_26;yoy_q2_26(base);phi_25;phi_26"
foreach ($d in ($d1agg.Keys | Sort-Object)) {
  $h = $d1agg[$d]
  $y1 = YoY $h $S1; $y2 = YoY $h $S2; $y3 = YoY $h $H1; $y4 = YoY $h $Q2
  $p25 = if ($y1 -gt 0 -and $y2 -gt 0) { [math]::Round($y2 / $y1, 2) } else { 'n/d' }
  $p26 = if ($y2 -gt 0 -and $y3 -gt 0) { [math]::Round($y3 / $y2, 2) } else { 'n/d' }
  Write-Output "$d;$(P $y1);$(P $y2);$(P $y3);$(P $y4);$p25;$p26"
}

# ---- backtest out-of-sample: prever jan-jun/26 com parametros de 2025 ----
$err = @{}
foreach ($k in $cell.Keys) {
  $d = $k.Split('|')[0]; $h = $cell[$k]
  $base = YoY $h $Q4
  if ($null -eq $base) { continue }
  $pc = PhiSem $h; $pd = PhiSem $d1agg[$d]
  foreach ($mod in @('phi_celula','phi_D1','sem_decaim')) {
    $psem = switch ($mod) { 'phi_celula' { $pc } 'phi_D1' { $pd } 'sem_decaim' { 1.0 } }
    $pm = [math]::Pow($psem, 1.0 / 6.0)
    for ($i = 0; $i -lt 6; $i++) {
      $m = $H1[$i]; $kk = $i + 1
      if (-not $h.ContainsKey($m)) { continue }
      $act = $h[$m].s; $mold = $h[$m].sly
      if ($act -le 0 -or $mold -le 0) { continue }
      $pred = $mold * (1 + $base * [math]::Pow($pm, $kk))
      foreach ($scope in @($d, 'TOTAL')) {
        $key = "$mod|$scope"
        if (-not $err.ContainsKey($key)) { $err[$key] = @{ abs = 0.0; act = 0.0; ape = 0.0; n = 0 } }
        $err[$key].abs += [math]::Abs($pred - $act)
        $err[$key].act += $act
        $err[$key].ape += [math]::Abs($pred - $act) / $act
        $err[$key].n++
      }
    }
  }
}
Write-Output ""
Write-Output "=== BACKTEST out-of-sample (fit 2025 -> preve jan-jun/26) ==="
Write-Output "modelo;escopo;WAPE_pct;MAPE_pct;n_obs"
foreach ($mod in @('phi_celula','phi_D1','sem_decaim')) {
  foreach ($scope in @('H_C','LARGE','SMALL','TOTAL')) {
    $key = "$mod|$scope"
    if (-not $err.ContainsKey($key)) { continue }
    $e = $err[$key]
    $wape = [math]::Round($e.abs / $e.act * 100, 1)
    $mape = [math]::Round($e.ape / $e.n * 100, 1)
    Write-Output "$mod;$scope;$wape;$mape;$($e.n)"
  }
}
