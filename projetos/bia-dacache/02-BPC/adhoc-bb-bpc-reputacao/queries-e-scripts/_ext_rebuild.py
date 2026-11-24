# Remonta a base diaria 14 meses (Q2'25->Mai'26) a partir de A(rep)+B(vis)+C(venda)
import pandas as pd, numpy as np
BASE = r'C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-06-bb-bpc-reputacao'

rep = pd.read_csv(BASE + r'\bd_rep.csv')      # seller_id, day, current_level, real_level, blindado
vis = pd.read_csv(BASE + r'\bd_vis.csv')      # seller_id, dia, visitas, visitas_vip
ven = pd.read_csv(BASE + r'\bd_venda.csv')    # seller_id, dia, nmv, nsi
rep = rep.rename(columns={'day': 'dia'})
for df in (rep, vis, ven):
    df['dia'] = pd.to_datetime(df['dia']).dt.strftime('%Y-%m-%d')

# espinha = reputacao (seller x dia continuo); junta vis e venda
d = rep.merge(vis, on=['seller_id', 'dia'], how='left').merge(ven, on=['seller_id', 'dia'], how='left')
for c in ['visitas', 'visitas_vip', 'nmv', 'nsi']:
    d[c] = pd.to_numeric(d[c], errors='coerce').fillna(0)
d['CVR'] = np.where(d['visitas'] > 0, d['nsi'] / d['visitas'] * 100, np.nan)

# perfil
s = pd.read_csv(BASE + r'\sellers.csv')[['cust', 'nickname', 'perfil']]
d = d.merge(s, left_on='seller_id', right_on='cust', how='left').drop(columns=['cust'])

d['Data'] = pd.to_datetime(d['dia'])
d['MONTH'] = d['Data'].dt.strftime('%Y-%m')
d['QUARTER'] = d['Data'].dt.year.astype(str) + 'Q' + d['Data'].dt.quarter.astype(str)
d.to_csv(BASE + r'\bd_diaria_14m.csv', index=False, encoding='utf-8-sig')

print('SHAPE:', d.shape, '| sellers:', d.seller_id.nunique(), '| dias:', d.dia.nunique(),
      '|', d.dia.min(), '->', d.dia.max())
print('esperado ~', d.seller_id.nunique() * d.dia.nunique(), 'linhas (seller x dia)')
print('\nlinhas por trimestre:'); print(d.groupby('QUARTER').size().to_string())
print('\nBlindado:', d['blindado'].value_counts(dropna=False).to_dict())
print('Real (dist):', d['real_level'].value_counts(dropna=False).to_dict())
print('Current (dist):', d['current_level'].value_counts(dropna=False).to_dict())
print('dias Visitas=0:', int((d.visitas == 0).sum()), '| NMV=0:', int((d.nmv == 0).sum()))
# cobertura do Real (a blindagem existia em 2025?)
def grp(x): x=str(x); return 'abaixo' if x in ['yellow','orange','red'] else 'verde'
d['real_grp'] = d['real_level'].map(grp)
print('\nsellers com Real abaixo de verde (algum dia):', d[d.real_grp=='abaixo'].seller_id.nunique(), '/30')
print('blindado por trimestre:'); print(d.groupby('QUARTER')['blindado'].mean().round(3).to_string())
