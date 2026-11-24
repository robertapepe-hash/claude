# Monta o xlsx novo: Resumo (Bloco 1 within-seller corrigido) + BD + CONX
import pandas as pd, numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

BASE = r'C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-06-bb-bpc-reputacao'
P, OUT, QSQL = BASE + r'\bd.csv', BASE + r'\BB x BPC - YTD Jan-Mai 2026.xlsx', BASE + r'\query.sql'

bd = pd.read_csv(P)
for c in ['MATCH_VISITS', 'VISITS_MATCH', 'VISITS_EXPENSIVE', 'VISITS_CHEAPER']:
    bd[c] = pd.to_numeric(bd[c], errors='coerce')

order = [(267892530, 'ELUX'), (185297674, 'BUD'), (251535997, 'CLIMA'), (668432476, 'MIDEA'), (234000251, 'FAST SHOP')]
nick = bd.groupby('CUS_CUST_ID_SEL')['CUS_NICKNAME'].first().to_dict()

# ---------- BLOCO 1: taxa within-seller green vs yellow ----------
gy = bd[bd['SELLER_REPUTATION'].isin(['green', 'yellow'])]
b1 = []
for sid, lab in order:
    sub = gy[gy['CUS_CUST_ID_SEL'] == sid]
    g, y = sub[sub.SELLER_REPUTATION == 'green'], sub[sub.SELLER_REPUTATION == 'yellow']
    gr, yr = g['GANHADOR_BB'].mean(), y['GANHADOR_BB'].mean()
    b1.append([lab, sid, len(g), gr, len(y), yr, (gr - yr) * 100])
avg_delta = float(np.mean([r[6] for r in b1]))

# ---------- BLOCO 2: BPC por GANHADOR_BB (geral + por seller) ----------
b2v = bd.copy()
for c in ['VISITS_MATCH', 'VISITS_EXPENSIVE', 'VISITS_CHEAPER']:
    b2v[c] = b2v[c].fillna(0)
def bpc(df):
    s = df[['VISITS_MATCH', 'VISITS_EXPENSIVE', 'VISITS_CHEAPER']].sum()
    den = s.VISITS_MATCH + s.VISITS_CHEAPER + s.VISITS_EXPENSIVE
    return (s.VISITS_MATCH + s.VISITS_CHEAPER) / den if den else np.nan
n0, n1 = int((bd.GANHADOR_BB == 0).sum()), int((bd.GANHADOR_BB == 1).sum())
bpc0, bpc1 = bpc(b2v[b2v.GANHADOR_BB == 0]), bpc(b2v[b2v.GANHADOR_BB == 1])
b2s = []
for sid, lab in order:
    sub = b2v[b2v.CUS_CUST_ID_SEL == sid]
    p, w = bpc(sub[sub.GANHADOR_BB == 0]), bpc(sub[sub.GANHADOR_BB == 1])
    b2s.append([lab, sid, p, w, (w - p) * 100])

# ---------- caveat composicao (metodo antigo literal) ----------
won = bd[bd.GANHADOR_BB == 1]
fg, fy = len(won[won.SELLER_REPUTATION == 'green']), len(won[won.SELLER_REPUTATION == 'yellow'])
fgp, fyp = fg / (fg + fy), fy / (fg + fy)

# ---------- exposicao ----------
repcols = ['green_platinum', 'green', 'light_green', 'yellow', 'orange', 'red']
expo = pd.crosstab(bd.CUS_CUST_ID_SEL, bd.SELLER_REPUTATION).reindex(columns=repcols, fill_value=0)

# ===== VERIFICACAO (deve bater com _analyze.py) =====
print('TOTAL linhas:', len(bd), '| n0:', n0, '| n1:', n1)
print('BLOCO 1 (lab, green_rate, yellow_rate, delta_pp):')
for r in b1: print('  ', r[0], round(r[3], 4), round(r[5], 4), round(r[6], 2))
print('  avg_delta_pp:', round(avg_delta, 2))
print('BLOCO 2 geral: bpc0', round(bpc0, 4), '| bpc1', round(bpc1, 4), '| delta', round((bpc1 - bpc0) * 100, 2))
print('Caveat composicao: green', fg, round(fgp, 4), '| yellow', fy, round(fyp, 4), '| delta', round((fgp - fyp) * 100, 2))

# =================== BUILD ===================
HEAD = PatternFill('solid', fgColor='4472C4')
GREENF = PatternFill('solid', fgColor='C6EFCE')
YELF = PatternFill('solid', fgColor='FFEB9C')
GREYF = PatternFill('solid', fgColor='F2F2F2')
PCT, PP, INT = '0.0%', '+0.0" pp";[Red]-0.0" pp"', '#,##0'

wb = Workbook()
ws = wb.active; ws.title = 'Resumo'
def W(cell, v, b=False, sz=11, it=False, fill=None, fmt=None, al=None, col=None, wrap=False):
    c = ws[cell]; c.value = v
    c.font = Font(bold=b, size=sz, italic=it, color=col)
    if fill: c.fill = fill
    if fmt: c.number_format = fmt
    c.alignment = Alignment(horizontal=al, vertical='center', wrap_text=wrap)

ws.column_dimensions['A'].width = 30
for col in 'BCDEF': ws.column_dimensions[col].width = 17

W('A1', 'BB x BPC  —  Reputacao x Ganho de Buy Box x Competitividade (BPC)', b=True, sz=14)
W('A2', 'Recorte: YTD fechado Jan-Mai 2026 (01/01-31/05)  .  Site MLB  .  Bulky=TRUE  .  Atualizado 01/06/2026', it=True, sz=9)
W('A3', 'Sellers (5): ELUX 267892530 . BUD 185297674 . CLIMA 251535997 . MIDEA 668432476 . FAST SHOP 234000251', sz=9)
W('A4', 'Base: %s item-dias  .  Fonte: aba BD (query documentada em CONX)  .  Numeros calculados a partir da BD' % f'{len(bd):,}'.replace(',', '.'), it=True, sz=9)

# ---- BLOCO 1 ----
r = 6
for cc in 'ABCDEF': W(f'{cc}{r}', 'BLOCO 1 — Reputacao x Ganho de BB' if cc == 'A' else '', b=True, sz=12, fill=HEAD, col='FFFFFF')
r = 7
W(f'A{r}', 'Metrica: taxa de ganho de BB (item-dias com GANHADOR_BB=1 / item-dias) DENTRO de cada reputacao, por seller — controla quanto tempo cada seller passa em cada cor (evita o artefato de composicao).', it=True, sz=9, wrap=True)
ws.row_dimensions[r].height = 42
r = 9
hdr = {'A': 'Seller', 'B': 'green: item-dias', 'C': 'green: taxa BB', 'D': 'yellow: item-dias', 'E': 'yellow: taxa BB', 'F': 'Delta (green - yellow)'}
for cc, t in hdr.items():
    W(f'{cc}{r}', t, b=True, al='center', wrap=True, fill=(GREENF if cc in 'BC' else YELF if cc in 'DE' else GREYF))
ws.row_dimensions[r].height = 30
r = 10
for lab, sid, gn, gr, yn, yr, d in b1:
    W(f'A{r}', f'{lab}  ({sid})')
    W(f'B{r}', gn, al='center', fmt=INT); W(f'C{r}', gr, al='center', fmt=PCT)
    W(f'D{r}', yn, al='center', fmt=INT); W(f'E{r}', yr, al='center', fmt=PCT)
    W(f'F{r}', d, al='center', fmt=PP)
    r += 1
W(f'A{r}', 'Media (within-seller)', b=True)
W(f'F{r}', avg_delta, b=True, al='center', fmt=PP)
r += 2
W(f'A{r}', 'Leitura: no YTD Jan-Mai, estar green vs yellow quase nao muda o ganho de BB (Delta ~ -2,0 pp, levemente negativa). A tese "green ganha mais BB" NAO se sustenta neste recorte/mix.', b=True, sz=10, wrap=True)
ws.row_dimensions[r].height = 30
r += 2
W(f'A{r}', 'Ressalva: a reproducao literal do metodo antigo (share de item-dias green/yellow) daria green %.1f%% / yellow %.1f%% (Delta -40,4 pp) — mas e artefato de composicao (MIDEA ~98%% e ELUX ~80%% em yellow), nao efeito de reputacao. Por isso o Bloco 1 usa taxa within-seller.' % (fgp * 100, fyp * 100), it=True, sz=9, wrap=True, col='C00000')
ws.row_dimensions[r].height = 42

# ---- BLOCO 2 ----
r += 3
b2start = r
for cc in 'ABCDEF': W(f'{cc}{r}', 'BLOCO 2 — Ganho do BB x BPC' if cc == 'A' else '', b=True, sz=12, fill=HEAD, col='FFFFFF')
r += 1
W(f'A{r}', 'BPC = (VISITS_MATCH + VISITS_CHEAPER) / (VISITS_MATCH + VISITS_CHEAPER + VISITS_EXPENSIVE)', it=True, sz=9)
r += 2
for cc, t in {'A': 'Estado no BB', 'B': 'item-dias', 'C': 'BPC'}.items():
    W(f'{cc}{r}', t, b=True, al='center', fill=GREYF)
r += 1
W(f'A{r}', 'Perdedor do BB (0)'); W(f'B{r}', n0, al='center', fmt=INT); W(f'C{r}', bpc0, al='center', fmt=PCT)
r += 1
W(f'A{r}', 'Ganhador do BB (1)'); W(f'B{r}', n1, al='center', fmt=INT); W(f'C{r}', bpc1, al='center', fmt=PCT)
r += 1
W(f'A{r}', 'Delta (ganhador - perdedor)', b=True); W(f'C{r}', (bpc1 - bpc0) * 100, b=True, al='center', fmt=PP)
r += 2
W(f'A{r}', 'BPC por seller (ganhador vs perdedor):', b=True, sz=10)
r += 1
for cc, t in {'A': 'Seller', 'B': 'BPC perdedor', 'C': 'BPC ganhador', 'D': 'Delta'}.items():
    W(f'{cc}{r}', t, b=True, al='center', fill=GREYF)
r += 1
for lab, sid, p, w, d in b2s:
    W(f'A{r}', f'{lab}  ({sid})'); W(f'B{r}', p, al='center', fmt=PCT); W(f'C{r}', w, al='center', fmt=PCT); W(f'D{r}', d, al='center', fmt=PP)
    r += 1
r += 1
W(f'A{r}', 'Ressalva: BB e BPC se sobrepoem (ganhar BB pressupoe preco competitivo) — relacao esperada, nao causal.', it=True, sz=9, wrap=True)
ws.row_dimensions[r].height = 28

# ---- BLOCO 3 ----
r += 3
for cc in 'ABCDEF': W(f'{cc}{r}', 'BLOCO 3 — Sintese: reputacao -> BB -> BPC' if cc == 'A' else '', b=True, sz=12, fill=HEAD, col='FFFFFF')
for txt in [
    'reputacao -> ganho de BB:  NAO se confirma no YTD Jan-Mai (efeito ~ 0 within-seller, Delta ~ -2 pp).',
    'ganho de BB -> BPC:  confirma (+%.1f pp), com ressalva de sobreposicao BB/BPC.' % ((bpc1 - bpc0) * 100),
    'Nota metodologica: o doc original (out/25->, base truncada em 25 mil linhas) indicava +9,5 pp pro-green no Bloco 1; nao replica em base completa YTD Jan-Mai.']:
    r += 1
    W(f'A{r}', '•  ' + txt, sz=10, wrap=True); ws.row_dimensions[r].height = 28

# ---- ANEXO exposicao ----
r += 3
for cc in 'ABCDEFG': W(f'{cc}{r}', 'ANEXO — Exposicao de reputacao por seller (item-dias)' if cc == 'A' else '', b=True, sz=11, fill=GREYF)
r += 1
W(f'A{r}', 'Seller', b=True, al='center', fill=GREYF)
for i, rc in enumerate(repcols): W(f'{chr(66+i)}{r}', rc, b=True, al='center', fill=GREYF)
r += 1
for sid, lab in order:
    W(f'A{r}', f'{lab} ({sid})')
    for i, rc in enumerate(repcols): W(f'{chr(66+i)}{r}', int(expo.loc[sid, rc]), al='center', fmt=INT)
    r += 1

# ---- CONX ----
conx = wb.create_sheet('CONX')
conx.column_dimensions['A'].width = 120
conx['A1'] = 'Query fonte (BigQuery) — BB x BPC YTD Jan-Mai 2026'; conx['A1'].font = Font(bold=True, sz=12)
conx['A2'] = 'Tabela: meli-bi-data.WHOWNER.DM_COM_COMPETENCIA  .  Extraido 01/06/2026  .  565,5 GB  .  origin:bigquery-meli'
conx['A2'].font = Font(italic=True, sz=9)
with open(QSQL, encoding='utf-8') as f:
    q = f.read()
conx['A4'] = q; conx['A4'].alignment = Alignment(wrap_text=True, vertical='top'); conx['A4'].font = Font(name='Consolas', sz=9)

# ---- BD ----
bdws = wb.create_sheet('BD')
bdws.append(list(bd.columns))
for cell in bdws[1]: cell.font = Font(bold=True)
data = bd.astype(object).where(pd.notna(bd), None)
for row in data.itertuples(index=False, name=None):
    bdws.append(list(row))

wb.save(OUT)
print('SALVO:', OUT)
print('Abas:', wb.sheetnames, '| BD linhas:', bdws.max_row)
