import pandas as pd, numpy as np
pd.set_option('display.width', 200)
f = r'C:\Users\bdacache\Downloads\base_diaria_30sellers.xlsx'
d = pd.read_excel(f, sheet_name='Diária')
d.columns = [str(c).strip() for c in d.columns]
d['Data'] = pd.to_datetime(d['Data'])

def grp(x):
    x = str(x)
    return 'verde' if (x.startswith('green') or x == 'light_green') else ('abaixo' if x in ['yellow', 'orange', 'red'] else 'outro')
d['real_grp'] = d['Real'].map(grp); d['cur_grp'] = d['Current'].map(grp)
d['blind'] = d['Blindado'].astype(str).str.strip().str.lower().isin(['sim', 's', 'true', '1'])

print('linhas:', len(d), '| sellers:', d['Seller ID'].nunique(), '| dias:', d['Data'].nunique(),
      '|', d['Data'].min().date(), '->', d['Data'].max().date())
print('Blindado:', d['blind'].value_counts().to_dict())
print('\nReal (dist):', d['Real'].value_counts().to_dict())
print('Current (dist):', d['Current'].value_counts().to_dict())

print('\n--- Blindado=SIM: Real (linhas) x Current (colunas) ---')
b = d[d.blind]
print('n blindado:', len(b), '| sellers já blindados:', b['Seller ID'].nunique())
print(pd.crosstab(b['Real'], b['Current']))

print('\n--- atividade ---')
print('dias com Visitas=0:', (d['Visitas'] == 0).sum(), '| NMV=0:', (d['NMV (R$)'] == 0).sum())

dd = d[d['Visitas'] > 0].copy()
print('\nCVR%% medio por REAL grp (visitas>0):')
print(dd.groupby('real_grp')['CVR %'].agg(['mean', 'count']).round(3).to_string())
print('\nCVR%% medio por CURRENT grp (visitas>0):')
print(dd.groupby('cur_grp')['CVR %'].agg(['mean', 'count']).round(3).to_string())
print('\nCVR%% por nivel REAL (visitas>0):')
print(dd.groupby('Real')['CVR %'].agg(['mean', 'count']).round(3).to_string())
