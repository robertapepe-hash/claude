# -*- coding: utf-8 -*-
# Gera a query do cubo Seller-Helper (CA, grupo economico) + salva de-para CSV no kit.
import openpyxl, csv, os

mapf=r"C:\Users\bdacache\Documents\grupos economicos - foco bc.xlsx"
kit=r"C:\Users\bdacache\Documents\Claude\Projects\Shield Against Asians"
scr=r"C:\Users\bdacache\AppData\Local\Temp\claude\C--Users-bdacache\bbb7afb0-3296-496f-bc54-c89f13e96eb2\scratchpad"

mb=openpyxl.load_workbook(mapf,data_only=True)
dep={}
for sh in mb.worksheets:
    for row in list(sh.iter_rows(values_only=True))[1:]:
        if row[0] is None: continue
        cid=str(row[0]).strip(); grp=(str(row[2]).strip() if row[2] is not None else "")
        if grp: dep[cid]=grp
print("custs mapeados:",len(dep),"grupos distintos:",len(set(dep.values())))

# persiste de-para no kit (perene)
with open(os.path.join(kit,"grupos_economicos.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["cust","grupo"])
    for c,g in sorted(dep.items()): w.writerow([c,g])

# monta UNNEST de structs
def esc(s): return s.replace("'","\\'")
structs=",".join([f"STRUCT('{c}' AS cust,'{esc(g)}' AS grupo)" for c,g in dep.items()])

FAIXA="CASE WHEN ITE_ITEM_FULL_UNIT_PRICE<200 THEN '1_<200' WHEN ITE_ITEM_FULL_UNIT_PRICE<500 THEN '2_200-500' WHEN ITE_ITEM_FULL_UNIT_PRICE<1500 THEN '3_500-1500' WHEN ITE_ITEM_FULL_UNIT_PRICE<3000 THEN '4_1500-3000' ELSE '5_>3000' END"

sql=f"""WITH dep AS (SELECT * FROM UNNEST([{structs}])),
base AS (SELECT FORMAT_DATE('%Y-%m',ORD_CLOSED_DT) mes, {FAIXA} AS faixa, DOM_DOMAIN_AGG2 AS d2, CAST(CUS_CUST_ID_SEL AS STRING) AS cust, SELLER_NAME AS nick, F_NMV_LC AS nmv, F_NSI AS nsi, ITE_ITEM_ID AS iid, COALESCE(NULLIF(ITE_ITEM_BRAND,''),'(sem marca)') AS brand FROM `meli-bi-data.WHOWNER.DM_EFICIENCIA_MLB` WHERE VERTICAL='HOME ELECTRONICS' AND DOM_DOMAIN_AGG1='LARGE APPLIANCES' AND SEGMENTO_DETAIL='CA' AND ORD_CLOSED_DT BETWEEN '2025-01-01' AND '2026-07-31' AND ITE_ITEM_FULL_UNIT_PRICE>0),
g AS (SELECT b.mes,b.faixa,b.d2,b.iid,b.brand,b.nmv,b.nsi, COALESCE(dep.grupo,b.nick) AS grupo FROM base b LEFT JOIN dep ON b.cust=dep.cust),
rk AS (SELECT grupo, SUM(nmv) sn, SUM(nsi) ss FROM g GROUP BY 1),
named AS (SELECT grupo FROM (SELECT grupo, ROW_NUMBER() OVER(ORDER BY sn DESC) rn, ROW_NUMBER() OVER(ORDER BY ss DESC) rs FROM rk) WHERE rn<=50 OR rs<=50)
SELECT g.mes, g.faixa, g.d2, IF(n.grupo IS NULL,'Outros',g.grupo) AS grupo, ROUND(SUM(g.nmv)/1e6,4) AS nmv_mi, ROUND(SUM(g.nsi),4) AS nsi, COUNT(DISTINCT g.iid) AS itens, COUNT(DISTINCT g.brand) AS marcas FROM g LEFT JOIN named n ON g.grupo=n.grupo GROUP BY 1,2,3,4"""

sql=" ".join(sql.split())  # 1 linha p/ bq
with open(os.path.join(scr,"q_sellercap.sql"),"w",encoding="utf-8") as f: f.write(sql)
print("SQL len:",len(sql),"chars -> q_sellercap.sql; de-para salvo em grupos_economicos.csv")
