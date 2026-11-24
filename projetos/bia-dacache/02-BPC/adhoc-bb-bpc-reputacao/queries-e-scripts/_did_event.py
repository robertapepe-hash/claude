# Event-study: trajetoria de CVR/NMV em torno da 1a queda publica (Current verde->abaixo)
import pandas as pd, numpy as np, statsmodels.formula.api as smf, warnings
warnings.filterwarnings('ignore')
f = r'C:\Users\bdacache\Downloads\base_diaria_30sellers.xlsx'
d = pd.read_excel(f, sheet_name='Diária')
d.columns = [str(c).strip() for c in d.columns]
d = d.rename(columns={'NMV (R$)': 'NMV', 'CVR %': 'CVR'})
d['Data'] = pd.to_datetime(d['Data'])
d = d[d['Visitas'] > 0].copy()

def grp(x):
    x = str(x); return 'abaixo' if x in ['yellow', 'orange', 'red'] else 'verde'
d['cur_below'] = (d['Current'].map(grp) == 'abaixo').astype(int)

# 1a data abaixo de verde por seller = evento
ev = d[d.cur_below == 1].groupby('Seller ID')['Data'].min().rename('event0').reset_index()
print('Sellers com queda publica (evento):', len(ev))
print('Quando caíram (1a vez):'); print(ev.assign(m=ev.event0.dt.strftime('%Y-%m')).groupby('m').size().to_string())

d = d.merge(ev, on='Seller ID', how='left')
d['rel'] = (d['Data'] - d['event0']).dt.days

def binf(r):
    if pd.isna(r) or r < -21: return 'base'
    if r < 0: return 'pre_1a21'
    if r <= 13: return 'post_0a13'
    if r <= 30: return 'post_14a30'
    return 'post_30+'
d['evbin'] = pd.Categorical(d['rel'].apply(binf), categories=['base', 'pre_1a21', 'post_0a13', 'post_14a30', 'post_30+'])
d['SellerID'] = d['Seller ID'].astype(str); d['day'] = d['Data'].dt.strftime('%Y%m%d')
d['npv'] = d['NMV'] / d['Visitas']
print('\nobs por bin (treated):'); print(d[d.event0.notna()].evbin.value_counts().reindex(['base','pre_1a21','post_0a13','post_14a30','post_30+']).to_string())

cl = {'groups': d['SellerID']}
def run(y, lab):
    m = smf.wls('%s ~ C(evbin) + C(SellerID) + C(day)' % y, data=d, weights=d['Visitas']).fit(cov_type='cluster', cov_kwds=cl)
    ci = m.conf_int()
    print('\n[%s]  (base = seller verde / >21d antes da queda)' % lab)
    for b in ['pre_1a21', 'post_0a13', 'post_14a30', 'post_30+']:
        nm = 'C(evbin)[T.%s]' % b
        if nm in m.params.index:
            p = m.pvalues[nm]; star = '***' if p < .01 else ('**' if p < .05 else ('*' if p < .1 else ''))
            print('  %-11s: %+.3f (SE %.3f, 95%%CI [%+.3f, %+.3f], p=%.3f) %s' % (b, m.params[nm], m.bse[nm], ci.loc[nm, 0], ci.loc[nm, 1], p, star))

run('CVR', 'CVR (pp) em torno da queda')
run('npv', 'NMV/visita (R$) em torno da queda')
