import pandas as pd, numpy as np
BASE = r'C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-06-bb-bpc-reputacao'
d = pd.read_csv(BASE + r'\bd_diaria_14m.csv')
d = d[(d['current_level'] != 'newbie') & (d['real_level'] != 'newbie')].copy()
d = d[d['visitas'] > 0].copy()
def lvl(x):
    x = str(x)
    if x in ['yellow', 'orange', 'red']: return x
    return 'verde'
d['niv'] = d['current_level'].map(lvl)

def cvr(g): return g['nsi'].sum() / g['visitas'].sum() * 100

print('================ POOLED (o todo — média por seller-dia) ================')
base = d[d.niv == 'verde']
bv, bn, bc = base['visitas'].mean(), base['nmv'].mean(), cvr(base)
print('BASELINE verde: %.0f visitas/dia | R$ %.0f NMV/dia | CVR %.3f%% (n=%d dias)' % (bv, bn, bc, len(base)))
print()
print('%-8s %6s %14s %16s %16s %10s' % ('nivel', 'ndias', 'visitas/dia', 'NMV/dia (R$)', 'ΔNMV vs verde', 'CVR%'))
for t in ['yellow', 'orange', 'red']:
    s = d[d.niv == t]
    v, n, c = s['visitas'].mean(), s['nmv'].mean(), cvr(s)
    print('%-8s %6d %8.0f (%+.0f%%) %10.0f (%+.0f%%) %10.0f (%+.0f%%) %8.3f' % (
        t, len(s), v, (v/bv-1)*100, n, (n/bn-1)*100, n-bn, (n/bn-1)*100, c))
print()
print('================ WITHIN-SELLER (normalizada — cada seller vs seu próprio verde; média entre sellers) ================')
print('%-8s %10s %12s %12s %10s' % ('nivel', 'n_sellers', 'Δ visitas %', 'Δ NMV %', 'Δ CVR pp'))
for t in ['yellow', 'orange', 'red']:
    dv, dn, dc = [], [], []
    for sid, g in d.groupby('seller_id'):
        gv, gt = g[g.niv == 'verde'], g[g.niv == t]
        if len(gv) >= 10 and len(gt) >= 10:
            dv.append(gt['visitas'].mean() / gv['visitas'].mean() - 1)
            if gv['nmv'].mean() > 0: dn.append(gt['nmv'].mean() / gv['nmv'].mean() - 1)
            dc.append(cvr(gt) - cvr(gv))
    print('%-8s %10d %11.0f%% %11.0f%% %+9.2f' % (t, len(dv), np.mean(dv)*100 if dv else np.nan, np.mean(dn)*100 if dn else np.nan, np.mean(dc) if dc else np.nan))

print('\n(amount absoluto por seller-dia varia muito de porte; % within-seller é o comparável)')
