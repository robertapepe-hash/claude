# Event-study 14 meses (pre-periodo real) + DiD + efeito blindagem. Ancora: Current (publico)
import pandas as pd, numpy as np, statsmodels.formula.api as smf, warnings
warnings.filterwarnings('ignore')
BASE = r'C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-06-bb-bpc-reputacao'
d = pd.read_csv(BASE + r'\bd_diaria_14m.csv')
d['Data'] = pd.to_datetime(d['Data'])
d = d[(d['current_level'] != 'newbie') & (d['real_level'] != 'newbie')].copy()
d = d[d['visitas'] > 0].copy()

def below(x): return 1.0 if str(x) in ['yellow', 'orange', 'red'] else 0.0
d['cur_below'] = d['current_level'].map(below)
d['real_below'] = d['real_level'].map(below)
for t in ['yellow', 'orange', 'red']:
    d['cur_' + t] = (d['current_level'] == t).astype(float)
d['npv'] = d['nmv'] / d['visitas']
d['SellerID'] = d['seller_id'].astype(str)
d['day'] = d['Data'].dt.strftime('%Y%m%d')
cl = {'groups': d['SellerID']}

def coef(m, nm):
    ci = m.conf_int(); p = m.pvalues[nm]
    star = '***' if p < .01 else ('**' if p < .05 else ('*' if p < .1 else ''))
    return '%+.3f (SE %.3f, CI[%+.3f,%+.3f], p=%.3f) %s' % (m.params[nm], m.bse[nm], ci.loc[nm, 0], ci.loc[nm, 1], p, star)

print('n linhas (visitas>0, sem newbie):', len(d), '| sellers:', d.SellerID.nunique())
print('\n===== DiD CONTEMPORANEO (FE seller+dia, CVR ponderado por visitas) =====')
m1 = smf.wls('CVR ~ cur_below + C(SellerID)+C(day)', data=d, weights=d['visitas']).fit(cov_type='cluster', cov_kwds=cl)
print('CVR ~ Current abaixo :', coef(m1, 'cur_below'))
m2 = smf.wls('CVR ~ cur_yellow+cur_orange+cur_red + C(SellerID)+C(day)', data=d, weights=d['visitas']).fit(cov_type='cluster', cov_kwds=cl)
for t in ['cur_yellow', 'cur_orange', 'cur_red']: print('   ', t, ':', coef(m2, t))
m3 = smf.ols('npv ~ cur_below + C(SellerID)+C(day)', data=d).fit(cov_type='cluster', cov_kwds=cl)
print('NMV/visita ~ Current abaixo :', coef(m3, 'cur_below'))

print('\n===== EVENT-STUDY (1a queda publica; base = verde / >60d antes ou nunca caiu) =====')
ev = d[d.cur_below == 1].groupby('seller_id')['Data'].min().rename('event0').reset_index()
print('sellers com evento:', len(ev), '| 1a queda por trimestre:',
      ev.assign(q=ev.event0.dt.year.astype(str)+'Q'+ev.event0.dt.quarter.astype(str)).groupby('q').size().to_dict())
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
print('obs por bin (treated):', d[d.event0.notna()].evbin.value_counts().reindex(order).to_dict())
for y, lab in [('CVR', 'CVR (pp)'), ('npv', 'NMV/visita (R$)')]:
    m = smf.wls('%s ~ C(evbin)+C(SellerID)+C(day)' % y, data=d, weights=d['visitas']).fit(cov_type='cluster', cov_kwds=cl)
    print('\n[%s]' % lab)
    for b in order[1:]:
        nm = 'C(evbin)[T.%s]' % b
        if nm in m.params.index: print('  %-10s: %s' % (b, coef(m, nm)))

print('\n===== EFEITO DA BLINDAGEM (entre dias Real-abaixo: Current verde vs nao) =====')
sub = d[d.real_below == 1].copy()
sub['shown_green'] = (sub.cur_below == 0).astype(float)  # blindado = Real abaixo mas Current verde
mb = smf.wls('CVR ~ shown_green + C(SellerID)+C(day)', data=sub, weights=sub['visitas']).fit(cov_type='cluster', cov_kwds=cl)
print('CVR ~ mostrado verde (blindado) | dias Real-abaixo n=%d:' % len(sub), coef(mb, 'shown_green'))
mbn = smf.ols('npv ~ shown_green + C(SellerID)+C(day)', data=sub).fit(cov_type='cluster', cov_kwds=cl)
print('NMV/visita ~ mostrado verde (blindado):', coef(mbn, 'shown_green'))
