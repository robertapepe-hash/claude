-- ETAPA 1 — Caracterização CBH
-- Grain máximo: mês × D1 × D2 × UF (receiver_state)
-- Período: nov/2025 → abr/2026 (6 meses)
-- Filtro: CBH (CUS_CUST_ID_SEL = 1046986303), Vertical HE
-- Custo: ~10,4 GB / US$ 0,05
-- Output: outputs/etapa1_cbh_raw.json + 6 CSVs derivados

WITH base AS (
  SELECT
    DATE_TRUNC(ORD_CLOSED_DT, MONTH) AS mes,
    DOM_DOMAIN_AGG1 AS d1,
    DOM_DOMAIN_AGG2 AS d2,
    RECEIVER_STATE AS uf,
    ORD_ORDER_ID,
    ITE_ITEM_ID,
    ITE_ITEM_CATALOG_PRODUCT_ID AS product_id,
    CASE WHEN NMV_FLG THEN GMV_LC ELSE 0 END AS nmv_lc,
    CASE WHEN NMV_FLG THEN SI ELSE 0 END AS nsi
  FROM `meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB`
  WHERE ORD_CLOSED_DT BETWEEN DATE '2025-11-01' AND DATE '2026-04-30'
    AND VERTICAL = 'HOME ELECTRONICS'
    AND CUS_CUST_ID_SEL = 1046986303
)
SELECT
  mes, d1, d2, uf,
  SUM(nmv_lc) AS nmv_lc,
  SUM(nsi) AS nsi,
  SAFE_DIVIDE(SUM(nmv_lc), SUM(nsi)) AS asp_lc,
  COUNT(DISTINCT ORD_ORDER_ID) AS orders,
  COUNT(DISTINCT ITE_ITEM_ID) AS qt_items,
  COUNT(DISTINCT product_id) AS qt_catalogos
FROM base
GROUP BY mes, d1, d2, uf
ORDER BY mes, nmv_lc DESC
