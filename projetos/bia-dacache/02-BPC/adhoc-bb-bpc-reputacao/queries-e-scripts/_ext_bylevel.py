# Efeito por NIVEL de reputacao (Current) em Visitas/CVR/Venda + corte por cluster (two-way FE)
import pandas as pd, numpy as np, statsmodels.formula.api as smf, warnings
warnings.filterwarnings('ignore')
BASE = r'C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-06-bb-bpc-reputacao'
d = pd.read_csv(BASE + r'\bd_diaria_14m.csv')
d['Data'] = pd.to_datetime(d['Data'])
d = d[(d['current_level'] != 'newbie') & (d['real_level'] != 'newbie')].copy()
d = d[d['visitas'] > 0].copy()
d['npv'] = d['nmv'] / d['visitas']
d['logvis'] = np.log1p(d['visitas'])
d['lognmv'] = np.log1p(d['nmv'])
def below(x): return 1.0 if str(x) in ['yellow', 'orange', 'red'] else 0.0
d['cur_below'] = d['current_level'].map(below)
for t in ['yellow', 'orange', 'red']:
    d['cur_' + t] = (d['current_level'] == t).astype(float)
d['SellerID'] = d['seller_id'].astype(str); d['day'] = d['Data'].dt.strftime('%Y%m%d')

def cf(m, nm):
    if nm not in m.params.index: return '   %-10s: (sem amostra)' % nm
    ci = m.conf_int(); p = m.pvalues[nm]
    s = '***' if p < .01 else ('**' if p < .05 else ('*' if p < .1 else ''))
    return '   %-10s: %+.3f (CI[%+.3f,%+.3f], p=%.3f) %s' % (nm, m.params[nm], ci.loc[nm, 0], ci.loc[nm, 1], p, s)

def fit(data, y, rhs, w=None):
    kw = {'cov_type': 'cluster', 'cov_kwds': {'groups': data['SellerID']}}
    if w is not None: return smf.wls('%s ~ %s + C(SellerID)+C(day)' % (y, rhs), data=data, weights=data[w]).fit(**kw)
    return smf.ols('%s ~ %s + C(SellerID)+C(day)' % (y, rhs), data=data).fit(**kw)

print('n=%d | sellers=%d' % (len(d), d.SellerID.nunique()))
print('\n================ POR NIVEL (Current), two-way FE, todos os sellers ================')
print('(base = verde; coef = efeito de estar naquele nivel vs verde, controlando seller+dia)')
for y, lab, w in [('logvis', 'log VISITAS (%~coef)', None), ('CVR', 'CVR (pp)', 'visitas'), ('lognmv', 'log VENDA/NMV (%~coef)', None)]:
    m = fit(d, y, 'cur_yellow+cur_orange+cur_red', w)
    print('\n[%s]' % lab)
    for t in ['cur_yellow', 'cur_orange', 'cur_red']: print(cf(m, t))

print('\n================ BINARIO (caiu) POR CLUSTER (D2C vs SELLER) ================')
for perf in ['D2C', 'SELLER']:
    sub = d[d.perfil == perf].copy()
    ndrop = sub[sub.cur_below == 1].SellerID.nunique()
    lvls = sub[sub.cur_below == 1].current_level.value_counts().to_dict()
    print('\n--- %s | sellers=%d | que caem=%d | dias por nivel(abaixo)=%s ---' % (perf, sub.SellerID.nunique(), ndrop, lvls))
    if ndrop >= 1:
        for y, lab, w in [('CVR', 'CVR (pp)', 'visitas'), ('lognmv', 'log VENDA', None)]:
            m = fit(sub, y, 'cur_below', w)
            print(cf(m, 'cur_below').replace('cur_below', '%s|caiu' % lab))

print('\n================ POR NIVEL x CLUSTER (so onde ha amostra) ================')
for perf in ['D2C', 'SELLER']:
    sub = d[d.perfil == perf].copy()
    have = [t for t in ['yellow', 'orange', 'red'] if (sub.current_level == t).sum() >= 30]
    if have:
        rhs = '+'.join('cur_' + t for t in have)
        m = fit(sub, 'CVR', rhs, 'visitas')
        print('\n[%s | CVR pp] niveis c/ amostra: %s' % (perf, have))
        for t in have: print(cf(m, 'cur_' + t))
