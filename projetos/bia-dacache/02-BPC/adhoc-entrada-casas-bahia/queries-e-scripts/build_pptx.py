"""Gera 1pager executivo CBH para liderança MELI."""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
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

# Cores
NAVY = '#1E2761'
NAVY_LIGHT = '#3E4A8A'
ICE = '#CADCFC'
GOLD = '#FFE600'  # MELI yellow accent
GREY_TEXT = '#333333'
GREY_LIGHT = '#666666'
WHITE = '#FFFFFF'
GREEN = '#2E7D32'
RED = '#C62828'

plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 11,
    'axes.edgecolor': '#CCCCCC',
    'axes.linewidth': 0.5,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# ===================================================================
# Gráfico 1 — Barras horizontais: Contribuição CBH em pp por região
# ===================================================================
fig, ax = plt.subplots(figsize=(6.2, 2.4), dpi=150)
regs = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
contrib = [17.3, 15.8, 11.1, 8.8, 7.0]
yoy_excbh = [45.9, 48.6, 36.8, 25.0, 30.6]
yoy_total = [c+e for c,e in zip(contrib, yoy_excbh)]

y_pos = np.arange(len(regs))
bars_ex = ax.barh(y_pos, yoy_excbh, color=ICE, height=0.62, label='YoY ex-CBH (orgânico MELI)')
bars_cbh = ax.barh(y_pos, contrib, left=yoy_excbh, color=NAVY, height=0.62, label='Contribuição CBH')

for i, (e, c, t) in enumerate(zip(yoy_excbh, contrib, yoy_total)):
    # Só rotula o YoY total no fim — limpa visual
    ax.text(t + 1.2, i, f'{t:.1f}% (CBH +{c:.1f}pp)', va='center', fontsize=9, color=GREY_TEXT, fontweight='bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(regs, fontsize=10.5)
ax.invert_yaxis()
ax.set_xlim(0, 88)
ax.set_xticks([])
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(left=False)
ax.legend(loc='lower center', fontsize=8.5, frameon=False, ncol=2,
          bbox_to_anchor=(0.5, -0.12))
ax.set_title('Crescimento YoY fev-abr/26 vs fev-abr/25 — com vs sem CBH',
             fontsize=11, fontweight='bold', color=NAVY, loc='left', pad=8)
plt.tight_layout()
plt.savefig(TMP / 'g1_regional.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("OK g1_regional")

# ===================================================================
# Gráfico 2 — Linha temporal NMV HE BR mensal
# ===================================================================
evol = pd.read_csv(OUT / "etapa2_lente3_evolutivo_NMV_regiao.csv", sep=';', decimal=',', encoding='utf-8')
share_cbh_mens = pd.read_csv(OUT / "etapa2_lente3_share_CBH_regiao.csv", sep=';', decimal=',', encoding='utf-8')
cbh_mens = pd.read_csv(OUT / "etapa2_lente3_evolutivo_NMV_CBH_regiao.csv", sep=';', decimal=',', encoding='utf-8')

evol_br = evol[['Mes','BR']].copy()
# NMV ex-CBH = total - CBH (que existe a partir de 2025-11)
cbh_dict = dict(zip(cbh_mens['Mes'], cbh_mens['BR']))
evol_br['BR_CBH'] = evol_br['Mes'].map(cbh_dict).fillna(0)
evol_br['BR_exCBH'] = evol_br['BR'] - evol_br['BR_CBH']

# Identifica mai/26 parcial (asterisco)
parcial_mask = evol_br['Mes'].str.endswith('*')

fig, ax = plt.subplots(figsize=(6.3, 2.4), dpi=150)
x = range(len(evol_br))
ax.fill_between(x, 0, evol_br['BR_exCBH'], color=ICE, alpha=0.85, label='NMV ex-CBH')
ax.fill_between(x, evol_br['BR_exCBH'], evol_br['BR'], color=NAVY, alpha=0.95, label='NMV CBH')
ax.plot(x, evol_br['BR'], color=NAVY, linewidth=1.5)

# Marca mai/26 parcial com hachura
if parcial_mask.any():
    p_idx = evol_br[parcial_mask].index[0]
    ax.fill_between([p_idx-0.5, p_idx+0.5], 0, 3200, color='white', alpha=0.5, hatch='///', edgecolor='#999', linewidth=0)

# Marca entrada CBH (nov/25)
nov25_idx = list(evol_br['Mes']).index('2025-11')
ax.axvline(nov25_idx, color=GOLD, linewidth=2, linestyle='--', alpha=0.9)
ax.annotate('Entrada CBH\n(nov/25)', xy=(nov25_idx, evol_br['BR'].max()*0.92),
            xytext=(nov25_idx-3.5, evol_br['BR'].max()*0.95),
            fontsize=8.5, color=NAVY, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.25', facecolor=GOLD, edgecolor='none', alpha=0.9))

# Labels eixos - mostra a cada 4 meses + sempre o último (parcial)
n = len(evol_br)
labels = []
for i, m in enumerate(evol_br['Mes']):
    if i == n - 1 and m.endswith('*'):
        labels.append(m)  # último = parcial
    elif (i % 4 == 0) and (i < n - 2):  # evita conflito com último
        labels.append(m)
    else:
        labels.append('')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=7.5, rotation=0)
ax.set_yticks([0, 1000, 2000, 3000])
ax.set_yticklabels(['0', '1 Bi', '2 Bi', '3 Bi'], fontsize=8)
ax.set_ylim(0, 3200)
ax.legend(loc='upper left', fontsize=8, frameon=False)
ax.set_title('Evolução mensal NMV HE BR (R$) — inflexão pós-nov/25 (*mai/26 = 1-27 dias)',
             fontsize=10, fontweight='bold', color=NAVY, loc='left', pad=8)
ax.grid(axis='y', alpha=0.2)
plt.tight_layout()
plt.savefig(TMP / 'g2_evolutivo.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("OK g2_evolutivo")

# ===================================================================
# Gráfico 3 — Barras horizontais: Mecanismos de growth (mais limpo que donut)
# ===================================================================
fig, ax = plt.subplots(figsize=(6.2, 2.4), dpi=150)
mecanismos = [
    ('Capilarização UF\nem catálogo existente', 456, NAVY),
    ('Coexistência em\ncatálogo consolidado', 236, NAVY_LIGHT),
    ('Reativação dormentes +\nsortimento novo', 183, ICE),
]
labels = [m[0] for m in mecanismos]
sizes = [m[1] for m in mecanismos]
colors = [m[2] for m in mecanismos]
total = 875  # 456+236+183

y_pos = np.arange(len(labels))
bars = ax.barh(y_pos, sizes, color=colors, height=0.65)
for i, s in enumerate(sizes):
    pct = s/total*100
    ax.text(s + 8, i, f'R$ {s} Mi  ({pct:.0f}%)', va='center', fontsize=10.5,
            color=GREY_TEXT, fontweight='bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=9.5)
ax.invert_yaxis()
ax.set_xticks([]); ax.set_xlim(0, 620)
ax.spines['bottom'].set_visible(False); ax.spines['left'].set_visible(False)
ax.tick_params(left=False)
ax.set_title('Mecanismos do growth CBH (em catálogos identificados, R$ 875 Mi)',
             fontsize=10.5, fontweight='bold', color=NAVY, loc='left', pad=10)
plt.tight_layout()
plt.savefig(TMP / 'g3_mecanismos.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("OK g3_mecanismos")

# ===================================================================
# Gráfico 4 — Barras D2 e Marcas (lado a lado)
# ===================================================================
fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.4), dpi=150)

# D2
d2_names = ['Laundry &\nDishwashers', 'Refrigeration', 'Televisions', 'Built In', 'Kitchen']
d2_contrib = [33.1, 31.5, 23.5, 9.1, 8.6]
d2_yoy_ex = [69.2, 30.8, 26.5, 42.9, 36.3]

ax = axes[0]
y = np.arange(len(d2_names))
ax.barh(y, d2_yoy_ex, color=ICE, height=0.65)
ax.barh(y, d2_contrib, left=d2_yoy_ex, color=NAVY, height=0.65)
for i, (e, c) in enumerate(zip(d2_yoy_ex, d2_contrib)):
    ax.text(e+c+1, i, f'+{c:.1f}pp', va='center', fontsize=8.5, color=NAVY, fontweight='bold')
ax.set_yticks(y); ax.set_yticklabels(d2_names, fontsize=8.5)
ax.invert_yaxis()
ax.set_xticks([]); ax.set_xlim(0, 115)
ax.spines['bottom'].set_visible(False); ax.spines['left'].set_visible(False)
ax.tick_params(left=False)
ax.set_title('Contribuição CBH ao YoY por D2', fontsize=10, fontweight='bold', color=NAVY, loc='left')

# Marcas
brand_names = ['TCL', 'Consul', 'Philips', 'Brastemp', 'LG', 'Mondial', 'Britânia', 'Samsung']
brand_contrib = [68.2, 42.1, 34.8, 26.4, 23.0, 22.8, 21.8, 15.5]
brand_share_cbh = [30.1, 20.9, 19.3, 14.1, 17.4, 13.0, 16.5, 14.1]

ax = axes[1]
y = np.arange(len(brand_names))
bars = ax.barh(y, brand_contrib, color=NAVY, height=0.65)
for i, (c, s) in enumerate(zip(brand_contrib, brand_share_cbh)):
    ax.text(c+1, i, f'+{c:.1f}pp (share CBH {s:.0f}%)', va='center', fontsize=8, color=GREY_TEXT)
ax.set_yticks(y); ax.set_yticklabels(brand_names, fontsize=8.5)
ax.invert_yaxis()
ax.set_xticks([]); ax.set_xlim(0, 130)
ax.spines['bottom'].set_visible(False); ax.spines['left'].set_visible(False)
ax.tick_params(left=False)
ax.set_title('Marcas mais impulsionadas pela CBH', fontsize=10, fontweight='bold', color=NAVY, loc='left')

plt.tight_layout()
plt.savefig(TMP / 'g4_d2_marcas.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("OK g4_d2_marcas")

# ===================================================================
# PPTX
# ===================================================================
print("\nMontando PPTX...")
prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

def add_text(slide, left, top, width, height, text, font_size=14, bold=False,
             color=GREY_TEXT, align=PP_ALIGN.LEFT, font_name='Arial', anchor=MSO_ANCHOR.TOP):
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
    r.font.color.rgb = RGBColor.from_string(color.lstrip('#'))
    return tb

def add_rect(slide, left, top, width, height, fill_color=NAVY, line=False):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor.from_string(fill_color.lstrip('#'))
    if not line:
        shape.line.fill.background()
    return shape

# ----------- HEADER (0 a 1.6") -----------
# Banner topo navy
add_rect(slide, 0, 0, 13.33, 1.15, NAVY)
add_text(slide, 0.4, 0.10, 12.5, 0.55,
         "Casas Bahia adicionou +9,9 pp ao growth YoY em HE — efeito 2,5x maior no Norte e Nordeste",
         font_size=20, bold=True, color=WHITE)
add_text(slide, 0.4, 0.72, 12.5, 0.35,
         "Análise de incrementalidade regional | Período pós-CBH: nov/2025 → abr/2026 | Home Electronics MLB",
         font_size=10, color=ICE)

# 4 KPIs em cards
kpi_y = 1.25
kpi_h = 0.85
kpi_w = 3.05
gap = 0.18
kpi_x_start = 0.4

kpis = [
    ("R$ 880 Mi", "NMV CBH em HE em 6 meses", NAVY),
    ("+9,9 pp", "Contribuição CBH ao YoY MELI HE", NAVY),
    ("+17,3 pp", "Contribuição CBH no Norte (maior efeito)", NAVY),
    ("~R$ 800 Mi", "Net incremental estimado ao MELI", NAVY),
]
for i, (val, lbl, col) in enumerate(kpis):
    x = kpi_x_start + i * (kpi_w + gap)
    add_rect(slide, x, kpi_y, kpi_w, kpi_h, '#F0F4FA')
    add_text(slide, x, kpi_y+0.05, kpi_w, 0.45, val,
             font_size=24, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    add_text(slide, x, kpi_y+0.5, kpi_w, 0.35, lbl,
             font_size=9.5, color=GREY_LIGHT, align=PP_ALIGN.CENTER)

# ----------- QUADRANTES (2.2 a 6.6") -----------
# TL: g1_regional
slide.shapes.add_picture(str(TMP / 'g1_regional.png'), Inches(0.25), Inches(2.30), width=Inches(6.4), height=Inches(2.2))

# TR: g2_evolutivo
slide.shapes.add_picture(str(TMP / 'g2_evolutivo.png'), Inches(6.7), Inches(2.30), width=Inches(6.4), height=Inches(2.2))

# BL: g3_mecanismos
slide.shapes.add_picture(str(TMP / 'g3_mecanismos.png'), Inches(0.25), Inches(4.55), width=Inches(6.4), height=Inches(2.2))

# BR: g4_d2_marcas
slide.shapes.add_picture(str(TMP / 'g4_d2_marcas.png'), Inches(6.7), Inches(4.55), width=Inches(6.4), height=Inches(2.2))

# ----------- FOOTER -----------
add_rect(slide, 0, 6.8, 13.33, 0.7, '#F5F5F5')
add_text(slide, 0.4, 6.82, 12.5, 0.25,
         "Insights complementares:",
         font_size=9, bold=True, color=NAVY)
add_text(slide, 0.4, 7.05, 12.5, 0.22,
         "• 90% do NMV CBH veio de catálogos já existentes em MELI — valor está em execução (capilaridade + preço + frete), não em sortimento novo",
         font_size=8.5, color=GREY_TEXT)
add_text(slide, 0.4, 7.25, 12.5, 0.22,
         "• Samsung cairia -5,2% YoY sem CBH; com ela cresce +10,3%. Em LAUNDRY e REFRIGERATION, 1/3 do crescimento veio da CBH (frete + capilaridade decisivos)",
         font_size=8.5, color=GREY_TEXT)

# Footnote
add_text(slide, 0.4, 7.42, 12.5, 0.08,
         "Fonte: DM_EFICIENCIA_MLB | Análise: Beatriz Dacache | 28-mai-2026 | Limitação: análise correlacional (sem A/B), CBH = único SELLER_ID 1046986303",
         font_size=7, color=GREY_LIGHT)

# Salva
TARGET = OUT / "1pager_CBH_HE.pptx"
prs.save(TARGET)
print(f"\nOK: {TARGET}")
print(f"Tamanho: {TARGET.stat().st_size / 1024:.0f} KB")
