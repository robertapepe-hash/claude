# Replica a cadeia do doc como 2 correlacoes (grao seller-dia):
#  Elo 1: reputacao (qualidade) -> taxa de ganho de BB
#  Elo 2: taxa de ganho de BB   -> BPC
import pandas as pd, numpy as np

BASE = r'C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-06-bb-bpc-reputacao'
order = [(267892530, 'ELUX'), (185297674, 'BUD'), (251535997, 'CLIMA'), (668432476, 'MIDEA'), (234000251, 'FAST SHOP')]
qmap = {'green_platinum': 5, 'green': 4, 'light_green': 3, 'yellow': 2, 'orange': 1, 'red': 0}

def load(p):
    d = pd.read_csv(p)
    for c in ['VISITS_MATCH', 'VISITS_EXPENSIVE', 'VISITS_CHEAPER']:
        d[c] = pd.to_numeric(d[c], errors='coerce').fillna(0)
    d['q'] = d.SELLER_REPUTATION.map(qmap)
    return d

def daily(d):
    g = d.groupby(['CUS_CUST_ID_SEL', 'TIM_DAY'])
    a = g.agg(q=('q', 'mean'), bb=('GANHADOR_BB', 'mean'),
              vm=('VISITS_MATCH', 'sum'), ve=('VISITS_EXPENSIVE', 'sum'), vc=('VISITS_CHEAPER', 'sum'),
              n=('GANHADOR_BB', 'size')).reset_index()
    den = a.vm + a.vc + a.ve
    a['bpc'] = np.where(den > 0, (a.vm + a.vc) / den, np.nan)
    return a

def corr(x, y):
    m = x.notna() & y.notna()
    if m.sum() < 3 or x[m].nunique() < 2 or y[m].nunique() < 2:
        return np.nan
    return np.corrcoef(x[m], y[m])[0, 1]

def run(d, nome):
    a = daily(d)
    print('\n' + '=' * 70)
    print(nome, '| seller-dias:', len(a))
    print('=' * 70)
    print('seller'.ljust(11) + 'dias'.rjust(6) + 'corr(rep,BB)'.rjust(14) + 'corr(BB,BPC)'.rjust(14))
    c1s, c2s = [], []
    for sid, lab in order:
        s = a[a.CUS_CUST_ID_SEL == sid]
        c1 = corr(s.q, s.bb)
        c2 = corr(s.bb, s.bpc)
        if not np.isnan(c1): c1s.append(c1)
        if not np.isnan(c2): c2s.append(c2)
        f = lambda v: ('n/d'.rjust(14) if np.isnan(v) else f'{v:+.3f}'.rjust(14))
        print(lab.ljust(11) + str(len(s)).rjust(6) + f(c1) + f(c2))
    print('-' * 45)
    print('MEDIA'.ljust(11) + ''.rjust(6) + f'{np.mean(c1s):+.3f}'.rjust(14) + f'{np.mean(c2s):+.3f}'.rjust(14))
    return np.mean(c1s), np.mean(c2s)

for f, nm in [('bd.csv', 'YTD Jan-Mai 2026 (normal)'), ('bd_q4.csv', 'Q4 Out-Dez 2025 (pico)')]:
    run(load(BASE + '\\' + f), nm)
