-- ============================================================================
-- ETAPA 2 — Crescimento regional MELI HE com vs sem CBH
-- Cobre Lentes 1 (núcleo YoY fev-abr 26/25), 2 (robustness pré/pós), 3 (evolutivo)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Q-A: Evolutivo mensal HE × D1 × Região × is_cbh (jan/2024 → abr/2026)
-- Cobre Lentes 1, 2, 3 em nível regional
-- Custo: ~35,4 GB / US$ 0,17
-- Output: outputs/etapa2_qa_regiao_raw.json (1353 linhas)
-- ----------------------------------------------------------------------------
SELECT
  DATE_TRUNC(ORD_CLOSED_DT, MONTH) AS mes,
  DOM_DOMAIN_AGG1 AS d1,
  CASE
    WHEN RECEIVER_STATE IN ('BR-AC','BR-AP','BR-AM','BR-PA','BR-RO','BR-RR','BR-TO') THEN 'N'
    WHEN RECEIVER_STATE IN ('BR-AL','BR-BA','BR-CE','BR-MA','BR-PB','BR-PE','BR-PI','BR-RN','BR-SE') THEN 'NE'
    WHEN RECEIVER_STATE IN ('BR-DF','BR-GO','BR-MT','BR-MS') THEN 'CO'
    WHEN RECEIVER_STATE IN ('BR-ES','BR-MG','BR-RJ','BR-SP') THEN 'SE'
    WHEN RECEIVER_STATE IN ('BR-PR','BR-RS','BR-SC') THEN 'S'
    ELSE 'OUTROS'
  END AS regiao,
  (CUS_CUST_ID_SEL = 1046986303) AS is_cbh,
  SUM(CASE WHEN NMV_FLG THEN GMV_LC ELSE 0 END) AS nmv_lc,
  SUM(CASE WHEN NMV_FLG THEN SI ELSE 0 END) AS nsi,
  COUNT(DISTINCT IF(NMV_FLG, ORD_ORDER_ID, NULL)) AS orders,
  COUNT(DISTINCT CUS_CUST_ID_SEL) AS qt_sellers
FROM `meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB`
WHERE ORD_CLOSED_DT BETWEEN DATE '2024-01-01' AND DATE '2026-04-30'
  AND VERTICAL = 'HOME ELECTRONICS'
GROUP BY mes, d1, regiao, is_cbh
ORDER BY mes, d1, regiao;

-- ----------------------------------------------------------------------------
-- Q-B: Lente 1 detalhado por UF (fev-abr/25 vs fev-abr/26)
-- Custo: ~7,8 GB / US$ 0,04
-- Output: outputs/etapa2_qb_uf_raw.json (486 linhas)
-- ----------------------------------------------------------------------------
SELECT
  CASE WHEN ORD_CLOSED_DT BETWEEN '2025-02-01' AND '2025-04-30' THEN 'L1_2025'
       WHEN ORD_CLOSED_DT BETWEEN '2026-02-01' AND '2026-04-30' THEN 'L1_2026'
  END AS periodo,
  DOM_DOMAIN_AGG1 AS d1,
  RECEIVER_STATE AS uf,
  (CUS_CUST_ID_SEL = 1046986303) AS is_cbh,
  SUM(CASE WHEN NMV_FLG THEN GMV_LC ELSE 0 END) AS nmv_lc,
  SUM(CASE WHEN NMV_FLG THEN SI ELSE 0 END) AS nsi,
  COUNT(DISTINCT IF(NMV_FLG, ORD_ORDER_ID, NULL)) AS orders
FROM `meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB`
WHERE ((ORD_CLOSED_DT BETWEEN '2025-02-01' AND '2025-04-30')
    OR (ORD_CLOSED_DT BETWEEN '2026-02-01' AND '2026-04-30'))
  AND VERTICAL = 'HOME ELECTRONICS'
GROUP BY periodo, d1, uf, is_cbh
ORDER BY periodo, d1, uf;
