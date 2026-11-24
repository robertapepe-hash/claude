# Visitas por item-dia x reputacao, por seller (hipotese: green -> mais visitas)
import pandas as pd, numpy as np

BASE = r'C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-06-bb-bpc-reputacao'
order = [(267892530, 'ELUX'), (185297674, 'BUD'), (251535997, 'CLIMA'), (668432476, 'MIDEA'), (234000251, 'FAST SHOP')]
tiers = ['green_platinum', 'green', 'light_green', 'yellow', 'orange', 'red']
qmap = {'green_platinum': 5, 'green': 4, 'light_green': 3, 'yellow': 2, 'orange': 1, 'red': 0}

def load(p):
    d = pd.read_csv(p)
    for c in ['MATCH_VISITS', 'VISITS_MATCH', 'VISITS_EXPENSIVE', 'VISITS_CHEAPER']:
        d[c] = pd.to_numeric(d[c], errors='coerce').fillna(0)
    d['VIS_ITEM'] = d['VISITS_MATCH'] + d['VISITS_EXPENSIVE'] + d['VISITS_CHEAPER']  # visitas item (competitivas)
    return d

def analyze(d, nome):
    print('\n' + '=' * 84)
    print(nome)
    print('=' * 84)
    print('--- MEDIA de visitas por item-dia (MATCH_VISITS), por seller x tier ---')
    print('seller'.ljust(11) + ''.join(t[:7].rjust(12) for t in tiers))
    for sid, lab in order:
        line = lab.ljust(11)
        for t in tiers:
            s = d[(d.CUS_CUST_ID_SEL == sid) & (d.SELLER_REPUTATION == t)]
            line += ('-'.rjust(12) if len(s) == 0 else f'{s.MATCH_VISITS.mean():,.0f}'.replace(',', '.').rjust(12))
        print(line)

    print('\n--- Razao green/yellow e green/red (media visitas item-dia) + corr within-seller ---')
    print('seller'.ljust(11) + 'g/yel'.rjust(8) + 'g/red'.rjust(8) + 'corr(q,vis)'.rjust(14))
    rgy, rgr, corrs = [], [], []
    for sid, lab in order:
        sub = d[d.CUS_CUST_ID_SEL == sid]
        mg = sub[sub.SELLER_REPUTATION == 'green'].MATCH_VISITS.mean()
        my = sub[sub.SELLER_REPUTATION == 'yellow'].MATCH_VISITS.mean()
        mr = sub[sub.SELLER_REPUTATION == 'red'].MATCH_VISITS.mean()
        gy = mg / my if (my and not np.isnan(my)) else np.nan
        gr = mg / mr if (mr and not np.isnan(mr)) else np.nan
        sub2 = sub.copy(); sub2['q'] = sub2.SELLER_REPUTATION.map(qmap)
        cc = np.corrcoef(sub2['q'], sub2.MATCH_VISITS)[0, 1] if sub2['q'].nunique() > 1 else np.nan
        for L, v in [(rgy, gy), (rgr, gr), (corrs, cc)]:
            if not (isinstance(v, float) and np.isnan(v)): L.append(v)
        f = lambda v: ('n/d'.rjust(8) if (isinstance(v, float) and np.isnan(v)) else f'{v:.2f}x'.rjust(8))
        print(lab.ljust(11) + f(gy) + f(gr) + (f'{cc:+.3f}'.rjust(14) if not np.isnan(cc) else 'n/d'.rjust(14)))
    print('-' * 41)
    print('MEDIA'.ljust(11) + f'{np.mean(rgy):.2f}x'.rjust(8) + f'{np.mean(rgr):.2f}x'.rjust(8) + f'{np.mean(corrs):+.3f}'.rjust(14))

    print('\n--- Agregado: media visitas/item-dia por tier (todos sellers) ---')
    for t in tiers:
        s = d[d.SELLER_REPUTATION == t]
        if len(s): print(f'   {t:15s} MATCH_VISITS {s.MATCH_VISITS.mean():7.0f} | VIS_ITEM {s.VIS_ITEM.mean():6.0f}  (n={len(s):,})'.replace(',', '.'))

analyze(load(BASE + r'\bd.csv'), 'YTD Jan-Mai 2026 (normal)')
analyze(load(BASE + r'\bd_q4.csv'), 'Q4 Out-Dez 2025 (pico)')
