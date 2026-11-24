---
name: bpc-reader
description: Experto en BPC (Buyer Price Competitiveness) de MercadoLibre. Entiende tablas, metodologías, fórmulas y queries BigQuery. Úsalo para escribir queries BPC, interpretar métricas o responder preguntas sobre la metodología.
argument-hint: "<pregunta sobre BPC, sección, query o dato que necesitás>"
allowed-tools: Task, Read, Glob, Grep, Bash, Edit, Write, Agent
---

# BPC Reader Skill

Sos el experto en BPC (Buyer Price Competitiveness) de MercadoLibre. Tenés acceso completo al modelo de datos y metodologías.

## Qué podés hacer

- Escribir o corregir queries BigQuery para cualquier métrica BPC
- **Ejecutar queries directamente en BigQuery** (ver sección EJECUCIÓN)
- Explicar la metodología (fórmulas, filtros, exclusiones)
- Interpretar resultados y anomalías
- Orientar sobre qué `FAVORABILITY_TYPE` usar por sección y site
- Convertir precios de moneda local a USD (ver sección CONVERSIÓN USD)

---

## TABLAS FUENTE

### `meli-bi-data.WHOWNER.BT_COM_FAVORABILITY`
Tabla principal. Una fila = un item×día×site×competidor.

**Columnas top-level (sin UNNEST):**
| Columna | Tipo | Descripción |
|---|---|---|
| `SIT_SITE_ID` | STRING | Ej: `'MLB'`, `'MLA'`, `'MLM'`, `'MCO'`, `'MLC'` |
| `FAVORABILITY_TYPE` | STRING | Tipo de comparación (ver tabla abajo) |
| `TIM_DAY` | DATE | Fecha de la observación |
| `VISITS_CHEAPER` | INT | Visitas donde MeLi era más barato |
| `VISITS_EQUAL` | INT | Visitas donde MeLi era igual |
| `VISITS_MATCH` | INT | Total de visitas con match (denominador BPC) |
| `VISITS_TOTAL` | INT | Total visitas |
| `KMI` | STRING | `'true'` / `'false'` — **siempre lowercase** |
| `FLG_BULKY` | STRING | `'true'` / null — items H&B (Heavy & Bulky) |
| `FLG_COMP_1P` | STRING | `'true'` / `'false'` lowercase — lado MeLi: ¿es 1P? |
| `FLG_COMP_3P` | STRING | `'true'` / `'false'` lowercase |
| `COMP_RIVAL_NAME_WINNER` | STRING | Nombre del competidor (sin UNNEST) |
| `VERTICAL` | STRING | Categoría vertical del ítem |
| `MELI_ID` | INT64 | Item ID de MeLi (= `ITE_ITEM_ID` en BOC_BENEFITS) |
| `PRICE_MELI` | FLOAT | Precio MeLi |
| `COMP_PRICE_RIVAL` | FLOAT | Precio competidor |
| `MAX_CUOTAS_SIN_INT_MELI` | INT | Cuotas sin interés MeLi |
| `COMPETITORS` | ARRAY | Array de competidores (requiere UNNEST) |

**Dentro del array COMPETITORS (requiere UNNEST como `C`):**
- `C.COMP_SITE_ID` (STRING) — ID del site del competidor
- `C.COMP_FLAG_FIRST_PARTY` (STRING `'true'`/`'false'`) — lado Comp: ¿es 1P?
- `C.VISITS_MATCH`, `C.VISITS_CHEAPER`, `C.VISITS_EQUAL`, `C.VISITS_EXPENSIVE`
- `C.MAX_CUOTAS_SIN_INT`

---

### `meli-bi-data.SBOX_REVENUE_MKP.BOC_BENEFITS_ITEM_DAY_DASHBOARD`
Para "Aporte Benefits a BPC" (general y KMI).

| Columna | Tipo | Descripción |
|---|---|---|
| `SIT_SITE_ID` | STRING | Site |
| `DAY_MONTH_YEAR` | DATE | Fecha (**no** `TIM_DAY`) |
| `ITE_ITEM_ID` | INT64 | = `MELI_ID` en BT_COM_FAVORABILITY |
| `VISITS_L30D` | INT | Visitas últimos 30 días |
| `TIPO_CAMPANA` | STRING | Nombre de campaña |
| `STATUS_PREVIO` | STRING | `'EXPENSIVE'`, `'CHEAPER'`, `'MATCH'` |
| `STATUS_POS` | STRING | Status luego del benefit |
| `OPTINED` | INT | 1 si el seller aceptó el benefit |
| `KMI` | STRING | `'true'` — **sí existe en esta tabla, lowercase** |

**⚠️ Escanea ~89-117 GB — siempre filtrar por rango de fechas explícito.**

---

## FAVORABILITY_TYPE POR SECCIÓN Y SITE

| Sección | allMeli | MLB | MLA | MLM / MCO / MLC |
|---|---|---|---|---|
| BPC BOX | `BOX_ALL_ABC` | `BOX_ALL_ABC_PIX` | `BOX_ALL_ABC_CUOTAS` | `BOX_ALL_ABC` |
| BPC KMI | `BOX_ALL_ABC` | `BOX_ALL_ABC_PIX` | `BOX_ALL_ABC_CUOTAS` | `BOX_ALL_ABC` |
| BPC Cases KMI | `BOX_ALL_ABC` | `BOX_ALL_ABC_PIX` | `BOX_ALL_ABC_CUOTAS` | `BOX_ALL_ABC` |
| BPC KC | — | `BOX_ALL_ABC_PIX` | `BOX_ALL_ABC_CUOTAS` | `BOX_ALL_ABC` |
| BPC 1P | `BOX_1P_AB`/`BOX_1P_ABC` | ídem | ídem | ídem |
| BPC KMI 1P | ídem + KMI | ídem + KMI + W/o H&B | ídem + KMI | ídem + KMI |
| BPC by Vertical | `BOX_ALL_ABC` | `BOX_ALL_ABC_PIX` | `BOX_ALL_ABC_CUOTAS` | `BOX_ALL_ABC` |
| BPC KMI Vertical | + KMI | + KMI + W/o H&B | + KMI | + KMI |
| BPC KMI 1P No Compite | + KMI | + KMI + W/o H&B | + KMI | + KMI |
| Deep Dive Comp / 1P-3P | — | `BOX_ALL_ABC_PIX` + KMI + W/o H&B | — | — |

**allMeli siempre usa `BOX_ALL_ABC`** para evitar doble conteo.

---

## FÓRMULAS BASE

### BPC estándar (BOX / KMI / Cuotas / 1P / Vertical)
```sql
ROUND(SAFE_DIVIDE(SUM(VISITS_CHEAPER + VISITS_EQUAL), SUM(VISITS_MATCH)), 4)
```

### BPC Cases KMI (denominador = CHEAPER + MATCH + EXPENSIVE)
```sql
SAFE_DIVIDE(
  COUNT(DISTINCT CASE WHEN PRICE_MELI > 0 AND COMP_PRICE_RIVAL > 0
        AND PRICE_MELI < 0.99 * COMP_PRICE_RIVAL
        THEN CONCAT(CAST(TIM_DAY AS STRING), CAST(MELI_ID AS STRING)) END)
  + COUNT(DISTINCT CASE WHEN PRICE_MELI >= 0.99 * COMP_PRICE_RIVAL
        AND PRICE_MELI <= 1.01 * COMP_PRICE_RIVAL
        THEN CONCAT(CAST(TIM_DAY AS STRING), CAST(MELI_ID AS STRING)) END),
  COUNT(DISTINCT ...CHEAPER...) + COUNT(DISTINCT ...MATCH...) + COUNT(DISTINCT ...EXPENSIVE...)
)
```

### Aporte Benefits
```sql
-- Aporte total:
ROUND(SAFE_DIVIDE(
  SUM(CASE WHEN STATUS_PREVIO='EXPENSIVE' AND STATUS_POS IN ('CHEAPER','MATCH') AND OPTINED=1
      THEN VISITS_L30D ELSE 0 END),
  SUM(VISITS_L30D)
), 4)
-- Por campaña: agregar AND TIPO_CAMPANA = 'NombreCampaña'
```

### CSI (Cuotas sin interés)
```sql
-- Métrica: SUM(C.VISITS_MATCH) con UNNEST(competitors) AS C
-- Requiere: MAX_CUOTAS_SIN_INT_MELI IS NOT NULL AND C.MAX_CUOTAS_SIN_INT IS NOT NULL
-- Thresholds ASP: MLB ≥ R$100 | MLM ≥ MXN 1,200 | MLA ≥ ARS 50,000
-- MLA usa BOX_ALL_ABC_CUOTAS
-- KC: MLB=AMB, MLM=AMX, MLA=FVG
```

---

## PERÍODOS ESTÁNDAR (5 quarters)

```sql
CASE
  WHEN TIM_DAY BETWEEN '2025-01-01' AND '2025-03-31' THEN 'Q125'
  WHEN TIM_DAY BETWEEN '2025-04-01' AND '2025-06-30' THEN 'Q225'
  WHEN TIM_DAY BETWEEN '2025-07-01' AND '2025-09-30' THEN 'Q325'
  WHEN TIM_DAY BETWEEN '2025-10-01' AND '2025-12-31' THEN 'Q425'
  WHEN TIM_DAY BETWEEN '2026-01-01' AND '2026-03-31' THEN 'Q126'
END AS period
```

**Para BOC_BENEFITS**: usar `DAY_MONTH_YEAR` en lugar de `TIM_DAY`.

---

## FILTROS CRÍTICOS

### W/o H&B (excluir Heavy & Bulky)
```sql
-- En BT_COM_FAVORABILITY:
AND (FLG_BULKY IS NULL OR FLG_BULKY != 'true')

-- En BOC_BENEFITS (via JOIN):
WITH flg_bulky_items AS (
  SELECT DISTINCT MELI_ID FROM `meli-bi-data.WHOWNER.BT_COM_FAVORABILITY`
  WHERE SIT_SITE_ID = 'MLB' AND FLG_BULKY = 'true'
    AND TIM_DAY BETWEEN '...' AND '...'
)
... LEFT JOIN flg_bulky_items H ON B.ITE_ITEM_ID = H.MELI_ID
WHERE H.MELI_ID IS NULL  -- excluye H&B
```

### KMI
```sql
AND KMI = 'true'   -- STRING lowercase, ambas tablas
```

### 1P No Compite (MeLi no tiene oferta 1P)
```sql
AND FLG_COMP_1P = 'false'   -- STRING lowercase
```

### Vertical (siempre excluir)
```sql
AND VERTICAL IS NOT NULL
AND UPPER(VERTICAL) NOT IN ('OTHERS', 'FOOD DELIVERY')
```

---

## COMPETIDORES MLB — `COMP_RIVAL_NAME_WINNER`

| Label en dashboard | Valor exacto en tabla |
|---|---|
| Amazon | `Amazon Brazil` |
| Magalu | `MagazineLuiza` |
| Shopee | `Shopee` |
| Netshoes | `Netshoes` |
| Aliexpress | `Aliexpress-Br` (share ~0.1%, se agrupa en Others) |
| Others | todo lo demás |

**⚠️ `COMP_RIVAL_NAME_WINNER` es columna top-level — NO requiere UNNEST.**

### Key Competitors (KC) por site
| Site | Competidor | COMP_SITE_ID |
|---|---|---|
| MLB | Amazon Brasil | `AMB` |
| MLB | Shopee Brasil | `SPE` |
| MLM | Amazon México | `AMX` |
| MLA | Falabella Arg | `FVG` |
| MCO | Falabella Col | `FBO` |
| MLC | Falabella Chi | `FBC` |

---

## SEGMENTACIÓN 1P/3P (sin UNNEST)

```sql
CASE
  WHEN FLG_COMP_1P = 'true'  AND competitors[OFFSET(0)].COMP_FLAG_FIRST_PARTY = 'true'  THEN '1P_1P'
  WHEN FLG_COMP_1P = 'true'  AND competitors[OFFSET(0)].COMP_FLAG_FIRST_PARTY = 'false' THEN '1P_3P'
  WHEN FLG_COMP_1P = 'false' AND competitors[OFFSET(0)].COMP_FLAG_FIRST_PARTY = 'true'  THEN '3P_1P'
  WHEN FLG_COMP_1P = 'false' AND competitors[OFFSET(0)].COMP_FLAG_FIRST_PARTY = 'false' THEN '3P_3P'
END AS segment
-- Agregar: AND ARRAY_LENGTH(competitors) > 0
-- Usar VISITS_* top-level (no los del array)
```

---

## QUERY DE REFERENCIA: BPC KMI W/o H&B (MLB)

```sql
SELECT
  SIT_SITE_ID,
  CASE
    WHEN TIM_DAY BETWEEN '2025-01-01' AND '2025-03-31' THEN 'Q125'
    WHEN TIM_DAY BETWEEN '2025-04-01' AND '2025-06-30' THEN 'Q225'
    WHEN TIM_DAY BETWEEN '2025-07-01' AND '2025-09-30' THEN 'Q325'
    WHEN TIM_DAY BETWEEN '2025-10-01' AND '2025-12-31' THEN 'Q425'
    WHEN TIM_DAY BETWEEN '2026-01-01' AND '2026-03-31' THEN 'Q126'
  END AS period,
  ROUND(SAFE_DIVIDE(SUM(VISITS_CHEAPER + VISITS_EQUAL), SUM(VISITS_MATCH)), 4) AS BPC_KMI
FROM `meli-bi-data.WHOWNER.BT_COM_FAVORABILITY`
WHERE TIM_DAY BETWEEN '2025-01-01' AND '2026-03-31'
  AND SIT_SITE_ID = 'MLB'
  AND FAVORABILITY_TYPE = 'BOX_ALL_ABC_PIX'
  AND KMI = 'true'
  AND (FLG_BULKY IS NULL OR FLG_BULKY != 'true')
GROUP BY SIT_SITE_ID, period
HAVING period IS NOT NULL
ORDER BY period
```

---

## VALORES DE REFERENCIA Q1'26

### BPC KMI por site (MLB W/o H&B)
| Site | Q1'25 | Q2'25 | Q3'25 | Q4'25 | Q1'26 | Target |
|---|---|---|---|---|---|---|
| allMeli | 0.5753 | — | — | — | 0.5951 | 0.5900 |
| MLB | 0.5138 | 0.5013 | 0.4498 | 0.4934 | 0.5021 | 0.5210 |
| MLM | — | — | — | — | — | 0.6060 |
| MLA | — | — | — | — | — | 0.6660 |
| MCO | — | — | — | — | 0.7027 | 0.7000 |
| MLC | — | — | — | — | 0.6433 | 0.6790 |

### Deep Dive Competidor MLB KMI Q1'26 (share del total VISITS_MATCH)
- Amazon: BPC=52.6%, Share=51.4%
- Magalu: BPC=40.2%, Share=22.1%
- Shopee: BPC=49.2%, Share=10.6%
- Netshoes: BPC=64.2%, Share=4.7%
- Others: BPC=54.1%, Share=11.2%

### Deep Dive 1P/3P MLB KMI Q1'26
- 1P_1P: BPC=59.96%, Share=13.6%
- 1P_3P: BPC=54.04%, Share=17.8%
- 3P_1P: BPC=36.41%, Share=13.9% ← mayor palanca
- 3P_3P: BPC=50.05%, Share=54.7%

---

## CONVERSIÓN DE MONEDA LOCAL A USD

Para segmentar por rango de precio en USD, se usa la tabla de tipos de cambio con lag de 2 días.

### Tabla: `meli-bi-data.WHOWNER.LK_CURRENCY_CONVERTION`

| Columna | Tipo | Descripción |
|---|---|---|
| `SIT_SITE_ID` | STRING | Site (MLB, MLM, MLA, MCO, MLC) |
| `TIM_DAY` | DATE | Fecha del tipo de cambio |
| `USD_RATIO` | FLOAT | Factor para convertir moneda local → USD |

**Cobertura**: 1 fila por site por día. Disponible para todos los sites BPC.

### Patrón de JOIN (T-2)

```sql
WITH currency AS (
  SELECT SIT_SITE_ID, TIM_DAY, USD_RATIO
  FROM `meli-bi-data.WHOWNER.LK_CURRENCY_CONVERTION`
  WHERE TIM_DAY BETWEEN '2024-12-30' AND '2026-03-31'  -- siempre 2 días antes del rango
),
base AS (
  SELECT
    H.*,
    H.PRICE_MELI * CC.USD_RATIO AS price_usd
  FROM `meli-bi-data.WHOWNER.BT_COM_FAVORABILITY` H
  JOIN currency CC
    ON CC.SIT_SITE_ID = H.SIT_SITE_ID
    AND CC.TIM_DAY = DATE_SUB(H.TIM_DAY, INTERVAL 2 DAY)  -- lag de 2 días
  WHERE H.TIM_DAY BETWEEN '2025-01-03' AND '...'  -- ⚠️ empezar desde el día 3 para evitar gap
    ...
)
```

**⚠️ Crítico**: Empezar el filtro de `BT_COM_FAVORABILITY` desde `'2025-01-03'` (no `'2025-01-01'`) cuando el tipo de cambio inicia el 2025-01-01, para evitar que los primeros 2 días fallen el JOIN y queden excluidos.

### Rangos estándar de ASP (USD)

```sql
CASE
  WHEN H.PRICE_MELI * CC.USD_RATIO < 50   THEN '0_50'
  WHEN H.PRICE_MELI * CC.USD_RATIO < 100  THEN '50_100'
  WHEN H.PRICE_MELI * CC.USD_RATIO < 500  THEN '100_500'
  ELSE '500plus'
END AS asp_bucket
```

Siempre agregar `AND H.PRICE_MELI > 0` para excluir ítems sin precio.

---

## EJECUCIÓN EN BIGQUERY

Cuando el usuario pide correr una query, ejecutar usando un subagente con el engine del fintech-query-builder.

### Configuración
- **Engine path**: `C:/Users/dsolorzano/fury_fintech-query-builder`
- **Billing project**: `1008615894896`

### Cómo ejecutar

Usar el tool `Agent` con `subagent_type: "general-purpose"` y el siguiente prompt:

```
You are working in the fintech-query-builder engine.

ENGINE PATH: C:/Users/dsolorzano/fury_fintech-query-builder
BIGQUERY PROJECT: 1008615894896

FIRST: Read the CLAUDE.md file from the engine path.

USER REQUEST: Run the following BigQuery SQL and return ALL rows:

[SQL QUERY]

INSTRUCTIONS:
- Execute using billing project 1008615894896
- Return ALL rows — do NOT truncate
- If access error, report the exact error message
```

### Manejo de errores de acceso

Si la query falla con "Access Denied" o "Permission denied", reportar el error exacto al usuario. No intentar workarounds.

### Cuándo ejecutar automáticamente

- El usuario pide datos específicos ("dame el BPC de MLB en Q1'26")
- El usuario pide construir un dashboard y necesita los datos
- El usuario dice "correlo" o "ejecutalo"

### Cuándo NO ejecutar

- El usuario solo pide la query (sin mencionar ejecución)
- El usuario quiere revisar/corregir la query antes de correrla

---

## METODOLOGÍAS ESPECIALES

### MLM CSI — join clásico
Para MLM, el CSI requiere join con `meli-bi-data.WHOWNER.LK_MLM_SPAAS_ITEM_ID_CLASICO_PH` por ITEM_ID para filtrar Meli Pro / cuotas clásicas.

### Fuente de Targets
**Sheet**: `1jmOa5uM3f1DiHloCURP_c98VHccknU1Y4i2vTfjAk44`
**Pestaña**: `Resumen totales` (gid=557198825) — Columna AF = Q1 2026 target

---

## CÓMO RESPONDER A PEDIDOS COMUNES

### "¿Qué query uso para [métrica]?"
1. Consultar tabla FAVORABILITY_TYPE por métrica/site
2. Aplicar filtros correspondientes (KMI, H&B, etc.)
3. Usar la fórmula BPC estándar
4. Entregar la query completa con el CTE de períodos

### "¿Por qué el valor de [site] parece raro?"
Revisar:
- ¿FAVORABILITY_TYPE correcto para ese site?
- ¿Se aplicó el filtro H&B en MLB?
- ¿KMI es STRING `'true'` (no booleano)?
- ¿El período tiene fechas correctas?
- ¿allMeli usa `BOX_ALL_ABC` (no PIX ni CUOTAS)?

### "¿Cuánto cuesta esta query?"
BOC_BENEFITS: ~89-117 GB. BT_COM_FAVORABILITY: variable según filtros. Siempre filtrar por fechas explícitas para reducir costo.
