import pandas as pd
BASE = r'C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-06-bb-bpc-reputacao'
bd = pd.read_csv(BASE + r'\bd_panel_master.csv')
bd['TIM_DAY'] = bd['TIM_DAY'].astype(str).str[:10]

dias_total = bd['TIM_DAY'].nunique()
print('Dias-calendario distintos no painel (Jan-Mai/26):', dias_total)

# sanity: reputacao e unica por (seller,dia)?
chk = bd.groupby(['CUS_CUST_ID_SEL', 'TIM_DAY'])['SELLER_REPUTATION'].nunique()
print('seller-dias com >1 reputacao (deveria ser 0):', (chk > 1).sum())
print()

orad = bd[bd.SELLER_REPUTATION.isin(['orange', 'red'])].CUS_CUST_ID_SEL.unique()
rows = []
for sid in orad:
    s = bd[bd.CUS_CUST_ID_SEL == sid]
    rows.append({
        'nick': s.nickname.iloc[0], 'perfil': s.perfil.iloc[0], 'me': s.me_dom.iloc[0],
        'dias_seller': s['TIM_DAY'].nunique(),
        'dias_laranja': s[s.SELLER_REPUTATION == 'orange']['TIM_DAY'].nunique(),
        'dias_vermelho': s[s.SELLER_REPUTATION == 'red']['TIM_DAY'].nunique(),
        'dias_lar_ou_verm': s[s.SELLER_REPUTATION.isin(['orange', 'red'])]['TIM_DAY'].nunique(),
    })
t = pd.DataFrame(rows).sort_values('dias_lar_ou_verm', ascending=False)
t['pct_dos_dias'] = (t['dias_lar_ou_verm'] / dias_total * 100).round(1)
print(t.to_string(index=False))
print()
print('Total seller-dias em laranja+vermelho (somando os 6):', int(t['dias_lar_ou_verm'].sum()),
      'de', dias_total * 30, 'seller-dias possiveis')
