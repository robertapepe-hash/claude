-- ============================================================================
-- ETAPA 3 — Sortimento incremental e Buy Box
-- Universo: catalogos CAT_PRODUCT_ID onde a CBH vendeu pos-nov/25 (n=1.566)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Q-3A: Universo catalogos CBH (nov/25-abr/26) com NMV, NSI, UFs alcancadas
-- Custo: ~12,0 GB / US$ 0,06
-- Output: outputs/etapa3a_catalogos_cbh_raw.json (1.566 linhas)
-- ----------------------------------------------------------------------------
SELECT
  ITE_ITEM_CATALOG_PRODUCT_ID AS product_id,
  ANY_VALUE(DOM_DOMAIN_AGG1) AS d1,
  ANY_VALUE(DOM_DOMAIN_AGG2) AS d2,
  ANY_VALUE(ITE_ITEM_BRAND) AS brand,
  SUM(CASE WHEN NMV_FLG THEN GMV_LC ELSE 0 END) AS nmv_cbh,
  SUM(CASE WHEN NMV_FLG THEN SI ELSE 0 END) AS nsi_cbh,
  COUNT(DISTINCT IF(NMV_FLG, ORD_ORDER_ID, NULL)) AS orders_cbh,
  COUNT(DISTINCT RECEIVER_STATE) AS qt_ufs_cbh,
  COUNT(DISTINCT ITE_ITEM_ID) AS qt_item_ids_cbh
FROM `meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB`
WHERE ORD_CLOSED_DT BETWEEN DATE '2025-11-01' AND DATE '2026-04-30'
  AND VERTICAL = 'HOME ELECTRONICS'
  AND CUS_CUST_ID_SEL = 1046986303
  AND ITE_ITEM_CATALOG_PRODUCT_ID IS NOT NULL
GROUP BY product_id
ORDER BY nmv_cbh DESC;

-- ----------------------------------------------------------------------------
-- Q-3B: Classifica catalogos CBH em Tipo A (existia pre) vs Tipo B (novo)
-- Custo: ~44,9 GB / US$ 0,22
-- Output: outputs/etapa3b_classificacao_AB_raw.json (1.566 linhas)
-- ----------------------------------------------------------------------------
WITH cbh_catalogs AS (
  SELECT
    ITE_ITEM_CATALOG_PRODUCT_ID AS product_id,
    ANY_VALUE(DOM_DOMAIN_AGG1) AS d1,
    ANY_VALUE(DOM_DOMAIN_AGG2) AS d2,
    ANY_VALUE(ITE_ITEM_BRAND) AS brand,
    SUM(CASE WHEN NMV_FLG THEN GMV_LC ELSE 0 END) AS nmv_cbh_pos,
    SUM(CASE WHEN NMV_FLG THEN SI ELSE 0 END) AS nsi_cbh_pos,
    COUNT(DISTINCT RECEIVER_STATE) AS ufs_cbh_pos
  FROM `meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB`
  WHERE ORD_CLOSED_DT BETWEEN DATE '2025-11-01' AND DATE '2026-04-30'
    AND VERTICAL = 'HOME ELECTRONICS'
    AND CUS_CUST_ID_SEL = 1046986303
    AND ITE_ITEM_CATALOG_PRODUCT_ID IS NOT NULL
  GROUP BY product_id
),
historico AS (
  SELECT
    ITE_ITEM_CATALOG_PRODUCT_ID AS product_id,
    SUM(CASE WHEN NMV_FLG THEN GMV_LC ELSE 0 END) AS nmv_pre,
    SUM(CASE WHEN NMV_FLG THEN SI ELSE 0 END) AS nsi_pre,
    COUNT(DISTINCT CUS_CUST_ID_SEL) AS qt_sellers_pre,
    COUNT(DISTINCT RECEIVER_STATE) AS qt_ufs_pre,
    MIN(ORD_CLOSED_DT) AS first_sale_pre
  FROM `meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB`
  WHERE ORD_CLOSED_DT BETWEEN DATE '2024-01-01' AND DATE '2025-10-31'
    AND VERTICAL = 'HOME ELECTRONICS'
    AND ITE_ITEM_CATALOG_PRODUCT_ID IS NOT NULL
  GROUP BY product_id
)
SELECT
  c.product_id, c.d1, c.d2, c.brand,
  c.nmv_cbh_pos, c.nsi_cbh_pos, c.ufs_cbh_pos,
  IF(h.product_id IS NULL, 'B_NOVO', 'A_EXISTENTE') AS tipo,
  h.nmv_pre, h.nsi_pre, h.qt_sellers_pre, h.qt_ufs_pre, h.first_sale_pre
FROM cbh_catalogs c
LEFT JOIN historico h ON c.product_id = h.product_id
ORDER BY c.nmv_cbh_pos DESC;

-- ----------------------------------------------------------------------------
-- Q-3C: Top seller pre vs pos por catalogo (BB winner change)
-- Custo: ~24,7 GB / US$ 0,12
-- Output: outputs/etapa3c_bb_winner_raw.json (1.566 linhas)
-- ----------------------------------------------------------------------------
WITH cbh_catalogs AS (
  SELECT DISTINCT ITE_ITEM_CATALOG_PRODUCT_ID AS product_id
  FROM `meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB`
  WHERE ORD_CLOSED_DT BETWEEN DATE '2025-11-01' AND DATE '2026-04-30'
    AND VERTICAL = 'HOME ELECTRONICS'
    AND CUS_CUST_ID_SEL = 1046986303
    AND ITE_ITEM_CATALOG_PRODUCT_ID IS NOT NULL
),
seller_periods AS (
  SELECT
    base.ITE_ITEM_CATALOG_PRODUCT_ID AS product_id,
    base.CUS_CUST_ID_SEL AS seller_id,
    ANY_VALUE(base.SELLER_NAME) AS seller_name,
    SUM(IF(base.ORD_CLOSED_DT < DATE '2025-11-01' AND base.NMV_FLG, base.GMV_LC, 0)) AS nmv_pre,
    SUM(IF(base.ORD_CLOSED_DT >= DATE '2025-11-01' AND base.NMV_FLG, base.GMV_LC, 0)) AS nmv_pos
  FROM `meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB` base
  INNER JOIN cbh_catalogs c ON base.ITE_ITEM_CATALOG_PRODUCT_ID = c.product_id
  WHERE base.ORD_CLOSED_DT BETWEEN DATE '2024-01-01' AND DATE '2026-04-30'
    AND base.VERTICAL = 'HOME ELECTRONICS'
  GROUP BY product_id, seller_id
),
ranked AS (
  SELECT product_id, seller_id, seller_name, nmv_pre, nmv_pos,
    ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY nmv_pre DESC) AS rk_pre,
    ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY nmv_pos DESC) AS rk_pos
  FROM seller_periods
),
tops AS (
  SELECT product_id,
    MAX(IF(rk_pre = 1, seller_id, NULL)) AS top_pre_seller_id,
    MAX(IF(rk_pre = 1, seller_name, NULL)) AS top_pre_seller_name,
    MAX(IF(rk_pre = 1, nmv_pre, NULL)) AS top_pre_nmv,
    MAX(IF(rk_pre = 1, nmv_pos, NULL)) AS top_pre_seller_nmv_pos,
    MAX(IF(rk_pos = 1, seller_id, NULL)) AS top_pos_seller_id,
    MAX(IF(rk_pos = 1, seller_name, NULL)) AS top_pos_seller_name,
    MAX(IF(rk_pos = 1, nmv_pos, NULL)) AS top_pos_nmv
  FROM ranked
  WHERE rk_pre = 1 OR rk_pos = 1
  GROUP BY product_id
),
totals AS (
  SELECT product_id,
    SUM(nmv_pre) AS total_pre,
    SUM(nmv_pos) AS total_pos,
    SUM(IF(seller_id = 1046986303, nmv_pos, 0)) AS nmv_cbh_pos,
    COUNT(DISTINCT IF(nmv_pre > 0, seller_id, NULL)) AS qt_sellers_pre,
    COUNT(DISTINCT IF(nmv_pos > 0, seller_id, NULL)) AS qt_sellers_pos
  FROM seller_periods
  GROUP BY product_id
)
SELECT t.product_id,
  tp.top_pre_seller_name, tp.top_pre_seller_id, tp.top_pre_nmv, tp.top_pre_seller_nmv_pos,
  tp.top_pos_seller_name, tp.top_pos_seller_id, tp.top_pos_nmv,
  t.total_pre, t.total_pos, t.nmv_cbh_pos,
  t.qt_sellers_pre, t.qt_sellers_pos
FROM totals t
LEFT JOIN tops tp USING (product_id)
ORDER BY t.nmv_cbh_pos DESC;
