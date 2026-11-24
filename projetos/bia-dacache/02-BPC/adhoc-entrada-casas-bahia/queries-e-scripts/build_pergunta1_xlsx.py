"""Gera XLSX com as 25 marcas do Pareto + análise completa."""
import pandas as pd
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE = Path(r"C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-05-entrada-cbh-incrementalidade-regional")
OUT = BASE / "outputs"
TARGET = OUT / "Pergunta1_25marcas_LA_TVs.xlsx"

CBH_ID = 1046986303

# Dados das 25 marcas do Pareto
dados = [
    {'pos':1,  'marca':'Electrolux','d1':'LA', 'npre':301016958, 'ntot':348696352, 'ncbh':41757190, 'tpre':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpre_id':480263032, 'tprenmv':162065123, 'tpos':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpos_id':480263032, 'tposnmv':160800581},
    {'pos':2,  'marca':'Brastemp','d1':'LA',   'npre':175357191, 'ntot':214835812, 'ncbh':30251239, 'tpre':'BUDCOMÉRCIOELETRODOMÉSTICOS', 'tpre_id':185297674, 'tprenmv':80382604, 'tpos':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpos_id':480263032, 'tposnmv':77522940},
    {'pos':3,  'marca':'LG','d1':'TVs',        'npre':207733502, 'ntot':212246744, 'ncbh':29160410, 'tpre':'VIKINGS_DIGITAL', 'tpre_id':1917068106, 'tprenmv':68080948, 'tpos':'VIKINGS_DIGITAL', 'tpos_id':1917068106, 'tposnmv':64007013},
    {'pos':4,  'marca':'Samsung','d1':'TVs',   'npre':187025626, 'ntot':200734583, 'ncbh':33052290, 'tpre':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpre_id':480263032, 'tprenmv':73374647, 'tpos':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpos_id':480263032, 'tposnmv':71966741},
    {'pos':5,  'marca':'Consul','d1':'LA',     'npre':114364023, 'ntot':177944487, 'ncbh':37143593, 'tpre':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpre_id':480263032, 'tprenmv':62806424, 'tpos':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpos_id':480263032, 'tposnmv':71099037},
    {'pos':6,  'marca':'TCL','d1':'TVs',       'npre':73736307,  'ntot':136762109, 'ncbh':40525850, 'tpre':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpre_id':480263032, 'tprenmv':52014771, 'tpos':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpos_id':480263032, 'tposnmv':66333665},
    {'pos':7,  'marca':'Midea','d1':'LA',      'npre':95971114,  'ntot':117099499, 'ncbh':13287965, 'tpre':'MIDEA STORE', 'tpre_id':668432476, 'tprenmv':35770836, 'tpos':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpos_id':480263032, 'tposnmv':41829573},
    {'pos':8,  'marca':'Philco','d1':'LA',     'npre':75742924,  'ntot':91151241,  'ncbh':3721064,  'tpre':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpre_id':480263032, 'tprenmv':39817535, 'tpos':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpos_id':480263032, 'tposnmv':41753646},
    {'pos':9,  'marca':'Philco','d1':'TVs',    'npre':133001097, 'ntot':86898714,  'ncbh':4142535,  'tpre':'VIKINGS_DIGITAL', 'tpre_id':1917068106, 'tprenmv':59777953, 'tpos':'VIKINGS_DIGITAL', 'tpos_id':1917068106, 'tposnmv':46033940},
    {'pos':10, 'marca':'Samsung','d1':'LA',    'npre':46300644,  'ntot':56335455,  'ncbh':3956417,  'tpre':'SAMSUNGLOJAOFICIAL', 'tpre_id':1158756553, 'tprenmv':34246522, 'tpos':'SAMSUNGLOJAOFICIAL', 'tpos_id':1158756553, 'tposnmv':36139697},
    {'pos':11, 'marca':'Aiwa','d1':'TVs',      'npre':40455261,  'ntot':53033161,  'ncbh':0,        'tpre':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpre_id':480263032, 'tprenmv':35796442, 'tpos':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpos_id':480263032, 'tposnmv':47917077},
    {'pos':12, 'marca':'Philips','d1':'TVs',   'npre':28912715,  'ntot':45741723,  'ncbh':9478961,  'tpre':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpre_id':480263032, 'tprenmv':21191398, 'tpos':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpos_id':480263032, 'tposnmv':17305887},
    {'pos':13, 'marca':'Dako','d1':'LA',       'npre':31508417,  'ntot':42548937,  'ncbh':3297730,  'tpre':'ATLAS ELETRODOMÉSTICOS', 'tpre_id':279642028, 'tprenmv':16297321, 'tpos':'ATLAS ELETRODOMÉSTICOS', 'tpos_id':279642028, 'tposnmv':14247234},
    {'pos':14, 'marca':'AOC','d1':'TVs',       'npre':30225129,  'ntot':41060878,  'ncbh':3774603,  'tpre':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpre_id':480263032, 'tprenmv':7843712, 'tpos':'ESHOP', 'tpos_id':1737442603, 'tposnmv':12449322},
    {'pos':15, 'marca':'Panasonic','d1':'LA',  'npre':45601146,  'ntot':37206137,  'ncbh':601387,   'tpre':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpre_id':480263032, 'tprenmv':33601172, 'tpos':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpos_id':480263032, 'tposnmv':27388714},
    {'pos':16, 'marca':'Itatiaia','d1':'LA',   'npre':28730355,  'ntot':33918201,  'ncbh':2377775,  'tpre':'MEGAMAMUTE FULLMG', 'tpre_id':1168726042, 'tprenmv':5295885, 'tpos':'MEGAMAMUTE FULLMG', 'tpos_id':1168726042, 'tposnmv':8942398},
    {'pos':17, 'marca':'Atlas','d1':'LA',      'npre':24200345,  'ntot':30655073,  'ncbh':6473958,  'tpre':'MEGAMAMUTE FULLMG', 'tpre_id':1168726042, 'tprenmv':7996495, 'tpos':'MEGAMAMUTE FULLMG', 'tpos_id':1168726042, 'tposnmv':10248103},
    {'pos':18, 'marca':'Suggar','d1':'LA',     'npre':28377524,  'ntot':30155139,  'ncbh':2460837,  'tpre':'XCOMM.', 'tpre_id':372535210, 'tprenmv':10688395, 'tpos':'XCOMM.', 'tpos_id':372535210, 'tposnmv':9455379},
    {'pos':19, 'marca':'Fischer','d1':'LA',    'npre':32663009,  'ntot':27546696,  'ncbh':25403,    'tpre':'2ELETRO INFO', 'tpre_id':743518733, 'tprenmv':5688946, 'tpos':'2ELETRO INFO', 'tpos_id':743518733, 'tposnmv':4466711},
    {'pos':20, 'marca':'Mondial','d1':'LA',    'npre':8754868,   'ntot':26072035,  'ncbh':1130491,  'tpre':'LOI BRASIL', 'tpre_id':130090710, 'tprenmv':2376439, 'tpos':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpos_id':480263032, 'tposnmv':19016984},
    {'pos':21, 'marca':'HQ','d1':'LA',         'npre':21623694,  'ntot':23637185,  'ncbh':0,        'tpre':'BELMICROSHOP', 'tpre_id':442421077, 'tprenmv':21351375, 'tpos':'BELMICROSHOP', 'tpos_id':442421077, 'tposnmv':22928133},
    {'pos':22, 'marca':'Colormaq','d1':'LA',   'npre':12744346,  'ntot':20408305,  'ncbh':11130785, 'tpre':'COLORVISÃO', 'tpre_id':316958268, 'tprenmv':8199178, 'tpos':'LOJAOFICIALCASASBAHIA', 'tpos_id':1046986303, 'tposnmv':11130785},
    {'pos':23, 'marca':'Mueller','d1':'LA',    'npre':17668313,  'ntot':18855317,  'ncbh':0,        'tpre':'MEGAMAMUTE FULLMG', 'tpre_id':1168726042, 'tprenmv':4296452, 'tpos':'MEGAMAMUTE FULLMG', 'tpos_id':1168726042, 'tposnmv':5251301},
    {'pos':24, 'marca':'Hisense','d1':'TVs',   'npre':12007895,  'ntot':18340656,  'ncbh':3467284,  'tpre':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpre_id':480263032, 'tprenmv':11068191, 'tpos':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpos_id':480263032, 'tposnmv':9311319},
    {'pos':25, 'marca':'Britania','d1':'LA',   'npre':16176738,  'ntot':17726480,  'ncbh':5316852,  'tpre':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpre_id':480263032, 'tprenmv':11400505, 'tpos':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpos_id':480263032, 'tposnmv':6441628},
]

# Calcula métricas e classifica
rows = []
for r in dados:
    excbh = r['ntot'] - r['ncbh']
    yoy_tot = (r['ntot']/r['npre']-1)*100
    yoy_excbh = (excbh/r['npre']-1)*100
    share_cbh = r['ncbh']/r['ntot']*100
    delta_tot = r['ntot'] - r['npre']
    contrib_cbh = (r['ncbh']/delta_tot)*100 if delta_tot > 0 else None
    delta_top_pre = (r['tposnmv']/r['tprenmv']-1)*100 if r['tpre_id']==r['tpos_id'] else None
    trocou_top = r['tpre_id'] != r['tpos_id']
    # Novo critério: cresceu E CBH foi material (contrib >= 50%)
    passa = (yoy_tot > 0) and (contrib_cbh is not None and contrib_cbh >= 50)
    cbh_eh_top = r['tpos_id']==CBH_ID
    if not passa:
        # Razão de não passar
        if yoy_tot <= 0:
            cluster = f'Marca em queda ({yoy_tot:.0f}% YoY)'
        elif r['ncbh'] == 0:
            cluster = 'CBH não atua na marca'
        elif contrib_cbh < 50:
            cluster = f'Cresceu sem CBH ser material (contrib {contrib_cbh:.0f}%)'
        else:
            cluster = '—'
    elif cbh_eh_top and yoy_excbh<0:
        cluster = 'A. Dominou e recuperou a marca'
    elif cbh_eh_top and yoy_excbh>=0:
        cluster = 'C. Virou top, marca compensou'
    else:
        cluster = 'B. Expandiu sem virar top'
    base_pequena = r['npre']<5_000_000
    rows.append({
        'Pos Pareto': r['pos'],
        'Marca': r['marca'],
        'D1': r['d1'],
        'NMV pré (R$ Mi)': round(r['npre']/1e6,2),
        'NMV pós (R$ Mi)': round(r['ntot']/1e6,2),
        'Δ NMV (R$ Mi)': round(delta_tot/1e6,2),
        'YoY total (%)': round(yoy_tot,1),
        'NMV pós ex-CBH (R$ Mi)': round(excbh/1e6,2),
        'YoY ex-CBH (%)': round(yoy_excbh,1),
        'NMV CBH (R$ Mi)': round(r['ncbh']/1e6,2),
        'Share CBH (%)': round(share_cbh,1),
        'Contrib CBH (%)': round(contrib_cbh,1) if contrib_cbh is not None else 'N/A',
        'Top seller PRÉ': r['tpre'],
        'NMV top pré (R$ Mi)': round(r['tprenmv']/1e6,2),
        'Top seller PÓS': r['tpos'],
        'NMV top pós (R$ Mi)': round(r['tposnmv']/1e6,2),
        'Δ top mesmo seller (%)': round(delta_top_pre,1) if delta_top_pre is not None else 'trocou',
        'Trocou top?': 'SIM' if trocou_top else 'não',
        'CBH foi material? (contrib≥50% E cresceu)': 'SIM' if passa else 'não',
        'Cluster / Situação': cluster,
        'Caveat base <R$ 5Mi pré': '⚠' if base_pequena else '',
    })

df = pd.DataFrame(rows)

# Estilos
FONT_TITULO = Font(name='Calibri', bold=True, size=14, color='1A1A1A')
FONT_SUB = Font(name='Calibri', italic=True, size=10, color='555555')
FONT_HEADER = Font(name='Calibri', bold=True, size=10, color='FFFFFF')
FONT_BODY = Font(name='Calibri', size=10, color='1A1A1A')
FILL_HEADER = PatternFill('solid', fgColor='1A1A1A')
FILL_PASSA_SIM = PatternFill('solid', fgColor='FFE600')
FILL_PASSA_NAO = PatternFill('solid', fgColor='F5F5F5')
FILL_CLUSTER_A = PatternFill('solid', fgColor='F9A825')
FILL_CLUSTER_B = PatternFill('solid', fgColor='FFF59D')
FILL_CLUSTER_C = PatternFill('solid', fgColor='9A7D0A')
BORDER_THIN = Border(
    left=Side(style='thin', color='CCCCCC'),
    right=Side(style='thin', color='CCCCCC'),
    top=Side(style='thin', color='CCCCCC'),
    bottom=Side(style='thin', color='CCCCCC'))

wb = Workbook()
ws = wb.active
ws.title = "25 marcas"

# Título e contexto
ws['A1'] = "Pergunta 1 — Como a CBH ajudou no sortimento (LA + TVs, top 25 do Pareto = 89,7% do NMV)"
ws['A1'].font = FONT_TITULO
ws.merge_cells('A1:V1')
ws['A2'] = "Período pré: ago-out/25 (sem CBH) | Período pós: fev-abr/26 (com CBH consolidada) | Métrica: F_NMV_LC"
ws['A2'].font = FONT_SUB
ws.merge_cells('A2:V2')
ws['A3'] = "Critério 'CBH foi material' (flexibilizado): YoY total > 0% E Contrib CBH no growth ≥ 50%"
ws['A3'].font = FONT_SUB
ws.merge_cells('A3:V3')

# Header
header_row = 5
for c_idx, col in enumerate(df.columns, start=1):
    cell = ws.cell(row=header_row, column=c_idx, value=col)
    cell.font = FONT_HEADER
    cell.fill = FILL_HEADER
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    cell.border = BORDER_THIN

# Dados
for r_idx, row in enumerate(df.itertuples(index=False), start=header_row+1):
    for c_idx, val in enumerate(row, start=1):
        cell = ws.cell(row=r_idx, column=c_idx, value=val)
        cell.font = FONT_BODY
        cell.border = BORDER_THIN
        col_name = df.columns[c_idx-1]
        if col_name == 'CBH foi material? (contrib≥50% E cresceu)':
            cell.fill = FILL_PASSA_SIM if val == 'SIM' else FILL_PASSA_NAO
            cell.alignment = Alignment(horizontal='center')
            if val == 'SIM': cell.font = Font(name='Calibri', bold=True, size=10, color='1A1A1A')
        elif col_name == 'Cluster / Situação':
            if val.startswith('A.'): cell.fill = FILL_CLUSTER_A
            elif val.startswith('B.'): cell.fill = FILL_CLUSTER_B
            elif val.startswith('C.'): cell.fill = FILL_CLUSTER_C
        elif isinstance(val, (int, float)):
            cell.number_format = '#,##0.0' if 'NMV' in col_name or 'Δ' in col_name or '%' in col_name else '#,##0'
            cell.alignment = Alignment(horizontal='right')

# Larguras
widths = {'Pos Pareto':6, 'Marca':12, 'D1':5, 'NMV pré (R$ Mi)':12, 'NMV pós (R$ Mi)':12, 'Δ NMV (R$ Mi)':12,
          'YoY total (%)':10, 'NMV pós ex-CBH (R$ Mi)':13, 'YoY ex-CBH (%)':12, 'NMV CBH (R$ Mi)':12,
          'Share CBH (%)':10, 'Contrib CBH (%)':12, 'Top seller PRÉ':38, 'NMV top pré (R$ Mi)':12,
          'Top seller PÓS':38, 'NMV top pós (R$ Mi)':12, 'Δ top mesmo seller (%)':14,
          'Trocou top?':10, 'CBH foi material? (contrib≥50% E cresceu)':18, 'Cluster / Situação':42, 'Caveat base <R$ 5Mi pré':9}
for c_idx, col in enumerate(df.columns, start=1):
    ws.column_dimensions[get_column_letter(c_idx)].width = widths.get(col, 12)

ws.row_dimensions[header_row].height = 50
ws.freeze_panes = 'D6'

# Sheet 2: Resumo dos clusters
ws2 = wb.create_sheet("Resumo_Clusters")
ws2['A1'] = "Resumo — marcas que passaram nos 3 critérios"
ws2['A1'].font = FONT_TITULO
ws2.merge_cells('A1:G1')

summary = df[df['CBH foi material? (contrib≥50% E cresceu)']=='SIM'][['Marca','D1','NMV pré (R$ Mi)','NMV pós (R$ Mi)','YoY total (%)','YoY ex-CBH (%)','Share CBH (%)','Contrib CBH (%)','Top seller PRÉ','Top seller PÓS','Cluster / Situação']].sort_values(['Cluster / Situação','NMV pós (R$ Mi)'], ascending=[True, False])

for c_idx, col in enumerate(summary.columns, start=1):
    cell = ws2.cell(row=3, column=c_idx, value=col)
    cell.font = FONT_HEADER; cell.fill = FILL_HEADER
    cell.alignment = Alignment(horizontal='center', wrap_text=True)
for r_idx, row in enumerate(summary.itertuples(index=False), start=4):
    for c_idx, val in enumerate(row, start=1):
        cell = ws2.cell(row=r_idx, column=c_idx, value=val)
        cell.font = FONT_BODY
        cell.border = BORDER_THIN
        col_name = summary.columns[c_idx-1]
        if col_name == 'Cluster / Situação':
            if val.startswith('A.'): cell.fill = FILL_CLUSTER_A
            elif val.startswith('B.'): cell.fill = FILL_CLUSTER_B
            elif val.startswith('C.'): cell.fill = FILL_CLUSTER_C
for c_idx in range(1, len(summary.columns)+1):
    ws2.column_dimensions[get_column_letter(c_idx)].width = 18
ws2.column_dimensions['A'].width = 12
ws2.column_dimensions['B'].width = 6
ws2.column_dimensions['I'].width = 40
ws2.column_dimensions['J'].width = 40
ws2.column_dimensions['K'].width = 32

# ============================================
# ABA 3: Step 1.2 - 7 marcas novas do Pareto CBH
# ============================================
dados_step2 = [
    {'pos':1, 'marca':'LG','d1':'LA',         'npre':12074728, 'ntot':17548273, 'ncbh':11457900, 'tpre':'LGLG20231107104529', 'tpre_id':1539956358, 'tprenmv':4571753, 'tpos':'LOJAOFICIALCASASBAHIA', 'tpos_id':1046986303, 'tposnmv':11457900},
    {'pos':2, 'marca':'Hisense','d1':'LA',    'npre':11838599, 'ntot':15960544, 'ncbh':2059533,  'tpre':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpre_id':480263032, 'tprenmv':9565018, 'tpos':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpos_id':480263032, 'tposnmv':11506701},
    {'pos':3, 'marca':'Semp TCL','d1':'TVs',  'npre':15947344, 'ntot':15699436, 'ncbh':5192654,  'tpre':'MEGAMAMUTE', 'tpre_id':1461582452, 'tprenmv':3895335, 'tpos':'LOJAOFICIALCASASBAHIA', 'tpos_id':1046986303, 'tposnmv':5192654},
    {'pos':4, 'marca':'Continental','d1':'LA','npre':5548472,  'ntot':14896569, 'ncbh':9869844,  'tpre':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpre_id':480263032, 'tprenmv':2462709, 'tpos':'LOJAOFICIALCASASBAHIA', 'tpos_id':1046986303, 'tposnmv':9869844},
    {'pos':5, 'marca':'Britania','d1':'TVs',  'npre':11659001, 'ntot':14105470, 'ncbh':3631653,  'tpre':'SHOP EV', 'tpre_id':750553953, 'tprenmv':7563712, 'tpos':'123 COMPROU', 'tpos_id':85263796, 'tposnmv':3855292},
    {'pos':6, 'marca':'Esmaltec','d1':'LA',   'npre':2436370,  'ntot':7484594,  'ncbh':6192983,  'tpre':'1P MELI (MERCADO LIVRE ELETRONICOS)', 'tpre_id':480263032, 'tprenmv':1072219, 'tpos':'LOJAOFICIALCASASBAHIA', 'tpos_id':1046986303, 'tposnmv':6192983},
    {'pos':7, 'marca':'TCL','d1':'LA',        'npre':365874,   'ntot':1569643,  'ncbh':1200833,  'tpre':'MEGAMAMUTE FULLMG', 'tpre_id':1168726042, 'tprenmv':352375, 'tpos':'LOJAOFICIALCASASBAHIA', 'tpos_id':1046986303, 'tposnmv':1200833},
]

rows_s2 = []
for r in dados_step2:
    excbh = r['ntot'] - r['ncbh']
    yoy_tot = (r['ntot']/r['npre']-1)*100
    yoy_excbh = (excbh/r['npre']-1)*100
    share_cbh = r['ncbh']/r['ntot']*100
    delta_tot = r['ntot'] - r['npre']
    contrib_cbh = (r['ncbh']/delta_tot)*100 if delta_tot > 0 else None
    delta_top_pre = (r['tposnmv']/r['tprenmv']-1)*100 if r['tpre_id']==r['tpos_id'] else None
    trocou_top = r['tpre_id'] != r['tpos_id']
    passa = (yoy_tot > 0) and (contrib_cbh is not None and contrib_cbh >= 50)
    cbh_eh_top = r['tpos_id']==CBH_ID
    if not passa:
        if yoy_tot <= 0:
            cluster = f'Marca em queda ({yoy_tot:.0f}% YoY) — CBH compensou parcial'
        elif r['ncbh'] == 0:
            cluster = 'CBH não atua na marca'
        elif contrib_cbh is None or contrib_cbh < 50:
            cluster = f'Cresceu sem CBH ser material (contrib {contrib_cbh:.0f}%)' if contrib_cbh is not None else 'N/A'
        else:
            cluster = '—'
    elif cbh_eh_top and yoy_excbh<0:
        cluster = 'A. Dominou e recuperou a marca'
    elif cbh_eh_top and yoy_excbh>=0:
        cluster = 'C. Virou top, marca compensou'
    else:
        cluster = 'B. Expandiu sem virar top'
    base_pequena = r['npre']<5_000_000
    rows_s2.append({
        'Pos Pareto CBH': r['pos'],
        'Marca': r['marca'], 'D1': r['d1'],
        'NMV pré (R$ Mi)': round(r['npre']/1e6,2),
        'NMV pós (R$ Mi)': round(r['ntot']/1e6,2),
        'Δ NMV (R$ Mi)': round(delta_tot/1e6,2),
        'YoY total (%)': round(yoy_tot,1),
        'NMV pós ex-CBH (R$ Mi)': round(excbh/1e6,2),
        'YoY ex-CBH (%)': round(yoy_excbh,1),
        'NMV CBH (R$ Mi)': round(r['ncbh']/1e6,2),
        'Share CBH (%)': round(share_cbh,1),
        'Contrib CBH (%)': round(contrib_cbh,1) if contrib_cbh is not None else 'N/A',
        'Top seller PRÉ': r['tpre'], 'NMV top pré (R$ Mi)': round(r['tprenmv']/1e6,2),
        'Top seller PÓS': r['tpos'], 'NMV top pós (R$ Mi)': round(r['tposnmv']/1e6,2),
        'Δ top mesmo seller (%)': round(delta_top_pre,1) if delta_top_pre is not None else 'trocou',
        'Trocou top?': 'SIM' if trocou_top else 'não',
        'CBH foi material?': 'SIM' if passa else 'não',
        'Cluster / Situação': cluster,
        'Caveat base <R$ 5Mi pré': '⚠' if base_pequena else '',
    })

df_s2 = pd.DataFrame(rows_s2)

ws3 = wb.create_sheet("Step1.2 - 7 marcas novas")
ws3['A1'] = "Step 1.2 — Marcas do Pareto CBH NÃO cobertas pelas 25 do Pareto geral"
ws3['A1'].font = FONT_TITULO
ws3.merge_cells('A1:U1')
ws3['A2'] = "Universo: marcas onde a CBH é representativa mas estão fora do top 25 LA+TVs geral (caso Esmaltec, LG/LA, etc)"
ws3['A2'].font = FONT_SUB
ws3.merge_cells('A2:U2')
ws3['A3'] = "Mesmo critério: YoY total > 0% E Contrib CBH ≥ 50%"
ws3['A3'].font = FONT_SUB
ws3.merge_cells('A3:U3')

for c_idx, col in enumerate(df_s2.columns, start=1):
    cell = ws3.cell(row=5, column=c_idx, value=col)
    cell.font = FONT_HEADER; cell.fill = FILL_HEADER
    cell.alignment = Alignment(horizontal='center', wrap_text=True)
    cell.border = BORDER_THIN
for r_idx, row in enumerate(df_s2.itertuples(index=False), start=6):
    for c_idx, val in enumerate(row, start=1):
        cell = ws3.cell(row=r_idx, column=c_idx, value=val)
        cell.font = FONT_BODY; cell.border = BORDER_THIN
        col_name = df_s2.columns[c_idx-1]
        if col_name == 'CBH foi material?':
            cell.fill = FILL_PASSA_SIM if val == 'SIM' else FILL_PASSA_NAO
            cell.alignment = Alignment(horizontal='center')
            if val == 'SIM': cell.font = Font(name='Calibri', bold=True, size=10, color='1A1A1A')
        elif col_name == 'Cluster / Situação':
            if val.startswith('A.'): cell.fill = FILL_CLUSTER_A
            elif val.startswith('B.'): cell.fill = FILL_CLUSTER_B
            elif val.startswith('C.'): cell.fill = FILL_CLUSTER_C
        elif isinstance(val, (int, float)):
            cell.number_format = '#,##0.0'
            cell.alignment = Alignment(horizontal='right')
for c_idx, col in enumerate(df_s2.columns, start=1):
    ws3.column_dimensions[get_column_letter(c_idx)].width = widths.get(col, 12) if col in widths else 14
ws3.column_dimensions['M'].width = 38
ws3.column_dimensions['O'].width = 38
ws3.column_dimensions['T'].width = 42
ws3.row_dimensions[5].height = 50
ws3.freeze_panes = 'D6'

# ============================================
# ABA 4: Consolidado 19 marcas onde CBH foi material
# ============================================
consolidado = []
# Step 1: passa+cluster
for r in rows:
    if r['CBH foi material? (contrib≥50% E cresceu)'] == 'SIM':
        consolidado.append({
            'Cluster': r['Cluster / Situação'],
            'Marca': r['Marca'], 'D1': r['D1'],
            'NMV pré (Mi)': r['NMV pré (R$ Mi)'],
            'NMV pós (Mi)': r['NMV pós (R$ Mi)'],
            'YoY (%)': r['YoY total (%)'],
            'YoY ex-CBH (%)': r['YoY ex-CBH (%)'],
            'Share CBH (%)': r['Share CBH (%)'],
            'Contrib CBH (%)': r['Contrib CBH (%)'],
            'Top pré': r['Top seller PRÉ'],
            'Top pós': r['Top seller PÓS'],
            'Step': '1 - Pareto geral'
        })
# Step 1.2: passa+cluster
for r in rows_s2:
    if r['CBH foi material?'] == 'SIM':
        consolidado.append({
            'Cluster': r['Cluster / Situação'],
            'Marca': r['Marca'], 'D1': r['D1'],
            'NMV pré (Mi)': r['NMV pré (R$ Mi)'],
            'NMV pós (Mi)': r['NMV pós (R$ Mi)'],
            'YoY (%)': r['YoY total (%)'],
            'YoY ex-CBH (%)': r['YoY ex-CBH (%)'],
            'Share CBH (%)': r['Share CBH (%)'],
            'Contrib CBH (%)': r['Contrib CBH (%)'],
            'Top pré': r['Top seller PRÉ'],
            'Top pós': r['Top seller PÓS'],
            'Step': '1.2 - Pareto CBH'
        })

df_cons = pd.DataFrame(consolidado).sort_values(['Cluster','NMV pós (Mi)'], ascending=[True,False])

ws4 = wb.create_sheet("Consolidado_19_marcas")
ws4['A1'] = "Consolidado — 19 marcas onde a CBH foi material (Steps 1 + 1.2)"
ws4['A1'].font = FONT_TITULO
ws4.merge_cells('A1:L1')
ws4['A2'] = "Universo HE (LA + TVs D2) | Período: ago-out/25 vs fev-abr/26 | Critério: YoY > 0% E Contrib CBH ≥ 50%"
ws4['A2'].font = FONT_SUB
ws4.merge_cells('A2:L2')

# Resumo por cluster no topo
ws4['A4'] = "Resumo por cluster:"
ws4['A4'].font = Font(name='Calibri', bold=True, size=11)
clusters_resumo = df_cons.groupby('Cluster').agg(Qt=('Marca','count'), NMV_pos_Mi=('NMV pós (Mi)','sum')).reset_index()
for c_idx, col in enumerate(['Cluster','Qt marcas','NMV pós agregado (Mi)'], start=1):
    cell = ws4.cell(row=5, column=c_idx, value=col)
    cell.font = FONT_HEADER; cell.fill = FILL_HEADER
    cell.alignment = Alignment(horizontal='center')
for r_idx, row in enumerate(clusters_resumo.itertuples(index=False), start=6):
    ws4.cell(row=r_idx, column=1, value=row[0]).font = FONT_BODY
    if row[0].startswith('A.'): ws4.cell(row=r_idx, column=1).fill = FILL_CLUSTER_A
    elif row[0].startswith('B.'): ws4.cell(row=r_idx, column=1).fill = FILL_CLUSTER_B
    elif row[0].startswith('C.'): ws4.cell(row=r_idx, column=1).fill = FILL_CLUSTER_C
    ws4.cell(row=r_idx, column=2, value=int(row[1])).font = FONT_BODY
    ws4.cell(row=r_idx, column=2).alignment = Alignment(horizontal='center')
    ws4.cell(row=r_idx, column=3, value=round(row[2],1)).font = FONT_BODY
    ws4.cell(row=r_idx, column=3).alignment = Alignment(horizontal='right')

# Tabela detalhada
detail_start = 11
ws4.cell(row=detail_start-1, column=1, value="Detalhe — 19 marcas:").font = Font(name='Calibri', bold=True, size=11)
for c_idx, col in enumerate(df_cons.columns, start=1):
    cell = ws4.cell(row=detail_start, column=c_idx, value=col)
    cell.font = FONT_HEADER; cell.fill = FILL_HEADER
    cell.alignment = Alignment(horizontal='center', wrap_text=True)
    cell.border = BORDER_THIN
for r_idx, row in enumerate(df_cons.itertuples(index=False), start=detail_start+1):
    for c_idx, val in enumerate(row, start=1):
        cell = ws4.cell(row=r_idx, column=c_idx, value=val)
        cell.font = FONT_BODY; cell.border = BORDER_THIN
        col_name = df_cons.columns[c_idx-1]
        if col_name == 'Cluster':
            if val.startswith('A.'): cell.fill = FILL_CLUSTER_A
            elif val.startswith('B.'): cell.fill = FILL_CLUSTER_B
            elif val.startswith('C.'): cell.fill = FILL_CLUSTER_C
        elif isinstance(val, (int, float)):
            cell.number_format = '#,##0.0'
            cell.alignment = Alignment(horizontal='right')

widths_cons = {'Cluster':32,'Marca':12,'D1':5,'NMV pré (Mi)':12,'NMV pós (Mi)':12,'YoY (%)':10,
               'YoY ex-CBH (%)':12,'Share CBH (%)':10,'Contrib CBH (%)':12,'Top pré':35,'Top pós':35,'Step':18}
for c_idx, col in enumerate(df_cons.columns, start=1):
    ws4.column_dimensions[get_column_letter(c_idx)].width = widths_cons.get(col, 12)

ws4.row_dimensions[detail_start].height = 50

# ============================================
# ABA 5: Step 2.1 — Trajetória antigos tops (Cluster A + C)
# ============================================
casos_step21 = [
    {'marca':'Colormaq', 'tname':'COLORVISÃO',
     'nmv_q1':13.66, 'nmv_q2':20.42, 'nmv_q3':11.91, 'nmv_pos':4.35,
     'tot_q1':16.42, 'tot_q2':23.79, 'tot_q3':16.93, 'tot_pos':20.41,
     'cbh_pos':11.13},
    {'marca':'Continental', 'tname':'OFICIALELECTROLUX',
     'nmv_q1':2.02, 'nmv_q2':2.80, 'nmv_q3':2.15, 'nmv_pos':1.21,
     'tot_q1':3.95, 'tot_q2':5.19, 'tot_q3':5.10, 'tot_pos':14.90,
     'cbh_pos':9.87},
    {'marca':'Esmaltec', 'tname':'MERCADO LIVRE ELETRONICOS (1P)',
     'nmv_q1':0.0, 'nmv_q2':2.00, 'nmv_q3':1.12, 'nmv_pos':0.0,
     'tot_q1':1.16, 'tot_q2':3.03, 'tot_q3':2.47, 'tot_pos':7.48,
     'cbh_pos':6.19},
    {'marca':'LG/LA', 'tname':'FASTSHOP OFICIAL',
     'nmv_q1':1.49, 'nmv_q2':3.98, 'nmv_q3':3.16, 'nmv_pos':1.02,
     'tot_q1':8.41, 'tot_q2':10.78, 'tot_q3':10.83, 'tot_pos':17.55,
     'cbh_pos':11.46},
    {'marca':'TCL/LA', 'tname':'MEGAMAMUTE FULLMG',
     'nmv_q1':0.0, 'nmv_q2':0.13, 'nmv_q3':0.33, 'nmv_pos':0.33,
     'tot_q1':0.0, 'tot_q2':0.14, 'tot_q3':0.33, 'tot_pos':1.57,
     'cbh_pos':1.20},
]

ws5 = wb.create_sheet("Step2.1_HistoricoAntigosTops")
ws5['A1'] = "Step 2.1 — Trajetória dos antigos tops vs CBH (Cluster A + C, todas em LA)"
ws5['A1'].font = FONT_TITULO
ws5.merge_cells('A1:M1')
ws5['A2'] = "Pergunta: a CBH desbancou sellers fortes ou ocupou vácuo de execução em marcas onde o top já caía?"
ws5['A2'].font = FONT_SUB
ws5.merge_cells('A2:M2')
ws5['A3'] = "Janelas trimestrais pré-CBH (Q1/25 jan-mar, Q2/25 abr-jun, Q3/25 jul-set) + POS (fev-abr/26). CBH entrou em nov/25."
ws5['A3'].font = FONT_SUB
ws5.merge_cells('A3:M3')

# TABELA 1: Trajetória do antigo top
ws5['A5'] = "TABELA 1 — Trajetória NMV do antigo top em cada trimestre (R$ Mi e % da marca)"
ws5['A5'].font = Font(name='Calibri', bold=True, size=11, color='1A1A1A')
ws5.merge_cells('A5:M5')

h1 = ['Marca/LA', 'Antigo top', 'Q1/25 NMV', 'Q1/25 %', 'Q2/25 NMV', 'Q2/25 %', 'Q3/25 NMV', 'Q3/25 %', 'POS NMV', 'POS %', 'Q1→Q2 %', 'Q2→Q3 %', 'Q3→POS %']
for c_idx, col in enumerate(h1, start=1):
    cell = ws5.cell(row=6, column=c_idx, value=col)
    cell.font = FONT_HEADER; cell.fill = FILL_HEADER
    cell.alignment = Alignment(horizontal='center', wrap_text=True)
    cell.border = BORDER_THIN

for r_idx, c in enumerate(casos_step21, start=7):
    s_q1 = c['nmv_q1']/c['tot_q1']*100 if c['tot_q1']>0 else 0
    s_q2 = c['nmv_q2']/c['tot_q2']*100 if c['tot_q2']>0 else 0
    s_q3 = c['nmv_q3']/c['tot_q3']*100 if c['tot_q3']>0 else 0
    s_pos = c['nmv_pos']/c['tot_pos']*100 if c['tot_pos']>0 else 0
    g_q1q2 = (c['nmv_q2']/c['nmv_q1']-1)*100 if c['nmv_q1']>0 else None
    g_q2q3 = (c['nmv_q3']/c['nmv_q2']-1)*100 if c['nmv_q2']>0 else None
    g_q3pos = (c['nmv_pos']/c['nmv_q3']-1)*100 if c['nmv_q3']>0 else None
    vals = [c['marca'], c['tname'],
            round(c['nmv_q1'],2), round(s_q1,1),
            round(c['nmv_q2'],2), round(s_q2,1),
            round(c['nmv_q3'],2), round(s_q3,1),
            round(c['nmv_pos'],2), round(s_pos,1),
            round(g_q1q2,0) if g_q1q2 is not None else 'N/A',
            round(g_q2q3,0) if g_q2q3 is not None else 'N/A',
            round(g_q3pos,0) if g_q3pos is not None else 'N/A']
    for c_idx, val in enumerate(vals, start=1):
        cell = ws5.cell(row=r_idx, column=c_idx, value=val)
        cell.font = FONT_BODY; cell.border = BORDER_THIN
        if isinstance(val, (int, float)):
            cell.number_format = '#,##0.0'
            cell.alignment = Alignment(horizontal='right')
            # Pinta vermelho se queda Q2→Q3 ou Q3→POS
            if c_idx in [12, 13] and val < 0:
                cell.font = Font(name='Calibri', size=10, color='C62828', bold=True)

# TABELA 2: Contribuição comparada
start2 = 7 + len(casos_step21) + 2
ws5.cell(row=start2, column=1, value="TABELA 2 — Contribuição comparada (% que cada player representa na marca)").font = Font(name='Calibri', bold=True, size=11, color='1A1A1A')
ws5.merge_cells(start_row=start2, start_column=1, end_row=start2, end_column=13)

h2 = ['Marca/LA', 'Antigo top', 'Antigo top Q3/25 (%)', 'Antigo top POS (%)', 'Variação top (p.p.)', 'CBH POS (%)']
for c_idx, col in enumerate(h2, start=1):
    cell = ws5.cell(row=start2+1, column=c_idx, value=col)
    cell.font = FONT_HEADER; cell.fill = FILL_HEADER
    cell.alignment = Alignment(horizontal='center', wrap_text=True)
    cell.border = BORDER_THIN

for r_idx, c in enumerate(casos_step21, start=start2+2):
    s_q3 = c['nmv_q3']/c['tot_q3']*100 if c['tot_q3']>0 else 0
    s_pos = c['nmv_pos']/c['tot_pos']*100 if c['tot_pos']>0 else 0
    s_cbh = c['cbh_pos']/c['tot_pos']*100
    var_top = s_pos - s_q3
    vals = [c['marca'], c['tname'], round(s_q3,1), round(s_pos,1), round(var_top,1), round(s_cbh,1)]
    for c_idx, val in enumerate(vals, start=1):
        cell = ws5.cell(row=r_idx, column=c_idx, value=val)
        cell.font = FONT_BODY; cell.border = BORDER_THIN
        if isinstance(val, (int, float)):
            cell.number_format = '#,##0.0'
            cell.alignment = Alignment(horizontal='right')
            if c_idx == 5 and val < 0:
                cell.font = Font(name='Calibri', size=10, color='C62828', bold=True)
            if c_idx == 6:
                cell.font = Font(name='Calibri', size=10, color='1A1A1A', bold=True)
                cell.fill = FILL_PASSA_SIM

# TABELA 3: Saldo absoluto
start3 = start2 + len(casos_step21) + 4
ws5.cell(row=start3, column=1, value="TABELA 3 — Saldo absoluto: o antigo top perdeu, mas a CBH compensou e adicionou").font = Font(name='Calibri', bold=True, size=11, color='1A1A1A')
ws5.merge_cells(start_row=start3, start_column=1, end_row=start3, end_column=13)

h3 = ['Marca/LA', 'Antigo top', 'Δ NMV antigo top Q3→POS (R$ Mi)', 'Δ NMV CBH 0→POS (R$ Mi)', 'Saldo líquido (R$ Mi)', 'Cresc marca Q3→POS (%)']
for c_idx, col in enumerate(h3, start=1):
    cell = ws5.cell(row=start3+1, column=c_idx, value=col)
    cell.font = FONT_HEADER; cell.fill = FILL_HEADER
    cell.alignment = Alignment(horizontal='center', wrap_text=True)
    cell.border = BORDER_THIN

total_delta_top = 0
total_delta_cbh = 0
for r_idx, c in enumerate(casos_step21, start=start3+2):
    delta_top = c['nmv_pos'] - c['nmv_q3']
    delta_cbh = c['cbh_pos']
    saldo = delta_cbh + delta_top
    cresc_marca = (c['tot_pos']/c['tot_q3']-1)*100 if c['tot_q3']>0 else 0
    total_delta_top += delta_top
    total_delta_cbh += delta_cbh
    vals = [c['marca'], c['tname'], round(delta_top,2), round(delta_cbh,2), round(saldo,2), round(cresc_marca,0)]
    for c_idx, val in enumerate(vals, start=1):
        cell = ws5.cell(row=r_idx, column=c_idx, value=val)
        cell.font = FONT_BODY; cell.border = BORDER_THIN
        if isinstance(val, (int, float)):
            cell.number_format = '#,##0.0'
            cell.alignment = Alignment(horizontal='right')
            if c_idx == 3 and val < 0:
                cell.font = Font(name='Calibri', size=10, color='C62828')
            if c_idx == 4:
                cell.font = Font(name='Calibri', size=10, color='2E7D32', bold=True)
            if c_idx == 5:
                cell.font = Font(name='Calibri', size=10, color='1A1A1A', bold=True)
                cell.fill = FILL_PASSA_SIM

# Linha TOTAL
total_row = start3+2+len(casos_step21)
saldo_total = total_delta_cbh + total_delta_top
ws5.cell(row=total_row, column=1, value="TOTAL (5 casos)").font = Font(name='Calibri', bold=True, size=10)
ws5.cell(row=total_row, column=1).fill = FILL_CLUSTER_B
ws5.cell(row=total_row, column=3, value=round(total_delta_top,2)).font = Font(name='Calibri', bold=True, size=10, color='C62828')
ws5.cell(row=total_row, column=3).number_format = '#,##0.0'
ws5.cell(row=total_row, column=3).alignment = Alignment(horizontal='right')
ws5.cell(row=total_row, column=4, value=round(total_delta_cbh,2)).font = Font(name='Calibri', bold=True, size=10, color='2E7D32')
ws5.cell(row=total_row, column=4).number_format = '#,##0.0'
ws5.cell(row=total_row, column=4).alignment = Alignment(horizontal='right')
ws5.cell(row=total_row, column=5, value=round(saldo_total,2)).font = Font(name='Calibri', bold=True, size=11, color='1A1A1A')
ws5.cell(row=total_row, column=5).fill = FILL_CLUSTER_A
ws5.cell(row=total_row, column=5).number_format = '#,##0.0'
ws5.cell(row=total_row, column=5).alignment = Alignment(horizontal='right')

# Insight box
ins_row = total_row + 3
ws5.cell(row=ins_row, column=1, value="INSIGHT-CHAVE — pra slide:").font = Font(name='Calibri', bold=True, size=11, color='1A1A1A')
ws5.merge_cells(start_row=ins_row, start_column=1, end_row=ins_row, end_column=13)
ws5.cell(row=ins_row+1, column=1, value="A CBH NÃO desbancou sellers fortes. Em 4 dos 5 casos, o antigo top já vinha perdendo volume no Q2→Q3/25 (antes da CBH entrar em nov/25): COLORVISÃO −42%, FASTSHOP −21%, 1P MELI/Esmaltec −44%, OFICIALELECTROLUX −23%. A CBH ocupou um VÁCUO DE EXECUÇÃO em marcas cujo líder vinha em queda.").font = Font(name='Calibri', size=10, color='1A1A1A')
ws5.merge_cells(start_row=ins_row+1, start_column=1, end_row=ins_row+1, end_column=13)
ws5.row_dimensions[ins_row+1].height = 50
ws5.cell(row=ins_row+1, column=1).alignment = Alignment(wrap_text=True, vertical='top')

ws5.cell(row=ins_row+3, column=1, value="SALDO LÍQUIDO: enquanto os 5 antigos tops perderam R$ 11,7 Mi de NMV, a CBH adicionou R$ 39,9 Mi nessas marcas — saldo positivo de +R$ 28,2 Mi pras marcas no MELI. Valeu a pena a CBH virar top.").font = Font(name='Calibri', size=10, italic=True, bold=True, color='1A1A1A')
ws5.merge_cells(start_row=ins_row+3, start_column=1, end_row=ins_row+3, end_column=13)
ws5.row_dimensions[ins_row+3].height = 40
ws5.cell(row=ins_row+3, column=1).alignment = Alignment(wrap_text=True, vertical='top')

# Larguras
ws5.column_dimensions['A'].width = 16
ws5.column_dimensions['B'].width = 35
for c_idx in range(3, 14):
    ws5.column_dimensions[get_column_letter(c_idx)].width = 14
ws5.row_dimensions[6].height = 40
ws5.row_dimensions[start2+1].height = 40
ws5.row_dimensions[start3+1].height = 40

# ============================================
# ABA 6: ASP CBH vs ex-CBH por D2
# ============================================
asp_data = [
    {'d2':'BUILT IN',                'asp_cbh':880,   'asp_excbh':607,   'nmv_cbh':36.2,  'nsi_cbh':41155,  'nmv_excbh':573.1, 'nsi_excbh':944431,
     'leitura':'CBH transita em ticket MAIS ALTO (+45%) — cooktops/fogões mais sofisticados (5+ bocas, recursos premium)'},
    {'d2':'LAUNDRY & DISHWASHERS',   'asp_cbh':1317,  'asp_excbh':1809,  'nmv_cbh':71.5,  'nsi_cbh':54245,  'nmv_excbh':366.8, 'nsi_excbh':202739,
     'leitura':'CBH transita em ticket MAIS BAIXO (-27%) — foco em lavadoras populares 11-13kg vs ex-CBH com lava-louças, secadoras, lavadoras 17kg+'},
    {'d2':'REFRIGERATION',           'asp_cbh':2960,  'asp_excbh':2278,  'nmv_cbh':86.5,  'nsi_cbh':29219,  'nmv_excbh':361.0, 'nsi_excbh':158431,
     'leitura':'CBH transita em ticket MAIS ALTO (+30%) — geladeiras frost-free média/alta vs cauda de mini-refrigeradores no ex-CBH'},
    {'d2':'TELEVISIONS',             'asp_cbh':2760,  'asp_excbh':1760,  'nmv_cbh':133.6, 'nsi_cbh':48413,  'nmv_excbh':722.1, 'nsi_excbh':410233,
     'leitura':'CBH transita em ticket MAIS ALTO (+57%) — foco em TVs 50-65"+ vs ex-CBH com volume em 32-43"'},
]

ws6 = wb.create_sheet("ASP_por_D2_CBHvs_exCBH")
ws6['A1'] = "ASP CBH vs ex-CBH por D2 — fev-abr/26 (Lente 2 pós)"
ws6['A1'].font = FONT_TITULO
ws6.merge_cells('A1:I1')
ws6['A2'] = "Pergunta: a CBH transita em tickets diferentes ou paira na média do MELI?"
ws6['A2'].font = FONT_SUB
ws6.merge_cells('A2:I2')
ws6['A3'] = "ASP = NMV ÷ NSI (preço médio por unidade vendida)"
ws6['A3'].font = FONT_SUB
ws6.merge_cells('A3:I3')

# Tabela principal
header_asp = ['D2', 'ASP CBH (R$)', 'ASP ex-CBH (R$)', 'Δ % (CBH vs ex-CBH)', 'NMV CBH (R$ Mi)', 'NSI CBH', 'NMV ex-CBH (R$ Mi)', 'NSI ex-CBH', 'Leitura']
for c_idx, col in enumerate(header_asp, start=1):
    cell = ws6.cell(row=5, column=c_idx, value=col)
    cell.font = FONT_HEADER; cell.fill = FILL_HEADER
    cell.alignment = Alignment(horizontal='center', wrap_text=True)
    cell.border = BORDER_THIN

for r_idx, a in enumerate(asp_data, start=6):
    delta_pct = (a['asp_cbh']/a['asp_excbh']-1)*100
    vals = [a['d2'], a['asp_cbh'], a['asp_excbh'], round(delta_pct,1),
            round(a['nmv_cbh'],1), a['nsi_cbh'], round(a['nmv_excbh'],1), a['nsi_excbh'], a['leitura']]
    for c_idx, val in enumerate(vals, start=1):
        cell = ws6.cell(row=r_idx, column=c_idx, value=val)
        cell.font = FONT_BODY; cell.border = BORDER_THIN
        if c_idx in [2,3,5,7]:
            cell.number_format = '#,##0'
            cell.alignment = Alignment(horizontal='right')
        elif c_idx == 4:
            cell.number_format = '+#,##0.0;-#,##0.0'
            cell.alignment = Alignment(horizontal='right', vertical='center')
            cell.font = Font(name='Calibri', bold=True, size=10,
                             color='2E7D32' if delta_pct > 0 else 'C62828')
            cell.fill = FILL_PASSA_SIM
        elif c_idx == 6 or c_idx == 8:
            cell.number_format = '#,##0'
            cell.alignment = Alignment(horizontal='right')
        elif c_idx == 9:
            cell.alignment = Alignment(wrap_text=True, vertical='top')

# Larguras
ws6.column_dimensions['A'].width = 24
for c in range(2, 9):
    ws6.column_dimensions[get_column_letter(c)].width = 15
ws6.column_dimensions['I'].width = 80
ws6.row_dimensions[5].height = 40
for r in range(6, 6+len(asp_data)):
    ws6.row_dimensions[r].height = 50

# Box insight
ins_row = 6 + len(asp_data) + 2
ws6.cell(row=ins_row, column=1, value="INSIGHT-CHAVE — pra slide:").font = Font(name='Calibri', bold=True, size=11, color='1A1A1A')
ws6.merge_cells(start_row=ins_row, start_column=1, end_row=ins_row, end_column=9)

ws6.cell(row=ins_row+1, column=1, value='A CBH NÃO opera na média do MELI: transita em tickets 30-57% acima do resto em Built In, Refrigeration e Televisions (foco em produtos médio-premium), e 27% abaixo em Laundry (foco em volume de produto popular). Não é cauda longa nem entry-level — é mid-to-premium nas categorias core.').font = Font(name='Calibri', size=10, italic=True, color='1A1A1A')
ws6.merge_cells(start_row=ins_row+1, start_column=1, end_row=ins_row+1, end_column=9)
ws6.row_dimensions[ins_row+1].height = 50
ws6.cell(row=ins_row+1, column=1).alignment = Alignment(wrap_text=True, vertical='top')

# Caveats
ws6.cell(row=ins_row+3, column=1, value="Caveats:").font = Font(name='Calibri', bold=True, size=10, color='1A1A1A')
ws6.cell(row=ins_row+4, column=1, value="· ASP é média ponderada — pode mascarar bimodalidade (ex: muitos itens muito baratos + alguns muito caros)").font = Font(name='Calibri', size=9, color='666666')
ws6.merge_cells(start_row=ins_row+4, start_column=1, end_row=ins_row+4, end_column=9)
ws6.cell(row=ins_row+5, column=1, value="· Diferença em Laundry pode ser efeito de mix de produto (CBH não vende lava-louças?) ou estratégia de preço — vale validar com auditoria do catálogo se for usar essa narrativa.").font = Font(name='Calibri', size=9, color='666666')
ws6.merge_cells(start_row=ins_row+5, start_column=1, end_row=ins_row+5, end_column=9)
ws6.row_dimensions[ins_row+5].height = 30
ws6.cell(row=ins_row+5, column=1).alignment = Alignment(wrap_text=True, vertical='top')

wb.save(TARGET)
print(f"OK: {TARGET}")
print(f"Tamanho: {TARGET.stat().st_size/1024:.0f} KB")
print(f"Abas: {wb.sheetnames}")

# Também exporta CSV pra processamento
df.to_csv(OUT / "Pergunta1_25marcas_LA_TVs.csv", sep=';', decimal=',', encoding='utf-8-sig', index=False)
df_s2.to_csv(OUT / "Pergunta1_step1_2_7marcas_novas.csv", sep=';', decimal=',', encoding='utf-8-sig', index=False)
df_cons.to_csv(OUT / "Pergunta1_consolidado_19marcas.csv", sep=';', decimal=',', encoding='utf-8-sig', index=False)
print(f"3 CSVs exportados")
