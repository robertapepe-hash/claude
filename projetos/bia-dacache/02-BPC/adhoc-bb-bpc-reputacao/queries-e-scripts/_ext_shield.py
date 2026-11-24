# Efeito da blindagem: entre dias Real-abaixo, mostrar verde (blindado) vs mostrar o real baixo
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
d['npv'] = d['nmv'] / d['visitas']
d['SellerID'] = d['seller_id'].astype(str)
d['mon'] = d['MONTH']

def coef(m, nm):
    ci = m.conf_int(); p = m.pvalues[nm]
    star = '***' if p < .01 else ('**' if p < .05 else ('*' if p < .1 else ''))
    return '%+.3f (SE %.3f, CI[%+.3f,%+.3f], p=%.3f) %s' % (m.params[nm], m.bse[nm], ci.loc[nm, 0], ci.loc[nm, 1], p, star)

sub = d[d.real_below == 1].copy()
sub['shown_green'] = (sub.cur_below == 0).astype(float)  # blindado
print('dias Real-abaixo (visitas>0):', len(sub), '| blindados:', int(sub.shown_green.sum()),
      '| nao-blindados:', int((1 - sub.shown_green).sum()), '| sellers:', sub.SellerID.nunique())
clb = {'groups': sub['SellerID']}
mb = smf.wls('CVR ~ shown_green + C(SellerID)+C(mon)', data=sub, weights=sub['visitas']).fit(cov_type='cluster', cov_kwds=clb)
print('\nCVR ~ mostrado-verde (FE seller+mes):', coef(mb, 'shown_green'))
mbn = smf.ols('npv ~ shown_green + C(SellerID)+C(mon)', data=sub).fit(cov_type='cluster', cov_kwds=clb)
print('NMV/visita ~ mostrado-verde:', coef(mbn, 'shown_green'))

print('\n--- por severidade do Real (efeito de mostrar verde), FE seller+mes ---')
for tier in ['yellow', 'orange', 'red']:
    s = sub[sub.real_level == tier].copy()
    n1, n0 = int(s.shown_green.sum()), int((1 - s.shown_green).sum())
    if n1 >= 20 and n0 >= 20 and s.SellerID.nunique() >= 2:
        cs = {'groups': s['SellerID']}
        try:
            m = smf.wls('CVR ~ shown_green + C(SellerID)+C(mon)', data=s, weights=s['visitas']).fit(cov_type='cluster', cov_kwds=cs)
            print('  Real=%-7s (bl/nbl %d/%d): CVR %s' % (tier, n1, n0, coef(m, 'shown_green')))
        except Exception as e:
            print('  Real=%-7s: erro (%s)' % (tier, str(e)[:50]))
    else:
        print('  Real=%-7s: amostra fraca (bl/nbl %d/%d)' % (tier, n1, n0))
