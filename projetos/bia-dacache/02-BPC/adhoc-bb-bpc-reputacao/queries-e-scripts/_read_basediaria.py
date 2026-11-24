import pandas as pd
pd.set_option('display.width', 240); pd.set_option('display.max_columns', 60)
f = r'C:\Users\bdacache\Downloads\base_diaria_30sellers.xlsx'
xl = pd.ExcelFile(f)
print('ABAS:', xl.sheet_names)
for sh in xl.sheet_names:
    d = pd.read_excel(f, sheet_name=sh)
    print('\n' + '=' * 90)
    print('ABA:', sh, '| shape:', d.shape)
    print('=' * 90)
    print('COLUNAS:', list(d.columns))
    print('\nDTYPES:')
    print(d.dtypes.to_string())
    print('\nHEAD (12):')
    print(d.head(12).to_string())
    # tentar achar coluna de data e de seller
    for c in d.columns:
        cl = str(c).lower()
        if any(k in cl for k in ['dia', 'date', 'dt', 'data', 'mes', 'month']):
            try:
                vals = pd.to_datetime(d[c], errors='coerce')
                if vals.notna().any():
                    print(f'\n[data?] {c}: {vals.min()} -> {vals.max()} | {vals.dt.date.nunique()} dias distintos')
            except Exception:
                pass
        if any(k in cl for k in ['cust', 'seller', 'sel', 'id']):
            print(f'[id?] {c}: nunique={d[c].nunique()} | sample={list(d[c].dropna().unique()[:5])}')
