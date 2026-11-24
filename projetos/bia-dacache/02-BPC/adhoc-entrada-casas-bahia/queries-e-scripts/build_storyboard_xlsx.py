"""Gera STORYBOARD_CBH_HE.xlsx — uma aba por gráfico na ordem da história.
Cada aba tem: título sugerido + talking point + tipo de gráfico + tabela limpa.
"""
import pandas as pd
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE = Path(r"C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-05-entrada-cbh-incrementalidade-regional")
OUT = BASE / "outputs"
TARGET = OUT / "STORYBOARD_CBH_HE.xlsx"

# Estilos minimalistas — Beatriz vai aplicar template MELI
FONT_TITULO = Font(name='Calibri', bold=True, size=14, color='1A1A1A')
FONT_SUB = Font(name='Calibri', italic=True, size=10, color='555555')
FONT_LABEL = Font(name='Calibri', bold=True, size=10, color='1A1A1A')
FONT_BODY = Font(name='Calibri', size=10, color='1A1A1A')
FONT_TIPO = Font(name='Calibri', bold=True, size=9, color='9A7D0A')
FILL_HEADER = PatternFill('solid', fgColor='FFE600')
FILL_LABEL = PatternFill('solid', fgColor='FFF59D')
BORDER_THIN = Border(
    left=Side(style='thin', color='CCCCCC'),
    right=Side(style='thin', color='CCCCCC'),
    top=Side(style='thin', color='CCCCCC'),
    bottom=Side(style='thin', color='CCCCCC'))

def write_aba(ws, secao, titulo, talking_point, tipo_grafico, df, eixos_sugeridos=None, notas=None):
    """Padrão de aba pra montagem de gráfico"""
    # Seção (camada da história)
    ws['A1'] = secao
    ws['A1'].font = FONT_TIPO
    # Título sugerido pro gráfico
    ws['A2'] = titulo
    ws['A2'].font = FONT_TITULO
    ws.merge_cells('A2:H2')
    # Talking point
    ws['A3'] = "Talking point:"
    ws['A3'].font = FONT_LABEL
    ws['B3'] = talking_point
    ws['B3'].font = FONT_BODY
    ws.merge_cells('B3:H3')
    ws['A3'].alignment = Alignment(vertical='top')
    ws['B3'].alignment = Alignment(wrap_text=True, vertical='top')
    ws.row_dimensions[3].height = 50
    # Tipo de gráfico
    ws['A4'] = "Gráfico sugerido:"
    ws['A4'].font = FONT_LABEL
    ws['B4'] = tipo_grafico
    ws['B4'].font = FONT_BODY
    ws.merge_cells('B4:H4')
    # Eixos
    if eixos_sugeridos:
        ws['A5'] = "Eixos / séries:"
        ws['A5'].font = FONT_LABEL
        ws['B5'] = eixos_sugeridos
        ws['B5'].font = FONT_BODY
        ws.merge_cells('B5:H5')
        start_row = 7
    else:
        start_row = 6
    # Header da tabela
    for c_idx, col in enumerate(df.columns, start=1):
        cell = ws.cell(row=start_row, column=c_idx, value=col)
        cell.font = FONT_LABEL
        cell.fill = FILL_HEADER
        cell.border = BORDER_THIN
        cell.alignment = Alignment(horizontal='center')
    # Dados
    for r_idx, row in enumerate(df.itertuples(index=False), start=start_row+1):
        for c_idx, val in enumerate(row, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = FONT_BODY
            cell.border = BORDER_THIN
            if isinstance(val, (int, float)) and not pd.isna(val):
                if abs(val) < 1000 and (val != int(val) if isinstance(val, float) else False):
                    cell.number_format = '#,##0.0'
                else:
                    cell.number_format = '#,##0'
    # Notas (opcional, rodapé)
    if notas:
        end_row = start_row + len(df) + 2
        ws.cell(row=end_row, column=1, value="Notas:").font = FONT_LABEL
        ws.cell(row=end_row+1, column=1, value=notas).font = FONT_SUB
        ws.merge_cells(start_row=end_row+1, start_column=1, end_row=end_row+1, end_column=8)
        ws.cell(row=end_row+1, column=1).alignment = Alignment(wrap_text=True, vertical='top')
        ws.row_dimensions[end_row+1].height = 35
    # Larguras
    for c in range(1, len(df.columns)+1):
        ws.column_dimensions[get_column_letter(c)].width = 18

# ======================================================================
# Carrega dados
# ======================================================================
print("Carregando dados...")
master = pd.read_csv(OUT / "etapa3_MESTRE_v2_com_perfil.csv", sep=';', decimal=',', encoding='utf-8')
for col in ['nmv_cbh_pos', 'total_pre', 'total_pos', 'nmv_pre_total']:
    if col in master.columns:
        master[col] = pd.to_numeric(master[col], errors='coerce').fillna(0)

decomp = pd.read_csv(OUT / "etapa2_decomposicao_regional.csv", sep=';', decimal=',', encoding='utf-8')
marcas = pd.read_csv(OUT / "etapa4a_marcas_growth.csv", sep=';', decimal=',', encoding='utf-8')
d2g = pd.read_csv(OUT / "etapa4b_d2_growth.csv", sep=';', decimal=',', encoding='utf-8')
asp = pd.read_csv(OUT / "etapa4c_asp_buckets.csv", sep=';', decimal=',', encoding='utf-8')
evol = pd.read_csv(OUT / "etapa2_lente3_evolutivo_NMV_regiao.csv", sep=';', decimal=',', encoding='utf-8')
cbh_mens = pd.read_csv(OUT / "etapa2_lente3_evolutivo_NMV_CBH_regiao.csv", sep=';', decimal=',', encoding='utf-8')
share_cbh = pd.read_csv(OUT / "etapa2_lente3_share_CBH_regiao.csv", sep=';', decimal=',', encoding='utf-8')
contrib_pp = pd.read_csv(OUT / "etapa2_lente1_contribCBH_pp_D1xRegiao.csv", sep=';', decimal=',', encoding='utf-8')
nmv_cbh_d1 = pd.read_csv(OUT / "etapa2_lente1_NMV_CBH26_D1xRegiao.csv", sep=';', decimal=',', encoding='utf-8')
fora_em = pd.read_csv(OUT / "etapa3e_fora_vs_em_catalogo.csv", sep=';', decimal=',', encoding='utf-8')
sellers_canib = pd.read_csv(OUT / "etapa3c_sellers_canibalizados.csv", sep=';', decimal=',', encoding='utf-8')

wb = Workbook()
wb.remove(wb.active)

# ======================================================================
# ABA 0 — STORYBOARD (índice da história)
# ======================================================================
ws = wb.create_sheet("00_Storyboard")
ws['A1'] = "STORYBOARD — Entrada Casas Bahia no MELI Home Electronics"
ws['A1'].font = Font(name='Calibri', bold=True, size=16, color='1A1A1A')
ws.merge_cells('A1:F1')
ws['A2'] = "Estrutura sugerida da apresentação · 14 gráficos na ordem da narrativa · Dados prontos em cada aba"
ws['A2'].font = FONT_SUB
ws.merge_cells('A2:F2')

storyboard = [
    ("01_KPIs_capa", "Capa", "Capa com 4 KPIs principais", "Cards / blocos numéricos"),
    ("02_Decomposicao_BR", "Camada 1-2: A prova", "Decomposição matemática dos +9,94 pp por região", "Barras horizontais empilhadas"),
    ("03_Intensidade_regional", "Camada 3: Onde a CBH puxou mais", "Crescimento YoY por região: orgânico vs CBH", "Barras horizontais empilhadas com YoY total"),
    ("04_3_Evidencias", "Camada 4: Como sabemos que foi a CBH", "3 evidências de causalidade-pela-CBH", "Texto / caixa (sem gráfico)"),
    ("05_D1_share_CBH", "Camada 5: Em quais categorias", "Mix do NMV CBH por D1 (LA + TVs = 84%)", "Pizza ou barras horizontais"),
    ("06_Heatmap_D1xRegiao", "Camada 5: Onde dentro das categorias", "Heatmap contribuição CBH (pp) por D1 × Região", "Heatmap / mapa de calor"),
    ("07_D2_aceleracao", "Camada 5: Quais D2 mais aceleraram", "Contribuição CBH ao YoY por D2 (Laundry, Refrig, TVs)", "Barras horizontais empilhadas"),
    ("08_Mecanismos_growth", "Camada 6: Como cresceu (REVISADO)", "4 mecanismos limpos do growth CBH (sem dupla contagem)", "Barras horizontais ou waterfall"),
    ("09_Capilaridade_pura", "Camada 6: Capilaridade pura", "208 catálogos com volume real onde CBH expandiu UFs (R$ 348 Mi)", "Barras horizontais por bucket UFs pré"),
    ("10_Dormentes_perfil", "Camada 6: Quem foi reativado", "307 dormentes — D2 e marcas que mais avançaram", "Barras horizontais + tabela top marcas"),
    ("11_Tipo_AB_sortimento", "Camada 6: Sortimento novo vs existente", "90% NMV em catálogo já existente; 10% novo (Tipo B)", "Pizza ou colunas"),
    ("12_Perfil_pre_cat", "Camada 7: NÃO foi território abandonado", "Perfil dos sellers pré-CBH em cada catálogo", "Barras horizontais"),
    ("13_Canibalizacao_sellers", "Camada 8: Quem perdeu", "Top 10 sellers que perderam BB pra CBH", "Barras horizontais (valores negativos)"),
    ("14_1P_MELI_deep", "Camada 8: Caso especial 1P MELI", "1P MELI: −R$ 3,3 Mi líquido (com upside em TVs)", "Barras por D1 (positivo/negativo)"),
    ("15_Evolutivo_mensal", "Camada 9: Tendência", "Evolutivo NMV HE BR jan/24 → mai/26* (inflexão + aceleração)", "Linha empilhada (area chart)"),
    ("16_Share_CBH_maio", "Camada 9: Aceleração mai/26", "Share CBH no NMV HE por região: abr/26 → mai/26*", "Barras agrupadas"),
    ("17_Marcas_aceleradas", "Camada 10: Marcas", "Top 12 marcas impulsionadas pela CBH (TCL, Samsung, etc)", "Barras horizontais empilhadas"),
    ("18_Sintese", "Camada 11: Síntese", "Resumo em 1 parágrafo + 5 bullets", "Texto / quote (sem gráfico)"),
    ("19_OUTROS_fora_cat", "Outros achados: Fora de catálogo", "R$ 140 Mi (16%) em anúncios livres CBH — TVs 20,7%", "Barras horizontais empilhadas"),
    ("20_OUTROS_asp", "Outros achados: ASP", "Distribuição CBH por faixa de preço (66% em R$ 1k-5k)", "Pizza ou colunas"),
]
headers = ['Aba', 'Camada', 'O que conta', 'Tipo de gráfico']
for c, h in enumerate(headers, start=1):
    cell = ws.cell(row=4, column=c, value=h)
    cell.font = FONT_LABEL; cell.fill = FILL_HEADER; cell.border = BORDER_THIN
for i, (aba, cam, conta, tipo) in enumerate(storyboard):
    r = 5 + i
    ws.cell(row=r, column=1, value=aba).font = Font(name='Calibri', bold=True, color='9A7D0A', size=10, underline='single')
    ws.cell(row=r, column=1).hyperlink = f"#{aba}!A1"
    ws.cell(row=r, column=2, value=cam).font = FONT_BODY
    ws.cell(row=r, column=3, value=conta).font = FONT_BODY
    ws.cell(row=r, column=4, value=tipo).font = FONT_BODY
    for c in range(1, 5):
        ws.cell(row=r, column=c).border = BORDER_THIN
ws.column_dimensions['A'].width = 28
ws.column_dimensions['B'].width = 22
ws.column_dimensions['C'].width = 55
ws.column_dimensions['D'].width = 35

# ======================================================================
# ABA 01 — KPIs CAPA
# ======================================================================
ws = wb.create_sheet("01_KPIs_capa")
df = pd.DataFrame({
    'KPI': [
        'NMV CBH em HE (6 meses)',
        'Contribuição CBH ao YoY MELI HE (fev-abr/26 vs 25)',
        'YoY MELI HE total (com CBH)',
        'YoY MELI HE ex-CBH (orgânico)',
        'Maior contribuição regional (Norte)',
        'Catálogos únicos onde CBH vendeu',
        'NMV CBH em catálogos JÁ existentes',
        'Net incremental estimado ao MELI',
    ],
    'Valor': ['R$ 880 Mi', '+9,94 pp', '+40,86%', '+30,92%', '+17,3 pp', '1.566', '90% (R$ 667 Mi)', '~R$ 800 Mi (90%)'],
    'Fonte': [
        'soma master CSV',
        'YoY total − YoY ex-CBH',
        'NMV 26 / NMV 25 − 1',
        'NMV 26 ex-CBH / NMV 25 − 1',
        'YoY N total − YoY N ex-CBH',
        'count distinct CAT_PRODUCT_ID',
        '1.402 cat Tipo A / 1.566 total',
        'NMV CBH − R$ 76 Mi perdas estimadas',
    ]
})
write_aba(ws,
    "Camada 1-2 · A pergunta e os números",
    "Capa: a CBH em 6 meses no MELI HE",
    "Em 6 meses, a Casas Bahia gerou R$ 880 Mi em HE e adicionou +9,94 pp ao crescimento YoY do MELI — com efeito concentrado nas regiões antes mal servidas.",
    "Cards numéricos (4 a 8 KPIs grandes) ou linha de stat callouts",
    df,
    notas="KPIs para capa. Recomenda-se selecionar 4-6 mais impactantes."
)

# ======================================================================
# ABA 02 — DECOMPOSICAO BR
# ======================================================================
ws = wb.create_sheet("02_Decomposicao_BR")
df = decomp.copy()
df = df.rename(columns={
    'Regiao': 'Região',
    'NMV_25_Mi': 'NMV fev-abr/25 (R$ Mi)',
    'NMV_26_Mi': 'NMV fev-abr/26 (R$ Mi)',
    'Delta_total_Mi': 'Δ NMV total (R$ Mi)',
    'Delta_exCBH_Mi': 'Δ NMV ex-CBH (R$ Mi)',
    'Delta_CBH_Mi': 'Δ NMV CBH (R$ Mi)',
    'Contrib_total_pp_BR': 'Contrib total ao BR (pp)',
    'Contrib_exCBH_pp_BR': 'Contrib ex-CBH ao BR (pp)',
    'Contrib_CBH_pp_BR': 'Contrib CBH ao BR (pp)'
})
df = df.drop(columns=['Share_25'], errors='ignore')
# Adiciona linha BR
df_br = pd.DataFrame([{
    'Região': 'BR TOTAL',
    'NMV fev-abr/25 (R$ Mi)': 3964.2,
    'NMV fev-abr/26 (R$ Mi)': 5584.0,
    'Δ NMV total (R$ Mi)': 1619.8,
    'Δ NMV ex-CBH (R$ Mi)': 1225.8,
    'Δ NMV CBH (R$ Mi)': 394.0,
    'Contrib total ao BR (pp)': 40.86,
    'Contrib ex-CBH ao BR (pp)': 30.92,
    'Contrib CBH ao BR (pp)': 9.95,
}])
df = pd.concat([df, df_br], ignore_index=True)
write_aba(ws,
    "Camada 1-2 · A prova matemática",
    "Decomposição do crescimento BR: cada região contribuiu quanto pro +40,86% YoY",
    "A soma das contribuições regionais bate exatamente com o YoY BR — provando que a CBH é responsável por 9,95 pp dos 40,86 pp de crescimento, distribuídos por todas as regiões.",
    "Barras horizontais empilhadas (orgânico ex-CBH + contribuição CBH) com YoY total no fim de cada barra",
    df,
    "Eixo Y = Região (ordenado por Contrib total ao BR). Eixo X = pp contribuído ao YoY BR. Empilhar Contrib ex-CBH + Contrib CBH.",
    "Cálculo: Contrib_pp_BR = Δ NMV região / NMV BR fev-abr/25 × 100. Verifica: soma = 40,86 pp = YoY BR total."
)

# ======================================================================
# ABA 03 — INTENSIDADE REGIONAL
# ======================================================================
ws = wb.create_sheet("03_Intensidade_regional")
df = pd.DataFrame({
    'Região': ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'],
    'NMV 25 (R$ Mi)': [113.0, 600.5, 269.6, 2334.8, 646.3],
    'NMV 26 total (R$ Mi)': [184.4, 987.6, 398.9, 3124.0, 889.1],
    'NMV 26 ex-CBH (R$ Mi)': [164.9, 892.6, 368.9, 2919.6, 844.1],
    'NMV 26 CBH (R$ Mi)': [19.5, 95.0, 30.0, 204.4, 45.0],
    'YoY total (%)': [63.2, 64.5, 48.0, 33.8, 37.6],
    'YoY ex-CBH (%)': [45.9, 48.6, 36.8, 25.0, 30.6],
    'Premium CBH (pp)': [17.3, 15.8, 11.1, 8.8, 7.0],
    '% growth regional puxado pela CBH': [27.3, 24.5, 23.2, 25.9, 18.5],
})
write_aba(ws,
    "Camada 3 · Intensidade regional",
    "Crescimento YoY por região: orgânico vs CBH — gradiente 2,5x maior no Norte vs Sul",
    "Sem CBH, o Norte cresceria 45,9% e o Sul 30,6%. Com CBH, Norte foi a 63,2% (+17,3 pp) e Sul 37,6% (+7,0 pp). O efeito CBH é 2,5x mais intenso nas regiões antes mal servidas — confirmando a tese de capilaridade.",
    "Barras horizontais empilhadas (YoY ex-CBH + Premium CBH) com YoY total como label",
    df,
    "Eixo Y = Região (ordenado por Premium CBH desc: N>NE>CO>SE>S). Eixo X = % YoY. Empilhar YoY ex-CBH + Premium CBH.",
    "Premium CBH (pp) = YoY total − YoY ex-CBH. % growth puxado pela CBH = Δ NMV CBH / Δ NMV total da região."
)

# ======================================================================
# ABA 04 — 3 EVIDENCIAS
# ======================================================================
ws = wb.create_sheet("04_3_Evidencias")
df = pd.DataFrame({
    '#': [1, 2, 3],
    'Evidência': ['Composição única da CBH', 'Mecanismo específico (capilaridade pura)', 'Robustness check em janela diferente'],
    'Detalhe': [
        'Frete grátis em ED e TVs + capilaridade logística própria + capacidade de preço. Nenhum outro seller 3P no MELI tem essa combinação simultânea.',
        'Em 208 catálogos com volume real (R$ 348 Mi, 39,5% do NMV CBH), a CBH levou produto a mais UFs do que ele cobria antes. Concentrado em catálogos com 6-26 UFs pré — produtos quase-nacionais que ela completou. Não acontece por agregação espontânea de sellers locais.',
        'Comparando ago-out/25 (pré-CBH) com fev-abr/26 (pós), dentro do mesmo ano fiscal, a ordenação de contribuição CBH é idêntica: N +13 pp | NE +12 pp | CO +8,4 pp | SE +7,3 pp | S +5,5 pp.'
    ],
    'Implicação': [
        'Outro 3P não substituiria essa equação.',
        'Mecanismo é logístico-específico, não puramente comercial.',
        'Não foi efeito artificial de viés YoY 24→25.'
    ]
})
write_aba(ws,
    "Camada 4 · Causalidade-pela-CBH",
    "Por que foi a CBH (e não outro seller cresceria isso)",
    "Três evidências em ordem de força que sustentam que o +9,94 pp veio especificamente da entrada da CBH — não de agregação espontânea de outros sellers.",
    "Slide de texto / 3 cards / 3 ícones com bullet — SEM gráfico de dados",
    df,
    notas="Esse slide é argumentativo, não numérico. Use formato de 3 caixas/cards."
)

# ======================================================================
# ABA 05 — D1 SHARE CBH
# ======================================================================
ws = wb.create_sheet("05_D1_share_CBH")
df = pd.DataFrame({
    'D1': ['LARGE APPLIANCES', 'TELEVISIONS & STREAMING DEVICES', 'SMALL APPLIANCES', 'AUDIO & GENERAL ELECTRONICS', 'HEATING, COOLING & AIR QUALITY', 'HOUSEHOLD APPLIANCES PARTS'],
    'NMV CBH (R$ Mi) - 6 meses': [400.3, 341.6, 110.9, 15.9, 11.4, 0.0],
    'Share do NMV CBH (%)': [45.5, 38.8, 12.6, 1.8, 1.3, 0.0],
})
write_aba(ws,
    "Camada 5 · Em quais categorias",
    "Mix do NMV CBH por D1 — LA + TVs concentram 84%",
    "A CBH concentra 84% do NMV em Large Appliances (45%) e Televisions (39%). Small Appliances tem 13%; demais D1s são marginais.",
    "Pizza/donut ou barras horizontais ordenadas",
    df,
    "Eixo categórico = D1. Valor = NMV CBH (R$ Mi) ou Share (%).",
    "Período: nov/25-abr/26 (6 meses). Cobertura: 100% do NMV CBH em HE (R$ 880 Mi)."
)

# ======================================================================
# ABA 06 — HEATMAP D1 x REGIAO
# ======================================================================
ws = wb.create_sheet("06_Heatmap_D1xRegiao")
df = contrib_pp.copy()
df = df.rename(columns={'D1':'D1'})
write_aba(ws,
    "Camada 5 · Cruzamento categoria × região",
    "Contribuição CBH (pp) ao YoY por D1 × Região — LA no Norte: +50,4 pp",
    "Large Appliances no Norte cresceu 93,7% YoY, e mais da metade (+50,4 pp) veio da CBH. Esse é o caso extremo da combinação 'produto pesado + região mal servida' onde só a CBH conseguia operar. TVs tem efeito mais homogêneo entre regiões.",
    "Heatmap (mapa de calor) com cores graduadas",
    df,
    "Linhas = D1. Colunas = Região (N, NE, CO, SE, S). Valores = contribuição CBH em pp do YoY. Cor mais quente = maior efeito.",
    "Sugestão: ordenar linhas por LA > TVs > SmlApp > demais."
)

# ======================================================================
# ABA 07 — D2 ACELERACAO
# ======================================================================
ws = wb.create_sheet("07_D2_aceleracao")
df = d2g.copy()
df = df.sort_values('Contrib_CBH_pp', ascending=False)
df = df.rename(columns={
    'D2':'D2',
    'NMV25_Mi':'NMV 25 (R$ Mi)',
    'NMV26_Mi':'NMV 26 (R$ Mi)',
    'NMV26_CBH_Mi':'NMV CBH 26 (R$ Mi)',
    'YoY_total':'YoY total (%)',
    'YoY_exCBH':'YoY ex-CBH (%)',
    'Contrib_CBH_pp':'Contrib CBH (pp)',
    'Share_CBH_pct':'Share CBH na D2 (%)'
})
write_aba(ws,
    "Camada 5 · Quais D2 mais aceleraram",
    "Contribuição CBH ao YoY por D2 — 1/3 do growth de Laundry e Refrigeration veio da CBH",
    "Laundry & Dishwashers (+33,1 pp) e Refrigeration (+31,5 pp) são onde a CBH mais alavancou — exatamente categorias onde frete grátis nacional é determinante (produto pesado, caro, sem capilaridade local). Built In já vinha em rampa orgânica forte (+42,9% ex-CBH).",
    "Barras horizontais empilhadas (YoY ex-CBH + Contrib CBH)",
    df,
    "Eixo Y = D2. Eixo X = YoY %. Empilhar 2 séries: YoY ex-CBH + Contrib CBH.",
    "Sugestão: top 8 D2s por Contrib CBH desc. Inclui caso 'Built In' como contraponto (cresceu organicamente)."
)

# ======================================================================
# ABA 08 — 4 MECANISMOS DO GROWTH (revisado 28-mai)
# ======================================================================
ws = wb.create_sheet("08_Mecanismos_growth")
df = pd.DataFrame({
    'Mecanismo': [
        'Capilaridade PURA (cat com volume + CBH expandiu UFs)',
        'Coexistência (cat com volume + CBH não expandiu UFs)',
        'Reativação dormentes (NMV pré <R$ 100K)',
        'Sortimento novo (Tipo B — catálogo novo em MELI)',
        'Fora de catálogo (anúncios livres sem product_id)',
    ],
    'NMV CBH (R$ Mi)': [347.8, 209.5, 109.9, 73.0, 140.0],
    'Share do NMV CBH (%)': [39.5, 23.8, 12.5, 8.3, 15.9],
    '# Catálogos': [208, 887, 307, 164, '—'],
    'Descrição': [
        'Catálogo com NMV pré ≥R$ 100K + ufs_cbh_pos > qt_ufs_pre. Capilaridade genuína em produto com volume',
        'Catálogo com NMV pré ≥R$ 100K + ufs_cbh_pos ≤ qt_ufs_pre. CBH apenas competiu junto',
        '307 cat com NMV pré combinado R$ 7,7 Mi → R$ 110 Mi pós (multiplicador médio 15x). Reativação de estoque parado',
        '164 cat nunca vendidos em MELI antes da CBH. Sortimento incremental puro',
        'ITEM_ID sem product_id (não disputa Buy Box) — anúncios próprios CBH',
    ]
})
write_aba(ws,
    "Camada 6 · Como cresceu (4 mecanismos)",
    "4 mecanismos do growth CBH — sem dupla contagem · Total: R$ 880 Mi",
    "REVISÃO 28-mai: a versão anterior contava 'Capilarização R$ 456 Mi' que incluía 84 catálogos dormentes em dupla contagem com 'Reativação'. Reclassificação correta abaixo. Capilaridade pura é R$ 348 Mi (39,5% do NMV CBH) — produto com volume real que a CBH levou a mais UFs. Continua sendo o maior mecanismo.",
    "Barras horizontais ordenadas (5 segmentos) ou waterfall do NMV total CBH",
    df,
    "Eixo Y = Mecanismo. Eixo X = NMV CBH (R$ Mi).",
    "Soma: 347,8 + 209,5 + 109,9 + 73,0 + 140,0 = 880,2 Mi = NMV CBH HE total. Mecanismos mutuamente exclusivos, sem sobreposição."
)

# ======================================================================
# ABA 09 — CAPILARIDADE PURA (nova)
# ======================================================================
ws = wb.create_sheet("09_Capilaridade_pura")
df = pd.DataFrame({
    'Bucket UFs pré do catálogo': ['6-15 UFs (nacional médio)', '16-26 UFs (quase full)', '1-5 UFs com volume'],
    'Qt catálogos': [91, 114, 3],
    'NMV CBH (R$ Mi)': [112.4, 235.3, 0.1],
    'Share da capilaridade pura (%)': [32.3, 67.6, 0.1],
    'Interpretação': [
        'Produto que vendia em 6-15 UFs e CBH levou para mais — capilaridade clássica',
        'Produto quase full nacional onde a CBH fechou as UFs que faltavam',
        'Irrelevante em volume — quase todos os 84 catálogos com 1-5 UFs pré eram dormentes',
    ]
})
write_aba(ws,
    "Camada 6 · Capilaridade pura",
    "Capilaridade genuína: 208 catálogos com volume real onde CBH expandiu UFs — R$ 348 Mi (39,5%)",
    "Esse é o mecanismo principal do valor CBH. Filtro: catálogos com NMV pré ≥R$ 100K (vendiam algo de verdade) E CBH vendeu em mais UFs do que cobriam antes. Concentrado em catálogos com 6-26 UFs pré — produtos quase-nacionais que a CBH completou.",
    "Barras horizontais (3 segmentos) ou stacked column",
    df,
    "Eixo Y = Bucket UFs pré. Eixo X = NMV CBH (R$ Mi).",
    "Critério de 'volume real': NMV pré combinado ≥ R$ 100K em 22 meses. Critério de 'expandiu': ufs_cbh_pos > qt_ufs_pre."
)

# ======================================================================
# ABA 10 — DORMENTES PERFIL (revisado: D2 + Marcas)
# ======================================================================
ws = wb.create_sheet("10_Dormentes_perfil")
df_d2 = pd.DataFrame({
    'D2': ['TELEVISIONS', 'REFRIGERATION', 'BUILT IN', 'KITCHEN', 'HOUSING & CLEANING',
           'LAUNDRY & DISHWASHERS', 'AUDIO', 'COOLING'],
    'Qt cat. dormentes': [25, 75, 25, 86, 37, 21, 11, 24],
    'NMV pré 22m (R$ Mi)': [0.81, 1.03, 0.85, 2.35, 1.05, 0.60, 0.46, 0.49],
    'NMV CBH pós 6m (R$ Mi)': [42.6, 41.5, 8.8, 7.4, 4.1, 2.4, 2.3, 0.7],
    'Multiplicador médio': ['52x', '40x', '10x', '3x', '4x', '4x', '5x', '2x'],
})
write_aba(ws,
    "Camada 6 · Dormentes reativados — quem ganhou voz",
    "307 catálogos dormentes (R$ 7,7 Mi pré) → R$ 110 Mi pós · Televisions + Refrigeration = 76% do volume",
    "Categorias mais beneficiadas pela reativação: Televisions (25 cat → R$ 42,6 Mi, mult 52x) e Refrigeration (75 cat → R$ 41,5 Mi, mult 40x). Juntas concentram R$ 84 Mi dos R$ 110 Mi (76%). São exatamente as categorias onde frete grátis nacional é decisivo.",
    "Barras horizontais por D2 (NMV CBH pós) + label com multiplicador",
    df_d2,
    "Eixo Y = D2. Eixo X = NMV CBH pós (R$ Mi). Label: multiplicador.",
    "Multiplicador = NMV CBH 6m / NMV pré 22m. Não é growth rate puro porque períodos diferem."
)

# Segunda tabela na mesma aba — Marcas
start_row = 6 + 9 + 4
ws.cell(row=start_row, column=1, value="Top marcas que mais avançaram (dormentes reativados)").font = Font(name='Calibri', bold=True, size=12, color='1A1A1A')
df_marca = pd.DataFrame({
    'Marca': ['Consul', 'Hisense', 'Philips', 'Electrolux', 'Philco', 'Brastemp', 'Esmaltec', 'Samsung', 'LG', 'TCL'],
    'Qt cat. dormentes': [20, 14, 4, 37, 30, 17, 4, 12, 18, 5],
    'NMV pré 22m (R$ mil)': [160, 200, 98, 1029, 667, 85, 211, 502, 793, 184],
    'NMV CBH pós 6m (R$ Mi)': [23.1, 17.0, 14.8, 10.0, 6.2, 5.7, 5.2, 4.8, 4.4, 3.9],
})
headers_m = list(df_marca.columns)
for c_idx, col in enumerate(headers_m, start=1):
    cell = ws.cell(row=start_row+1, column=c_idx, value=col)
    cell.font = FONT_LABEL; cell.fill = FILL_HEADER; cell.border = BORDER_THIN
    cell.alignment = Alignment(horizontal='center')
for r_idx, row in enumerate(df_marca.itertuples(index=False), start=start_row+2):
    for c_idx, val in enumerate(row, start=1):
        cell = ws.cell(row=r_idx, column=c_idx, value=val)
        cell.font = FONT_BODY
        cell.border = BORDER_THIN

# Notas na aba 10
nota_row = start_row + len(df_marca) + 3
ws.cell(row=nota_row, column=1, value="Casos individuais extremos (top 5 catálogos dormentes):").font = Font(name='Calibri', bold=True, size=11, color='1A1A1A')
casos = [
    "Hisense TV 53505423: R$ 7.564 em 22m → R$ 8,3 Mi em 6m (mult 1.096x)",
    "Philips TV 52714724: R$ 46 mil → R$ 10,5 Mi (mult 227x)",
    "Consul Refrig 52458477: R$ 17 mil → R$ 5,8 Mi (mult 337x)",
    "Consul Refrig 52435146: R$ 19 mil → R$ 4,9 Mi (mult 262x)",
    "Philips TV 57723340: R$ 0 → R$ 4,3 Mi (não vendia nada antes)",
]
for i, c in enumerate(casos):
    ws.cell(row=nota_row+1+i, column=1, value="· " + c).font = FONT_SUB
    ws.merge_cells(start_row=nota_row+1+i, start_column=1, end_row=nota_row+1+i, end_column=6)
ws.column_dimensions['A'].width = 32

# ======================================================================
# ABA 10 — TIPO A vs B
# ======================================================================
ws = wb.create_sheet("11_Tipo_AB_sortimento")
df = pd.DataFrame({
    'Tipo de catálogo': [
        'A — Catálogo já existia em MELI',
        'B — Catálogo NOVO em MELI (sortimento incremental)',
    ],
    'Qt catálogos': [1402, 164],
    'Share Qt (%)': [89.5, 10.5],
    'NMV CBH (R$ Mi)': [667.2, 73.0],
    'Share NMV (%)': [90.1, 9.9],
})
write_aba(ws,
    "Camada 6 · Sortimento novo vs existente",
    "90% do NMV CBH veio de catálogos já existentes — não trouxe sortimento massivamente novo",
    "Apenas 164 catálogos (10,5%) eram totalmente novos em MELI, gerando R$ 73 Mi (9,9% do NMV em catálogo). A grande maioria do valor veio de catálogos pré-existentes — a CBH não inventou produto, executou melhor o existente.",
    "Pizza / donut ou 2 barras",
    df,
    notas="Universo: 1.566 catálogos com product_id (R$ 740 Mi de R$ 880 Mi)."
)

# ======================================================================
# ABA 11 — PERFIL PRE
# ======================================================================
ws = wb.create_sheet("12_Perfil_pre_cat")
df = pd.DataFrame({
    'Perfil pré-CBH no catálogo': [
        'Catálogo tinha 1P MELI vendendo',
        'Catálogo tinha Tienda Oficial (sem 1P)',
        'Catálogo novo em MELI',
        'Só Seller Dev (Long Tail / Midtail 3P)',
    ],
    'Qt catálogos': [951, 415, 164, 36],
    'Share Qt (%)': [60.7, 26.5, 10.5, 2.3],
    'NMV CBH (R$ Mi)': [469.6, 195.2, 73.0, 2.4],
    'Share NMV (%)': [63.4, 26.4, 9.9, 0.3],
})
write_aba(ws,
    "Camada 7 · NÃO foi território abandonado",
    "Onde a CBH entrou — 87% do NMV em catálogos com 1P ou TO já operando",
    "A CBH NÃO entrou em territórios fracos. 87% do NMV vem de catálogos onde já havia 1P MELI (63%) ou Tienda Oficial (26%). Apenas 0,3% (R$ 2,4 Mi) vem de catálogos com só sellers dev. Em TVs, ZERO catálogos eram 'só dev'.",
    "Barras horizontais ordenadas",
    df,
    "Eixo Y = Perfil pré. Eixo X = NMV CBH (R$ Mi) ou % share NMV.",
    "Insight: o valor CBH é capilaridade + execução em catálogos disputados, NÃO substituição de sellers fracos."
)

# ======================================================================
# ABA 12 — CANIBALIZACAO SELLERS
# ======================================================================
ws = wb.create_sheet("13_Canibalizacao_sellers")
df = sellers_canib.head(10).copy()
df.columns = ['Seller', 'Catálogos perdeu BB', 'Perda NMV (R$ Mi)', 'NMV pré taxa 6m (R$ Mi)', 'NMV pós (R$ Mi)', 'NMV CBH capturada (R$ Mi)']
write_aba(ws,
    "Camada 8 · Quem perdeu",
    "Top 10 sellers que perderam BB pra CBH — canibalização modesta e pulverizada",
    "Soma da perda agregada dos top sellers afetados = −R$ 76 Mi vs taxa pré projetada. O 1P MELI é o mais afetado (−R$ 50,7 Mi nesse filtro). Demais são pulverizados — não há 'vilão' único. Net incremental estimado do CBH: ~R$ 800 Mi (90% do NMV CBH).",
    "Barras horizontais com valores negativos (perdas)",
    df,
    "Eixo Y = Seller. Eixo X = Perda NMV (negativo). Adicionar # catálogos como label.",
    "Filtro: top 10 sellers cuja perda em NMV pós (real) vs taxa pré projetada (NMV pré 22m ÷ 22 × 6) é mais negativa. Apenas catálogos Tipo A com NMV pré > R$ 100K."
)

# ======================================================================
# ABA 13 — 1P MELI DEEP
# ======================================================================
ws = wb.create_sheet("14_1P_MELI_deep")
df = pd.DataFrame({
    'D1': ['LARGE APPLIANCES', 'SMALL APPLIANCES', 'AUDIO & GENERAL ELECTRONICS', 'HEATING, COOLING & AIR QUALITY', 'TELEVISIONS & STREAMING DEVICES'],
    'Qt catálogos onde 1P perdeu BB': [59, 45, 1, 1, 22],
    'Δ NMV 1P (R$ Mi)': [-9.0, -2.4, -0.15, 0.54, 7.71],
    'NMV CBH capturada (R$ Mi)': [88.9, 19.9, 0.18, 2.96, 53.9],
})
df.loc[len(df)] = ['TOTAL (128 catálogos universo completo)', 128, -3.3, 165.8]
write_aba(ws,
    "Camada 8 · Caso especial 1P MELI",
    "1P MELI: −R$ 3,3 Mi líquido — perdeu em LA mas CRESCEU em TVs",
    "Universo completo (128 catálogos onde 1P era top pré e CBH virou top pós): NMV 1P pré projetado 6m = R$ 82 Mi, real pós = R$ 62,8 Mi, Δ líquido = −R$ 3,3 Mi. Por D1: 1P perdeu R$ 9 Mi em LA e R$ 2,4 Mi em Small App, mas CRESCEU +R$ 7,7 Mi em TVs (carregado pelo growth orgânico forte). Canibalização do 1P é muito menor que o aparente.",
    "Barras horizontais por D1 com valores positivos e negativos",
    df,
    "Eixo Y = D1. Eixo X = Δ NMV 1P (R$ Mi). Mostrar barra negativa em laranja, positiva em verde.",
    "Cálculo: Δ = NMV 1P real pós 6m − NMV 1P pré projetado pra 6m equivalentes (NMV pré 22m ÷ 22 × 6)."
)

# ======================================================================
# ABA 14 — EVOLUTIVO MENSAL
# ======================================================================
ws = wb.create_sheet("15_Evolutivo_mensal")
df = evol[['Mes','BR']].copy()
cbh_dict = dict(zip(cbh_mens['Mes'], cbh_mens['BR']))
df['NMV CBH BR (R$ Mi)'] = df['Mes'].map(cbh_dict).fillna(0)
df['NMV ex-CBH BR (R$ Mi)'] = df['BR'] - df['NMV CBH BR (R$ Mi)']
df = df.rename(columns={'Mes':'Mês', 'BR':'NMV total BR (R$ Mi)'})
df = df[['Mês', 'NMV ex-CBH BR (R$ Mi)', 'NMV CBH BR (R$ Mi)', 'NMV total BR (R$ Mi)']]
write_aba(ws,
    "Camada 9 · Tendência temporal",
    "Evolutivo mensal NMV HE BR (R$) — inflexão pós-nov/25 e aceleração mantida em mai/26",
    "Série mensal jan/2024 → mai/2026* mostrando inflexão clara no mês da entrada CBH e aceleração mantida em maio/2026 (1-27 dias, parcial).",
    "Área empilhada (stacked area) ou linha + barras",
    df,
    "Eixo X = Mês. Eixo Y = R$ Mi. Séries empilhadas: ex-CBH (base) + CBH (topo). Marcar nov/25 com linha vertical destacando entrada.",
    "*mai/26 cobre 1-27 dias (período parcial). Run-rate estimado para 31 dias: ~R$ 2,29 Bi."
)

# ======================================================================
# ABA 15 — SHARE CBH MAIO
# ======================================================================
ws = wb.create_sheet("16_Share_CBH_maio")
df = pd.DataFrame({
    'Região': ['Nordeste', 'Sudeste', 'Centro-Oeste', 'Sul', 'Norte'],
    'Share CBH abr/26 (%)': [10.5, 6.9, 7.7, 5.8, 10.3],
    'Share CBH mai/26* (%)': [13.9, 9.4, 9.7, 7.7, 11.5],
    'Δ pp': [3.4, 2.5, 2.0, 1.9, 1.2],
})
write_aba(ws,
    "Camada 9 · Aceleração recente",
    "Share CBH no NMV HE total por região — abr/26 → mai/26* (subiu em todas)",
    "A CBH não desacelerou — aumentou share em todas as 5 regiões em maio/26. Nordeste lidera o salto (+3,4 pp). Confirma que o efeito não foi 'novidade da entrada' que se acomoda — segue ganhando relevância no 7º mês de operação.",
    "Barras agrupadas (colunas pareadas) ou slope chart (linha conectando abr→mai por região)",
    df,
    "Eixo X = Região. Eixo Y = Share CBH (%). 2 séries: abril e maio*. Destacar Δ pp como label.",
    "*mai/26 = 1-27 dias. Tendência de aceleração apesar de mês parcial."
)

# ======================================================================
# ABA 16 — MARCAS
# ======================================================================
ws = wb.create_sheet("17_Marcas_aceleradas")
df = marcas[marcas['Contrib_CBH_pp'] > 0].sort_values('Contrib_CBH_pp', ascending=False).head(15).copy()
df = df.rename(columns={
    'brand':'Marca',
    'NMV25_Mi':'NMV 25 (R$ Mi)',
    'NMV26_Mi':'NMV 26 (R$ Mi)',
    'NMV26_exCBH_Mi':'NMV 26 ex-CBH (R$ Mi)',
    'NMV26_CBH_Mi':'NMV 26 CBH (R$ Mi)',
    'YoY_total_pct':'YoY total (%)',
    'YoY_exCBH_pct':'YoY ex-CBH (%)',
    'Contrib_CBH_pp':'Contrib CBH (pp)',
    'Share_CBH_pct':'Share CBH na marca (%)'
})
write_aba(ws,
    "Camada 10 · Marcas impulsionadas",
    "Top marcas aceleradas pela CBH — TCL dobrou, Samsung salva de queda",
    "Duas histórias-bomba pra negociação com fornecedor: (1) TCL cresceu +127% no MELI (dobrou) com 30% das vendas via CBH — argumento forte pro fabricante. (2) Samsung CAIRIA −5,2% sem CBH; com ela, cresce +10,3% — a CBH é hedge contra perda de marca estratégica. Marcas onde CBH é dominante no canal: Esmaltec (83% via CBH), Continental (65%), Colormaq (55%).",
    "Barras horizontais empilhadas (YoY ex-CBH + Contrib CBH) com share CBH como label",
    df,
    "Eixo Y = Marca (ordenado por Contrib CBH desc). Eixo X = YoY %. Marcas com YoY ex-CBH negativo (ex: Samsung) merecem destaque visual.",
    "Filtro: marcas com NMV25 ≥ R$ 5 Mi ou NMV CBH ≥ R$ 3 Mi. Top 15 por Contrib CBH."
)

# ======================================================================
# ABA 17 — SINTESE
# ======================================================================
ws = wb.create_sheet("18_Sintese")
df = pd.DataFrame({
    '#': [1, 2, 3, 4, 5],
    'Mensagem síntese': [
        'Casa Bahia adicionou +9,94 pp ao crescimento YoY do MELI HE em 6 meses (R$ 880 Mi NMV, ~R$ 800 Mi incrementais)',
        'Efeito 2,5x mais intenso em regiões antes mal servidas: Norte +17,3 pp, NE +15,8 pp vs Sul +7 pp',
        'Em LA no Norte, METADE do crescimento veio da CBH (+50,4 pp de +93,7% total)',
        '90% do NMV em catálogos JÁ existentes — valor é execução (frete + preço + capilaridade), não sortimento novo',
        'Canibalização modesta: 1P MELI sentiu −R$ 3,3 Mi líquido; tendência segue acelerando em mai/26'
    ]
})
write_aba(ws,
    "Camada 11 · Síntese executiva",
    "Resumo em 5 mensagens — para fechamento do deck",
    "Frase central proposta: 'A Casas Bahia foi 2,5x mais intensa em adicionar growth onde MELI tinha pior proposta de valor — operando em catálogos existentes via capilaridade + execução, não substituindo sellers. R$ 800 Mi incrementais ao MELI HE em 6 meses.'",
    "Slide de texto com 5 bullets numerados ou cards",
    df,
    notas="Sem gráfico — slide de fechamento textual."
)

# ======================================================================
# ABA 18 — FORA DE CATALOGO
# ======================================================================
ws = wb.create_sheet("19_OUTROS_fora_cat")
df = fora_em.copy()
df = df.rename(columns={
    'D1':'D1',
    'D2':'D2',
    'NMV_em_catalogo_Mi':'NMV em catálogo (R$ Mi)',
    'NMV_fora_catalogo_Mi':'NMV fora catálogo (R$ Mi)',
    'NMV_total_Mi':'NMV total (R$ Mi)',
    'Pct_fora_catalogo':'% fora catálogo'
})
write_aba(ws,
    "Outros achados · Fora de catálogo",
    "R$ 140 Mi (16%) do NMV CBH em anúncios livres — TVs lidera com 20,7%",
    "Item_ID sem product_id (não disputa BB). TVs tem 20,7% fora (R$ 70,6 Mi) — provavelmente bundles, configurações específicas ou estratégia de evitar BB com sellers que dominam. Built In: 15,3% fora (R$ 12 Mi) — vale auditar.",
    "Barras horizontais empilhadas (em catálogo + fora) com % fora como label",
    df,
    "Eixo Y = D2. Eixo X = NMV (R$ Mi). 2 séries empilhadas.",
    "Anúncios fora de catálogo são incrementais puros — não disputam BB com ninguém."
)

# ======================================================================
# ABA 19 — ASP
# ======================================================================
ws = wb.create_sheet("20_OUTROS_asp")
df = asp.copy()
df = df.rename(columns={
    'Bucket_ASP':'Faixa ASP (R$ por unidade)',
    'QtCatalogos':'Qt catálogos',
    'NMV_CBH_Mi':'NMV CBH (R$ Mi)',
    'Share_NMV':'Share NMV (%)'
})
write_aba(ws,
    "Outros achados · Faixa de preço",
    "66% do NMV CBH em ASP R$ 1k-5k — onde frete grátis e financiamento mais valem",
    "Concentração CBH em produtos de ticket médio-alto: TVs grandes, geladeira frost-free, lavadora 11-13kg, fogão 5 bocas, lava-louças. Faixa onde frete grátis + financiamento + capilaridade fazem mais diferença vs loja física.",
    "Pizza/donut OU colunas verticais ordenadas",
    df,
    "Eixo categórico = Bucket ASP. Valor = NMV CBH ou Share.",
    "ASP por catálogo = NMV CBH ÷ NSI CBH. Catálogos com NSI=0 excluídos."
)

# Salva
wb.active = 0
wb.save(TARGET)
print(f"\nOK: {TARGET}")
print(f"Tamanho: {TARGET.stat().st_size / 1024:.0f} KB")
print(f"Abas: {len(wb.sheetnames)}")
for s in wb.sheetnames:
    print(f"  · {s}")
