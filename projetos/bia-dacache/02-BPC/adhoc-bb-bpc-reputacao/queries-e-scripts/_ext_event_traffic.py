# Event-study para VISITAS e VENDA (log) - checar se queda e causal (pos) ou confundida (pre)
import pandas as pd, numpy as np, statsmodels.formula.api as smf, warnings
warnings.filterwarnings('ignore')
BASE = r'C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-06-bb-bpc-reputacao'
d = pd.read_csv(BASE + r'\bd_diaria_14m.csv')
d['Data'] = pd.to_datetime(d['Data'])
d = d[(d['current_level'] != 'newbie') & (d['real_level'] != 'newbie')].copy()
d = d[d['visitas'] > 0].copy()
d['logvis'] = np.log1p(d['visitas']); d['lognmv'] = np.log1p(d['nmv'])
def below(x): return 1.0 if str(x) in ['yellow', 'orange', 'red'] else 0.0
d['cur_below'] = d['current_level'].map(below)
d['SellerID'] = d['seller_id'].astype(str); d['day'] = d['Data'].dt.strftime('%Y%m%d')
cl = {'groups': d['SellerID']}
ev = d[d.cur_below == 1].groupby('seller_id')['Data'].min().rename('event0').reset_index()
d = d.merge(ev, on='seller_id', how='left')
d['rel'] = (d['Data'] - d['event0']).dt.days
def binf(r):
    if pd.isna(r) or r < -60: return 'base'
    if r <= -31: return 'pre_60a31'
    if r < 0: return 'pre_30a1'
    if r <= 13: return 'post_0a13'
    if r <= 30: return 'post_14a30'
    if r <= 60: return 'post_31a60'
    return 'post_60+'
order = ['base', 'pre_60a31', 'pre_30a1', 'post_0a13', 'post_14a30', 'post_31a60', 'post_60+']
d['evbin'] = pd.Categorical(d['rel'].apply(binf), categories=order)

def coef(m, nm):
    ci = m.conf_int(); p = m.pvalues[nm]
    s = '***' if p < .01 else ('**' if p < .05 else ('*' if p < .1 else ''))
    return '%+.3f (CI[%+.3f,%+.3f], p=%.3f) %s' % (m.params[nm], ci.loc[nm, 0], ci.loc[nm, 1], p, s)

for y, lab in [('logvis', 'log VISITAS'), ('lognmv', 'log VENDA/NMV')]:
    m = smf.ols('%s ~ C(evbin)+C(SellerID)+C(day)' % y, data=d).fit(cov_type='cluster', cov_kwds=cl)
    print('\n[%s] (base = verde / >60d antes / nunca caiu; coef ~ %% vs base)' % lab)
    for b in order[1:]:
        nm = 'C(evbin)[T.%s]' % b
        if nm in m.params.index: print('  %-10s: %s' % (b, coef(m, nm)))
