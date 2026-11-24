# DiD / two-way fixed effects (seller + dia): efeito da queda PUBLICA na conversao/NMV
import pandas as pd, numpy as np
import statsmodels.formula.api as smf
import warnings; warnings.filterwarnings('ignore')

f = r'C:\Users\bdacache\Downloads\base_diaria_30sellers.xlsx'
d = pd.read_excel(f, sheet_name='Diária')
d.columns = [str(c).strip() for c in d.columns]
d = d.rename(columns={'NMV (R$)': 'NMV', 'CVR %': 'CVR'})
d['Data'] = pd.to_datetime(d['Data'])
d = d[d['Visitas'] > 0].copy()

def grp(x):
    x = str(x); return 'verde' if (x.startswith('green') or x == 'light_green') else 'abaixo'
d['cur_below'] = (d['Current'].map(grp) == 'abaixo').astype(float)
d['real_below'] = (d['Real'].map(grp) == 'abaixo').astype(float)
for t in ['yellow', 'orange', 'red']:
    d['cur_' + t] = (d['Current'] == t).astype(float)
d['SellerID'] = d['Seller ID'].astype(str)
d['day'] = d['Data'].dt.strftime('%Y%m%d')
d['npv'] = d['NMV'] / d['Visitas']

cl = {'groups': d['SellerID']}

def show(m, names, label):
    ci = m.conf_int()
    print(f'\n[{label}]  n={int(m.nobs)}')
    for nm in names:
        if nm in m.params.index:
            star = '***' if m.pvalues[nm] < .01 else ('**' if m.pvalues[nm] < .05 else ('*' if m.pvalues[nm] < .1 else ''))
            print(f'  {nm:12s}: {m.params[nm]:+.3f}  (SE {m.bse[nm]:.3f}, 95%CI [{ci.loc[nm,0]:+.3f}, {ci.loc[nm,1]:+.3f}], p={m.pvalues[nm]:.3f}) {star}')

print('=' * 76)
print('Desfecho 1: CVR (conversao, pp) — ponderado por Visitas')
print('=' * 76)
m1 = smf.wls('CVR ~ cur_below + C(SellerID) + C(day)', data=d, weights=d['Visitas']).fit(cov_type='cluster', cov_kwds=cl)
show(m1, ['cur_below'], 'Current abaixo de verde -> CVR')
m1r = smf.wls('CVR ~ real_below + C(SellerID) + C(day)', data=d, weights=d['Visitas']).fit(cov_type='cluster', cov_kwds=cl)
show(m1r, ['real_below'], 'Real abaixo (contraste; blindagem deve mascarar) -> CVR')
m2 = smf.wls('CVR ~ cur_yellow + cur_orange + cur_red + C(SellerID) + C(day)', data=d, weights=d['Visitas']).fit(cov_type='cluster', cov_kwds=cl)
show(m2, ['cur_yellow', 'cur_orange', 'cur_red'], 'Severidade publica -> CVR (base=verde)')

print('\n' + '=' * 76)
print('Desfecho 2: NMV por visita (R$)')
print('=' * 76)
m3 = smf.ols('npv ~ cur_below + C(SellerID) + C(day)', data=d).fit(cov_type='cluster', cov_kwds=cl)
show(m3, ['cur_below'], 'Current abaixo -> NMV/visita')
m4 = smf.ols('npv ~ cur_yellow + cur_orange + cur_red + C(SellerID) + C(day)', data=d).fit(cov_type='cluster', cov_kwds=cl)
show(m4, ['cur_yellow', 'cur_orange', 'cur_red'], 'Severidade publica -> NMV/visita (base=verde)')

print('\nMedia geral CVR: %.3f%% | media NMV/visita: R$ %.1f' % (
    (d['NSI'].sum() / d['Visitas'].sum() * 100), (d['NMV'].sum() / d['Visitas'].sum())))
print('dias publicos abaixo de verde (cur_below=1):', int(d['cur_below'].sum()), '/', len(d))
print('sellers clusters:', d['SellerID'].nunique())
