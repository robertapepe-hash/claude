# Validacao dos 3 blocos do Resumo - BB x BPC (YTD Jan-Mai 2026, 5 sellers)
import pandas as pd

P = r'C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-06-bb-bpc-reputacao\bd.csv'
bd = pd.read_csv(P)
for c in ['VISITS_MATCH', 'VISITS_EXPENSIVE', 'VISITS_CHEAPER', 'MATCH_VISITS']:
    bd[c] = pd.to_numeric(bd[c], errors='coerce').fillna(0)

names = bd.groupby('CUS_CUST_ID_SEL')['CUS_NICKNAME'].first().to_dict()
print('SHAPE', bd.shape, '| dias', bd['TIM_DAY'].nunique(), '|', bd['TIM_DAY'].min(), '->', bd['TIM_DAY'].max())
print('SELLERS:', names)
print()
print('=== REPUTACAO x SELLER (linhas) ===')
print(pd.crosstab(bd['CUS_CUST_ID_SEL'], bd['SELLER_REPUTATION']).to_string())
print()

# ---- BLOCO 1: ganho de BB (item-dias, GANHADOR_BB=1) por seller x green/yellow ----
won = bd[bd['GANHADOR_BB'] == 1]
b1 = (won[won['SELLER_REPUTATION'].isin(['green', 'yellow'])]
      .groupby(['CUS_CUST_ID_SEL', 'SELLER_REPUTATION']).size()
      .unstack(fill_value=0).reindex(columns=['green', 'yellow'], fill_value=0))
b1['tot'] = b1['green'] + b1['yellow']
b1['green_%'] = (b1['green'] / b1['tot']).round(4)
b1['yellow_%'] = (b1['yellow'] / b1['tot']).round(4)
print('=== BLOCO 1 - ganho de BB (item-dias) por seller x green/yellow ===')
print(b1.to_string())
tg, ty = b1['green'].sum(), b1['yellow'].sum()
gp, yp = tg / (tg + ty), ty / (tg + ty)
print(f'TOTAL GERAL: green {tg} ({gp:.4f}) | yellow {ty} ({yp:.4f}) | delta {round((gp-yp)*100,2)} pp')
print()

# ---- BLOCO 2: BPC por GANHADOR_BB (1 ganhador vs 0 perdedor) ----
g = bd.groupby('GANHADOR_BB')[['VISITS_MATCH', 'VISITS_EXPENSIVE', 'VISITS_CHEAPER']].sum()
g['BPC'] = (g['VISITS_MATCH'] + g['VISITS_CHEAPER']) / (g['VISITS_MATCH'] + g['VISITS_CHEAPER'] + g['VISITS_EXPENSIVE'])
print('=== BLOCO 2 - BPC por GANHADOR_BB ===')
print(g['BPC'].round(4).to_string())
print(f'delta {round((g["BPC"].get(1,0)-g["BPC"].get(0,0))*100,2)} pp')
print()

# ---- Cross-check: quanto green/yellow cobre do total de ganhos de BB ----
won_all = len(won)
won_gy = len(won[won['SELLER_REPUTATION'].isin(['green', 'yellow'])])
print(f'COBERTURA green/yellow nos ganhos de BB: {won_gy}/{won_all} = {won_gy/won_all:.1%} (resto fica fora do Bloco 1)')
