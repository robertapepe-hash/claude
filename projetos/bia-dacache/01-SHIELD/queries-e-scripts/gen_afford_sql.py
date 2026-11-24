# -*- coding: utf-8 -*-
import csv, os, datetime
kit=r"C:\Users\bdacache\Documents\Claude\Projects\Shield Against Asians"
scr=r"C:\Users\bdacache\AppData\Local\Temp\claude\C--Users-bdacache\bbb7afb0-3296-496f-bc54-c89f13e96eb2\scratchpad"
dep={}
for row in csv.DictReader(open(os.path.join(kit,"grupos_economicos.csv"),encoding="utf-8-sig")):
    dep[row["cust"].strip()]=row["grupo"].strip()
def esc(s): return s.replace("'","\\'")
structs=",".join([f"STRUCT('{c}' AS cust,'{esc(g)}' AS grupo)" for c,g in dep.items()])
FAIXA="CASE WHEN ITE_ITEM_FULL_UNIT_PRICE<200 THEN '1_<200' WHEN ITE_ITEM_FULL_UNIT_PRICE<500 THEN '2_200-500' WHEN ITE_ITEM_FULL_UNIT_PRICE<1500 THEN '3_500-1500' WHEN ITE_ITEM_FULL_UNIT_PRICE<3000 THEN '4_1500-3000' ELSE '5_>3000' END"
SEG="CASE SEGMENTO_DETAIL WHEN 'CA' THEN '3P Assessorada' WHEN 'SD' THEN '3P Dev' WHEN 'PL' THEN '1P' ELSE SEGMENTO_DETAIL END"
MEIO="CASE WHEN PAYMENT_METHOD_1='pix' AND DXB_PAYMENT_METHOD='PIX' THEN 'Pix incentivado' WHEN PAYMENT_METHOD_1='pix' THEN 'Pix organico' WHEN PAYMENT_METHOD_TYPE_1='credit_card' THEN 'Credito' WHEN PAYMENT_METHOD_TYPE_1='account_money' THEN 'Meli saldo' WHEN PAYMENT_METHOD_TYPE_1='digital_currency' THEN 'Mercado Credito' WHEN PAYMENT_METHOD_TYPE_1='ticket' THEN 'Boleto' WHEN PAYMENT_METHOD_TYPE_1='prepaid_card' THEN 'Pre-pago' WHEN PAYMENT_METHOD_TYPE_1 IS NULL THEN 'Sem info' ELSE 'Outros' END"
FILT="VERTICAL='HOME ELECTRONICS' AND DOM_DOMAIN_AGG1='LARGE APPLIANCES' AND ITE_ITEM_FULL_UNIT_PRICE>0"

# MENSAL: 1 scan, 2 grupos de grao -> mix(grupo+d2+meio) e inst(faixa+segmento, sem grupo/d2)
mon=f"""WITH dep AS (SELECT * FROM UNNEST([{structs}])),
base AS (SELECT FORMAT_DATE('%Y-%m',ORD_CLOSED_DT) AS mes, {FAIXA} AS faixa, DOM_DOMAIN_AGG2 AS d2, {SEG} AS segmento, COALESCE(dep.grupo, SELLER_NAME) AS grupo, {MEIO} AS meio, IF(PAYMENT_METHOD_TYPE_1='credit_card', COALESCE(INSTALLMENTS_1,'?'), 'x') AS inst, F_NMV_LC AS nmv, ORD_ORDER_ID AS oid FROM `meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB` LEFT JOIN dep ON CAST(CUS_CUST_ID_SEL AS STRING)=dep.cust WHERE {FILT} AND ORD_CLOSED_DT BETWEEN '2025-01-01' AND '2026-07-31'),
rk AS (SELECT grupo, SUM(nmv) sn FROM base GROUP BY 1),
named AS (SELECT grupo FROM (SELECT grupo, ROW_NUMBER() OVER(ORDER BY sn DESC) rn FROM rk) WHERE rn<=30),
b2 AS (SELECT base.*, IF(n.grupo IS NULL,'Outros',base.grupo) AS grp FROM base LEFT JOIN named n ON base.grupo=n.grupo)
SELECT mes,faixa,d2,segmento,grp AS grupo,meio,inst, GROUPING(meio) gm, GROUPING(inst) gi, ROUND(SUM(nmv)/1e6,4) nmv_mi, COUNT(DISTINCT oid) ped FROM b2 GROUP BY GROUPING SETS ((mes,faixa,d2,segmento,grp,meio),(mes,faixa,segmento,inst))"""

# DATA DUPLA enxuta: dia x faixa x meio (sem grupo/d2/seg) -> query curta, sem structs
dd=[]
for m in range(2,8):
    b=datetime.date(2026,m,m)
    for off in(-1,0,1): dd.append((b+datetime.timedelta(days=off)).isoformat())
dd_in=",".join(f"'{d}'" for d in dd)
ddq=f"""SELECT CAST(ORD_CLOSED_DT AS STRING) AS dia, {FAIXA} AS faixa, {MEIO} AS meio, ROUND(SUM(F_NMV_LC)/1e6,4) nmv_mi, COUNT(DISTINCT ORD_ORDER_ID) ped FROM `meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB` WHERE {FILT} AND ORD_CLOSED_DT IN ({dd_in}) GROUP BY 1,2,3"""

open(os.path.join(scr,"q_afford_mon.sql"),"w",encoding="utf-8").write(" ".join(mon.split()))
open(os.path.join(scr,"q_afford_dd.sql"),"w",encoding="utf-8").write(" ".join(ddq.split()))
print("mon len",len(" ".join(mon.split())),"| dd len",len(" ".join(ddq.split())),"| dd dates",len(dd))
