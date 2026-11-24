# Diagnostico: a queda dói? a blindagem funciona? (within-seller, base diaria do time)
import pandas as pd, numpy as np
pd.set_option('display.width', 200)
f = r'C:\Users\bdacache\Downloads\base_diaria_30sellers.xlsx'
d = pd.read_excel(f, sheet_name='Diária')
d.columns = [str(c).strip() for c in d.columns]
d = d.rename(columns={'NMV (R$)': 'NMV', 'CVR %': 'CVR'})
d['Data'] = pd.to_datetime(d['Data'])

def grp(x):
    x = str(x)
    return 'verde' if (x.startswith('green') or x == 'light_green') else ('abaixo' if x in ['yellow', 'orange', 'red'] else 'outro')
d['cur_grp'] = d['Current'].map(grp); d['real_grp'] = d['Real'].map(grp)
d['blind'] = d['Blindado'].astype(str).str.strip().str.lower().isin(['sim', 's', 'true', '1'])
d = d[d['Visitas'] > 0].copy()   # CVR/NMV-per-visit exigem visitas

def cvr(g):  # conversao visit-weighted (%)
    v = g['Visitas'].sum(); return g['NSI'].sum() / v * 100 if v > 0 else np.nan
def npv(g):  # NMV por visita (R$)
    v = g['Visitas'].sum(); return g['NMV'].sum() / v if v > 0 else np.nan

def within(df, col, A, B, minn=10):
    """delta within-seller A vs B no campo col; retorna lista (nick, perfil, nA, nB, cvrA, cvrB, dCVR, dNPV)"""
    out = []
    for sid, g in df.groupby('Seller ID'):
        ga, gb = g[g[col] == A], g[g[col] == B]
        if len(ga) >= minn and len(gb) >= minn:
            out.append([g['Seller'].iloc[0], g['Perfil'].iloc[0], len(ga), len(gb),
                        cvr(ga), cvr(gb), cvr(ga) - cvr(gb), npv(ga) - npv(gb)])
    return pd.DataFrame(out, columns=['nick', 'perfil', 'nA', 'nB', 'cvrA', 'cvrB', 'dCVR_pp', 'dNPV'])

print('=' * 78); print('Q1 — A QUEDA (PUBLICA / Current) DOI? CVR verde vs abaixo, within-seller'); print('=' * 78)
q1 = within(d, 'cur_grp', 'verde', 'abaixo')
print(q1.to_string(index=False, float_format=lambda x: f'{x:.3f}'))
print(f"\nMEDIA within-seller: dCVR {q1.dCVR_pp.mean():+.3f} pp | dNMV/visita {q1.dNPV.mean():+.2f} R$ | sellers={len(q1)} | positivos(verde>abaixo): {(q1.dCVR_pp>0).sum()}/{len(q1)}")
print('Por perfil (dCVR medio):', q1.groupby('perfil').dCVR_pp.mean().round(3).to_dict())

print('\n' + '=' * 78); print('Q1b — GRADIENTE: CVR verde - CVR(Current=tier), within-seller'); print('=' * 78)
for tier in ['yellow', 'orange', 'red']:
    ds, dn = [], []
    for sid, g in d.groupby('Seller ID'):
        gv, gt = g[g.cur_grp == 'verde'], g[g.Current == tier]
        if len(gv) >= 10 and len(gt) >= 10:
            ds.append(cvr(gv) - cvr(gt)); dn.append(g['Seller'].iloc[0])
    if ds: print(f'  verde - {tier:7s}: dCVR medio {np.mean(ds):+.3f} pp (n_sellers={len(ds)})')
    else: print(f'  verde - {tier:7s}: amostra insuficiente (<10 dias publicos em {len(dn)} sellers)')

print('\n' + '=' * 78); print('Q2 — A BLINDAGEM FUNCIONA? entre dias Real-abaixo: blindado vs nao, within-seller'); print('=' * 78)
sub = d[d.real_grp == 'abaixo'].copy()
sub['bl'] = np.where(sub.blind, 'blindado', 'naoblind')
q2 = within(sub, 'bl', 'blindado', 'naoblind')
print(q2.to_string(index=False, float_format=lambda x: f'{x:.3f}'))
if len(q2):
    print(f"\nMEDIA within-seller: dCVR {q2.dCVR_pp.mean():+.3f} pp | dNMV/visita {q2.dNPV.mean():+.2f} R$ | sellers={len(q2)} | positivos(blindado>nao): {(q2.dCVR_pp>0).sum()}/{len(q2)}")
print('\n--- valor da blindagem por SEVERIDADE Real (blindado vs nao, pooled visit-weighted) ---')
for tier in ['yellow', 'orange', 'red']:
    s = sub[sub.Real == tier]
    bl, nb = s[s.blind], s[~s.blind]
    if len(bl) >= 10 and len(nb) >= 10:
        print(f'  {tier:7s}: CVR blindado {cvr(bl):.3f} vs nao {cvr(nb):.3f} -> {cvr(bl)-cvr(nb):+.3f} pp | dias bl/nb {len(bl)}/{len(nb)}')
    else:
        print(f'  {tier:7s}: amostra fraca (dias bl/nb {len(bl)}/{len(nb)})')
