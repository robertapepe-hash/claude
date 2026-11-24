-- =====================================================================
-- SHOPEE: FATURAMENTO E PECAS POR LOJA x FAIXA DE ASP (sem abertura por item)
-- Fonte: meli-bi-data.WHOWNER.DM_YIPIT_SHOPEE_ITEMS
-- Janela: os 3 ultimos meses FECHADOS da propria base (hoje: abr, mai, jun/26)
--
-- >>>>>> PARA RODAR EM OUTRA CATEGORIA, MUDE SO O CTE `params` ABAIXO. <<<<<<
--        E o UNICO lugar da query com nome de categoria.
--
-- Beatriz Dacache | 02/09/2026 | Shield Against Asians / Plano de Combate BC
-- =====================================================================
--
-- COMO LER O RESULTADO
--   1 linha = 1 loja x 1 mes x 1 faixa de ASP.
--   NMV = faturamento (R$) · NSI = pecas vendidas · ASP_MEDIO = NMV/NSI da celula
--   ITENS_ATIVOS = quantos itens distintos a loja teve naquela faixa naquele mes
--
-- POR QUE A QUERY TEM DUAS ETAPAS (nao juntar numa so)
--   A faixa de ASP e calculada POR ITEM (CTE `item`) e so DEPOIS agregada por loja.
--   Se agregar direto por loja, o ASP vira a media da loja inteira e cada loja cai
--   numa faixa unica -- o mix desaparece. Exemplo real (Electrolux, jun/26):
--   com o calculo por item ela aparece em 3 faixas (29,5 Mi em 1500-3000,
--   12,8 Mi em 500-1500, 9,9 Mi acima de 3000); agregando direto, apareceria so em uma.
--
-- ARMADILHAS DESTA BASE (custaram tempo, ja resolvidas aqui)
--   1) COUNTRY = 'BRAZIL', nao 'BR'.
--   2) A competencia e MONTHLY_TO_APPLY_SALES. DATE e a data de COLETA -- nao usar.
--   3) A base tem DEFASAGEM (~2 meses). Por isso a janela NAO usa CURRENT_DATE:
--      `DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH)` hoje daria >= 01/07/2026 e a base
--      fecha em jun/26 -> ZERO LINHAS. A janela e ancorada no MAX da propria base.
--   4) Agrupar por SHOP_ID, nunca por SHOP_NAME: o nome tem espaco, acento e emoji,
--      e muda. O nome vai no resultado via ANY_VALUE, so para leitura.
--   5) Item com NSI = 0 gera ASP nulo. Sem um ELSE no CASE ele viraria NULL e
--      desapareceria da tabela -- aqui vai para 'Sem ASP (NSI=0)'.
--
-- NOTA DE FONTE: este NMV_LC e a MESMA coisa que o GMV_SHOPEE do Planning
--   (SBOX_MKPBR.DM_MARKET_ASP_MONTHLY_VERTICAL_D1), verificado em 21/08/2026 com
--   erro de 0,00% a 0,15% em 18 combinacoes de D1 x mes. Da para cruzar os dois.
-- =====================================================================

WITH params AS (
  -- >>> MUDE AQUI E SO AQUI <<<
  SELECT 'HOME ELECTRONICS' AS vertical,
         'LARGE APPLIANCES' AS d1            -- deixe NULL para trazer TODAS as D1s da vertical
),
lim AS (
  -- ultima competencia disponivel na base (nao depende de CURRENT_DATE)
  SELECT MAX(MONTHLY_TO_APPLY_SALES) AS ultimo
  FROM `meli-bi-data.WHOWNER.DM_YIPIT_SHOPEE_ITEMS`
),
item AS (
  -- ETAPA 1: ASP e faixa POR ITEM
  SELECT
    DATE_TRUNC(y.MONTHLY_TO_APPLY_SALES, MONTH)  AS MES,
    y.D1_CATEGORIZADOR_D1                        AS D1,
    y.SHOP_ID,
    y.ITEM_ID,
    ANY_VALUE(y.SHOP_NAME)                       AS SHOP_NAME,
    ANY_VALUE(y.OFFICIAL_SHOP)                   AS OFFICIAL_SHOP,
    ANY_VALUE(y.IS_OFFICIAL_SHOP)                AS IS_OFFICIAL_SHOP,
    ANY_VALUE(y.MONTHLY_SELLER_COHORT)           AS MONTHLY_SELLER_COHORT,
    SUM(y.NMV_LC)                                AS NMV,
    SUM(y.NSI)                                   AS NSI
  FROM `meli-bi-data.WHOWNER.DM_YIPIT_SHOPEE_ITEMS` y, lim, params p
  WHERE y.COUNTRY = 'BRAZIL'
    AND UPPER(y.VERTICAL_CATEGORIZADOR) = p.vertical
    AND (p.d1 IS NULL OR UPPER(y.D1_CATEGORIZADOR_D1) = p.d1)
    AND y.MONTHLY_TO_APPLY_SALES >= DATE_SUB(lim.ultimo, INTERVAL 2 MONTH)
  GROUP BY MES, D1, y.SHOP_ID, y.ITEM_ID
),
faixa AS (
  SELECT i.*,
    CASE
      WHEN SAFE_DIVIDE(i.NMV, i.NSI) IS NULL THEN 'Sem ASP (NSI=0)'
      WHEN SAFE_DIVIDE(i.NMV, i.NSI) <  200  THEN 'Menor de 200'
      WHEN SAFE_DIVIDE(i.NMV, i.NSI) <  500  THEN '200 a 500'
      WHEN SAFE_DIVIDE(i.NMV, i.NSI) < 1500  THEN '500 a 1500'
      WHEN SAFE_DIVIDE(i.NMV, i.NSI) < 3000  THEN '1500 a 3000'
      ELSE 'Acima de 3000'
    END AS ASP_CLUSTER,
    CASE
      WHEN SAFE_DIVIDE(i.NMV, i.NSI) IS NULL THEN 9
      WHEN SAFE_DIVIDE(i.NMV, i.NSI) <  200  THEN 1
      WHEN SAFE_DIVIDE(i.NMV, i.NSI) <  500  THEN 2
      WHEN SAFE_DIVIDE(i.NMV, i.NSI) < 1500  THEN 3
      WHEN SAFE_DIVIDE(i.NMV, i.NSI) < 3000  THEN 4
      ELSE 5
    END AS ASP_ORD                               -- so para ordenar faixa em pivot
  FROM item i
)
-- ETAPA 2: agrega por LOJA (o item desaparece aqui)
SELECT
  FORMAT_DATE('%Y-%m', MES)                  AS MES,
  D1,
  SHOP_ID,
  ANY_VALUE(SHOP_NAME)                       AS SHOP_NAME,
  ANY_VALUE(OFFICIAL_SHOP)                   AS OFFICIAL_SHOP,
  ANY_VALUE(IS_OFFICIAL_SHOP)                AS IS_OFFICIAL_SHOP,
  ANY_VALUE(MONTHLY_SELLER_COHORT)           AS MONTHLY_SELLER_COHORT,
  ASP_ORD,
  ASP_CLUSTER,
  ROUND(SUM(NMV), 2)                         AS NMV,
  ROUND(SUM(NMV)/1e6, 4)                     AS NMV_MI,
  CAST(SUM(NSI) AS INT64)                    AS NSI,
  ROUND(SAFE_DIVIDE(SUM(NMV), SUM(NSI)), 2)  AS ASP_MEDIO,
  COUNT(DISTINCT ITEM_ID)                    AS ITENS_ATIVOS
FROM faixa
GROUP BY MES, D1, SHOP_ID, ASP_ORD, ASP_CLUSTER
ORDER BY MES, D1, NMV DESC;


-- =====================================================================
-- CATALOGO DE VALORES VALIDOS (levantado em 02/09/2026)
-- Todas as combinacoes com > R$ 30 Mi na Shopee em Q2'26. Todas fecham em jun/26.
--
--  vertical                     | d1                                    | Q2'26 Mi | lojas
--  -----------------------------+---------------------------------------+----------+------
--  FASHION                      | APPAREL                               |  6.596,2 | 10787
--  FASHION                      | FOOTWEAR                              |  1.553,2 |  4172
--  FURNISHING & HOUSEWARE       | HOUSEHOLD ITEMS                       |  1.551,1 |  9959
--  FURNISHING & HOUSEWARE       | FURNITURE                             |  1.461,1 |  3534
--  FASHION                      | APPAREL ACCESSORIES                   |    969,3 | 10455
--  CONSTRUCTION & INDUSTRY      | TOOLS                                 |    740,3 |  4933
--  CONSTRUCTION & INDUSTRY      | CONSTRUCTION                          |    700,3 |  5477
--  FURNISHING & HOUSEWARE       | TEXTILES                              |    698,7 |  3805
--  HOME ELECTRONICS             | SMALL APPLIANCES                      |    591,8 |  2211
--  T & B                        | TOYS AND GAMES                        |    563,7 |  8112
--  HEALTH                       | HEALTH GOODS                          |    562,4 |  7336
--  CONSTRUCTION & INDUSTRY      | INDUSTRY                              |    532,0 |  6483
--  FURNISHING & HOUSEWARE       | DECOR                                 |    512,8 |  6167
--  HOME ELECTRONICS             | LARGE APPLIANCES                      |    511,4 |   701
--  CPG                          | PET                                   |    497,8 |  4721
--  TECHNOLOGY                   | SMARTPHONES & TABLETS                 |    495,9 |  3499
--  VEHICLE PARTS & ACCESSORIES  | ACC CARS & VANS                       |    485,0 |  5054
--  BEAUTY                       | BEAUTY PROFESSIONAL                   |    454,2 |  5629
--  T & B                        | BABY                                  |    378,1 |  5307
--  SPORTS                       | CYCLING AND OTHERS                    |    362,6 |  2496
--  VEHICLE PARTS & ACCESSORIES  | ACC TIRES                             |    344,6 |   569
--  CPG                          | FOODS                                 |    337,8 |  3999
--  CONSTRUCTION & INDUSTRY      | STATIONERY                            |    336,6 |  7097
--  T & B                        | PARTY                                 |    331,5 |  6022
--  TECHNOLOGY                   | IT PERIPHERALS, PARTS & ACCESSORIES   |    329,8 |  4216
--  SPORTS                       | MOUNTAIN & OUTDOORS                   |    322,2 |  4302
--  VEHICLE PARTS & ACCESSORIES  | ACC MOTORCYCLES                       |    314,8 |  2738
--  CPG                          | CPG HOME CARE                         |    303,8 |  4515
--  HOME ELECTRONICS             | HEATING, COOLING & AIR QUALITY        |    303,4 |  1093
--  HOME ELECTRONICS             | TELEVISIONS & STREAMING DEVICES       |    296,3 |  1213
--  CONSTRUCTION & INDUSTRY      | LIGHTING                              |    269,4 |  2536
--  HEALTH                       | SUPPLEMENTS                           |    256,5 |  1590
--  SPORTS                       | INDOOR SPORTS                         |    246,9 |  3461
--  BEAUTY                       | HAIR                                  |    240,0 |  2396
--  BEAUTY                       | BEAUTY PERSONAL CARE                  |    239,0 |  4452
--  TECHNOLOGY                   | WEARABLES                             |    222,9 |  1963
--  HOME ELECTRONICS             | AUDIO & GENERAL ELECTRONICS           |    196,2 |  3335
--  CPG                          | CPG PERSONAL CARE                     |    188,1 |  3588
--  BEAUTY                       | MAKEUP                                |    186,7 |  3757
--  BEAUTY                       | BEAUTY ELECTRONICS                    |    174,7 |  1911
--  BEAUTY                       | FRAGRANCES                            |    155,5 |  1525
--  TECHNOLOGY                   | CAMERAS & DRONES                      |    143,0 |  1823
--  HOME ELECTRONICS             | HOUSEHOLD APPLIANCES PARTS            |    138,5 |  2230
--  FURNISHING & HOUSEWARE       | HABERDASHERY                          |    133,5 |  2829
--  CONSTRUCTION & INDUSTRY      | HOME OUTDOORS                         |    123,7 |  2835
--  ENTERTAINMENT                | BOOKS AND OTHERS                      |    117,3 |  3157
--  OTHERS                       | OTHER                                 |     99,6 |  2715
--  CONSTRUCTION & INDUSTRY      | SECURITY                              |     97,5 |  1757
--  TECHNOLOGY                   | COMPUTERS & NOTEBOOKS                 |     86,2 |   253
--  VEHICLE PARTS & ACCESSORIES  | ACC VEHICULAR MULTIMEDIA              |     81,3 |   836
--  TECHNOLOGY                   | CONSOLE GAMING HARDWARE               |     80,4 |  1402
--  SPORTS                       | OTHER SPORTS                          |     80,1 |  2280
--  SPORTS                       | SPORTS ACCESSORIES                    |     78,3 |  1825
--  ENTERTAINMENT                | MUSICAL INSTRUMENTS                   |     76,3 |  2052
--  TECHNOLOGY                   | IT APPLIANCES                         |     74,3 |  1555
--  FURNISHING & HOUSEWARE       | MATTRESSES & SOMMIER                  |     73,1 |   212
--  VEHICLE PARTS & ACCESSORIES  | ACC COMMERCIAL VEHICLES               |     52,0 |  1250
--  SPORTS                       | FOOTBALL                              |     34,2 |  1503
--
-- Os nomes ja vem em MAIUSCULA na base, mas o UPPER() no filtro deixa a query
-- tolerante a quem digitar em minuscula.
-- ATENCAO: VERTICAL_CATEGORIZADOR e D1_CATEGORIZADOR_D1 sao classificacao do
-- modelo categorizador do ML aplicada ao catalogo da Shopee -- nao e a taxonomia
-- oficial dela. Para HOME ELECTRONICS os nomes coincidem com DOM_DOMAIN_AGG1 do
-- Planning (verificado); para as outras verticais isso NAO foi conferido.
--
-- CUSTO: ~0,8 a 1,5 GB por rodada, independente da categoria filtrada -- o scan
-- desta base e dirigido pelas COLUNAS referenciadas, nao pelas linhas.
-- =====================================================================
