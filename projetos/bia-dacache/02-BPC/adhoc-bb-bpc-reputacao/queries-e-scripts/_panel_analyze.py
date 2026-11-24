# Painel reputacao->BB->BPC, 30 sellers, YTD Jan-Mai 2026 (Metodologia 2.0)
import pandas as pd, numpy as np
pd.set_option('display.width', 200)

BASE = r'C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-06-bb-bpc-reputacao'
bd = pd.read_csv(BASE + r'\bd_panel_master.csv')
for c in ['VISITS_MATCH', 'VISITS_EXPENSIVE', 'VISITS_CHEAPER']:
    bd[c] = pd.to_numeric(bd[c], errors='coerce').fillna(0)

# verde = qualquer subnivel green + light_green ; abaixo = yellow/orange/red
bd['verde'] = bd.SELLER_REPUTATION.str.startswith('green') | bd.SELLER_REPUTATION.eq('light_green')
bd['abaixo'] = bd.SELLER_REPUTATION.isin(['yellow', 'orange', 'red'])
qual = {'green_platinum': 7, 'green_gold': 6, 'green_silver': 5, 'green': 4, 'light_green': 3, 'yellow': 2, 'orange': 1, 'red': 0}
bd['q'] = bd.SELLER_REPUTATION.map(qual)

def bpc(df):
    s = df[['VISITS_MATCH', 'VISITS_EXPENSIVE', 'VISITS_CHEAPER']].sum()
    d = s.VISITS_MATCH + s.VISITS_CHEAPER + s.VISITS_EXPENSIVE
    return (s.VISITS_MATCH + s.VISITS_CHEAPER) / d if d else np.nan

prof = bd.groupby('CUS_CUST_ID_SEL').agg(nick=('nickname', 'first'), perfil=('perfil', 'first'),
                                         me=('me_dom', 'first'), n=('GANHADOR_BB', 'size'),
                                         n_ab=('abaixo', 'sum'), n_vd=('verde', 'sum')).reset_index()
prof['pct_abaixo'] = prof.n_ab / prof.n

print('=' * 70); print('SECAO 1 — QUEM CAI? (% item-dias abaixo de verde, por seller)'); print('=' * 70)
print(prof.sort_values('pct_abaixo', ascending=False)[['nick', 'perfil', 'me', 'n', 'pct_abaixo']].to_string(index=False, formatters={'pct_abaixo': '{:.1%}'.format}))
droppers = prof[prof.n_ab > 0].CUS_CUST_ID_SEL.tolist()
print(f'\nSellers que cairam (>0 item-dias abaixo): {len(droppers)}/30 | nunca cairam: {30-len(droppers)}/30')
print('Cai por PERFIL:', prof.groupby('perfil').apply(lambda x: f"{(x.n_ab>0).sum()}/{len(x)} caem | media %abaixo {x.pct_abaixo.mean():.1%}").to_dict())
print('Cai por ME   :', prof.groupby('me').apply(lambda x: f"{(x.n_ab>0).sum()}/{len(x)} caem | media %abaixo {x.pct_abaixo.mean():.1%}").to_dict())

print('\n' + '=' * 70); print('SECAO 2 — ELO 1: caiu -> perde BB? (within-seller, 11 droppers)'); print('=' * 70)
rows = []
for sid in droppers:
    s = bd[bd.CUS_CUST_ID_SEL == sid]
    vr = s[s.verde].GANHADOR_BB.mean(); ar = s[s.abaixo].GANHADOR_BB.mean()
    rows.append([s.nickname.iloc[0], s.perfil.iloc[0], s.me_dom.iloc[0], int(s.verde.sum()), int(s.abaixo.sum()), vr, ar, (vr - ar) * 100])
d1 = pd.DataFrame(rows, columns=['nick', 'perfil', 'me', 'n_vd', 'n_ab', 'taxa_vd', 'taxa_ab', 'delta_pp']).sort_values('delta_pp', ascending=False)
print(d1.to_string(index=False, formatters={'taxa_vd': '{:.3f}'.format, 'taxa_ab': '{:.3f}'.format, 'delta_pp': '{:+.1f}'.format}))
print(f'\nMEDIA within-seller delta (caiu): {d1.delta_pp.mean():+.1f} pp | positivos: {(d1.delta_pp>0).sum()}/{len(d1)}')
print('Por PERFIL:', d1.groupby('perfil').delta_pp.mean().round(1).to_dict())
print('Por ME    :', d1.groupby('me').delta_pp.mean().round(1).to_dict())

print('\n' + '=' * 70); print('SECAO 3 — GRADIENTE / DOSE-RESPOSTA (taxa BB por tier)'); print('=' * 70)
order_t = ['green_platinum', 'green_gold', 'green_silver', 'green', 'light_green', 'yellow', 'orange', 'red']
agg = bd.groupby('SELLER_REPUTATION').agg(n=('GANHADOR_BB', 'size'), taxa=('GANHADOR_BB', 'mean'))
agg = agg.reindex([t for t in order_t if t in agg.index])
print('Agregado (todos sellers):')
print(agg.to_string(formatters={'taxa': '{:.3f}'.format}))
# dentro dos droppers: taxa por tier ABAIXO (yellow/orange/red) within-seller
print('\nDose-resposta within-seller (droppers): delta vs verde por severidade')
for tier in ['yellow', 'orange', 'red']:
    ds = []
    for sid in droppers:
        s = bd[bd.CUS_CUST_ID_SEL == sid]
        vr = s[s.verde].GANHADOR_BB.mean(); tr = s[s.SELLER_REPUTATION == tier].GANHADOR_BB.mean()
        if s[s.SELLER_REPUTATION == tier].shape[0] >= 50 and not np.isnan(vr):
            ds.append((vr - tr) * 100)
    if ds: print(f'  verde - {tier:7s}: media {np.mean(ds):+.1f} pp  (n_sellers={len(ds)})')

print('\n' + '=' * 70); print('SECAO 4 — SELLER x PERIODO (delta caiu por mes, droppers)'); print('=' * 70)
cells = []
for sid in droppers:
    for mo in sorted(bd.MONTH.unique()):
        s = bd[(bd.CUS_CUST_ID_SEL == sid) & (bd.MONTH == mo)]
        nv, na = int(s.verde.sum()), int(s.abaixo.sum())
        if nv >= 50 and na >= 50:
            cells.append([s.nickname.iloc[0], mo, (s[s.verde].GANHADOR_BB.mean() - s[s.abaixo].GANHADOR_BB.mean()) * 100])
cdf = pd.DataFrame(cells, columns=['nick', 'mes', 'delta'])
print(f'Celulas (seller x mes) com dados suficientes: {len(cdf)}')
if len(cdf):
    print('Efeito SELLER (media por seller):'); print(cdf.groupby('nick').delta.mean().round(1).sort_values().to_string())
    print('\nEfeito PERIODO (media por mes):'); print(cdf.groupby('mes').delta.mean().round(1).to_string())
    print(f'\nVariancia entre sellers: {cdf.groupby("nick").delta.mean().var():.1f} | entre meses: {cdf.groupby("mes").delta.mean().var():.1f}')

print('\n' + '=' * 70); print('SECAO 5 — ELO 2: BB -> BPC (ganhador vs perdedor)'); print('=' * 70)
b0, b1 = bpc(bd[bd.GANHADOR_BB == 0]), bpc(bd[bd.GANHADOR_BB == 1])
print(f'GERAL: perdedor {b0:.3f} | ganhador {b1:.3f} | delta {(b1-b0)*100:+.1f} pp')
for col, lab in [('perfil', 'PERFIL'), ('me_dom', 'ME')]:
    print(f'Por {lab}:')
    for g, sub in bd.groupby(col):
        p, w = bpc(sub[sub.GANHADOR_BB == 0]), bpc(sub[sub.GANHADOR_BB == 1])
        print(f'   {g:8s} perdedor {p:.3f} | ganhador {w:.3f} | delta {(w-p)*100:+.1f} pp')
