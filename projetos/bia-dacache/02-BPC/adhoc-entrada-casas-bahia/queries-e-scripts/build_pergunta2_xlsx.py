"""Gera XLSX da Pergunta 2 — Regionalização (LA + TVs)."""
import pandas as pd
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE = Path(r"C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-05-entrada-cbh-incrementalidade-regional")
OUT = BASE / "outputs"
TARGET = OUT / "Pergunta2_Regional_LA_TVs.xlsx"

FONT_TITULO = Font(name='Calibri', bold=True, size=14, color='1A1A1A')
FONT_SUB = Font(name='Calibri', italic=True, size=10, color='555555')
FONT_HEADER = Font(name='Calibri', bold=True, size=10, color='FFFFFF')
FONT_BODY = Font(name='Calibri', size=10, color='1A1A1A')
FILL_HEADER = PatternFill('solid', fgColor='1A1A1A')
FILL_HIGHLIGHT = PatternFill('solid', fgColor='FFE600')
FILL_SOFT = PatternFill('solid', fgColor='FFF59D')
FILL_GREY = PatternFill('solid', fgColor='F5F5F5')
BORDER_THIN = Border(
    left=Side(style='thin', color='CCCCCC'),
    right=Side(style='thin', color='CCCCCC'),
    top=Side(style='thin', color='CCCCCC'),
    bottom=Side(style='thin', color='CCCCCC'))

wb = Workbook()

# ===========================================
# ABA 1: Tabela final por região (LA + TVs)
# ===========================================
ws = wb.active
ws.title = "Regional_LA_TVs"

ws['A1'] = "Pergunta 2 — Em quais regiões a CBH mais contribuiu? (LA + TVs · fev-abr/26 vs ago-out/25)"
ws['A1'].font = FONT_TITULO
ws.merge_cells('A1:J1')
ws['A2'] = "Período pré: ago-out/25 (sem CBH) | Período pós: fev-abr/26 (com CBH) | Universo: LA + TVs (D2=TELEVISIONS)"
ws['A2'].font = FONT_SUB
ws.merge_cells('A2:J2')

# Dados das 5 regiões
regional = [
    {'reg':'N',  'pre':47.2,   'pos':65.3,   'cbh':15.9,  'delta_tot':38.3, 'delta_excbh':4.7,  'contrib':33.6, 'share':24.3,
     'la_pos':'#1 (25,9%)', 'la_top':'CBH lidera',
     'tvs_pos':'#2 (21,9%)', 'tvs_top':'1P MELI #1 (26,6%)'},
    {'reg':'NE', 'pre':317.7,  'pos':406.6,  'cbh':81.7,  'delta_tot':28.0, 'delta_excbh':2.3,  'contrib':25.7, 'share':20.1,
     'la_pos':'#1 (25,0%)', 'la_top':'⚠️ empate técnico c/ 1P MELI (24,8%)',
     'tvs_pos':'#3 (14,2%)', 'tvs_top':'1P MELI #1 (29,1%)'},
    {'reg':'CO', 'pre':122.4,  'pos':149.5,  'cbh':24.7,  'delta_tot':22.1, 'delta_excbh':1.9,  'contrib':20.2, 'share':16.5,
     'la_pos':'#2 (14,8%)', 'la_top':'1P MELI #1 (24,7%)',
     'tvs_pos':'#2 (19,9%)', 'tvs_top':'1P MELI #1 (26,6%)'},
    {'reg':'SE', 'pre':1178.7, 'pos':1361.2, 'cbh':169.4, 'delta_tot':15.5, 'delta_excbh':1.1,  'contrib':14.4, 'share':12.4,
     'la_pos':'#2 (10,6%)', 'la_top':'1P MELI #1 (35,9%)',
     'tvs_pos':'#3 (16,0%)', 'tvs_top':'1P MELI #1 (28,3%)'},
    {'reg':'S',  'pre':336.1,  'pos':361.7,  'cbh':36.2,  'delta_tot':7.6,  'delta_excbh':-3.2, 'contrib':10.8, 'share':10.0,
     'la_pos':'#2 (8,2%)', 'la_top':'1P MELI #1 (31,2%)',
     'tvs_pos':'#3 (13,4%)', 'tvs_top':'1P MELI #1 (28,7%)'},
]

headers = ['Região', 'NMV pré (R$ Mi)', 'NMV pós (R$ Mi)', 'Δ total (%)', 'Δ ex-CBH (%)', 'Contrib CBH (pp)', 'Share CBH (%)', 'Pos. CBH em LA', 'Top vendor LA', 'Pos. CBH em TVs', 'Top vendor TVs']
for c_idx, col in enumerate(headers, start=1):
    cell = ws.cell(row=4, column=c_idx, value=col)
    cell.font = FONT_HEADER; cell.fill = FILL_HEADER
    cell.alignment = Alignment(horizontal='center', wrap_text=True)
    cell.border = BORDER_THIN

for r_idx, r in enumerate(regional, start=5):
    vals = [r['reg'], r['pre'], r['pos'], r['delta_tot'], r['delta_excbh'], r['contrib'], r['share'],
            r['la_pos'], r['la_top'], r['tvs_pos'], r['tvs_top']]
    for c_idx, val in enumerate(vals, start=1):
        cell = ws.cell(row=r_idx, column=c_idx, value=val)
        cell.font = FONT_BODY; cell.border = BORDER_THIN
        if c_idx == 1:
            cell.font = Font(name='Calibri', bold=True, size=11, color='1A1A1A')
            cell.alignment = Alignment(horizontal='center', vertical='center')
        elif isinstance(val, (int, float)):
            cell.number_format = '#,##0.0'
            cell.alignment = Alignment(horizontal='right')
            if c_idx == 5 and val < 0:
                cell.font = Font(name='Calibri', size=10, color='C62828', bold=True)
            elif c_idx == 6:
                cell.fill = FILL_HIGHLIGHT
                cell.font = Font(name='Calibri', size=10, color='1A1A1A', bold=True)
        elif c_idx == 8 and val.startswith('#1'):
            cell.fill = FILL_HIGHLIGHT
            cell.font = Font(name='Calibri', size=10, color='1A1A1A', bold=True)

# Larguras
widths = [10, 15, 15, 12, 13, 14, 12, 16, 32, 16, 32]
for c_idx, w in enumerate(widths, start=1):
    ws.column_dimensions[get_column_letter(c_idx)].width = w
ws.row_dimensions[4].height = 40

# Insight box
ins_row = 11
ws.cell(row=ins_row, column=1, value="INSIGHTS-CHAVE:").font = Font(name='Calibri', bold=True, size=11, color='1A1A1A')
ws.merge_cells(start_row=ins_row, start_column=1, end_row=ins_row, end_column=11)

insights = [
    "1. CBH é #1 vendor em LA no Norte (25,9%) e Nordeste (25%, empate com 1P MELI) — exatamente as 2 regiões onde mais contribuiu (+33,6 pp / +25,7 pp).",
    "2. Em TVs, 1P MELI lidera em todas as 5 regiões (26-29%) — CBH NÃO destrona em TVs em região nenhuma.",
    "3. No Sul, ex-CBH caiu -3,2% em LA+TVs — único caso de queda orgânica. Toda a contribuição veio da CBH.",
    "4. Em Centro-Oeste e Sudeste, CBH é #2 em LA mas com share moderado (14-15%) — coexistência com 1P MELI dominante.",
]
for i, ins in enumerate(insights):
    ws.cell(row=ins_row+1+i, column=1, value=ins).font = Font(name='Calibri', size=10, color='1A1A1A')
    ws.merge_cells(start_row=ins_row+1+i, start_column=1, end_row=ins_row+1+i, end_column=11)
    ws.row_dimensions[ins_row+1+i].height = 25
    ws.cell(row=ins_row+1+i, column=1).alignment = Alignment(wrap_text=True, vertical='center')

# Frase pra slide
ws.cell(row=ins_row+6, column=1, value="FRASE PRA SLIDE:").font = Font(name='Calibri', bold=True, size=11, color='1A1A1A')
ws.merge_cells(start_row=ins_row+6, start_column=1, end_row=ins_row+6, end_column=11)

ws.cell(row=ins_row+7, column=1, value='"A CBH é #1 vendor em Large Appliances no Norte e Nordeste — as 2 regiões onde também mais contribuiu pro crescimento (+33,6 pp e +25,7 pp). Em Televisions, o 1P MELI continua líder em todas as regiões e a CBH ocupa #2 ou #3. Em Large Appliances, a presença da CBH é estratégica: domina onde mais agrega."').font = Font(name='Calibri', size=10, italic=True, color='1A1A1A')
ws.merge_cells(start_row=ins_row+7, start_column=1, end_row=ins_row+7, end_column=11)
ws.row_dimensions[ins_row+7].height = 60
ws.cell(row=ins_row+7, column=1).alignment = Alignment(wrap_text=True, vertical='top')

# Caveats
ws.cell(row=ins_row+9, column=1, value="Caveats metodológicos:").font = Font(name='Calibri', bold=True, size=10, color='1A1A1A')
ws.cell(row=ins_row+10, column=1, value="· Lente 2 (3m pré vs 3m pós, mesmo ano) — diferente da Lente 1 YoY usada na Pergunta 1. YoY (fev-abr/26 vs fev-abr/25) HE BR total é +40,6%; Lente 2 é +13,5%. Ambas válidas, recortes diferentes.").font = Font(name='Calibri', size=9, color='666666')
ws.merge_cells(start_row=ins_row+10, start_column=1, end_row=ins_row+10, end_column=11)
ws.row_dimensions[ins_row+10].height = 30
ws.cell(row=ins_row+10, column=1).alignment = Alignment(wrap_text=True, vertical='top')

ws.cell(row=ins_row+11, column=1, value="· Ex-CBH 'quase retraindo' em LA+TVs é normal e específico desse recorte: a CBH 'engole' bastante volume nessas D1s. Em HE total agregado, ex-CBH cresce entre +3-13% nas regiões.").font = Font(name='Calibri', size=9, color='666666')
ws.merge_cells(start_row=ins_row+11, start_column=1, end_row=ins_row+11, end_column=11)
ws.row_dimensions[ins_row+11].height = 30
ws.cell(row=ins_row+11, column=1).alignment = Alignment(wrap_text=True, vertical='top')

# ===========================================
# ABA 2: Marca × Região × LA (13 marcas × 5 regiões = 65 linhas)
# ===========================================
ws2 = wb.create_sheet("Marca_x_Regiao_LA")
ws2['A1'] = "Marca × Região × LA — Lente 2 (ago-out/25 vs fev-abr/26)"
ws2['A1'].font = FONT_TITULO
ws2.merge_cells('A1:K1')
ws2['A2'] = "13 marcas Cluster A+B+C em LA × 5 regiões. Ordenado por região e NMV pós."
ws2['A2'].font = FONT_SUB
ws2.merge_cells('A2:K2')

cluster_map = {
    'Colormaq':'A','LG':'A','Continental':'A','Esmaltec':'A',
    'Electrolux':'B','Brastemp':'B','Consul':'B','Midea':'B',
    'Atlas':'B','Suggar':'B','Britania':'B','Hisense':'B',
    'TCL':'C'
}

# Dados regionais (mesma lista do PowerShell anterior)
dados_marca_regiao = [
    ('N','Electrolux',5.68,8.23,2.40,5.83),
    ('N','Brastemp',3.20,4.91,1.47,3.43),
    ('N','Consul',1.48,3.94,1.97,1.97),
    ('N','Midea',2.95,3.68,0.54,3.14),
    ('N','Atlas',0.46,1.06,0.43,0.62),
    ('N','Suggar',0.74,0.97,0.10,0.87),
    ('N','Britania',0.28,0.75,0.41,0.34),
    ('N','Continental',0.11,0.63,0.53,0.10),
    ('N','LG',0.18,0.58,0.49,0.09),
    ('N','Colormaq',0.10,0.55,0.51,0.05),
    ('N','Esmaltec',0.03,0.45,0.43,0.01),
    ('N','Hisense',0.14,0.32,0.12,0.20),
    ('N','TCL',0.01,0.11,0.10,0.01),
    ('NE','Electrolux',29.09,39.86,9.45,30.40),
    ('NE','Consul',22.67,38.20,13.87,24.33),
    ('NE','Brastemp',27.75,31.32,8.69,22.63),
    ('NE','Midea',11.99,16.43,3.83,12.60),
    ('NE','Atlas',2.74,5.73,1.90,3.83),
    ('NE','Suggar',4.09,4.56,0.57,3.99),
    ('NE','Colormaq',1.05,4.41,3.54,0.87),
    ('NE','Britania',2.72,4.08,1.57,2.50),
    ('NE','Continental',0.71,2.81,2.20,0.61),
    ('NE','Esmaltec',0.39,2.53,2.33,0.20),
    ('NE','LG',0.60,2.40,2.02,0.38),
    ('NE','Hisense',0.95,1.51,0.46,1.05),
    ('NE','TCL',0.04,0.31,0.28,0.04),
    ('CO','Electrolux',15.15,19.11,3.44,15.67),
    ('CO','Brastemp',12.92,15.96,2.97,13.00),
    ('CO','Midea',6.95,8.38,1.00,7.38),
    ('CO','Consul',4.77,7.94,2.08,5.87),
    ('CO','Suggar',2.24,2.21,0.13,2.08),
    ('CO','Atlas',1.21,1.92,0.45,1.47),
    ('CO','LG',0.90,1.54,0.95,0.59),
    ('CO','Colormaq',0.52,1.15,0.76,0.39),
    ('CO','Britania',0.87,1.06,0.32,0.74),
    ('CO','Hisense',0.69,0.77,0.20,0.56),
    ('CO','Continental',0.23,0.75,0.52,0.23),
    ('CO','Esmaltec',0.06,0.34,0.31,0.03),
    ('CO','TCL',0.03,0.11,0.10,0.01),
    ('SE','Electrolux',201.28,227.86,21.79,206.06),
    ('SE','Brastemp',105.95,133.97,13.94,120.03),
    ('SE','Consul',69.41,104.77,15.88,88.89),
    ('SE','Midea',57.07,67.14,6.22,60.92),
    ('SE','Suggar',16.66,17.85,1.52,16.33),
    ('SE','Atlas',16.23,17.44,3.15,14.29),
    ('SE','Colormaq',10.14,13.22,5.87,7.35),
    ('SE','Hisense',7.35,10.85,1.04,9.81),
    ('SE','LG',7.12,9.49,6.23,3.27),
    ('SE','Continental',3.88,9.34,5.84,3.50),
    ('SE','Britania',9.00,8.10,2.46,5.64),
    ('SE','Esmaltec',1.76,3.75,2.82,0.94),
    ('SE','TCL',0.20,0.69,0.48,0.21),
    ('S','Electrolux',49.13,53.31,4.66,48.65),
    ('S','Brastemp',25.24,28.41,3.18,25.22),
    ('S','Consul',15.96,22.99,3.34,19.65),
    ('S','Midea',17.00,21.42,1.70,19.73),
    ('S','Suggar',4.65,4.56,0.13,4.43),
    ('S','Atlas',3.57,4.50,0.54,3.96),
    ('S','Britania',3.31,3.74,0.56,3.19),
    ('S','LG',2.96,3.15,1.78,1.37),
    ('S','Hisense',2.70,2.44,0.24,2.20),
    ('S','Continental',0.59,1.33,0.77,0.56),
    ('S','Colormaq',0.90,1.07,0.45,0.61),
    ('S','Esmaltec',0.19,0.40,0.30,0.10),
    ('S','TCL',0.08,0.35,0.25,0.10),
]

# Cluster fill por linha
FILL_A = PatternFill('solid', fgColor='F9A825')
FILL_B = PatternFill('solid', fgColor='FFF59D')
FILL_C = PatternFill('solid', fgColor='9A7D0A')

headers2 = ['Região', 'Marca', 'Cluster', 'NMV pré (Mi)', 'NMV pós (Mi)', 'Δ total (%)', 'NMV pós ex-CBH (Mi)', 'Δ ex-CBH (%)', 'NMV CBH (Mi)', 'Share CBH (%)', 'Contrib CBH (pp)']
for c_idx, col in enumerate(headers2, start=1):
    cell = ws2.cell(row=4, column=c_idx, value=col)
    cell.font = FONT_HEADER; cell.fill = FILL_HEADER
    cell.alignment = Alignment(horizontal='center', wrap_text=True)
    cell.border = BORDER_THIN

ordemReg = ['N','NE','CO','SE','S']
sorted_data = sorted(dados_marca_regiao, key=lambda x: (ordemReg.index(x[0]), -x[3]))

for r_idx, (reg, m, pre, pos, cbh, excbh) in enumerate(sorted_data, start=5):
    cl = cluster_map[m]
    delta_tot = (pos/pre-1)*100 if pre > 0 else 0
    delta_excbh = (excbh/pre-1)*100 if pre > 0 else 0
    share = cbh/pos*100 if pos > 0 else 0
    contrib = delta_tot - delta_excbh
    vals = [reg, m, cl, pre, pos, round(delta_tot,1), excbh, round(delta_excbh,1), cbh, round(share,1), round(contrib,1)]
    for c_idx, val in enumerate(vals, start=1):
        cell = ws2.cell(row=r_idx, column=c_idx, value=val)
        cell.font = FONT_BODY; cell.border = BORDER_THIN
        if c_idx == 3:
            if cl == 'A': cell.fill = FILL_A
            elif cl == 'B': cell.fill = FILL_B
            elif cl == 'C': cell.fill = FILL_C
            cell.alignment = Alignment(horizontal='center')
            cell.font = Font(name='Calibri', bold=True, size=10, color='1A1A1A')
        elif isinstance(val, (int, float)):
            cell.number_format = '#,##0.00' if c_idx in [4,5,7,9] else '#,##0.0'
            cell.alignment = Alignment(horizontal='right')
            if c_idx == 8 and val < 0:
                cell.font = Font(name='Calibri', size=10, color='C62828')

widths2 = [8,12,9,13,13,11,15,12,12,12,14]
for c_idx, w in enumerate(widths2, start=1):
    ws2.column_dimensions[get_column_letter(c_idx)].width = w
ws2.row_dimensions[4].height = 40
ws2.freeze_panes = 'D5'

# ===========================================
# ABA 3: Resumo Cluster x Região
# ===========================================
ws3 = wb.create_sheet("Cluster_x_Regiao")
ws3['A1'] = "Composição NMV CBH em LA — Cluster Estrutural (B) vs Dominadas (A) vs TCL (C) por região"
ws3['A1'].font = FONT_TITULO
ws3.merge_cells('A1:H1')
ws3['A2'] = "Resposta direta: 75-80% do volume CBH em LA vem de marcas estruturais em TODAS as regiões."
ws3['A2'].font = FONT_SUB
ws3.merge_cells('A2:H2')

dados_cluster_reg = [
    ('N', 9.51, 1.96, 7.46, 0.10),
    ('NE', 50.72, 10.10, 40.35, 0.28),
    ('CO', 13.23, 2.54, 10.59, 0.10),
    ('SE', 87.23, 20.75, 65.99, 0.48),
    ('S', 17.92, 3.30, 14.36, 0.25),
]
headers3 = ['Região', 'NMV CBH Total (Mi)', 'NMV A (Mi)', 'NMV B (Mi)', 'NMV C (Mi)', '% A (dominadas)', '% B (estrutural)', '% C']
for c_idx, col in enumerate(headers3, start=1):
    cell = ws3.cell(row=4, column=c_idx, value=col)
    cell.font = FONT_HEADER; cell.fill = FILL_HEADER
    cell.alignment = Alignment(horizontal='center', wrap_text=True)
    cell.border = BORDER_THIN

for r_idx, (reg, tot, a, b, c) in enumerate(dados_cluster_reg, start=5):
    pct_a = a/tot*100
    pct_b = b/tot*100
    pct_c = c/tot*100
    vals = [reg, tot, a, b, c, round(pct_a,1), round(pct_b,1), round(pct_c,1)]
    for c_idx, val in enumerate(vals, start=1):
        cell = ws3.cell(row=r_idx, column=c_idx, value=val)
        cell.font = FONT_BODY; cell.border = BORDER_THIN
        if c_idx == 1:
            cell.font = Font(name='Calibri', bold=True, size=11)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        elif isinstance(val, (int, float)):
            cell.number_format = '#,##0.0'
            cell.alignment = Alignment(horizontal='right')
            if c_idx == 6: cell.fill = FILL_A
            elif c_idx == 7:
                cell.fill = FILL_B
                cell.font = Font(name='Calibri', bold=True, size=10, color='1A1A1A')
            elif c_idx == 8: cell.fill = FILL_C

widths3 = [10, 18, 12, 12, 12, 16, 17, 10]
for c_idx, w in enumerate(widths3, start=1):
    ws3.column_dimensions[get_column_letter(c_idx)].width = w
ws3.row_dimensions[4].height = 40

# ===========================================
# ABA 4: Liderança CBH em LA por marca×região
# ===========================================
ws4 = wb.create_sheet("Lideranca_CBH_LA")
ws4['A1'] = "Liderança CBH em LA — em quantas marcas a CBH é #1 vendor por região?"
ws4['A1'].font = FONT_TITULO
ws4.merge_cells('A1:G1')
ws4['A2'] = "CBH é #1 em marcas Cluster B SOMENTE no Norte (Atlas 41%, Britania 55%, Consul 50%)."
ws4['A2'].font = FONT_SUB
ws4.merge_cells('A2:G2')

# Tabela 1: top vendor por marca×região
ws4['A4'] = "TABELA 1 — Top vendor por marca × região (Cluster B)"
ws4['A4'].font = Font(name='Calibri', bold=True, size=11)
ws4.merge_cells('A4:G4')

marca_top = [
    ('Atlas', 'CBH (41%)','MEGAMAMUTE','MEGAMAMUTE','MEGAMAMUTE','MEGAMAMUTE'),
    ('Brastemp', 'BUDCOM','BUDCOM','BUDCOM','1P MELI','1P MELI'),
    ('Britania', 'CBH (55%)','1P MELI','1P MELI','1P MELI','1P MELI'),
    ('Consul', 'CBH (50%)','BUDCOM','BUDCOM','1P MELI','1P MELI'),
    ('Electrolux', '1P MELI','1P MELI','1P MELI','1P MELI','1P MELI'),
    ('Hisense', '1P MELI','1P MELI','1P MELI','1P MELI','1P MELI'),
    ('Midea', 'MIDEA STORE','MIDEA STORE','MIDEA STORE','1P MELI','1P MELI'),
    ('Suggar', 'XCOMM.','XCOMM.','XCOMM.','XCOMM.','XCOMM.'),
]
headers4 = ['Marca (B)', 'N', 'NE', 'CO', 'SE', 'S']
for c_idx, col in enumerate(headers4, start=1):
    cell = ws4.cell(row=5, column=c_idx, value=col)
    cell.font = FONT_HEADER; cell.fill = FILL_HEADER
    cell.alignment = Alignment(horizontal='center')
    cell.border = BORDER_THIN

for r_idx, (m, n, ne, co, se, s) in enumerate(marca_top, start=6):
    vals = [m, n, ne, co, se, s]
    for c_idx, val in enumerate(vals, start=1):
        cell = ws4.cell(row=r_idx, column=c_idx, value=val)
        cell.font = FONT_BODY; cell.border = BORDER_THIN
        cell.alignment = Alignment(horizontal='center')
        if c_idx == 1:
            cell.font = Font(name='Calibri', bold=True, size=10)
            cell.alignment = Alignment(horizontal='left')
        elif 'CBH' in str(val):
            cell.fill = FILL_HIGHLIGHT
            cell.font = Font(name='Calibri', bold=True, size=10, color='1A1A1A')

for c_idx in range(1, 7):
    ws4.column_dimensions[get_column_letter(c_idx)].width = 15
ws4.column_dimensions['A'].width = 16

# Tabela 2: quadro geral de liderança CBH em LA
start_t2 = 6 + len(marca_top) + 2
ws4.cell(row=start_t2, column=1, value="TABELA 2 — Em quantas marcas a CBH é #1 vendor em LA, por região?").font = Font(name='Calibri', bold=True, size=11)
ws4.merge_cells(start_row=start_t2, start_column=1, end_row=start_t2, end_column=7)

quadro = [
    ('N', 8, 'Colormaq, LG, Continental, Esmaltec, TCL · Atlas, Britania, Consul'),
    ('NE', 5, 'Colormaq, LG, Continental, Esmaltec, TCL'),
    ('CO', 5, 'Colormaq, LG, Continental, Esmaltec, TCL'),
    ('SE', 5, 'Colormaq, LG, Continental, Esmaltec, TCL'),
    ('S', 5, 'Colormaq, LG, Continental, Esmaltec, TCL'),
]
headers_q = ['Região', 'Qt marcas onde CBH é #1', 'Marcas']
for c_idx, col in enumerate(headers_q, start=1):
    cell = ws4.cell(row=start_t2+1, column=c_idx, value=col)
    cell.font = FONT_HEADER; cell.fill = FILL_HEADER
    cell.alignment = Alignment(horizontal='center')
    cell.border = BORDER_THIN
ws4.merge_cells(start_row=start_t2+1, start_column=3, end_row=start_t2+1, end_column=7)

for r_idx, (reg, qt, marcas) in enumerate(quadro, start=start_t2+2):
    ws4.cell(row=r_idx, column=1, value=reg).font = Font(name='Calibri', bold=True, size=10)
    ws4.cell(row=r_idx, column=1).alignment = Alignment(horizontal='center', vertical='center')
    ws4.cell(row=r_idx, column=2, value=qt).font = FONT_BODY
    ws4.cell(row=r_idx, column=2).alignment = Alignment(horizontal='center')
    if qt == 8:
        ws4.cell(row=r_idx, column=2).fill = FILL_HIGHLIGHT
        ws4.cell(row=r_idx, column=2).font = Font(name='Calibri', bold=True, size=11, color='1A1A1A')
    cell_m = ws4.cell(row=r_idx, column=3, value=marcas)
    cell_m.font = FONT_BODY
    ws4.merge_cells(start_row=r_idx, start_column=3, end_row=r_idx, end_column=7)
    for c in range(1, 8):
        ws4.cell(row=r_idx, column=c).border = BORDER_THIN

# ===========================================
# ABA 5: Insights
# ===========================================
ws5 = wb.create_sheet("Insights")
ws5['A1'] = "Insights consolidados — Pergunta 2 (Regionalização LA+TVs)"
ws5['A1'].font = FONT_TITULO
ws5.merge_cells('A1:C1')

insights_finais = [
    ('Insight 1', 'Top 3 regiões onde CBH mais contribuiu', 'N (+33,6 pp), NE (+25,7 pp), CO (+20,2 pp). Em LA+TVs (categorias core), efeito é 2-2,6x mais intenso que em HE total.'),
    ('Insight 2', 'PA é a UF mais transformada pela CBH', 'Contribuição CBH ao YoY do PA em LA+TVs: +43,5 pp (de +45% total). PA = 51% do NMV Norte.'),
    ('Insight 3', 'Sul é o único caso onde ex-CBH caiu em LA+TVs', 'Ex-CBH no Sul: -3,2%. Toda contribuição veio da CBH (+10,8 pp).'),
    ('Insight 4', '75-80% do NMV CBH em LA vem de marcas estruturais em todas as regiões', 'Pattern uniforme: Cluster B (Electrolux, Brastemp, Consul, Midea, Atlas, Suggar, Britania, Hisense) = 75-80% em qualquer região. Cluster A (dominadas) = 18-24%.'),
    ('Insight 5', 'Esmaltec é praticamente CBH-only no Norte', 'Share CBH na marca: Esmaltec/N 97% · Colormaq/N 92% · LG/N 84% · Continental/N 84%. Marcas Cluster A são CBH-only nas regiões periféricas.'),
    ('Insight 6', 'Norte é o único caso onde CBH lidera marcas estruturais', 'CBH é #1 vendor em LA no Norte para Atlas (41%), Britania (55%) e Consul (50%) — além das 5 marcas Cluster A+C. Total: 8 marcas. Nas outras regiões, lidera apenas 5 (só as Cluster A+C).'),
    ('Insight 7', 'CBH não é líder em TVs em região nenhuma', '1P MELI lidera Televisions em todas as 5 regiões (26-29% share). CBH ocupa #2 ou #3.'),
    ('Insight 8', 'Mesmo mix de marcas, dominância seletiva no Norte', 'A CBH não regionalizou um mix diferente — leva as mesmas marcas estruturais a todas regiões. A diferença é que no Norte ela tem share muito maior nessas marcas, porque outros sellers (1P MELI, BUDCOM, MIDEA STORE) estão concentrados em SE.'),
]

ws5.cell(row=3, column=1, value="#").font = FONT_HEADER
ws5.cell(row=3, column=1).fill = FILL_HEADER
ws5.cell(row=3, column=2, value="Insight").font = FONT_HEADER
ws5.cell(row=3, column=2).fill = FILL_HEADER
ws5.cell(row=3, column=3, value="Detalhe / Frase pra slide").font = FONT_HEADER
ws5.cell(row=3, column=3).fill = FILL_HEADER

for r_idx, (n, t, d) in enumerate(insights_finais, start=4):
    ws5.cell(row=r_idx, column=1, value=n).font = Font(name='Calibri', bold=True, size=10)
    ws5.cell(row=r_idx, column=2, value=t).font = Font(name='Calibri', bold=True, size=10, color='1A1A1A')
    ws5.cell(row=r_idx, column=3, value=d).font = Font(name='Calibri', size=10)
    ws5.cell(row=r_idx, column=2).alignment = Alignment(wrap_text=True, vertical='top')
    ws5.cell(row=r_idx, column=3).alignment = Alignment(wrap_text=True, vertical='top')
    ws5.row_dimensions[r_idx].height = 50
    for c in range(1, 4):
        ws5.cell(row=r_idx, column=c).border = BORDER_THIN
    if 'Norte' in t or 'Norte' in d:
        ws5.cell(row=r_idx, column=2).fill = FILL_HIGHLIGHT

ws5.column_dimensions['A'].width = 12
ws5.column_dimensions['B'].width = 50
ws5.column_dimensions['C'].width = 90

# Frase mestre
ws5.cell(row=len(insights_finais)+5, column=1, value="FRASE MESTRE PRA SLIDE:").font = Font(name='Calibri', bold=True, size=11)
ws5.merge_cells(start_row=len(insights_finais)+5, start_column=1, end_row=len(insights_finais)+5, end_column=3)
frase = '"A CBH puxou 75-80% do seu volume em LA com marcas estruturais consolidadas (Electrolux, Brastemp, Consul, Midea) — o mesmo mix em todas as regiões. A diferença é que no Norte ela é #1 vendor em 8 marcas (Cluster A+C + 3 estruturais: Atlas, Britania, Consul), enquanto nas outras regiões lidera apenas as 5 dominadas. Não regionalizou um mix diferente — capilarizou as mesmas marcas onde os outros sellers não chegavam."'
ws5.cell(row=len(insights_finais)+6, column=1, value=frase).font = Font(name='Calibri', italic=True, size=10, color='1A1A1A')
ws5.merge_cells(start_row=len(insights_finais)+6, start_column=1, end_row=len(insights_finais)+6, end_column=3)
ws5.row_dimensions[len(insights_finais)+6].height = 80
ws5.cell(row=len(insights_finais)+6, column=1).alignment = Alignment(wrap_text=True, vertical='top')

wb.save(TARGET)
print(f"OK: {TARGET}")
print(f"Tamanho: {TARGET.stat().st_size/1024:.0f} KB")
print(f"Abas: {wb.sheetnames}")
