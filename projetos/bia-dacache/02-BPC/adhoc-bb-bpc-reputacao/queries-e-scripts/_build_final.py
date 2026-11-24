# Consolidado BB x BPC: YTD Jan-Mai 2026 vs Q4 Out-Dez 2025, abas distintas
import pandas as pd, numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

BASE = r'C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-06-bb-bpc-reputacao'
OUT = BASE + r'\BB x BPC - Consolidado YTD vs Q4.xlsx'
order = [(267892530, 'ELUX'), (185297674, 'BUD'), (251535997, 'CLIMA'), (668432476, 'MIDEA'), (234000251, 'FAST SHOP')]
repcols = ['green_platinum', 'green', 'light_green', 'yellow', 'orange', 'red']
VIS = ['VISITS_MATCH', 'VISITS_EXPENSIVE', 'VISITS_CHEAPER']

def load(p):
    d = pd.read_csv(p)
    for c in VIS + ['MATCH_VISITS']:
        d[c] = pd.to_numeric(d[c], errors='coerce')
    return d

def bpc_of(df):
    s = df[VIS].fillna(0).sum(); den = s.VISITS_MATCH + s.VISITS_CHEAPER + s.VISITS_EXPENSIVE
    return (s.VISITS_MATCH + s.VISITS_CHEAPER) / den if den else np.nan

def compute(d):
    gy = d[d.SELLER_REPUTATION.isin(['green', 'yellow'])]
    b1 = []
    for sid, lab in order:
        sub = gy[gy.CUS_CUST_ID_SEL == sid]
        g, y = sub[sub.SELLER_REPUTATION == 'green'], sub[sub.SELLER_REPUTATION == 'yellow']
        gr = g.GANHADOR_BB.mean() if len(g) else np.nan
        yr = y.GANHADOR_BB.mean() if len(y) else np.nan
        b1.append([lab, sid, len(g), gr, len(y), yr, (gr - yr) * 100])
    avg = np.nanmean([r[6] for r in b1])
    n0, n1 = int((d.GANHADOR_BB == 0).sum()), int((d.GANHADOR_BB == 1).sum())
    bpc0, bpc1 = bpc_of(d[d.GANHADOR_BB == 0]), bpc_of(d[d.GANHADOR_BB == 1])
    b2s = []
    for sid, lab in order:
        sub = d[d.CUS_CUST_ID_SEL == sid]
        b2s.append([lab, sid, bpc_of(sub[sub.GANHADOR_BB == 0]), bpc_of(sub[sub.GANHADOR_BB == 1]),
                    (bpc_of(sub[sub.GANHADOR_BB == 1]) - bpc_of(sub[sub.GANHADOR_BB == 0])) * 100])
    won = d[d.GANHADOR_BB == 1]
    fg, fy = len(won[won.SELLER_REPUTATION == 'green']), len(won[won.SELLER_REPUTATION == 'yellow'])
    fgp = fg / (fg + fy) if (fg + fy) else np.nan
    expo = pd.crosstab(d.CUS_CUST_ID_SEL, d.SELLER_REPUTATION).reindex(columns=repcols, fill_value=0)
    return dict(b1=b1, avg=avg, n0=n0, n1=n1, bpc0=bpc0, bpc1=bpc1, b2s=b2s, fgp=fgp, fyp=1 - fgp,
                expo=expo, rows=len(d), days=d.TIM_DAY.nunique(), dmin=d.TIM_DAY.min(), dmax=d.TIM_DAY.max())

ytd = load(BASE + r'\bd.csv'); q4 = load(BASE + r'\bd_q4.csv')
RY, RQ = compute(ytd), compute(q4)

# ---- verificacao ----
print('YTD avg B1:', round(RY['avg'], 2), '| B2 delta:', round((RY['bpc1'] - RY['bpc0']) * 100, 2), '| rows', RY['rows'])
print('Q4  avg B1:', round(RQ['avg'], 2), '| B2 delta:', round((RQ['bpc1'] - RQ['bpc0']) * 100, 2), '| rows', RQ['rows'])

# ===== estilos =====
HEAD = PatternFill('solid', fgColor='4472C4'); GREENF = PatternFill('solid', fgColor='C6EFCE')
YELF = PatternFill('solid', fgColor='FFEB9C'); GREYF = PatternFill('solid', fgColor='F2F2F2')
TITLEF = PatternFill('solid', fgColor='D9E1F2')
PCT, PP, INT = '0.0%', '+0.0" pp";[Red]-0.0" pp"', '#,##0'

def W(ws, cell, v, b=False, sz=11, it=False, fill=None, fmt=None, al=None, col=None, wrap=False):
    c = ws[cell]; c.value = v
    c.font = Font(bold=b, size=sz, italic=it, color=col)
    if fill: c.fill = fill
    if fmt: c.number_format = fmt
    c.alignment = Alignment(horizontal=al, vertical='center', wrap_text=wrap)

def pctcell(ws, cell, v, **kw):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        W(ws, cell, 'n/d', al='center', **kw)
    else:
        W(ws, cell, v, al='center', fmt=PCT, **kw)

def ppcell(ws, cell, v, **kw):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        W(ws, cell, 'n/d', al='center', **kw)
    else:
        W(ws, cell, v, al='center', fmt=PP, **kw)

wb = Workbook()

# ============ SUMARIO ============
s = wb.active; s.title = 'Sumario'
s.column_dimensions['A'].width = 95
W(s, 'A1', 'BB x BPC  —  Reputacao x Ganho de Buy Box x Competitividade (BPC)', b=True, sz=15, fill=TITLEF)
W(s, 'A2', 'Consolidado: YTD Jan-Mai 2026  vs  Q4 Out-Dez 2025  |  Site MLB  |  Bulky=TRUE  |  Atualizado 01/06/2026', it=True, sz=10)
W(s, 'A3', 'Sellers (5): ELUX (267892530) . BUD (185297674) . CLIMA (251535997) . MIDEA (668432476) . FAST SHOP (234000251)', sz=10)
W(s, 'A4', f'Base: YTD {RY["rows"]:,} item-dias ({RY["days"]} dias) . Q4 {RQ["rows"]:,} item-dias ({RQ["days"]} dias) . Fonte: abas BD / queries em CONX'.replace(',', '.'), it=True, sz=9)
r = 6
W(s, f'A{r}', 'PRINCIPAIS ACHADOS', b=True, sz=12, fill=HEAD, col='FFFFFF')
findings = [
    '1) Reputacao -> ganho de BB e um FENOMENO DE PICO. No Q4 (alta demanda), estar green ganha +4,0 pp mais BB que yellow (todos os sellers computaveis positivos). No YTD normal o efeito some/inverte (-2,0 pp).',
    '2) Ganho de BB -> BPC e ESTAVEL nos dois periodos (+23 a +24 pp). Ressalva: BB e BPC se sobrepoem (ganhar BB pressupoe preco competitivo) -> relacao esperada, nao causal.',
    '3) A reputacao dos sellers PIOROU de Q4/25 para 2026 (de majoritariamente green para mais yellow/red). Ex.: ELUX ~77% green no Q4 -> ~13% green no YTD.',
    '4) Metodologia: a metrica do doc antigo (share de item-dias green/yellow) e confundida por composicao (quanto tempo cada seller passa em cada cor). Aqui usamos a TAXA within-seller (controlada). O doc original ainda rodava em base TRUNCADA (25 mil linhas, teto do Connected Sheets) e incluia o pico.']
for f in findings:
    r += 1; W(s, f'A{r}', f, sz=10, wrap=True); s.row_dimensions[r].height = 44
r += 2
W(s, f'A{r}', 'GUIA DE ABAS', b=True, sz=12, fill=HEAD, col='FFFFFF')
for g in ['Comparacao YTD x Q4 — Blocos 1 e 2 lado a lado (aba headline).',
          'Resumo YTD / Resumo Q4 — analise completa de cada periodo (Blocos 1, 2, 3 + exposicao).',
          'CONX — queries fonte (BigQuery) dos dois periodos.',
          'BD YTD / BD Q4 — bases granulares completas (dia x item x seller).']:
    r += 1; W(s, f'A{r}', '. ' + g, sz=10, wrap=True)

# ============ COMPARACAO ============
cp = wb.create_sheet('Comparacao YTD x Q4')
cp.column_dimensions['A'].width = 22
for c in 'BCDEFG': cp.column_dimensions[c].width = 14
W(cp, 'A1', 'Comparacao YTD Jan-Mai 2026  vs  Q4 Out-Dez 2025', b=True, sz=13, fill=TITLEF)
r = 3
W(cp, f'A{r}', 'BLOCO 1 — Taxa de ganho de BB: green vs yellow (within-seller)', b=True, sz=12, fill=HEAD, col='FFFFFF')
for c in 'BCDEFG': W(cp, f'{c}{r}', '', fill=HEAD)
r = 4
W(cp, f'A{r}', '', fill=GREYF)
W(cp, f'B{r}', 'YTD', b=True, al='center', fill=TITLEF); cp.merge_cells(f'B{r}:D{r}')
W(cp, f'E{r}', 'Q4', b=True, al='center', fill=TITLEF); cp.merge_cells(f'E{r}:G{r}')
r = 5
for c, t in {'A': 'Seller', 'B': 'green', 'C': 'yellow', 'D': 'Delta', 'E': 'green', 'F': 'yellow', 'G': 'Delta'}.items():
    W(cp, f'{c}{r}', t, b=True, al='center', fill=GREYF)
r = 6
for i, (_, lab) in enumerate(order):
    y = RY['b1'][i]; q = RQ['b1'][i]
    W(cp, f'A{r}', lab)
    pctcell(cp, f'B{r}', y[3]); pctcell(cp, f'C{r}', y[5]); ppcell(cp, f'D{r}', y[6])
    pctcell(cp, f'E{r}', q[3]); pctcell(cp, f'F{r}', q[5]); ppcell(cp, f'G{r}', q[6])
    r += 1
W(cp, f'A{r}', 'Media', b=True); ppcell(cp, f'D{r}', RY['avg'], b=True); ppcell(cp, f'G{r}', RQ['avg'], b=True)
r += 2
W(cp, f'A{r}', 'Leitura: no pico (Q4) green ganha mais BB (+4,0 pp); no YTD normal o efeito some (-2,0 pp). Reputacao->BB e fenomeno de pico.', it=True, sz=9, wrap=True); cp.merge_cells(f'A{r}:G{r}'); cp.row_dimensions[r].height = 30
r += 3
W(cp, f'A{r}', 'BLOCO 2 — BPC: ganhador vs perdedor do BB', b=True, sz=12, fill=HEAD, col='FFFFFF')
for c in 'BCDEFG': W(cp, f'{c}{r}', '', fill=HEAD)
r += 1
for c, t in {'A': 'Periodo', 'B': 'perdedor (0)', 'C': 'ganhador (1)', 'D': 'Delta'}.items():
    W(cp, f'{c}{r}', t, b=True, al='center', fill=GREYF)
r += 1
W(cp, f'A{r}', 'YTD Jan-Mai'); pctcell(cp, f'B{r}', RY['bpc0']); pctcell(cp, f'C{r}', RY['bpc1']); ppcell(cp, f'D{r}', (RY['bpc1'] - RY['bpc0']) * 100)
r += 1
W(cp, f'A{r}', 'Q4 Out-Dez'); pctcell(cp, f'B{r}', RQ['bpc0']); pctcell(cp, f'C{r}', RQ['bpc1']); ppcell(cp, f'D{r}', (RQ['bpc1'] - RQ['bpc0']) * 100)
r += 2
W(cp, f'A{r}', 'Leitura: BB->BPC estavel (~+23 pp) nos dois periodos; nao depende de sazonalidade.', it=True, sz=9, wrap=True); cp.merge_cells(f'A{r}:G{r}')

# ============ RESUMO por periodo ============
def write_resumo(ws, titulo, meta, R, synth):
    ws.column_dimensions['A'].width = 30
    for c in 'BCDEF': ws.column_dimensions[c].width = 17
    W(ws, 'A1', titulo, b=True, sz=14, fill=TITLEF)
    W(ws, 'A2', meta, it=True, sz=9)
    r = 4
    W(ws, f'A{r}', 'BLOCO 1 — Reputacao x Ganho de BB (taxa within-seller)', b=True, sz=12, fill=HEAD, col='FFFFFF')
    for c in 'BCDEF': W(ws, f'{c}{r}', '', fill=HEAD)
    r = 5
    W(ws, f'A{r}', 'Metrica: item-dias com GANHADOR_BB=1 / item-dias, DENTRO de cada reputacao, por seller (controla exposicao).', it=True, sz=9, wrap=True); ws.row_dimensions[r].height = 30
    r = 7
    for c, t in {'A': 'Seller', 'B': 'green: item-dias', 'C': 'green: taxa', 'D': 'yellow: item-dias', 'E': 'yellow: taxa', 'F': 'Delta (g-y)'}.items():
        W(ws, f'{c}{r}', t, b=True, al='center', wrap=True, fill=(GREENF if c in 'BC' else YELF if c in 'DE' else GREYF))
    ws.row_dimensions[r].height = 30
    r = 8
    for lab, sid, gn, gr, yn, yr, d in R['b1']:
        W(ws, f'A{r}', f'{lab} ({sid})'); W(ws, f'B{r}', gn, al='center', fmt=INT); pctcell(ws, f'C{r}', gr)
        W(ws, f'D{r}', yn, al='center', fmt=INT); pctcell(ws, f'E{r}', yr); ppcell(ws, f'F{r}', d)
        r += 1
    W(ws, f'A{r}', 'Media (within-seller)', b=True); ppcell(ws, f'F{r}', R['avg'], b=True)
    r += 2
    W(ws, f'A{r}', 'Ressalva: metodo antigo (share green/yellow) daria green %.1f%% / yellow %.1f%% (Delta %+.1f pp) — artefato de composicao, nao efeito de reputacao.' % (R['fgp'] * 100, R['fyp'] * 100, (R['fgp'] - R['fyp']) * 100), it=True, sz=9, wrap=True, col='C00000'); ws.row_dimensions[r].height = 30
    r += 3
    W(ws, f'A{r}', 'BLOCO 2 — Ganho do BB x BPC', b=True, sz=12, fill=HEAD, col='FFFFFF')
    for c in 'BCDEF': W(ws, f'{c}{r}', '', fill=HEAD)
    r += 1
    W(ws, f'A{r}', 'BPC = (VISITS_MATCH + VISITS_CHEAPER) / (VISITS_MATCH + VISITS_CHEAPER + VISITS_EXPENSIVE)', it=True, sz=9)
    r += 2
    for c, t in {'A': 'Estado no BB', 'B': 'item-dias', 'C': 'BPC'}.items():
        W(ws, f'{c}{r}', t, b=True, al='center', fill=GREYF)
    r += 1
    W(ws, f'A{r}', 'Perdedor (0)'); W(ws, f'B{r}', R['n0'], al='center', fmt=INT); pctcell(ws, f'C{r}', R['bpc0'])
    r += 1
    W(ws, f'A{r}', 'Ganhador (1)'); W(ws, f'B{r}', R['n1'], al='center', fmt=INT); pctcell(ws, f'C{r}', R['bpc1'])
    r += 1
    W(ws, f'A{r}', 'Delta (ganhador - perdedor)', b=True); ppcell(ws, f'C{r}', (R['bpc1'] - R['bpc0']) * 100, b=True)
    r += 2
    W(ws, f'A{r}', 'BPC por seller (perdedor / ganhador / delta):', b=True, sz=10)
    r += 1
    for c, t in {'A': 'Seller', 'B': 'BPC perdedor', 'C': 'BPC ganhador', 'D': 'Delta'}.items():
        W(ws, f'{c}{r}', t, b=True, al='center', fill=GREYF)
    r += 1
    for lab, sid, p, w, d in R['b2s']:
        W(ws, f'A{r}', f'{lab} ({sid})'); pctcell(ws, f'B{r}', p); pctcell(ws, f'C{r}', w); ppcell(ws, f'D{r}', d)
        r += 1
    r += 2
    W(ws, f'A{r}', 'BLOCO 3 — Sintese', b=True, sz=12, fill=HEAD, col='FFFFFF')
    for c in 'BCDEF': W(ws, f'{c}{r}', '', fill=HEAD)
    for t in synth:
        r += 1; W(ws, f'A{r}', '. ' + t, sz=10, wrap=True); ws.row_dimensions[r].height = 28
    r += 2
    W(ws, f'A{r}', 'EXPOSICAO de reputacao por seller (item-dias)', b=True, sz=11, fill=GREYF)
    r += 1
    W(ws, f'A{r}', 'Seller', b=True, al='center', fill=GREYF)
    for i, rc in enumerate(repcols): W(ws, f'{chr(66+i)}{r}', rc, b=True, al='center', fill=GREYF)
    r += 1
    for sid, lab in order:
        W(ws, f'A{r}', f'{lab} ({sid})')
        for i, rc in enumerate(repcols): W(ws, f'{chr(66+i)}{r}', int(R['expo'].loc[sid, rc]), al='center', fmt=INT)
        r += 1

write_resumo(wb.create_sheet('Resumo YTD'),
             'Resumo — YTD Jan-Mai 2026 (periodo normal)',
             f'01/01-31/05/2026 . {RY["rows"]:,} item-dias . Site MLB . Bulky'.replace(',', '.'), RY,
             ['reputacao -> ganho de BB: NAO se confirma (efeito ~0 within-seller, Delta -2,0 pp).',
              'ganho de BB -> BPC: confirma (+23,8 pp), com ressalva de sobreposicao BB/BPC.',
              'reputacoes mais degradadas que no Q4 (mais yellow/red).'])
write_resumo(wb.create_sheet('Resumo Q4'),
             'Resumo — Q4 Out-Dez 2025 (pico)',
             f'01/10-31/12/2025 . {RQ["rows"]:,} item-dias . Site MLB . Bulky'.replace(',', '.'), RQ,
             ['reputacao -> ganho de BB: CONFIRMA no pico (+4,0 pp medio, todos sellers computaveis positivos).',
              'ganho de BB -> BPC: confirma (+22,8 pp), estavel vs YTD.',
              'FAST SHOP sem yellow no Q4 (fora da media B1). Amostras yellow menores -> mais ruido.'])

# ============ CONX ============
conx = wb.create_sheet('CONX'); conx.column_dimensions['A'].width = 125
conx['A1'] = 'Queries fonte (BigQuery) — meli-bi-data.WHOWNER.DM_COM_COMPETENCIA'; conx['A1'].font = Font(bold=True, size=12)
with open(BASE + r'\query.sql', encoding='utf-8') as f: qy = f.read()
with open(BASE + r'\_exec_q4.sql', encoding='utf-8') as f: qq = f.read()
conx['A3'] = 'QUERY YTD (Jan-Mai 2026) — 565,5 GB'; conx['A3'].font = Font(bold=True)
conx['A4'] = qy; conx['A4'].alignment = Alignment(wrap_text=True, vertical='top'); conx['A4'].font = Font(name='Consolas', size=9)
conx['A6'] = 'QUERY Q4 (Out-Dez 2025) — 294,4 GB'; conx['A6'].font = Font(bold=True)
conx['A7'] = qq; conx['A7'].alignment = Alignment(wrap_text=True, vertical='top'); conx['A7'].font = Font(name='Consolas', size=9)

# ============ BD ============
for name, d in [('BD YTD', ytd), ('BD Q4', q4)]:
    ws = wb.create_sheet(name)
    ws.append(list(d.columns))
    for cell in ws[1]: cell.font = Font(bold=True)
    for row in d.astype(object).where(pd.notna(d), None).itertuples(index=False, name=None):
        ws.append(list(row))

wb.save(OUT)
print('SALVO:', OUT)
print('ABAS:', wb.sheetnames)
