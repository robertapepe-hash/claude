import pandas as pd, numpy as np
BASE = r'C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-06-bb-bpc-reputacao'
bd = pd.read_csv(BASE + r'\bd_panel_master.csv')
for c in ['VISITS_MATCH', 'VISITS_EXPENSIVE', 'VISITS_CHEAPER']:
    bd[c] = pd.to_numeric(bd[c], errors='coerce').fillna(0)
bd['verde'] = bd.SELLER_REPUTATION.str.startswith('green') | bd.SELLER_REPUTATION.eq('light_green')
bd['MONTH'] = bd.MONTH.astype(str)

def bpc(df):
    s = df[['VISITS_MATCH', 'VISITS_EXPENSIVE', 'VISITS_CHEAPER']].sum(); d = s.sum()
    return (s.VISITS_MATCH + s.VISITS_CHEAPER) / d if d else np.nan

for mo in ['202601', '202605']:
    s = bd[bd.MONTH == mo]
    ab = ~s.verde
    oran = s.SELLER_REPUTATION.isin(['orange', 'red'])
    print('--- %s (%s item-dias) ---' % (mo, format(len(s), ',').replace(',', '.')))
    mix = s.SELLER_REPUTATION.value_counts(normalize=True)
    print('  mix:', {k: '%.1f%%' % (v * 100) for k, v in mix.items()})
    print('  pct abaixo de verde: %.1f%% | sellers c/ abaixo: %d/30 | pct orange+red: %.1f%%'
          % (ab.mean() * 100, s[ab].CUS_CUST_ID_SEL.nunique(), oran.mean() * 100))
    ds = []
    for sid, g in s.groupby('CUS_CUST_ID_SEL'):
        if g.verde.sum() >= 50 and (~g.verde).sum() >= 50:
            ds.append((g[g.verde].GANHADOR_BB.mean() - g[~g.verde].GANHADOR_BB.mean()) * 100)
    print('  Elo1 binario within-seller (verde-abaixo): media %+.1f pp (n=%d sellers)' % (np.mean(ds), len(ds)))
    for tier in ['orange', 'red']:
        dd = [(g[g.verde].GANHADOR_BB.mean() - g[g.SELLER_REPUTATION == tier].GANHADOR_BB.mean()) * 100
              for sid, g in s.groupby('CUS_CUST_ID_SEL') if (g.SELLER_REPUTATION == tier).sum() >= 50 and g.verde.sum() >= 50]
        if dd:
            print('    verde-%s: %+.1f pp (n=%d)' % (tier, np.mean(dd), len(dd)))
    b0, b1 = bpc(s[s.GANHADOR_BB == 0]), bpc(s[s.GANHADOR_BB == 1])
    print('  Elo2 BB->BPC: delta %+.1f pp (perd %.3f / ganh %.3f)' % ((b1 - b0) * 100, b0, b1))
    print()
