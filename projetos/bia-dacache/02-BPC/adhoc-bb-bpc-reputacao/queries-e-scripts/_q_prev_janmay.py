import pandas as pd, numpy as np
pd.set_option('display.width', 200)
BASE = r'C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-06-bb-bpc-reputacao'
bd = pd.read_csv(BASE + r'\bd_panel_master.csv')
for c in ['VISITS_MATCH', 'VISITS_EXPENSIVE', 'VISITS_CHEAPER']:
    bd[c] = pd.to_numeric(bd[c], errors='coerce').fillna(0)
bd['verde'] = bd.SELLER_REPUTATION.str.startswith('green') | bd.SELLER_REPUTATION.eq('light_green')
def bpc(df):
    s = df[['VISITS_MATCH', 'VISITS_EXPENSIVE', 'VISITS_CHEAPER']].sum(); d = s.sum()
    return (s.VISITS_MATCH + s.VISITS_CHEAPER) / d if d else np.nan
N = len(bd)

print('=' * 68); print('Q1 — QUAO FREQUENTE E orange/red?'); print('=' * 68)
for t in ['yellow', 'orange', 'red']:
    n = (bd.SELLER_REPUTATION == t).sum(); print(f'  {t:7s}: {n:>8,} item-dias ({n/N:.1%})'.replace(',', '.'))
oran = bd.SELLER_REPUTATION.isin(['orange', 'red'])
print(f'  orange+red juntos: {oran.sum():,} ({oran.mean():.1%})'.replace(',', '.'))
per = bd[oran].groupby('CUS_CUST_ID_SEL').agg(nick=('nickname', 'first'), perfil=('perfil', 'first'), me=('me_dom', 'first'), n_or=('GANHADOR_BB', 'size')).reset_index()
tot = bd.groupby('CUS_CUST_ID_SEL').size().rename('n_tot')
per = per.merge(tot, left_on='CUS_CUST_ID_SEL', right_index=True)
per['pct'] = per.n_or / per.n_tot
print('\nSellers com QUALQUER orange/red:', len(per), '/30')
print(per.sort_values('n_or', ascending=False)[['nick', 'perfil', 'me', 'n_or', 'pct']].to_string(index=False, formatters={'pct': '{:.1%}'.format}))
print(f"\nSellers com >=50 item-dias em orange/red: {(per.n_or>=50).sum()} | >=500: {(per.n_or>=500).sum()}")
print(f"Taxa de ganho de BB: orange {bd[bd.SELLER_REPUTATION=='orange'].GANHADOR_BB.mean():.3f} | red {bd[bd.SELLER_REPUTATION=='red'].GANHADOR_BB.mean():.3f}")

print('\n' + '=' * 68); print('Q2 — JANEIRO vs MAIO'); print('=' * 68)
for mo in ['202601', '202605']:
    s = bd[bd.MONTH == mo]
    print(f'\n--- {mo} ({len(s):,} item-dias) ---'.replace(',', '.'))
    mix = s.SELLER_REPUTATION.value_counts(normalize=True)
    print('  mix reputacao:', {k: f'{v:.1%}' for k, v in mix.items()})
    ab = ~s.verde
    print(f'  % abaixo de verde: {ab.mean():.1%} | sellers c/ algum abaixo: {s[ab].CUS_CUST_ID_SEL.nunique()}/30')
    # within-seller binario verde vs abaixo (sellers com >=50 em cada)
    ds = []
    for sid, g in s.groupby('CUS_CUST_ID_SEL'):
        nv, na = g.verde.sum(), (~g.verde).sum()
        if nv >= 50 and na >= 50:
            ds.append((g[g.verde].GANHADOR_BB.mean() - g[~g.verde].GANHADOR_BB.mean()) * 100)
    print(f'  Elo1 binario (verde-abaixo) within-seller: media {np.mean(ds):+.1f} pp (n={len(ds)} sellers)')
    # dose
    for tier in ['orange', 'red']:
        dd = [ (g[g.verde].GANHADOR_BB.mean() - g[g.SELLER_REPUTATION==tier].GANHADOR_BB.mean())*100
               for sid, g in s.groupby('CUS_CUST_ID_SEL') if (g.SELLER_REPUTATION==tier).sum()>=50 and g.verde.sum()>=50 ]
        if dd: print(f'    verde-{tier}: {np.mean(dd):+.1f} pp (n={len(dd)})')
    b0, b1 = bpc(s[s.GANHADOR_BB == 0]), bpc(s[s.GANHADOR_BB == 1])
    print(f'  Elo2 BB->BPC: perdedor {b0:.3f} | ganhador {b1:.3f} | delta {(b1-b0)*100:+.1f} pp')
