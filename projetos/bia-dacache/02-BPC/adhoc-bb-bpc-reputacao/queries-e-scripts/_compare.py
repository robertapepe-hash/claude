# Comparacao YTD Jan-Mai vs Q4 Out-Dez (mesmos 5 sellers) - mesma logica validada
import pandas as pd, numpy as np

BASE = r'C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-06-bb-bpc-reputacao'
order = [(267892530, 'ELUX'), (185297674, 'BUD'), (251535997, 'CLIMA'), (668432476, 'MIDEA'), (234000251, 'FAST SHOP')]

def load(path):
    d = pd.read_csv(path)
    for c in ['VISITS_MATCH', 'VISITS_EXPENSIVE', 'VISITS_CHEAPER']:
        d[c] = pd.to_numeric(d[c], errors='coerce').fillna(0)
    return d

def block1(d):
    gy = d[d.SELLER_REPUTATION.isin(['green', 'yellow'])]
    out = {}
    for sid, lab in order:
        sub = gy[gy.CUS_CUST_ID_SEL == sid]
        gr = sub[sub.SELLER_REPUTATION == 'green']['GANHADOR_BB'].mean()
        yr = sub[sub.SELLER_REPUTATION == 'yellow']['GANHADOR_BB'].mean()
        out[lab] = (gr, yr, (gr - yr) * 100)
    avg = np.nanmean([v[2] for v in out.values()])
    return out, avg

def block2(d):
    g = d.groupby('GANHADOR_BB')[['VISITS_MATCH', 'VISITS_EXPENSIVE', 'VISITS_CHEAPER']].sum()
    g['BPC'] = (g.VISITS_MATCH + g.VISITS_CHEAPER) / (g.VISITS_MATCH + g.VISITS_CHEAPER + g.VISITS_EXPENSIVE)
    return g['BPC'].get(0, np.nan), g['BPC'].get(1, np.nan)

ytd = load(BASE + r'\bd.csv')
q4 = load(BASE + r'\bd_q4.csv')

print('=============== VOLUME ===============')
for nm, d in [('YTD Jan-Mai', ytd), ('Q4 Out-Dez', q4)]:
    print(f'{nm:14s}: {len(d):>7,} linhas | {d.TIM_DAY.nunique()} dias | {d.TIM_DAY.min()} -> {d.TIM_DAY.max()}')

print()
print('=============== EXPOSICAO reputacao x seller (Q4) ===============')
print(pd.crosstab(q4.CUS_CUST_ID_SEL, q4.SELLER_REPUTATION).to_string())

b1y, avgy = block1(ytd)
b1q, avgq = block1(q4)
print()
print('=============== BLOCO 1: taxa BB green vs yellow (within-seller) ===============')
print(f'{"Seller":12s} | {"YTD g":>6} {"YTD y":>6} {"YTD d":>7} || {"Q4 g":>6} {"Q4 y":>6} {"Q4 d":>7}')
for _, lab in order:
    gy_, yy_, dy_ = b1y[lab]
    gq_, yq_, dq_ = b1q[lab]
    print(f'{lab:12s} | {gy_*100:5.1f}% {yy_*100:5.1f}% {dy_:+6.1f} || {gq_*100:5.1f}% {yq_*100:5.1f}% {dq_:+6.1f}')
print(f'{"MEDIA":12s} | {"":6} {"":6} {avgy:+6.1f} || {"":6} {"":6} {avgq:+6.1f}')

b2y0, b2y1 = block2(ytd)
b2q0, b2q1 = block2(q4)
print()
print('=============== BLOCO 2: BPC ganhador vs perdedor ===============')
print(f'{"Periodo":12s} | perdedor(0) | ganhador(1) | delta')
print(f'{"YTD Jan-Mai":12s} | {b2y0*100:9.1f}% | {b2y1*100:9.1f}% | {(b2y1-b2y0)*100:+.1f} pp')
print(f'{"Q4 Out-Dez":12s} | {b2q0*100:9.1f}% | {b2q1*100:9.1f}% | {(b2q1-b2q0)*100:+.1f} pp')
