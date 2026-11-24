"""Gera deck principal (3 slides) + backup deck (5 slides) — paleta MELI."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

BASE = Path(r"C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-05-entrada-cbh-incrementalidade-regional")
OUT = BASE / "outputs"
TMP = OUT / "_pptx_tmp"
TMP.mkdir(exist_ok=True)

# === Paleta MELI ===
MELI_YELLOW = '#FFE600'   # Primária
YELLOW_2 = '#FFF176'      # Neutro 2
YELLOW_BASE = '#FFF59D'   # Neutro base
ORANGE = '#F9A825'        # Alerta
MUSTARD = '#9A7D0A'       # Secundária
BLACK = '#1A1A1A'
DARK_GREY = '#333333'
GREY = '#666666'
LIGHT_GREY = '#CCCCCC'
WHITE = '#FFFFFF'
BG_SOFT = '#FAFAF5'       # quase branco creme bem suave

plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 10.5,
    'axes.edgecolor': '#BBBBBB',
    'axes.linewidth': 0.5,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# ====================================================================
# Helpers PPTX
# ====================================================================
def add_text(slide, left, top, width, height, text, font_size=14, bold=False,
             color=DARK_GREY, align=PP_ALIGN.LEFT, font_name='Arial',
             anchor=MSO_ANCHOR.TOP, italic=False):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.margin_left = Inches(0.05); tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.02); tf.margin_bottom = Inches(0.02)
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.name = font_name
    r.font.size = Pt(font_size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = RGBColor.from_string(color.lstrip('#'))
    return tb

def add_rect(slide, left, top, width, height, fill_color=BLACK, line=False, line_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor.from_string(fill_color.lstrip('#'))
    if not line:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = RGBColor.from_string((line_color or LIGHT_GREY).lstrip('#'))
        shape.line.width = Pt(0.5)
    return shape

def add_header(slide, title, subtitle=None, slide_num=None, total=None):
    """Header preto com título amarelo accent"""
    add_rect(slide, 0, 0, 13.33, 1.0, BLACK)
    # Faixa amarela fina abaixo
    add_rect(slide, 0, 1.0, 13.33, 0.08, MELI_YELLOW)
    add_text(slide, 0.4, 0.16, 11.5, 0.5, title,
             font_size=20, bold=True, color=WHITE)
    if subtitle:
        add_text(slide, 0.4, 0.62, 11.5, 0.30, subtitle,
                 font_size=10, color=YELLOW_BASE)
    if slide_num and total:
        add_text(slide, 12.4, 0.16, 0.85, 0.4, f"{slide_num}/{total}",
                 font_size=11, color=MELI_YELLOW, align=PP_ALIGN.RIGHT, bold=True)

def add_kpi_card(slide, x, y, w, h, val, lbl, color=BLACK, bg=YELLOW_BASE):
    add_rect(slide, x, y, w, h, bg)
    add_text(slide, x, y+0.05, w, 0.5, val,
             font_size=22, bold=True, color=color, align=PP_ALIGN.CENTER)
    add_text(slide, x, y+0.50, w, 0.35, lbl,
             font_size=9, color=DARK_GREY, align=PP_ALIGN.CENTER)

def add_footer(slide, fonte_extra=""):
    add_rect(slide, 0, 7.30, 13.33, 0.20, '#F0F0F0')
    txt = f"Fonte: DM_EFICIENCIA_MLB · Análise: Beatriz Dacache · 28-mai-2026 · Limitação: correlacional (sem A/B teste). CBH = seller_id 1046986303."
    if fonte_extra:
        txt += f" {fonte_extra}"
    add_text(slide, 0.3, 7.31, 12.7, 0.18, txt,
             font_size=7, color=GREY)

# ====================================================================
# Carrega dados
# ====================================================================
print("Carregando dados...")
decomp = pd.read_csv(OUT / "etapa2_decomposicao_regional.csv", sep=';', decimal=',', encoding='utf-8')
marcas = pd.read_csv(OUT / "etapa4a_marcas_growth.csv", sep=';', decimal=',', encoding='utf-8')
d2g = pd.read_csv(OUT / "etapa4b_d2_growth.csv", sep=';', decimal=',', encoding='utf-8')
asp = pd.read_csv(OUT / "etapa4c_asp_buckets.csv", sep=';', decimal=',', encoding='utf-8')
evol = pd.read_csv(OUT / "etapa2_lente3_evolutivo_NMV_regiao.csv", sep=';', decimal=',', encoding='utf-8')
cbh_mens = pd.read_csv(OUT / "etapa2_lente3_evolutivo_NMV_CBH_regiao.csv", sep=';', decimal=',', encoding='utf-8')
share_cbh = pd.read_csv(OUT / "etapa2_lente3_share_CBH_regiao.csv", sep=';', decimal=',', encoding='utf-8')
contrib_pp = pd.read_csv(OUT / "etapa2_lente1_contribCBH_pp_D1xRegiao.csv", sep=';', decimal=',', encoding='utf-8')
fora_em = pd.read_csv(OUT / "etapa3e_fora_vs_em_catalogo.csv", sep=';', decimal=',', encoding='utf-8')
sellers_canib = pd.read_csv(OUT / "etapa3c_sellers_canibalizados.csv", sep=';', decimal=',', encoding='utf-8')

# ====================================================================
# CHARTS
# ====================================================================
def save_chart(fig, name):
    fig.savefig(TMP / name, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"OK {name}")

# === CHART D1_decomposicao: barras horizontais decomposição BR ===
fig, ax = plt.subplots(figsize=(7.5, 3.2), dpi=150)
d = decomp.sort_values('Contrib_total_pp_BR', ascending=True)
y = np.arange(len(d))
ax.barh(y, d['Contrib_exCBH_pp_BR'], color=MUSTARD, height=0.62, label='Crescimento orgânico (ex-CBH)')
ax.barh(y, d['Contrib_CBH_pp_BR'], left=d['Contrib_exCBH_pp_BR'], color=MELI_YELLOW,
        edgecolor=BLACK, linewidth=0.8, height=0.62, label='Contribuição CBH')
for i, (e, c) in enumerate(zip(d['Contrib_exCBH_pp_BR'], d['Contrib_CBH_pp_BR'])):
    tot = e + c
    ax.text(tot + 0.4, i, f'  {tot:.2f} pp  (CBH +{c:.2f})', va='center',
            fontsize=10.5, color=BLACK, fontweight='bold')
ax.set_yticks(y)
ax.set_yticklabels(d['Regiao'], fontsize=11, fontweight='bold')
ax.set_xticks([])
ax.set_xlim(0, 24)
ax.spines['bottom'].set_visible(False); ax.spines['left'].set_visible(False)
ax.tick_params(left=False)
ax.legend(loc='lower right', fontsize=9.5, frameon=False)
ax.set_title('Cada região contribuiu quanto pp para o YoY BR de +40,86%?',
             fontsize=11.5, fontweight='bold', color=BLACK, loc='left', pad=10)
plt.tight_layout()
save_chart(fig, 's1_decomposicao.png')

# === CHART regional contrib (slide 2) ===
fig, ax = plt.subplots(figsize=(6.4, 2.6), dpi=150)
regs = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
contrib = [17.3, 15.8, 11.1, 8.8, 7.0]
yoy_excbh = [45.9, 48.6, 36.8, 25.0, 30.6]
y = np.arange(len(regs))
ax.barh(y, yoy_excbh, color=MUSTARD, height=0.62, label='YoY orgânico (ex-CBH)')
ax.barh(y, contrib, left=yoy_excbh, color=MELI_YELLOW, edgecolor=BLACK, linewidth=0.8,
        height=0.62, label='Contribuição CBH')
for i, (e, c) in enumerate(zip(yoy_excbh, contrib)):
    tot = e + c
    ax.text(tot + 1.5, i, f'{tot:.1f}% (CBH +{c:.1f}pp)', va='center',
            fontsize=10, color=BLACK, fontweight='bold')
ax.set_yticks(y); ax.set_yticklabels(regs, fontsize=10.5, fontweight='bold')
ax.invert_yaxis()
ax.set_xticks([]); ax.set_xlim(0, 90)
ax.spines['bottom'].set_visible(False); ax.spines['left'].set_visible(False)
ax.tick_params(left=False)
ax.legend(loc='lower center', fontsize=9, frameon=False, ncol=2, bbox_to_anchor=(0.5, -0.18))
ax.set_title('Crescimento YoY fev-abr/26 vs fev-abr/25 — com vs sem CBH',
             fontsize=11, fontweight='bold', color=BLACK, loc='left', pad=8)
plt.tight_layout()
save_chart(fig, 's2_regional.png')

# === CHART evolutivo (slide 2) ===
evol_br = evol[['Mes','BR']].copy()
cbh_dict = dict(zip(cbh_mens['Mes'], cbh_mens['BR']))
evol_br['BR_CBH'] = evol_br['Mes'].map(cbh_dict).fillna(0)
evol_br['BR_exCBH'] = evol_br['BR'] - evol_br['BR_CBH']

fig, ax = plt.subplots(figsize=(6.4, 2.6), dpi=150)
x = range(len(evol_br))
ax.fill_between(x, 0, evol_br['BR_exCBH'], color=MUSTARD, alpha=0.85, label='NMV ex-CBH')
ax.fill_between(x, evol_br['BR_exCBH'], evol_br['BR'], color=MELI_YELLOW, alpha=1.0, label='NMV CBH')
ax.plot(x, evol_br['BR'], color=BLACK, linewidth=1.5)

nov25_idx = list(evol_br['Mes']).index('2025-11')
ax.axvline(nov25_idx, color=ORANGE, linewidth=2.5, linestyle='--', alpha=0.9)
ax.annotate('Entrada CBH\n(nov/25)', xy=(nov25_idx, evol_br['BR'].max()*0.92),
            xytext=(nov25_idx-3.5, evol_br['BR'].max()*0.95),
            fontsize=9, color=BLACK, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=ORANGE, edgecolor='none', alpha=0.95))

n = len(evol_br)
labels = []
for i, m in enumerate(evol_br['Mes']):
    if i == n - 1 and m.endswith('*'):
        labels.append(m)
    elif (i % 4 == 0) and (i < n - 2):
        labels.append(m)
    else:
        labels.append('')
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8, rotation=0)
ax.set_yticks([0, 1000, 2000, 3000])
ax.set_yticklabels(['0', '1 Bi', '2 Bi', '3 Bi'], fontsize=8)
ax.set_ylim(0, 3200)
ax.legend(loc='upper left', fontsize=9, frameon=False)
ax.set_title('Evolução mensal NMV HE BR (R$) — inflexão pós-nov/25 (*mai/26 = 1-27 dias)',
             fontsize=10, fontweight='bold', color=BLACK, loc='left', pad=8)
ax.grid(axis='y', alpha=0.2)
plt.tight_layout()
save_chart(fig, 's2_evolutivo.png')

# === CHART heatmap D1 x Região (slide 2) ===
fig, ax = plt.subplots(figsize=(6.4, 2.5), dpi=150)
d1_ord = ['LA','TVs','SmlApp','Audio','H/C','Parts']
reg_ord = ['N','NE','CO','SE','S']
mat = []
for d1n in d1_ord:
    row = contrib_pp[contrib_pp['D1']==d1n]
    if len(row) > 0:
        mat.append([row[reg_ord[0]].values[0], row[reg_ord[1]].values[0],
                    row[reg_ord[2]].values[0], row[reg_ord[3]].values[0], row[reg_ord[4]].values[0]])
mat = np.array(mat)
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('meli', ['#FFFFFF', YELLOW_BASE, MELI_YELLOW, ORANGE, MUSTARD])
im = ax.imshow(mat, cmap=cmap, vmin=0, vmax=55, aspect='auto')
for i in range(len(d1_ord)):
    for j in range(len(reg_ord)):
        v = mat[i, j]
        txt_color = BLACK if v < 30 else WHITE
        ax.text(j, i, f'{v:.1f}', ha='center', va='center',
                color=txt_color, fontsize=10, fontweight='bold')
ax.set_xticks(range(len(reg_ord))); ax.set_xticklabels(reg_ord, fontsize=10, fontweight='bold')
ax.set_yticks(range(len(d1_ord))); ax.set_yticklabels(d1_ord, fontsize=10, fontweight='bold')
ax.set_title('Contribuição CBH (pp) ao YoY por D1 × Região — LA no Norte: +50,4 pp',
             fontsize=10.5, fontweight='bold', color=BLACK, loc='left', pad=8)
plt.tight_layout()
save_chart(fig, 's2_heatmap.png')

# === CHART mecanismos (slide 3) — 4 mecanismos limpos ===
fig, ax = plt.subplots(figsize=(7.0, 3.0), dpi=150)
mecanismos = [
    ('Capilaridade pura\n(catálogos com volume + CBH expandiu UFs)', 347.8, MELI_YELLOW, '39,5%'),
    ('Coexistência\n(catálogos consolidados, CBH não dominou)', 209.5, YELLOW_2, '23,8%'),
    ('Fora de catálogo\n(anúncios livres CBH)', 140.0, '#E8E8E8', '15,9%'),
    ('Reativação de dormentes\n(NMV pré <R$ 100K)', 109.9, YELLOW_BASE, '12,5%'),
    ('Sortimento novo (Tipo B)\n(catálogo nunca vendido em MELI)', 73.0, ORANGE, '8,3%'),
]
y = np.arange(len(mecanismos))
sizes = [m[1] for m in mecanismos]
colors = [m[2] for m in mecanismos]
labels = [m[0] for m in mecanismos]
pcts = [m[3] for m in mecanismos]
ax.barh(y, sizes, color=colors, edgecolor=BLACK, linewidth=0.8, height=0.66)
for i, (s, p) in enumerate(zip(sizes, pcts)):
    ax.text(s + 6, i, f'R$ {s:.1f} Mi  ({p})', va='center', fontsize=10.5,
            color=BLACK, fontweight='bold')
ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9.5, fontweight='bold')
ax.invert_yaxis()
ax.set_xticks([]); ax.set_xlim(0, 500)
ax.spines['bottom'].set_visible(False); ax.spines['left'].set_visible(False)
ax.tick_params(left=False)
ax.set_title('Os 5 mecanismos do growth CBH (sem dupla contagem) — Total: R$ 880 Mi',
             fontsize=10.5, fontweight='bold', color=BLACK, loc='left', pad=10)
plt.tight_layout()
save_chart(fig, 's3_mecanismos.png')

# === CHART marcas + D2 (slide 3) ===
fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8), dpi=150)

ax = axes[0]
d2_names = ['Laundry & D.', 'Refrigeration', 'Televisions', 'Built In', 'Kitchen']
d2_contrib = [33.1, 31.5, 23.5, 9.1, 8.6]
d2_yoy_ex = [69.2, 30.8, 26.5, 42.9, 36.3]
y = np.arange(len(d2_names))
ax.barh(y, d2_yoy_ex, color=MUSTARD, height=0.65)
ax.barh(y, d2_contrib, left=d2_yoy_ex, color=MELI_YELLOW, edgecolor=BLACK, linewidth=0.6, height=0.65)
for i, (e, c) in enumerate(zip(d2_yoy_ex, d2_contrib)):
    ax.text(e+c+1.5, i, f'+{c:.1f}pp', va='center', fontsize=9, color=BLACK, fontweight='bold')
ax.set_yticks(y); ax.set_yticklabels(d2_names, fontsize=9.5)
ax.invert_yaxis()
ax.set_xticks([]); ax.set_xlim(0, 118)
ax.spines['bottom'].set_visible(False); ax.spines['left'].set_visible(False)
ax.tick_params(left=False)
ax.set_title('Contribuição CBH ao YoY por D2', fontsize=10.5, fontweight='bold', color=BLACK, loc='left')

ax = axes[1]
brand_names = ['TCL', 'Consul', 'Philips', 'Brastemp', 'LG', 'Mondial', 'Britânia', 'Samsung']
brand_contrib = [68.2, 42.1, 34.8, 26.4, 23.0, 22.8, 21.8, 15.5]
brand_share = [30.1, 20.9, 19.3, 14.1, 17.4, 13.0, 16.5, 14.1]
y = np.arange(len(brand_names))
ax.barh(y, brand_contrib, color=MELI_YELLOW, edgecolor=BLACK, linewidth=0.6, height=0.65)
for i, (c, s) in enumerate(zip(brand_contrib, brand_share)):
    ax.text(c+1.5, i, f'+{c:.1f}pp ({s:.0f}% da marca via CBH)', va='center', fontsize=8.5, color=BLACK)
ax.set_yticks(y); ax.set_yticklabels(brand_names, fontsize=9.5, fontweight='bold')
ax.invert_yaxis()
ax.set_xticks([]); ax.set_xlim(0, 145)
ax.spines['bottom'].set_visible(False); ax.spines['left'].set_visible(False)
ax.tick_params(left=False)
ax.set_title('Marcas mais impulsionadas pela CBH', fontsize=10.5, fontweight='bold', color=BLACK, loc='left')
plt.tight_layout()
save_chart(fig, 's3_d2_marcas.png')

# === BACKUP charts ===
# B1 — Metodologia visual (simples timeline)
fig, ax = plt.subplots(figsize=(11.5, 2.2), dpi=150)
ax.set_xlim(0, 28); ax.set_ylim(0, 3)
ax.axis('off')
# Eixo do tempo
ax.annotate('', xy=(27.5, 1.5), xytext=(0.5, 1.5), arrowprops=dict(arrowstyle='->', lw=1.5, color=BLACK))
meses_marc = ['jan/24','ago/25','out/25','nov/25','fev/26','abr/26','mai/26*']
positions = [0.5, 19, 21, 22, 25, 27, 27.5]
for m, p in zip(meses_marc, positions):
    ax.plot(p, 1.5, 'o', color=BLACK, markersize=5)
    ax.text(p, 1.2, m, ha='center', fontsize=9, color=BLACK)
# Anotação entrada CBH
ax.axvline(22, ymin=0.3, ymax=0.8, color=ORANGE, linewidth=3)
ax.text(22, 2.3, 'ENTRADA CBH\nnov/25', ha='center', fontsize=10, fontweight='bold', color=BLACK,
        bbox=dict(boxstyle='round,pad=0.3', facecolor=ORANGE, edgecolor='none'))
# Lentes
ax.add_patch(mpatches.FancyBboxPatch((19, 0.2), 2, 0.6, boxstyle='round,pad=0.05', facecolor=YELLOW_BASE, edgecolor=BLACK, linewidth=0.6))
ax.text(20, 0.5, 'L2 PRÉ\nago-out/25', ha='center', va='center', fontsize=8, color=BLACK, fontweight='bold')
ax.add_patch(mpatches.FancyBboxPatch((25, 0.2), 2, 0.6, boxstyle='round,pad=0.05', facecolor=MELI_YELLOW, edgecolor=BLACK, linewidth=0.6))
ax.text(26, 0.5, 'L1 + L2 PÓS\nfev-abr/26', ha='center', va='center', fontsize=8, color=BLACK, fontweight='bold')
plt.tight_layout()
save_chart(fig, 'b1_timeline.png')

# B2 — Perfil pré (barras)
fig, ax = plt.subplots(figsize=(7.5, 3.2), dpi=150)
perfis = ['C — Catálogo tinha 1P\nMELI vendendo', 'B — Catálogo tinha\nTienda Oficial', 'B_NOVO — Catálogo\nnovo em MELI', 'A — Só Seller Dev\n(LongTail / Midtail)']
qts = [951, 415, 164, 36]
nmvs = [469.6, 195.2, 73.0, 2.4]
y = np.arange(len(perfis))
ax.barh(y, nmvs, color=[MELI_YELLOW, YELLOW_2, YELLOW_BASE, ORANGE],
        edgecolor=BLACK, linewidth=0.8, height=0.62)
for i, (q, n) in enumerate(zip(qts, nmvs)):
    pct = n / sum(nmvs) * 100
    ax.text(n + 10, i, f'R$ {n} Mi ({pct:.1f}%)  |  {q} catálogos', va='center',
            fontsize=10.5, color=BLACK, fontweight='bold')
ax.set_yticks(y); ax.set_yticklabels(perfis, fontsize=10, fontweight='bold')
ax.invert_yaxis()
ax.set_xticks([]); ax.set_xlim(0, 700)
ax.spines['bottom'].set_visible(False); ax.spines['left'].set_visible(False)
ax.tick_params(left=False)
ax.set_title('Onde a CBH entrou: 87% do NMV veio de catálogos com 1P ou TO (NÃO foi território abandonado)',
             fontsize=10.5, fontweight='bold', color=BLACK, loc='left', pad=10)
plt.tight_layout()
save_chart(fig, 'b2_perfil_pre.png')

# B3 — Canibalização (recarrega CSV atualizado)
sellers_canib = pd.read_csv(OUT / "etapa3c_sellers_canibalizados.csv", sep=';', decimal=',', encoding='utf-8')
fig, ax = plt.subplots(figsize=(7.5, 3.6), dpi=150)
sc = sellers_canib.head(10).copy()
sc = sc.sort_values('Perda_NMV_Mi')
# Encurta nomes muito longos
sc['Seller_curto'] = sc['Seller'].apply(lambda s: s[:25] + '...' if len(s) > 25 else s)
y = np.arange(len(sc))
min_p = sc['Perda_NMV_Mi'].min()
ax.barh(y, sc['Perda_NMV_Mi'], color=ORANGE, edgecolor=BLACK, linewidth=0.6, height=0.62)
for i, (p, n) in enumerate(zip(sc['Perda_NMV_Mi'], sc['Catalogos_perdeu_BB'])):
    ax.text(p - 1.2, i, f'R$ {p:.1f} Mi ({n} cat.)', va='center', ha='right',
            fontsize=9, color=BLACK, fontweight='bold')
ax.set_yticks(y); ax.set_yticklabels(sc['Seller_curto'], fontsize=9, fontweight='bold')
ax.invert_yaxis()
ax.set_xlim(min_p * 1.25, 1)
ax.set_xticks([])
ax.spines['bottom'].set_visible(False); ax.spines['left'].set_visible(False)
ax.tick_params(left=False)
ax.set_title('Top 10 sellers que perderam BB para a CBH — perda vs taxa pré projetada 6m',
             fontsize=10.5, fontweight='bold', color=BLACK, loc='left', pad=10)
plt.tight_layout()
save_chart(fig, 'b3_canib.png')

# B4 — Marcas top 12 (mais legível)
fig, ax = plt.subplots(figsize=(9.5, 6.5), dpi=140)
m = marcas[marcas['Contrib_CBH_pp'] > 0].sort_values('Contrib_CBH_pp', ascending=True).tail(12)
y = np.arange(len(m))
ax.barh(y, m['YoY_exCBH_pct'], color=MUSTARD, height=0.70, label='YoY ex-CBH (orgânico)')
ax.barh(y, m['Contrib_CBH_pp'], left=m['YoY_exCBH_pct'], color=MELI_YELLOW,
        edgecolor=BLACK, linewidth=0.8, height=0.70, label='Contribuição CBH (pp)')
for i, row in enumerate(m.itertuples()):
    tot = row.YoY_exCBH_pct + row.Contrib_CBH_pp
    color = ORANGE if row.YoY_exCBH_pct < 0 else BLACK
    ax.text(tot + 4, i, f'{tot:+.0f}%  ·  share {row.Share_CBH_pct:.0f}%',
            va='center', fontsize=11, color=color, fontweight='bold')
ax.set_yticks(y); ax.set_yticklabels(m['brand'], fontsize=13, fontweight='bold')
xmax = max(400, (m['YoY_exCBH_pct'] + m['Contrib_CBH_pp']).max() * 1.25)
ax.set_xticks([]); ax.set_xlim(-30, xmax)
ax.axvline(0, color=BLACK, linewidth=0.8)
ax.spines['bottom'].set_visible(False); ax.spines['left'].set_visible(False)
ax.tick_params(left=False)
ax.legend(loc='lower right', fontsize=11, frameon=False)
ax.set_title('Top 12 marcas — aceleração YoY com vs sem CBH (fev-abr/26 vs fev-abr/25)',
             fontsize=13, fontweight='bold', color=BLACK, loc='left', pad=14)
plt.tight_layout()
fig.savefig(TMP / 'b4_marcas.png', dpi=140, facecolor='white')
plt.close(fig)
print(f"OK b4_marcas (custom save)")

# B4b — ASP buckets (donut)
fig, ax = plt.subplots(figsize=(4.5, 3.5), dpi=150)
asp_d = asp[asp['NMV_CBH_Mi'] > 0]
sizes = asp_d['NMV_CBH_Mi'].tolist()
colors_asp = [MUSTARD, '#B89A30', YELLOW_BASE, YELLOW_2, MELI_YELLOW, ORANGE, '#C8631D']
labels = asp_d['Bucket_ASP'].tolist()
wedges, _ = ax.pie(sizes, colors=colors_asp, startangle=90, counterclock=False,
                   wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))
for i, (w, lbl, s) in enumerate(zip(wedges, labels, sizes)):
    ang = (w.theta2 + w.theta1) / 2
    x = 1.15 * np.cos(np.deg2rad(ang))
    y = 1.15 * np.sin(np.deg2rad(ang))
    ha = 'left' if x > 0 else 'right'
    pct = s/sum(sizes)*100
    ax.annotate(f"{lbl}\n{pct:.1f}%", xy=(x*0.85, y*0.85), xytext=(x*1.35, y*1.15),
                ha=ha, va='center', fontsize=8, color=BLACK, fontweight='bold',
                arrowprops=dict(arrowstyle='-', color='#999', lw=0.5))
ax.text(0, 0.08, 'R$ 740 Mi', ha='center', va='center', fontsize=14, fontweight='bold', color=BLACK)
ax.text(0, -0.15, 'em catálogos', ha='center', va='center', fontsize=8, color=GREY)
ax.set_xlim(-2.4, 2.4); ax.set_ylim(-1.6, 1.6)
ax.set_title('Distribuição CBH por faixa de ASP', fontsize=10.5, fontweight='bold', color=BLACK, loc='left', pad=10)
plt.tight_layout()
save_chart(fig, 'b4_asp.png')

# B5 — Fora de catálogo
fig, ax = plt.subplots(figsize=(7.5, 3.2), dpi=150)
fe = fora_em.sort_values('Pct_fora_catalogo', ascending=True)
y = np.arange(len(fe))
ax.barh(y, fe['NMV_em_catalogo_Mi'], color=YELLOW_2, height=0.62, label='Em catálogo (BB)')
ax.barh(y, fe['NMV_fora_catalogo_Mi'], left=fe['NMV_em_catalogo_Mi'], color=MELI_YELLOW,
        edgecolor=BLACK, linewidth=0.6, height=0.62, label='Fora catálogo (anúncio livre)')
for i, row in enumerate(fe.itertuples()):
    tot = row.NMV_em_catalogo_Mi + row.NMV_fora_catalogo_Mi
    ax.text(tot + 5, i, f'{row.Pct_fora_catalogo:.1f}% fora ({row.NMV_fora_catalogo_Mi:.1f} Mi)',
            va='center', fontsize=9, color=BLACK, fontweight='bold')
ax.set_yticks(y); ax.set_yticklabels(fe['D2'], fontsize=9, fontweight='bold')
ax.invert_yaxis()
ax.set_xticks([])
ax.spines['bottom'].set_visible(False); ax.spines['left'].set_visible(False)
ax.tick_params(left=False)
ax.legend(loc='lower right', fontsize=9, frameon=False)
ax.set_title('NMV CBH em catálogo (Buy Box) vs fora de catálogo (anúncio livre) — TVs lidera com 20,7% fora',
             fontsize=10.5, fontweight='bold', color=BLACK, loc='left', pad=10)
plt.tight_layout()
save_chart(fig, 'b5_fora_cat.png')

print("\n=== Montando PPTX ===")

# ====================================================================
# DECK PRINCIPAL — 3 slides
# ====================================================================
prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

# ----------- SLIDE 1: HEADLINE + DECOMPOSIÇÃO ------------
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide,
    "Casas Bahia adicionou +9,9 pp ao crescimento YoY do MELI em Home Electronics",
    "Análise de incrementalidade · Período pós-CBH: nov/2025 → mai/2026 · Vertical: Home Electronics MLB",
    1, 3)

# 4 KPIs (com fundo amarelo claro)
kpi_y = 1.25; kpi_h = 0.95; kpi_w = 3.05; gap = 0.18
kpi_x_start = 0.4
kpis = [
    ("R$ 880 Mi", "NMV CBH em HE (6 meses, nov/25-abr/26)"),
    ("+9,9 pp", "Contribuição CBH ao YoY MELI HE"),
    ("+17,3 pp", "Maior efeito: contribuição CBH no Norte"),
    ("~R$ 800 Mi", "Net incremental estimado (90% do NMV CBH)"),
]
for i, (val, lbl) in enumerate(kpis):
    x = kpi_x_start + i * (kpi_w + gap)
    add_kpi_card(slide, x, kpi_y, kpi_w, kpi_h, val, lbl, BLACK, YELLOW_BASE)

# Título seção decomposição
add_text(slide, 0.4, 2.40, 12.5, 0.4,
         "Decomposição matemática: quanto cada região contribuiu pro +40,86% YoY do BR",
         font_size=14, bold=True, color=BLACK)

# Gráfico decomposição
slide.shapes.add_picture(str(TMP / 's1_decomposicao.png'),
                          Inches(0.4), Inches(2.85), width=Inches(8.5), height=Inches(3.5))

# Box "3 evidências" do lado direito
box_x, box_y, box_w, box_h = 9.2, 2.85, 3.85, 3.5
add_rect(slide, box_x, box_y, box_w, box_h, '#FAFAF5', line=True, line_color=BLACK)
add_text(slide, box_x+0.15, box_y+0.10, box_w-0.3, 0.35,
         "Por que foi a CBH (e não outro seller)?",
         font_size=12, bold=True, color=BLACK)
evidencias = [
    ("1. Composição única", "Frete grátis em ED+TVs + capilaridade logística + capacidade de preço. Nenhum outro 3P no MELI tem essa combinação."),
    ("2. Mecanismo específico", "31% dos catálogos a CBH expandiu cobertura UF (R$ 456 Mi). Em catálogos antes regionais (1-5 UFs), expandiu em 83%."),
    ("3. Robustness check", "Lente 2 (ago-out/25 vs fev-abr/26, sem viés YoY) replica a mesma ordenação N>NE>CO>SE>S."),
]
cy = box_y + 0.55
for titulo, txt in evidencias:
    add_text(slide, box_x+0.15, cy, box_w-0.3, 0.30, titulo,
             font_size=10.5, bold=True, color=BLACK)
    add_text(slide, box_x+0.15, cy+0.30, box_w-0.3, 0.62, txt,
             font_size=9, color=DARK_GREY)
    cy += 1.00

# Frase abaixo do gráfico
add_text(slide, 0.4, 6.45, 12.5, 0.40,
         "Sem a CBH, o MELI HE cresceria +30,9% YoY. A CBH amplificou esse growth pra +40,9% — adicionando 9,95 pp distribuídos de forma desproporcional em regiões antes mal servidas.",
         font_size=11, italic=True, color=BLACK)
add_footer(slide)

# ----------- SLIDE 2: ONDE — CAPILARIDADE ------------
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide,
    "Onde a CBH cresceu o MELI: capilaridade 2,5x mais forte nas regiões mal servidas",
    "Gradiente Norte → Sul · Inflexão clara em nov/25 · Aceleração mantida em mai/26",
    2, 3)

# 2 charts em cima (regional + evolutivo)
slide.shapes.add_picture(str(TMP / 's2_regional.png'), Inches(0.3), Inches(1.25), width=Inches(6.4), height=Inches(2.7))
slide.shapes.add_picture(str(TMP / 's2_evolutivo.png'), Inches(6.75), Inches(1.25), width=Inches(6.4), height=Inches(2.7))

# Heatmap em baixo esquerda
slide.shapes.add_picture(str(TMP / 's2_heatmap.png'), Inches(0.3), Inches(4.10), width=Inches(7.5), height=Inches(2.7))

# Box "Achado mai/26"
box_x, box_y, box_w, box_h = 8.0, 4.10, 5.05, 2.7
add_rect(slide, box_x, box_y, box_w, box_h, MELI_YELLOW)
add_text(slide, box_x+0.20, box_y+0.10, box_w-0.4, 0.35,
         "📈 Achado recente: aceleração mantida em mai/26",
         font_size=11.5, bold=True, color=BLACK)
add_text(slide, box_x+0.20, box_y+0.50, box_w-0.4, 0.35,
         "Share CBH no NMV HE total por região (abr/26 → mai/26*):",
         font_size=10, color=BLACK, bold=True)
ac_data = [
    ("Nordeste", "10,5%", "13,9%", "+3,4 pp"),
    ("Sudeste",  "6,9%",  "9,4%",  "+2,5 pp"),
    ("Centro-O.","7,7%",  "9,7%",  "+2,0 pp"),
    ("Sul",      "5,8%",  "7,7%",  "+1,9 pp"),
    ("Norte",    "10,3%", "11,5%", "+1,2 pp"),
]
cy = box_y + 0.92
for reg, a, m, d in ac_data:
    add_text(slide, box_x+0.25, cy, 1.2, 0.22, reg, font_size=9.5, bold=True, color=BLACK)
    add_text(slide, box_x+1.30, cy, 0.85, 0.22, a, font_size=9.5, color=DARK_GREY)
    add_text(slide, box_x+2.20, cy, 0.85, 0.22, "→ " + m, font_size=9.5, color=BLACK, bold=True)
    add_text(slide, box_x+3.10, cy, 1.5, 0.22, d, font_size=9.5, color=MUSTARD, bold=True)
    cy += 0.27
add_text(slide, box_x+0.20, box_y+2.32, box_w-0.4, 0.35,
         "Run-rate mai/26: ~R$ 2,29 Bi (vs R$ 1,89 Bi em abr/26).",
         font_size=10, color=BLACK, italic=True)

add_footer(slide, "*mai/26 com 1-27 dias.")

# ----------- SLIDE 3: COMO — MECANISMOS ------------
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide,
    "Como a CBH cresceu o MELI: execução, não sortimento novo",
    "90% do NMV em catálogos já existentes · Capilarização UF + Coexistência + Reativação de dormentes",
    3, 3)

# Frase de abertura (em destaque amarelo)
add_rect(slide, 0.3, 1.20, 12.8, 0.55, MELI_YELLOW)
add_text(slide, 0.5, 1.30, 12.4, 0.45,
         "90% do NMV CBH veio de catálogos que já existiam em MELI — o valor está em EXECUÇÃO (frete + preço + capilaridade), não em catálogo inédito.",
         font_size=12, italic=True, color=BLACK, bold=True, align=PP_ALIGN.CENTER)

# Gráfico mecanismos
slide.shapes.add_picture(str(TMP / 's3_mecanismos.png'), Inches(0.3), Inches(1.95), width=Inches(8.5), height=Inches(2.6))

# Box destaque dormentes (com perfil: D2 + marcas)
box_x = 8.95; box_y = 1.95; box_w = 4.2; box_h = 2.6
add_rect(slide, box_x, box_y, box_w, box_h, YELLOW_BASE)
add_text(slide, box_x+0.15, box_y+0.08, box_w-0.3, 0.28,
         "307 dormentes reativados — quem ganhou voz",
         font_size=11, bold=True, color=BLACK)
add_text(slide, box_x+0.15, box_y+0.36, box_w-0.3, 0.30,
         "R$ 7,7 Mi pré (22m) → R$ 110 Mi pós (6m)",
         font_size=10, color=DARK_GREY, italic=True)
add_text(slide, box_x+0.15, box_y+0.70, box_w-0.3, 0.28,
         "Categorias: TVs (R$ 42,6 Mi) + Refrig (R$ 41,5 Mi) = 76%",
         font_size=9.5, bold=True, color=BLACK)
add_text(slide, box_x+0.15, box_y+1.00, box_w-0.3, 0.28,
         "Marcas que mais avançaram:",
         font_size=9.5, bold=True, color=BLACK)
add_text(slide, box_x+0.15, box_y+1.28, box_w-0.3, 0.85,
         "· Consul: R$ 23 Mi (de R$ 160 mil pré)\n· Hisense: R$ 17 Mi (de R$ 200 mil)\n· Philips: R$ 14,8 Mi (em 4 cat. quase parados)\n· Electrolux: R$ 10 Mi  ·  Philco: R$ 6,2 Mi",
         font_size=9, color=DARK_GREY)
add_text(slide, box_x+0.15, box_y+2.20, box_w-0.3, 0.35,
         "Caso extremo: Hisense TV mult 1.096x",
         font_size=9, italic=True, bold=True, color=ORANGE)

# Gráfico D2 + Marcas
slide.shapes.add_picture(str(TMP / 's3_d2_marcas.png'), Inches(0.3), Inches(4.70), width=Inches(11.0), height=Inches(2.40))

# Box highlight TCL/Samsung
box_x = 11.4; box_y = 4.70; box_w = 1.75; box_h = 2.40
add_rect(slide, box_x, box_y, box_w, box_h, ORANGE)
add_text(slide, box_x+0.10, box_y+0.08, box_w-0.2, 0.30,
         "Casos extremos",
         font_size=11, bold=True, color=BLACK)
add_text(slide, box_x+0.10, box_y+0.40, box_w-0.2, 0.30,
         "TCL",
         font_size=14, bold=True, color=BLACK)
add_text(slide, box_x+0.10, box_y+0.68, box_w-0.2, 0.55,
         "30% das vendas TCL no MELI vêm da CBH. NMV TCL dobrou.",
         font_size=8.5, color=BLACK)
add_text(slide, box_x+0.10, box_y+1.28, box_w-0.2, 0.30,
         "Samsung",
         font_size=14, bold=True, color=BLACK)
add_text(slide, box_x+0.10, box_y+1.55, box_w-0.2, 0.80,
         "Cairia −5,2% sem CBH. Com ela, cresce +10,3%. CBH é hedge contra perda de marca.",
         font_size=8.5, color=BLACK)

add_footer(slide)

TARGET = OUT / "deck_CBH_HE_principal.pptx"
prs.save(TARGET)
print(f"OK Principal: {TARGET}")

# ====================================================================
# BACKUP DECK — 5 slides
# ====================================================================
prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

# B1 — Metodologia
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide, "Backup 1 · Metodologia",
    "3 lentes temporais combinadas · Universo HE MLB · Filtros e justificativas", 'B1', 'B5')

add_text(slide, 0.4, 1.25, 12.5, 0.4, "Janelas temporais usadas",
         font_size=14, bold=True, color=BLACK)
slide.shapes.add_picture(str(TMP / 'b1_timeline.png'), Inches(0.4), Inches(1.7), width=Inches(12.5), height=Inches(2.0))

# Tabela das lentes
add_text(slide, 0.4, 4.0, 12.5, 0.35, "As 3 lentes",
         font_size=13, bold=True, color=BLACK)

lentes = [
    ("Lente 1 — NÚCLEO (YoY recente)", "fev-abr/26 vs fev-abr/25",
     "Mesmo período do ano, sem BF dos dois lados, CBH consolidada (3-6 meses de operação). Mitiga viés de crescimento orgânico forte 24→25."),
    ("Lente 2 — ROBUSTNESS (mesmo ano)", "ago-out/25 (pré-CBH) vs fev-abr/26 (pós)",
     "Mesmo macro/ano, sem confundir com crescimento YoY. Confirma a ordenação N>NE>CO>SE>S da Lente 1."),
    ("Lente 3 — CONTEXTO (evolutivo)", "jan/2024 → mai/2026*",
     "Série mensal contínua. Mostra inflexão visível pós-nov/25 e aceleração mantida em mai/26."),
]
cy = 4.45
for titulo, janela, desc in lentes:
    add_rect(slide, 0.4, cy, 12.5, 0.78, '#FAFAF5', line=True, line_color=LIGHT_GREY)
    add_text(slide, 0.55, cy+0.08, 4.5, 0.32, titulo, font_size=10.5, bold=True, color=BLACK)
    add_text(slide, 5.1, cy+0.08, 4.0, 0.32, janela, font_size=10, color=MUSTARD, bold=True)
    add_text(slide, 0.55, cy+0.40, 12.2, 0.38, desc, font_size=9.5, color=DARK_GREY)
    cy += 0.85

add_footer(slide)

# B2 — Não foi território abandonado
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide, "Backup 2 · Onde a CBH entrou — competição já consolidada",
    "Perfil dos sellers que vendiam pré-CBH em cada catálogo · Confirma: 87% dos catálogos já tinham 1P ou TO", 'B2', 'B5')

slide.shapes.add_picture(str(TMP / 'b2_perfil_pre.png'), Inches(0.4), Inches(1.30), width=Inches(8.5), height=Inches(3.8))

# Box destaque
box_x, box_y, box_w, box_h = 9.1, 1.30, 3.95, 3.8
add_rect(slide, box_x, box_y, box_w, box_h, BLACK)
add_text(slide, box_x+0.20, box_y+0.15, box_w-0.4, 0.40,
         "Implicação", font_size=14, bold=True, color=MELI_YELLOW)
add_text(slide, box_x+0.20, box_y+0.55, box_w-0.4, 1.2,
         "A CBH NÃO entrou em territórios fracos — competiu com os players mais consolidados desde o dia 1.",
         font_size=11, color=WHITE, bold=True)
add_text(slide, box_x+0.20, box_y+1.85, box_w-0.4, 1.8,
         "Em TVs: ZERO catálogos eram 'só dev' antes — categoria 100% consolidada.\n\nO valor agregado da CBH foi capilaridade regional + execução de preço/frete em catálogos onde 1P e TOs já operavam — não substituição de fracos.\n\nPor isso o efeito líquido sobre players consolidados foi pequeno (coexistência majoritária + canibalização modesta).",
         font_size=9, color=YELLOW_BASE)

# Frase rodapé
add_text(slide, 0.4, 5.3, 12.5, 0.45,
         "Conclusão: a CBH não 'limpou' espaço vazio — somou execução superior em mercado já disputado, justificando porque o efeito líquido sobre players existentes foi pequeno.",
         font_size=11, italic=True, color=BLACK, bold=True)

add_footer(slide)

# B3 — Canibalização
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide, "Backup 3 · Quem perdeu — canibalização modesta e pulverizada",
    "Sellers que perderam BB pra CBH e o caso especial do 1P MELI", 'B3', 'B5')

slide.shapes.add_picture(str(TMP / 'b3_canib.png'), Inches(0.4), Inches(1.30), width=Inches(8.5), height=Inches(3.9))

# Box 1P
box_x, box_y, box_w, box_h = 9.1, 1.30, 3.95, 3.9
add_rect(slide, box_x, box_y, box_w, box_h, YELLOW_BASE)
add_text(slide, box_x+0.20, box_y+0.15, box_w-0.4, 0.40,
         "Deep no 1P MELI", font_size=13, bold=True, color=BLACK)
add_text(slide, box_x+0.20, box_y+0.60, box_w-0.4, 0.30,
         "(MERCADO LIVRE ELETRONICOS)",
         font_size=10, color=DARK_GREY, italic=True)
add_text(slide, box_x+0.20, box_y+0.95, box_w-0.4, 1.4,
         "Visão filtrada (gráfico ao lado, top NMV pré > R$ 100K, Tipo A): 61 catálogos, perda −R$ 50,7 Mi vs taxa pré.\n\nVisão universo COMPLETO (128 catálogos onde 1P era top pré, sem filtro):",
         font_size=9, color=DARK_GREY)
add_text(slide, box_x+0.20, box_y+2.45, box_w-0.4, 0.45,
         "Δ líquido 1P: −R$ 3,3 Mi",
         font_size=15, bold=True, color=ORANGE)
add_text(slide, box_x+0.20, box_y+2.95, box_w-0.4, 0.85,
         "Por D1: LA −R$ 9 Mi · Small App −R$ 2,4 Mi · TVs +R$ 7,7 Mi (1P até CRESCEU em TVs)",
         font_size=9, color=DARK_GREY, italic=True)

add_text(slide, 0.4, 5.4, 12.5, 0.4,
         "Soma agregada perdedores (top sellers, Tipo A): −R$ 76 Mi · Net incremental estimado CBH: ~R$ 800 Mi (~90% do NMV CBH)",
         font_size=11, italic=True, bold=True, color=BLACK)

add_footer(slide, "Caveat: taxa pré assume zero growth orgânico; ajustando por +30% esperado a perda real é maior, mas não muda a ordem de magnitude.")

# B4 — Marcas + ASP
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide, "Backup 4 · Aceleração por marca e por faixa de preço",
    "Top 12 marcas mais impulsionadas · Distribuição CBH por ASP (concentração R$ 1k-5k)", 'B4', 'B5')

slide.shapes.add_picture(str(TMP / 'b4_marcas.png'), Inches(0.3), Inches(1.30), width=Inches(8.2), height=Inches(5.7))
slide.shapes.add_picture(str(TMP / 'b4_asp.png'), Inches(8.6), Inches(1.30), width=Inches(4.5), height=Inches(3.8))

# Insights ASP
box_x, box_y, box_w, box_h = 8.6, 5.20, 4.5, 1.30
add_rect(slide, box_x, box_y, box_w, box_h, MELI_YELLOW)
add_text(slide, box_x+0.15, box_y+0.10, box_w-0.3, 0.30,
         "66% do NMV CBH em R$ 1k-5k",
         font_size=12, bold=True, color=BLACK)
add_text(slide, box_x+0.15, box_y+0.45, box_w-0.3, 0.75,
         "TVs 50-65', geladeira frost-free, lavadora 11-13kg, fogão 5 bocas — faixa onde frete grátis + financiamento + capilaridade fazem mais diferença vs loja física.",
         font_size=9, color=DARK_GREY)

add_footer(slide)

# B5 — Fora de catálogo
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide, "Backup 5 · NMV CBH fora de catálogo — R$ 140 Mi (16%)",
    "Item_ID sem product_id (anúncios livres) · TVs lidera com 20,7% fora de BB", 'B5', 'B5')

slide.shapes.add_picture(str(TMP / 'b5_fora_cat.png'), Inches(0.4), Inches(1.30), width=Inches(8.5), height=Inches(4.2))

# Box hipóteses
box_x, box_y, box_w, box_h = 9.1, 1.30, 3.95, 4.2
add_rect(slide, box_x, box_y, box_w, box_h, '#FAFAF5', line=True, line_color=BLACK)
add_text(slide, box_x+0.15, box_y+0.10, box_w-0.3, 0.40,
         "Hipóteses & oportunidades",
         font_size=13, bold=True, color=BLACK)
hipoteses = [
    ("Por que 20,7% das TVs CBH ficam fora?",
     "Bundles (TV + acessório), modelos com configuração exata não unificada, ou estratégia de não disputar BB com sellers que já dominam."),
    ("Built In (sua D2): 15,3% fora",
     "R$ 12 Mi em anúncios próprios CBH. Vale auditar caso a caso pra ver se há oportunidade de unificar ao catálogo MELI (ganho de exposição)."),
    ("Implicação metodológica",
     "Os números 'em catálogo' nas análises de canibalização cobrem apenas R$ 740 Mi dos R$ 880 Mi. O fora-catálogo é dinheiro incremental puro (não disputa BB com ninguém)."),
]
cy = box_y + 0.55
for tit, txt in hipoteses:
    add_text(slide, box_x+0.15, cy, box_w-0.3, 0.30, tit,
             font_size=10, bold=True, color=BLACK)
    add_text(slide, box_x+0.15, cy+0.30, box_w-0.3, 0.85, txt,
             font_size=8.5, color=DARK_GREY)
    cy += 1.20

add_footer(slide)

TARGET = OUT / "deck_CBH_HE_backup.pptx"
prs.save(TARGET)
print(f"OK Backup: {TARGET}")

print("\n=== DONE ===")
