# Une os CSVs mensais + junta perfil dos sellers + perfila a base do painel
import pandas as pd, numpy as np, glob, os

BASE = r'C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-06-bb-bpc-reputacao'
VERDE = ['green_platinum', 'green', 'light_green']   # "verde" = bom standing
ABAIXO = ['yellow', 'orange', 'red']                  # "abaixo de verde" = caiu

files = sorted(glob.glob(BASE + r'\bd_panel_2026*.csv'))
print('arquivos:', [os.path.basename(f) for f in files])
dfs = []
for f in files:
    d = pd.read_csv(f)
    d['MONTH'] = os.path.basename(f).replace('bd_panel_', '')[:6]
    dfs.append(d)
bd = pd.concat(dfs, ignore_index=True)
for c in ['MATCH_VISITS', 'VISITS_MATCH', 'VISITS_EXPENSIVE', 'VISITS_CHEAPER']:
    bd[c] = pd.to_numeric(bd[c], errors='coerce')

# perfil dos sellers
s = pd.read_csv(BASE + r'\sellers.csv')
prof = s.set_index('cust')[['nickname', 'perfil', 'pct_me1', 'pct_me2']]
prof['me_dom'] = np.where(prof.pct_me1 >= 0.7, 'ME1', np.where(prof.pct_me2 >= 0.7, 'ME2', 'misto'))
bd = bd.merge(prof, left_on='CUS_CUST_ID_SEL', right_index=True, how='left')

bd['rep_grp'] = np.where(bd.SELLER_REPUTATION.isin(VERDE), 'VERDE',
                np.where(bd.SELLER_REPUTATION.isin(ABAIXO), 'ABAIXO', '?'))

bd.to_csv(BASE + r'\bd_panel_master.csv', index=False, encoding='utf-8-sig')
print('MASTER:', bd.shape)
print('linhas por mes:'); print(bd.groupby('MONTH').size().to_string())
print('sellers no painel:', bd.CUS_CUST_ID_SEL.nunique(), '/ 30')
print('reputacao (linhas):', bd.SELLER_REPUTATION.value_counts(dropna=False).to_dict())
ct = pd.crosstab(bd.CUS_CUST_ID_SEL, bd.rep_grp)
both = ((ct.get('VERDE', 0) > 0) & (ct.get('ABAIXO', 0) > 0)).sum()
print('sellers com item-dias em AMBOS (VERDE e ABAIXO):', both, '/ 30  <- base p/ delta within-seller')
print('sellers 100%% verde no YTD (nunca cairam):', ((ct.get('ABAIXO', 0) == 0)).sum())
