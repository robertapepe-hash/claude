# Correlacao reputacao x ganho de BB: gradiente por tier + green vs (yellow+orange+red) + corr within-seller
import pandas as pd, numpy as np

BASE = r'C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-06-bb-bpc-reputacao'
order = [(267892530, 'ELUX'), (185297674, 'BUD'), (251535997, 'CLIMA'), (668432476, 'MIDEA'), (234000251, 'FAST SHOP')]
tiers = ['green_platinum', 'green', 'light_green', 'yellow', 'orange', 'red']
qmap = {'green_platinum': 5, 'green': 4, 'light_green': 3, 'yellow': 2, 'orange': 1, 'red': 0}  # maior = melhor

def load(p):
    return pd.read_csv(p)

def rate(df, sid, reps):
    s = df[(df.CUS_CUST_ID_SEL == sid) & (df.SELLER_REPUTATION.isin(reps))]
    return (s.GANHADOR_BB.mean(), len(s)) if len(s) else (np.nan, 0)

def analyze(d, nome):
    print('\n' + '=' * 78)
    print(nome)
    print('=' * 78)
    print('--- Taxa de ganho de BB por TIER (win_rate | n), por seller ---')
    hdr = 'seller'.ljust(11) + ''.join(t[:6].rjust(11) for t in tiers)
    print(hdr)
    for sid, lab in order:
        line = lab.ljust(11)
        for t in tiers:
            r, n = rate(d, sid, [t])
            line += ('-'.rjust(11) if n == 0 else f'{r*100:4.0f}%/{n//1000}k'.rjust(11))
        print(line)

    print('\n--- DELTAS within-seller (pp) ---')
    print('seller'.ljust(11) + 'g-y'.rjust(9) + 'g-(y+o+r)'.rjust(12) + 'g-red'.rjust(9) + 'corr'.rjust(9))
    dgy, dbad, dred, corrs = [], [], [], []
    for sid, lab in order:
        g, _ = rate(d, sid, ['green'])
        y, ny = rate(d, sid, ['yellow'])
        bad, nbad = rate(d, sid, ['yellow', 'orange', 'red'])
        rd, nrd = rate(d, sid, ['red'])
        a = (g - y) * 100 if ny else np.nan
        b = (g - bad) * 100 if nbad else np.nan
        c = (g - rd) * 100 if nrd else np.nan
        # corr within-seller: qualidade vs GANHADOR_BB (point-biserial / Pearson)
        sub = d[d.CUS_CUST_ID_SEL == sid].copy()
        sub['q'] = sub.SELLER_REPUTATION.map(qmap)
        cc = np.nan
        if sub['q'].nunique() > 1 and sub.GANHADOR_BB.nunique() > 1:
            cc = np.corrcoef(sub['q'], sub.GANHADOR_BB)[0, 1]
        for L, v in [(dgy, a), (dbad, b), (dred, c), (corrs, cc)]:
            if not (isinstance(v, float) and np.isnan(v)): L.append(v)
        fmt = lambda v: ('n/d'.rjust(9) if (isinstance(v, float) and np.isnan(v)) else f'{v:+.1f}'.rjust(9))
        print(lab.ljust(11) + fmt(a) + fmt(b)[2:].rjust(12) + fmt(c) + (f'{cc:+.3f}'.rjust(9) if not np.isnan(cc) else 'n/d'.rjust(9)))
    print('-' * 50)
    print('MEDIA'.ljust(11) + f'{np.mean(dgy):+.1f}'.rjust(9) + f'{np.mean(dbad):+.1f}'.rjust(12) + f'{np.mean(dred):+.1f}'.rjust(9) + f'{np.mean(corrs):+.3f}'.rjust(9))

    # pooled (confundido) para contraste
    d2 = d.copy(); d2['q'] = d2.SELLER_REPUTATION.map(qmap)
    print(f'\nCorr POOLED (confundida por seller): {np.corrcoef(d2["q"], d2.GANHADOR_BB)[0,1]:+.3f}')
    print('Win-rate agregado por tier (todos sellers):')
    for t in tiers:
        s = d[d.SELLER_REPUTATION == t]
        if len(s): print(f'   {t:15s} {s.GANHADOR_BB.mean()*100:5.1f}%  (n={len(s):,})'.replace(',', '.'))

analyze(load(BASE + r'\bd.csv'), 'YTD Jan-Mai 2026 (normal)')
analyze(load(BASE + r'\bd_q4.csv'), 'Q4 Out-Dez 2025 (pico)')
