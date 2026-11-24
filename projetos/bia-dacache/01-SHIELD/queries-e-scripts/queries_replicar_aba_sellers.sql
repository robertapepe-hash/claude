-- =====================================================================
-- REPLICAR A ABA "MIGRACAO DOS SELLERS" EM OUTRAS D1s
-- Escrito para TVs e Audio (vertical HOME ELECTRONICS), mas o unico
-- ponto a trocar e a lista de D1 nas queries A, B e C.
--
-- Beatriz Dacache | 21/08/2026 | projeto Shield Against Asians / Plano de Combate BC
-- =====================================================================
--
-- NOMES DE D1 (identicos no Yipit e no Planning):
--   'TELEVISIONS & STREAMING DEVICES'
--   'AUDIO & GENERAL ELECTRONICS'
--   'LARGE APPLIANCES' / 'SMALL APPLIANCES'
--   'HEATING, COOLING & AIR QUALITY' / 'HOUSEHOLD APPLIANCES PARTS'
--
-- PEGADINHAS QUE CUSTARAM TEMPO:
--   1) No Yipit o pais e COUNTRY='BRAZIL' (nao 'BR').
--   2) A competencia e MONTHLY_TO_APPLY_SALES (nao DATE). DATE e a data de coleta.
--   3) O Yipit fecha um mes ANTES do DM Eficiencia. Hoje: Yipit vai ate jun/26,
--      DM vai ate jul/26. Nunca comparar N meses de um lado com N+1 do outro.
--   4) DM_EFICIENCIA_MLB NAO tem nickname do seller - so CUS_CUST_ID_SEL.
--      O nome vem de DM_MKP_SELLERS_HIST (CUS_NICKNAME).
--   5) O scan do DM Eficiencia e dirigido pelas COLUNAS, nao pelas linhas:
--      filtrar D1 ou cust_id NAO reduz o custo (~1,2-1,4 GB por mes de particao).
--
-- IMPORTANTE - Yipit e Planning sao A MESMA FONTE (verificado em 21/08/2026):
--   SBOX_MKPBR.DM_MARKET_ASP_MONTHLY_VERTICAL_D1.GMV_SHOPEE
--   == WHOWNER.DM_YIPIT_SHOPEE_ITEMS.NMV_LC agregado por D1 x mes
--   Diferenca de 0,00% a 0,15% em 18 combinacoes testadas.
--   Logo E VALIDO dividir um pelo outro (ex.: share do grupo no total da D1).


-- =====================================================================
-- QUERY A - QUEM OLHAR: ranking das lojas da Shopee
-- Roda primeiro. Da a lista de alvos e mostra a concentracao da D1.
-- Custo: ~0,6 GB
-- =====================================================================
WITH base AS (
  SELECT D1_CATEGORIZADOR_D1 AS D1, SHOP_ID, SHOP_NAME,
    MAX(IS_OFFICIAL_SHOP) AS OFICIAL,
    SUM(CASE WHEN MONTHLY_TO_APPLY_SALES BETWEEN '2026-05-01' AND '2026-06-30' THEN CAST(NMV_LC AS FLOAT64) END) AS N_2M_26,
    SUM(CASE WHEN MONTHLY_TO_APPLY_SALES BETWEEN '2025-05-01' AND '2025-06-30' THEN CAST(NMV_LC AS FLOAT64) END) AS N_2M_25,
    SUM(CASE WHEN MONTHLY_TO_APPLY_SALES='2026-06-01' THEN CAST(NMV_LC AS FLOAT64) END) AS N_JUN26
  FROM `meli-bi-data.WHOWNER.DM_YIPIT_SHOPEE_ITEMS`
  WHERE COUNTRY='BRAZIL' AND VERTICAL_CATEGORIZADOR='HOME ELECTRONICS'
    AND D1_CATEGORIZADOR_D1 IN ('TELEVISIONS & STREAMING DEVICES','AUDIO & GENERAL ELECTRONICS')
  GROUP BY 1,2,3
), tot AS (SELECT D1, SUM(N_2M_26) AS T26 FROM base GROUP BY 1)
SELECT b.D1, ROW_NUMBER() OVER (PARTITION BY b.D1 ORDER BY b.N_2M_26 DESC) AS POS,
  b.SHOP_NAME, b.SHOP_ID, b.OFICIAL,
  ROUND(b.N_2M_26/1e6,1)   AS MAIJUN26_MI,
  ROUND(b.N_2M_26/2/1e6,1) AS MEDIA_MES_MI,
  ROUND(b.N_JUN26/1e6,1)   AS JUN26_MI,
  ROUND(b.N_2M_25/1e6,1)   AS MAIJUN25_MI,
  CASE WHEN b.N_2M_25>0 THEN ROUND((b.N_2M_26/b.N_2M_25-1)*100,0) END AS YOY_PCT,
  ROUND(b.N_2M_26/t.T26*100,1) AS SOB_D1_PCT,
  ROUND(SUM(b.N_2M_26) OVER (PARTITION BY b.D1 ORDER BY b.N_2M_26 DESC)/t.T26*100,1) AS SOB_ACUM_PCT
FROM base b JOIN tot t USING(D1)
WHERE b.N_2M_26 > 0
QUALIFY POS <= 30
ORDER BY b.D1, POS;


-- =====================================================================
-- QUERY B - LADO SHOPEE DO GRAFICO: serie mensal por grupo economico
-- Troque o de-para do CTE `depara` pelos SHOP_IDs que a Query A devolveu.
-- Use SHOP_ID, nunca SHOP_NAME (o nome tem espaco/acento/emoji e muda).
-- Custo: ~0,6 GB
-- =====================================================================
WITH depara AS (
  SELECT * FROM UNNEST([
    STRUCT(1512106181 AS shop_id, 'SHOP EV (KILL)'   AS grupo),
    STRUCT( 811034337,            'PHILCO/BRITANIA'),
    STRUCT(1388709282,            '3 GREEN'),          -- Belmicro Oficial
    STRUCT( 898761179,            'REP STORE'),
    STRUCT( 344381236,            'TNTINFOLOJA'),
    STRUCT(1062544851,            'MERCADO FACIL'),
    STRUCT( 359168917,            'LOI BRASIL'),
    STRUCT( 389315825,            'MULTI')             -- Multi Oficial
  ])
)
SELECT d.grupo, FORMAT_DATE('%Y-%m', y.MONTHLY_TO_APPLY_SALES) AS mes,
  y.D1_CATEGORIZADOR_D1 AS d1,
  ROUND(SUM(CAST(y.NMV_LC AS FLOAT64))/1e6,4) AS shopee_mi
FROM `meli-bi-data.WHOWNER.DM_YIPIT_SHOPEE_ITEMS` y
JOIN depara d ON d.shop_id = y.SHOP_ID
WHERE y.COUNTRY='BRAZIL'
  AND y.D1_CATEGORIZADOR_D1 IN ('TELEVISIONS & STREAMING DEVICES','AUDIO & GENERAL ELECTRONICS')
  AND y.MONTHLY_TO_APPLY_SALES BETWEEN '2025-07-01' AND '2026-06-30'
GROUP BY 1,2,3
ORDER BY 1,3,2;


-- =====================================================================
-- QUERY C - LADO MELI DO GRAFICO: serie mensal por grupo economico
-- Metodologia de NMV travada no projeto: SUM(GMV_LC) com NMV_FLG e GMV_FLG,
-- por ORD_CLOSED_DT, sem filtro de SIT_SITE.
-- Custo: ~1,2-1,4 GB por mes de particao -> 13 meses ~ 17 GB.
-- >>> RODAR dry_run ANTES. Se ficar caro, cortar a janela para 7 meses.
-- =====================================================================
WITH depara AS (
  SELECT * FROM UNNEST([
    STRUCT(1512106181 AS cus_cust_id, 'SHOP EV (KILL)' AS grupo)
    -- ^ TROCAR pelos CUS_CUST_ID do MELI (a Query D ajuda a descobrir).
    --   ATENCAO: o id da loja na Shopee NAO e o cust_id do MELI.
  ])
)
SELECT d.grupo, FORMAT_DATE('%Y-%m', e.ORD_CLOSED_DT) AS mes,
  e.DOM_DOMAIN_AGG1 AS d1,
  ROUND(SUM(CAST(e.GMV_LC AS FLOAT64))/1e6,4) AS meli_mi
FROM `meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB` e
JOIN depara d ON d.cus_cust_id = e.CUS_CUST_ID_SEL
WHERE e.ORD_CLOSED_DT BETWEEN '2025-07-01' AND '2026-07-31'
  AND e.NMV_FLG AND e.GMV_FLG
  AND e.DOM_DOMAIN_AGG1 IN ('TELEVISIONS & STREAMING DEVICES','AUDIO & GENERAL ELECTRONICS')
  AND e.SEGMENTO = '3P - VERTICALES'   -- Carteira Assessorada. Tirar para pegar todo 3P.
GROUP BY 1,2,3
ORDER BY 1,3,2;


-- =====================================================================
-- QUERY D - CONSTRUIR O DE-PARA: candidatos no MELI por semelhanca de nome
-- Cole os nomes das lojas da Shopee em `alvos`. Devolve candidatos por
-- nickname normalizado. CONFERIR A MAO - match de nome erra.
-- Custo: ~1,4 GB (1 mes de particao) + a DM_MKP_SELLERS_HIST
-- =====================================================================
WITH alvos AS (
  SELECT * FROM UNNEST(['REP STORE','TNTINFOLOJA','MERCADO FACIL','LOI BRASIL',
                        'MULTI','PICHAU','CARREFOUR','TREVO','JACKCELL']) AS alvo
), norm AS (
  SELECT alvo, REGEXP_REPLACE(UPPER(alvo), r'[^A-Z0-9]', '') AS chave FROM alvos
), sellers AS (
  SELECT s.CUS_CUST_ID, s.CUS_NICKNAME, s.TOP_VERTICAL,
    REGEXP_REPLACE(UPPER(s.CUS_NICKNAME), r'[^A-Z0-9]', '') AS chave_nick
  FROM `meli-bi-data.WHOWNER.DM_MKP_SELLERS_HIST` s
  WHERE s.CUS_NICKNAME IS NOT NULL
), fat AS (
  SELECT CUS_CUST_ID_SEL AS cust, DOM_DOMAIN_AGG1 AS d1,
    SUM(CAST(GMV_LC AS FLOAT64))/1e6 AS meli_jun26_mi
  FROM `meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB`
  WHERE ORD_CLOSED_DT BETWEEN '2026-06-01' AND '2026-06-30'
    AND NMV_FLG AND GMV_FLG
    AND DOM_DOMAIN_AGG1 IN ('TELEVISIONS & STREAMING DEVICES','AUDIO & GENERAL ELECTRONICS')
  GROUP BY 1,2
)
SELECT n.alvo, s.CUS_NICKNAME, s.CUS_CUST_ID, s.TOP_VERTICAL,
  f.d1, ROUND(f.meli_jun26_mi,2) AS meli_jun26_mi
FROM norm n
JOIN sellers s ON (s.chave_nick = n.chave
                   OR STARTS_WITH(s.chave_nick, n.chave)
                   OR STARTS_WITH(n.chave, s.chave_nick))
LEFT JOIN fat f ON f.cust = s.CUS_CUST_ID
ORDER BY n.alvo, f.meli_jun26_mi DESC NULLS LAST;


-- =====================================================================
-- QUERY E - TABELA DE BAIXO (ranking atacar/proteger) ja pronta
-- Precisa das saidas de B e C. Aqui como CTE ilustrativo do calculo final.
-- A regra de classificacao e derivada do dado, nao arbitrada:
--   Shopee > MELI  -> ATACAR
--   MELI  >= Shopee -> PROTEGER
-- E a coluna de oportunidade:
--   "se trouxessemos 30% do que ele vende la" = shopee_mes * 0,30
-- =====================================================================
-- SELECT grupo,
--   ROUND(meli_maijun26,1)    AS meli_maijun26_mi,
--   ROUND(shopee_maijun26,1)  AS shopee_maijun26_mi,
--   ROUND(shopee_maijun26/NULLIF(meli_maijun26,0)*100,0) AS shopee_sobre_meli_pct,
--   IF(shopee_maijun26 > meli_maijun26,'ATACAR','PROTEGER') AS prioridade,
--   ROUND(shopee_maijun26*0.30/2,1) AS trazer_30pct_mi_mes
-- FROM <junta de B e C por grupo>
-- ORDER BY shopee_maijun26 DESC;
--
-- ADAPTACAO DA BEATRIZ (melhor que o valor absoluto):
--   converter o amount de 30% em % de uplift sobre o BAU mensal do proprio
--   seller (maio+junho/26 / 2), e aplicar esse fator % a cada mes da meta.
--   Motivo: R$ 14,9 Mi de incremental segura o ratio contra uma base de
--   maio/junho, mas nao muda nada contra a base de novembro, que e muito maior.
--   Em % o alvo fica proporcional ao mes.
