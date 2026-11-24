"""Gera XLSX master da análise CBH HE — 8 abas."""
import pandas as pd
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
from pathlib import Path

BASE = Path(r"C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-05-entrada-cbh-incrementalidade-regional")
OUT = BASE / "outputs"
TARGET = OUT / "ANALISE_CBH_HE_master.xlsx"

# --- Estilos ---
FONT_HEADER = Font(name='Arial', bold=True, color='FFFFFF', size=11)
FONT_TITULO = Font(name='Arial', bold=True, size=14, color='2E4A7B')
FONT_KPI_NUM = Font(name='Arial', bold=True, size=20, color='2E4A7B')
FONT_KPI_LABEL = Font(name='Arial', size=10, color='666666')
FONT_BODY = Font(name='Arial', size=10)
FILL_HEADER = PatternFill('solid', fgColor='2E4A7B')
FILL_KPI = PatternFill('solid', fgColor='F0F4FA')
FILL_HIGHLIGHT = PatternFill('solid', fgColor='FFF8DC')
FILL_TOTAL = PatternFill('solid', fgColor='E8F0F8')
BORDER_THIN = Border(left=Side(style='thin', color='CCCCCC'),
                     right=Side(style='thin', color='CCCCCC'),
                     top=Side(style='thin', color='CCCCCC'),
                     bottom=Side(style='thin', color='CCCCCC'))
ALIGN_CENTER = Alignment(horizontal='center', vertical='center')
ALIGN_LEFT = Alignment(horizontal='left', vertical='center')
ALIGN_RIGHT = Alignment(horizontal='right', vertical='center')

def header_row(ws, row, headers, start_col=1):
    for i, h in enumerate(headers):
        c = ws.cell(row=row, column=start_col+i, value=h)
        c.font = FONT_HEADER
        c.fill = FILL_HEADER
        c.alignment = ALIGN_CENTER
        c.border = BORDER_THIN

def write_df(ws, df, start_row=1, start_col=1, num_fmt_cols=None, pct_cols=None):
    num_fmt_cols = num_fmt_cols or []
    pct_cols = pct_cols or []
    header_row(ws, start_row, list(df.columns), start_col)
    for r_idx, row in enumerate(df.itertuples(index=False), start=start_row+1):
        for c_idx, val in enumerate(row, start=start_col):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = FONT_BODY
            cell.border = BORDER_THIN
            col_name = df.columns[c_idx-start_col]
            if col_name in num_fmt_cols:
                cell.number_format = '#,##0.0'
                cell.alignment = ALIGN_RIGHT
            elif col_name in pct_cols:
                cell.number_format = '0.0%'
                cell.alignment = ALIGN_RIGHT
            elif isinstance(val, (int, float)) and not pd.isna(val):
                cell.number_format = '#,##0'
                cell.alignment = ALIGN_RIGHT
            else:
                cell.alignment = ALIGN_LEFT
    for c_idx in range(start_col, start_col+len(df.columns)):
        col_letter = get_column_letter(c_idx)
        col_name = df.columns[c_idx-start_col]
        max_len = max(len(str(col_name)), df.iloc[:, c_idx-start_col].astype(str).map(len).max() if len(df) > 0 else 0)
        ws.column_dimensions[col_letter].width = min(max(max_len+2, 12), 45)

# --- Carrega dados ---
print("Carregando dados...")

# Master catalogos (com perfil)
master = pd.read_csv(OUT / "etapa3_MESTRE_v2_com_perfil.csv", sep=';', decimal=',', encoding='utf-8')
# Converte colunas numéricas
for col in ['nmv_cbh_pos', 'top_pre_nmv', 'top_pre_nmv_pos', 'total_pre', 'total_pos',
            'impacto_top_pre', 'nmv_pre_1P', 'nmv_pre_TO_CG', 'nmv_pre_dev', 'nmv_pre_total',
            'top_pre_taxa6m_proj']:
    if col in master.columns:
        master[col] = pd.to_numeric(master[col], errors='coerce').fillna(0)

# Sellers canibalizados
sellers_canib = pd.read_csv(OUT / "etapa3c_sellers_canibalizados.csv", sep=';', decimal=',', encoding='utf-8')

# Fora vs em catalogo
fora_em = pd.read_csv(OUT / "etapa3e_fora_vs_em_catalogo.csv", sep=';', decimal=',', encoding='utf-8')

# Lente 3 evolutivo
evol = pd.read_csv(OUT / "etapa2_lente3_evolutivo_NMV_regiao.csv", sep=';', decimal=',', encoding='utf-8')
share_cbh = pd.read_csv(OUT / "etapa2_lente3_share_CBH_regiao.csv", sep=';', decimal=',', encoding='utf-8')

# Lente 1 D1 x Regiao
contrib_pp = pd.read_csv(OUT / "etapa2_lente1_contribCBH_pp_D1xRegiao.csv", sep=';', decimal=',', encoding='utf-8')
yoy_total = pd.read_csv(OUT / "etapa2_lente1_yoyTotal_D1xRegiao.csv", sep=';', decimal=',', encoding='utf-8')
nmv_cbh_d1reg = pd.read_csv(OUT / "etapa2_lente1_NMV_CBH26_D1xRegiao.csv", sep=';', decimal=',', encoding='utf-8')

print(f"Master: {len(master)} catalogos x {len(master.columns)} cols")

# --- Cria workbook ---
wb = Workbook()
wb.remove(wb.active)

# ========================================================================
# ABA 1 — SUMARIO
# ========================================================================
ws = wb.create_sheet("Sumario")
ws['A1'] = "Análise CBH × MELI HE — Incrementalidade Regional"
ws['A1'].font = FONT_TITULO
ws.merge_cells('A1:F1')
ws['A2'] = "Período pós-CBH: nov/2025 → abr/2026 (6 meses) | Período comparativo: nov/2023 → out/2025"
ws['A2'].font = Font(name='Arial', size=10, italic=True, color='666666')
ws.merge_cells('A2:F2')
ws['A3'] = "Beatriz Dacache | 2026-05-28"
ws['A3'].font = Font(name='Arial', size=9, color='999999')

# KPIs principais
kpis = [
    ("R$ 880,1 Mi", "NMV CBH em HE (6 meses)"),
    ("+9,9 pp", "Contribuição CBH ao YoY MELI HE (Lente 1)"),
    ("+17,3 pp", "Contribuição CBH no Norte (maior efeito)"),
    ("1.566", "Catálogos únicos onde CBH vendeu"),
    ("90,1%", "NMV CBH em catálogos JÁ existentes em MELI"),
    ("31%", "Catálogos onde CBH expandiu cobertura UF"),
    ("R$ 700-800 Mi", "Net incremental estimado"),
    ("-R$ 3,3 Mi", "Impacto líquido no 1P MELI"),
]
row = 5
for i, (val, lbl) in enumerate(kpis):
    r = row + (i // 4) * 3
    c = 1 + (i % 4) * 2
    ws.cell(row=r, column=c, value=val).font = FONT_KPI_NUM
    ws.cell(row=r, column=c).fill = FILL_KPI
    ws.cell(row=r, column=c).alignment = ALIGN_CENTER
    ws.cell(row=r+1, column=c, value=lbl).font = FONT_KPI_LABEL
    ws.cell(row=r+1, column=c).fill = FILL_KPI
    ws.cell(row=r+1, column=c).alignment = ALIGN_CENTER
    ws.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c+1)
    ws.merge_cells(start_row=r+1, start_column=c, end_row=r+1, end_column=c+1)

# Indice
ws['A12'] = "Navegação"
ws['A12'].font = Font(name='Arial', bold=True, size=12)
indice = [
    ("Aba 1", "Sumario", "KPIs principais e índice"),
    ("Aba 2", "Catalogos_Master", "1.566 catálogos × 32 campos — base completa filtrável"),
    ("Aba 3", "PerfilPre_Pivot", "Tipo A/B × Perfil pré (1P/TO/CG/Dev) × D1"),
    ("Aba 4", "Sellers_Canibalizados", "Ranking de sellers que perderam BB pra CBH"),
    ("Aba 5", "Top_Brands_D2", "Top marcas por D2 (NMV CBH)"),
    ("Aba 6", "Fora_vs_em_Catalogo", "NMV CBH em catálogo vs anúncios livres por D2"),
    ("Aba 7", "Capilaridade_Regional", "Contribuição CBH em pp × D1 × Região"),
    ("Aba 8", "Evolutivo_Mensal", "NMV HE mensal jan/24-abr/26 com share CBH"),
]
ws['A13'] = "Aba"; ws['A13'].font = FONT_HEADER; ws['A13'].fill = FILL_HEADER
ws['B13'] = "Nome"; ws['B13'].font = FONT_HEADER; ws['B13'].fill = FILL_HEADER
ws['C13'] = "Descrição"; ws['C13'].font = FONT_HEADER; ws['C13'].fill = FILL_HEADER
ws.merge_cells('C13:F13')
for i, (n, nm, dsc) in enumerate(indice):
    r = 14 + i
    ws.cell(row=r, column=1, value=n).font = FONT_BODY
    ws.cell(row=r, column=2, value=nm).font = Font(name='Arial', size=10, bold=True, color='2E4A7B', underline='single')
    ws.cell(row=r, column=2).hyperlink = f"#{nm}!A1"
    ws.cell(row=r, column=3, value=dsc).font = FONT_BODY
    ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=6)

# Limitações
ws['A24'] = "Limitações declaradas"
ws['A24'].font = Font(name='Arial', bold=True, size=12)
lims = [
    "1. Sem contrafactual real — análise correlacional, não causal",
    "2. BF 2025 = entrada CBH no mesmo mês; mitigado com Lente 1 (fev-abr) e Lente 2 (ago-out vs fev-abr)",
    "3. Crescimento orgânico MELI 24→25 forte; mitigado com lentes recentes",
    "4. Canibalização inferida vs taxa pré projetada — base de growth zero, pode subestimar perda real",
    "5. Tech excluído (CBH com share ≤0,4% em qualquer D1 Tech, sem materialidade)",
]
for i, txt in enumerate(lims):
    ws.cell(row=25+i, column=1, value=txt).font = FONT_BODY
    ws.merge_cells(start_row=25+i, start_column=1, end_row=25+i, end_column=6)

ws.column_dimensions['A'].width = 12
ws.column_dimensions['B'].width = 22
ws.column_dimensions['C'].width = 18
ws.column_dimensions['D'].width = 18
ws.column_dimensions['E'].width = 18
ws.column_dimensions['F'].width = 18

# ========================================================================
# ABA 2 — CATALOGOS MASTER
# ========================================================================
ws = wb.create_sheet("Catalogos_Master")
ws['A1'] = "1.566 catálogos onde CBH vendeu (nov/25-abr/26) — base completa filtrável"
ws['A1'].font = FONT_TITULO
ws.merge_cells('A1:F1')

# Reordena colunas pra leitura
cols_ord = ['product_id', 'd1', 'd2', 'brand', 'tipo_sortimento', 'perfil_pre',
            'cbh_eh_top_pos', 'cbh_tomou_bb', 'top_pre', 'top_pos',
            'nmv_cbh_pos', 'top_pre_nmv', 'top_pre_nmv_pos', 'impacto_top_pre',
            'total_pre', 'total_pos', 'qt_sellers_pre', 'qt_sellers_pos',
            'ufs_cbh_pos', 'qt_ufs_pre',
            'has_1P_pre', 'has_TO_pre', 'has_CG_pre',
            'qt_1P_pre', 'qt_TO_pre', 'qt_CG_pre', 'qt_dev_pre',
            'nmv_pre_1P', 'nmv_pre_TO_CG', 'nmv_pre_dev']
cols_keep = [c for c in cols_ord if c in master.columns]
mdf = master[cols_keep].copy()
# Sort por NMV CBH desc
mdf = mdf.sort_values('nmv_cbh_pos', ascending=False).reset_index(drop=True)

write_df(ws, mdf, start_row=3)
ws.freeze_panes = 'E4'
ws.auto_filter.ref = f"A3:{get_column_letter(len(mdf.columns))}{len(mdf)+3}"

# ========================================================================
# ABA 3 — PERFIL PRE PIVOT
# ========================================================================
ws = wb.create_sheet("PerfilPre_Pivot")
ws['A1'] = "Perfil dos sellers pré-CBH × D1 — quem operava antes?"
ws['A1'].font = FONT_TITULO
ws.merge_cells('A1:G1')
ws['A2'] = "Classificação: A_so_dev (só LongTail/Midtail 3P) | B_com_TO (Loja Oficial sem 1P) | C_com_1P (1P MELI vendia) | B_NOVO (catálogo novo em MELI)"
ws['A2'].font = Font(name='Arial', size=9, italic=True, color='666666')
ws.merge_cells('A2:G2')

# Pivot qt catalogos por D1 x perfil
piv_qt = master.pivot_table(index='d1', columns='perfil_pre', values='product_id', aggfunc='count', fill_value=0)
piv_qt['Total'] = piv_qt.sum(axis=1)
piv_qt = piv_qt.sort_values('Total', ascending=False).reset_index()

ws['A4'] = "QUANTIDADE DE CATÁLOGOS"
ws['A4'].font = Font(name='Arial', bold=True, size=11, color='2E4A7B')
write_df(ws, piv_qt, start_row=5)

# Pivot NMV
piv_nmv = master.pivot_table(index='d1', columns='perfil_pre', values='nmv_cbh_pos', aggfunc='sum', fill_value=0) / 1e6
piv_nmv['Total'] = piv_nmv.sum(axis=1)
piv_nmv = piv_nmv.sort_values('Total', ascending=False).reset_index()
piv_nmv = piv_nmv.round(1)

start = len(piv_qt) + 8
ws.cell(row=start, column=1, value="NMV CBH (R$ Mi)").font = Font(name='Arial', bold=True, size=11, color='2E4A7B')
write_df(ws, piv_nmv, start_row=start+1)

# Resumo total
res_perfil = master.groupby('perfil_pre').agg(
    qt_catalogos=('product_id', 'count'),
    nmv_cbh_mi=('nmv_cbh_pos', lambda x: round(x.sum()/1e6, 1))
).reset_index()
tot_nmv = master['nmv_cbh_pos'].sum()
res_perfil['share_qt'] = (res_perfil['qt_catalogos'] / len(master) * 100).round(1).astype(str) + '%'
res_perfil['share_nmv'] = (res_perfil['nmv_cbh_mi']*1e6 / tot_nmv * 100).round(1).astype(str) + '%'
res_perfil = res_perfil.sort_values('nmv_cbh_mi', ascending=False)

start2 = start + len(piv_nmv) + 5
ws.cell(row=start2, column=1, value="RESUMO TOTAL").font = Font(name='Arial', bold=True, size=11, color='2E4A7B')
write_df(ws, res_perfil, start_row=start2+1)

# ========================================================================
# ABA 4 — SELLERS CANIBALIZADOS
# ========================================================================
ws = wb.create_sheet("Sellers_Canibalizados")
ws['A1'] = "Sellers que perderam BB para a CBH — perda vs taxa pré projetada (6m)"
ws['A1'].font = FONT_TITULO
ws.merge_cells('A1:F1')
ws['A2'] = "Filtro: catálogos onde CBH tomou BB + top pré tinha NMV > R$ 100K. Δ = NMV pós real - taxa pré ajustada pra 6m equivalentes."
ws['A2'].font = Font(name='Arial', size=9, italic=True, color='666666')
ws.merge_cells('A2:F2')

write_df(ws, sellers_canib, start_row=4)
ws.freeze_panes = 'A5'
ws.auto_filter.ref = f"A4:{get_column_letter(len(sellers_canib.columns))}{len(sellers_canib)+4}"

# ========================================================================
# ABA 5 — TOP BRANDS x D2
# ========================================================================
ws = wb.create_sheet("Top_Brands_D2")
ws['A1'] = "Top marcas da CBH por D2 (NMV em R$ Mi)"
ws['A1'].font = FONT_TITULO
ws.merge_cells('A1:F1')

brands = master.groupby(['d1', 'd2', 'brand']).agg(
    qt_catalogos=('product_id', 'count'),
    nmv_cbh_mi=('nmv_cbh_pos', lambda x: round(x.sum()/1e6, 2)),
    ufs_alcancadas=('ufs_cbh_pos', 'mean')
).reset_index()
brands['ufs_alcancadas'] = brands['ufs_alcancadas'].round(0)
brands = brands.sort_values('nmv_cbh_mi', ascending=False).reset_index(drop=True)

write_df(ws, brands, start_row=3)
ws.freeze_panes = 'A4'
ws.auto_filter.ref = f"A3:{get_column_letter(len(brands.columns))}{len(brands)+3}"

# ========================================================================
# ABA 6 — FORA VS EM CATALOGO
# ========================================================================
ws = wb.create_sheet("Fora_vs_em_Catalogo")
ws['A1'] = "NMV CBH em catálogo (BB) vs fora de catálogo (anúncios livres) — por D2"
ws['A1'].font = FONT_TITULO
ws.merge_cells('A1:F1')
ws['A2'] = "Anúncios fora de catálogo: ITEM_ID sem CAT_PRODUCT_ID (não disputam BB). R$ 140 Mi (16%) do NMV CBH HE."
ws['A2'].font = Font(name='Arial', size=9, italic=True, color='666666')
ws.merge_cells('A2:F2')

write_df(ws, fora_em, start_row=4)

# ========================================================================
# ABA 7 — CAPILARIDADE REGIONAL
# ========================================================================
ws = wb.create_sheet("Capilaridade_Regional")
ws['A1'] = "Contribuição da CBH ao crescimento YoY HE por D1 × Região (Lente 1: fev-abr/26 vs fev-abr/25)"
ws['A1'].font = FONT_TITULO
ws.merge_cells('A1:G1')

ws['A3'] = "CONTRIBUIÇÃO CBH (em pp do YoY)"
ws['A3'].font = Font(name='Arial', bold=True, size=11, color='2E4A7B')
write_df(ws, contrib_pp, start_row=4)

start = len(contrib_pp) + 7
ws.cell(row=start, column=1, value="YoY TOTAL (com CBH) — %").font = Font(name='Arial', bold=True, size=11, color='2E4A7B')
write_df(ws, yoy_total, start_row=start+1)

start2 = start + len(yoy_total) + 4
ws.cell(row=start2, column=1, value="NMV CBH POR D1 × REGIÃO (R$ Mi, fev-abr/26)").font = Font(name='Arial', bold=True, size=11, color='2E4A7B')
write_df(ws, nmv_cbh_d1reg, start_row=start2+1)

# ========================================================================
# ABA 8 — EVOLUTIVO MENSAL
# ========================================================================
ws = wb.create_sheet("Evolutivo_Mensal")
ws['A1'] = "Evolutivo mensal NMV HE por região (jan/24-abr/26) — inflexão em nov/25"
ws['A1'].font = FONT_TITULO
ws.merge_cells('A1:H1')

ws['A3'] = "NMV TOTAL (R$ Mi) — todos os sellers"
ws['A3'].font = Font(name='Arial', bold=True, size=11, color='2E4A7B')
write_df(ws, evol, start_row=4)

start = len(evol) + 7
ws.cell(row=start, column=1, value="SHARE CBH (%) NO NMV TOTAL — pós-nov/25").font = Font(name='Arial', bold=True, size=11, color='2E4A7B')
write_df(ws, share_cbh, start_row=start+1)

# ========================================================================
# ABA 9 — DECOMPOSIÇÃO REGIONAL (validação dos +9,9 pp)
# ========================================================================
ws = wb.create_sheet("Decomposicao_Regional")
ws['A1'] = "Decomposição do crescimento BR (+40,9% YoY) por região — com e sem CBH"
ws['A1'].font = FONT_TITULO
ws.merge_cells('A1:I1')
ws['A2'] = "Lógica: contrib_pp_BR de cada região = Δ NMV regional / NMV BR fev-abr/25 × 100. Soma das contribuições = YoY BR."
ws['A2'].font = Font(name='Arial', size=9, italic=True, color='666666')
ws.merge_cells('A2:I2')

decomp = pd.read_csv(OUT / "etapa2_decomposicao_regional.csv", sep=';', decimal=',', encoding='utf-8')
write_df(ws, decomp, start_row=4)

ws.cell(row=len(decomp)+6, column=1, value="VALIDAÇÃO MATEMÁTICA").font = Font(name='Arial', bold=True, size=11, color='2E4A7B')
validacao = pd.DataFrame([
    {'Métrica': 'Soma Contrib Total (pp)', 'Valor': '40,86', 'Bate com': 'YoY BR 40,86%'},
    {'Métrica': 'Soma Contrib ex-CBH (pp)', 'Valor': '30,92', 'Bate com': 'YoY ex-CBH 30,92%'},
    {'Métrica': 'Soma Contrib CBH (pp)', 'Valor': '9,95', 'Bate com': '+9,9 pp ✓'},
])
write_df(ws, validacao, start_row=len(decomp)+7)

# ========================================================================
# ABA 10 — MARCAS_GROWTH
# ========================================================================
ws = wb.create_sheet("Marcas_Growth")
ws['A1'] = "Aceleração por marca: NMV YoY fev-abr/26 vs fev-abr/25 (com vs sem CBH)"
ws['A1'].font = FONT_TITULO
ws.merge_cells('A1:I1')
ws['A2'] = "Filtro: marcas com NMV25 ≥ R$ 5 Mi ou NMV CBH ≥ R$ 3 Mi. Ordenado por Contrib_CBH_pp desc."
ws['A2'].font = Font(name='Arial', size=9, italic=True, color='666666')
ws.merge_cells('A2:I2')

marcas = pd.read_csv(OUT / "etapa4a_marcas_growth.csv", sep=';', decimal=',', encoding='utf-8')
marcas = marcas.sort_values('Contrib_CBH_pp', ascending=False).reset_index(drop=True)
write_df(ws, marcas, start_row=4)
ws.freeze_panes = 'A5'
ws.auto_filter.ref = f"A4:{get_column_letter(len(marcas.columns))}{len(marcas)+4}"

# ========================================================================
# ABA 11 — D2_GROWTH
# ========================================================================
ws = wb.create_sheet("D2_Growth")
ws['A1'] = "Aceleração por D2: contribuição CBH ao YoY"
ws['A1'].font = FONT_TITULO
ws.merge_cells('A1:H1')
ws['A2'] = "Filtro: D2s com NMV25 ≥ R$ 10 Mi. Ordenado por Contrib_CBH_pp desc."
ws['A2'].font = Font(name='Arial', size=9, italic=True, color='666666')
ws.merge_cells('A2:H2')

d2 = pd.read_csv(OUT / "etapa4b_d2_growth.csv", sep=';', decimal=',', encoding='utf-8')
d2 = d2.sort_values('Contrib_CBH_pp', ascending=False).reset_index(drop=True)
write_df(ws, d2, start_row=4)

# ========================================================================
# ABA 12 — ASP_BUCKETS
# ========================================================================
ws = wb.create_sheet("ASP_Buckets")
ws['A1'] = "Distribuição do NMV CBH por faixa de ASP (preço médio por unidade)"
ws['A1'].font = FONT_TITULO
ws.merge_cells('A1:F1')
ws['A2'] = "ASP = NMV CBH / NSI CBH no catálogo. Concentração em R$ 1k-5k (66% do NMV CBH)."
ws['A2'].font = Font(name='Arial', size=9, italic=True, color='666666')
ws.merge_cells('A2:F2')

asp = pd.read_csv(OUT / "etapa4c_asp_buckets.csv", sep=';', decimal=',', encoding='utf-8')
write_df(ws, asp, start_row=4)

# Sumario - novo bloco lateral (col H em diante) com novas abas
ws_sum = wb['Sumario']
ws_sum.cell(row=12, column=8, value="Abas analíticas adicionais").font = Font(name='Arial', bold=True, size=12)
ws_sum.cell(row=13, column=8, value="Aba").font = FONT_HEADER; ws_sum.cell(row=13, column=8).fill = FILL_HEADER
ws_sum.cell(row=13, column=9, value="Nome").font = FONT_HEADER; ws_sum.cell(row=13, column=9).fill = FILL_HEADER
ws_sum.cell(row=13, column=10, value="Descrição").font = FONT_HEADER; ws_sum.cell(row=13, column=10).fill = FILL_HEADER
novos_indices = [
    ("Aba 9", "Decomposicao_Regional", "Validação matemática dos +9,9 pp por região"),
    ("Aba 10", "Marcas_Growth", "Marcas mais aceleradas (TCL, Samsung, Consul)"),
    ("Aba 11", "D2_Growth", "Categorias D2 mais impulsionadas"),
    ("Aba 12", "ASP_Buckets", "Faixa de preço CBH concentra valor"),
]
for i, (n, nm, dsc) in enumerate(novos_indices):
    r = 14 + i
    ws_sum.cell(row=r, column=8, value=n).font = FONT_BODY
    c_nm = ws_sum.cell(row=r, column=9, value=nm)
    c_nm.font = Font(name='Arial', size=10, bold=True, color='2E4A7B', underline='single')
    c_nm.hyperlink = f"#{nm}!A1"
    ws_sum.cell(row=r, column=10, value=dsc).font = FONT_BODY
ws_sum.column_dimensions['H'].width = 10
ws_sum.column_dimensions['I'].width = 22
ws_sum.column_dimensions['J'].width = 45

# Salva
wb.active = 0
wb.save(TARGET)
print(f"OK: {TARGET}")
print(f"Tamanho: {TARGET.stat().st_size / 1024:.0f} KB")
