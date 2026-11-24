# Consolidado executivo BB x BPC x Venda - abas tematicas com contexto
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
OUT = r'C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-06-bb-bpc-reputacao\BB x BPC - Consolidado.xlsx'
BLUE='1F4E79'; HEAD='4472C4'; LIGHT='D9E1F2'; GREY='F2F2F2'
b=Side(style='thin',color='BFBFBF'); BORD=Border(top=b,bottom=b,left=b,right=b)
wb=Workbook(); wb.remove(wb.active)

def tab(name, title, ctx, blocks):
    ws=wb.create_sheet(name); ws.sheet_view.showGridLines=False
    ws.column_dimensions['A'].width=46
    for c in 'BCDEFG': ws.column_dimensions[c].width=16
    ws['A1']=title; ws['A1'].font=Font(bold=True,size=14,color=BLUE)
    r=2
    for line in ctx:
        ws.cell(r,1,line); c=ws.cell(r,1); c.font=Font(italic=True,size=10,color='404040'); c.alignment=Alignment(wrap_text=True,vertical='top')
        ws.merge_cells(start_row=r,start_column=1,end_row=r,end_column=7); ws.row_dimensions[r].height=14*(1+len(line)//95); r+=1
    r+=1
    for blk in blocks:
        if blk.get('h'): ws.cell(r,1,blk['h']); ws.cell(r,1).font=Font(bold=True,size=11,color=BLUE); r+=1
        hdr=blk['headers']; rows=blk['rows']
        for j,h in enumerate(hdr):
            cc=ws.cell(r,1+j,h); cc.font=Font(bold=True,color='FFFFFF'); cc.fill=PatternFill('solid',fgColor=HEAD); cc.alignment=Alignment(wrap_text=True,vertical='center',horizontal='center' if j else 'left'); cc.border=BORD
        r+=1
        for row in rows:
            for j,v in enumerate(row):
                cc=ws.cell(r,1+j,v); cc.border=BORD; cc.alignment=Alignment(horizontal='center' if j else 'left',vertical='center',wrap_text=(j==0))
                if isinstance(v,str) and (v.startswith('+') or v.startswith('-') or v.startswith('−')): cc.font=Font(color=('C00000' if (v.startswith('-') or v.startswith('−')) else '1F7A1F'))
            tot = isinstance(row[0],str) and ('Total' in row[0] or 'Média' in row[0] or 'MEDIA' in row[0])
            if tot:
                for j in range(len(row)): ws.cell(r,1+j).font=Font(bold=True); ws.cell(r,1+j).fill=PatternFill('solid',fgColor=GREY)
            r+=1
        if blk.get('note'):
            ws.cell(r,1,blk['note']); ws.cell(r,1).font=Font(italic=True,size=9,color='808080'); ws.cell(r,1).alignment=Alignment(wrap_text=True); ws.merge_cells(start_row=r,start_column=1,end_row=r,end_column=7); ws.row_dimensions[r].height=14*(1+len(blk['note'])//95); r+=1
        r+=1

# ---------- 0 Sumario ----------
tab('0. Sumário Executivo','BB × BPC × Venda — Sumário Executivo',
 ['Pergunta: a queda de reputação prejudica o negócio do seller (BB, BPC, conversão, NMV)? Vale a MELI blindar reputação de sellers estratégicos?',
  'Escopo: 30 top sellers assessorados (ex-1P), HOME ELECTRONICS / Large Appliances + TV, H&B (Heavy & Bulky), MLB. Período: YTD Jan–Mai/26 + extensão Q2/25→Mai/26 (14 meses). Método: taxa within-seller (Metodologia 2.0).'],
 [{'h':'Achados confirmados','headers':['Achado','Resultado'],'rows':[
   ['1. Quem cai é PERFIL/logística','D2C 6/7 e ME1 7/8 caem muito; SELLER/ME2 quase nunca. Só 13/30 caem em 14m.'],
   ['2. Reputação → BB escalona por cor','Binário ≈0; dose: verde−yellow +0,6 / orange +2,8 / red +4,6 pp. É fenômeno de PICO (Q4 +4 vs normal ~0).'],
   ['3. BB → BPC','Ganhador de BB tem BPC +13 pp (estável). Ressalva: tautológico (BB=menor preço).'],
   ['4. Reputação → conversão/NMV','SEM penalidade (event-study limpo, 14m): pós-queda CVR e NMV/visita ficam iguais ou maiores.'],
   ['5. Blindagem','Já existe e é pesada no severo (Q4 20%). Efeito na conversão nulo a negativo, mas confundido por seleção.'],
 ],'note':'Conclusão: reputação tem impacto de negócio LIMITADO nesses top sellers. Justificativa de receita pra blindar é fraca. Pra decidir de verdade: A/B test de blindagem.'}])

# ---------- 1 Quem cai ----------
tab('1. Quem cai (perfil)','Achado 1 — Quem cai de reputação é efeito de perfil (logística)',
 ['Contexto: medimos a frequência de cada seller ficar abaixo de verde (yellow/orange/red). A queda NÃO é aleatória — concentra num perfil. Mecanismo provável: ME1 (logística própria) acumula atritos de entrega → reputação cai; ME2 (logística MELI/Full) se mantém verde.'],
 [{'headers':['Corte','Sellers que caem','% médio de dias abaixo de verde'],'rows':[
   ['D2C (loja oficial da marca)','6 / 7','44,9%'],
   ['SELLER (marketplace)','5 / 23','5,5%'],
   ['ME1 (logística própria)','7 / 8','46,9%'],
   ['ME2 (logística MELI)','4 / 22','3,0%'],
 ],'note':'Só 13/30 sellers caíram abaixo de verde em 14 meses (11/30 no YTD; 19 nunca caíram). Campeões de queda: MIDEA, OFICIALELECTROLUX, BUD — todos D2C + ME1. → "É entre lojas", não entre períodos.'}])

# ---------- 2 Reputacao x BB ----------
tab('2. Reputação x Ganho BB','Achado 2 — Reputação → ganho de BB: escalona por cor (dose-resposta)',
 ['Contexto: taxa de ganho de BB (proxy = menor preço MELI) within-seller, por nível de reputação. O binário "verde vs abaixo" some (~0) porque o yellow domina o "abaixo" e yellow ≈ neutro. Mas quanto mais grave a cor, maior o tombo no BB. E o efeito é de PICO.'],
 [{'h':'Dose-resposta (within-seller, 30 sellers, YTD)','headers':['Severidade','Δ taxa de ganho de BB vs verde'],'rows':[
   ['verde − yellow','+0,6 pp'],['verde − orange','+2,8 pp'],['verde − red','+4,6 pp'],
 ],'note':'orange/red são raros: 3,5% dos item-dias, concentrados em 6 sellers (quase todos ME1). Ex.: Electrolux 31 dias no vermelho (20,5% do YTD).'},
  {'h':'Fenômeno de pico (efeito green↔yellow within-seller)','headers':['Período','Δ green − yellow'],'rows':[
   ['Out/25–Mar/26 (com pico)','+3,7 pp'],['Q4 Out–Dez/25 (pico)','+4,0 pp'],['YTD Jan–Mai/26 (normal)','−2,0 pp'],
 ],'note':'Reputação pesa no BB sobretudo no pico. No período normal o efeito some. (Método antigo "share" dava +9,5 pp pró-green — artefato de exposição.)'}])

# ---------- 3 BB x BPC ----------
tab('3. BB x BPC','Achado 3 — Ganho de BB → BPC: firme e estável',
 ['Contexto: BPC = (visitas match + cheaper) / (match + cheaper + expensive). Comparamos o BPC quando o seller é ganhador do BB (1) vs perdedor (0). Relação sólida em todo recorte — com a ressalva de ser meio tautológica (ganhar BB = ter menor preço, que é o que o BPC mede).'],
 [{'headers':['Recorte','BPC perdedor (0)','BPC ganhador (1)','Δ'],'rows':[
   ['30 sellers (YTD)','31,1%','44,1%','+13,1 pp'],
   ['5 sellers (YTD)','39,2%','63,1%','+23,8 pp'],
   ['Doc original (Out/25–Mar/26)','41,5%','69,6%','+28,1 pp'],
 ],'note':'Direção e magnitude estáveis. Ressalva: relação esperada (não causal) pela sobreposição BB↔BPC.'}])

# ---------- 4 Conversao/NMV ----------
tab('4. Conversão e NMV','Achado 4 — Reputação → conversão/NMV: sem penalidade (event-study 14m)',
 ['Contexto: event-study (FE seller + dia, CVR ponderado por visitas) em torno da 1ª queda PÚBLICA (Current) abaixo de verde, 13 sellers, 14 meses. Pré-tendência plana = desenho válido (sem viés de antecipação). Ancorado no Current porque é o que o buyer vê.'],
 [{'h':'Trajetória em torno da queda (base = verde / >60d antes)','headers':['Janela','Δ CVR (pp)','Δ NMV/visita (R$)'],'rows':[
   ['pré (−60 a −31d)','−0,04 (ns)','−0,4 (ns)'],
   ['pré (−30 a −1d)','−0,13 (ns)','−2,6 (ns)'],
   ['pós (0–13d)','+0,07 (ns)','+2,5 **'],
   ['pós (31–60d)','+0,18 **','+4,5 ***'],
   ['pós (60d+)','+0,25 **','+4,0 *'],
 ],'note':'Cair abaixo de verde NÃO derruba venda; conversão e NMV/visita ficam iguais ou MAIORES depois (provável reação de preço/promo = causalidade reversa). DiD contemporâneo confirma (Current abaixo → CVR +0,12 pp; orange +3,2; red +1,3).'}])

# ---------- 5 Blindagem ----------
tab('5. Blindagem','Achado 5 — Blindagem: já existe, pesada no severo, efeito não-identificável',
 ['Contexto: Current = nível público; Real = real; Blindado quando Current mostra verde sobre um Real pior. A MELI já blinda boa parte do severo. O efeito de "mostrar verde" na conversão é nulo a negativo — MAS é confundido por seleção (a MELI blinda justamente os casos/momentos mais frágeis), então blindado vs não-blindado não é comparável.'],
 [{'h':'Quanto já se blinda','headers':['Item','Valor'],'rows':[
   ['Seller-dias blindados (14m)','13,8%'],['Pico Q4/25','20,2%'],
   ['Real=orange mostrado verde','~75%'],['Real=red mostrado verde','~56%'],
 ]},
  {'h':'Efeito de mostrar verde (entre dias Real-abaixo)','headers':['Desfecho','Efeito'],'rows':[
   ['CVR (geral)','−0,14 pp (ns)'],['NMV/visita (geral)','−R$ 11,3 **'],
   ['CVR | Real=yellow','+0,13 pp *'],['CVR | Real=red','−1,30 pp ***'],
 ],'note':'Efeito nulo/negativo NÃO significa que blindar atrapalha — é seleção (não-aleatório). Só um A/B test (blindar aleatoriamente) responde causalmente.'}])

# ---------- 6 Queries ----------
wsq=wb.create_sheet('6. Queries'); wsq.sheet_view.showGridLines=False; wsq.column_dimensions['A'].width=130
wsq['A1']='Queries fonte'; wsq['A1'].font=Font(bold=True,size=14,color=BLUE)
import os
qfiles=[('Painel BB/BPC (item-dia) — DM_COM_COMPETENCIA','query.sql'),
        ('Base diária A — Reputação (Real/Current/Blindado) — BT_REP_SELLER_REPUTATION_LOG','_ext_A_rep.sql'),
        ('Base diária B — Visitas (escopo H&B) — BT_VISITS_MLB_UF','_ext_B_vis.sql'),
        ('Base diária C — Venda (NMV/NSI) — DM_EFICIENCIA_MLB','_ext_C_venda.sql')]
r=3
base=r'C:\Users\bdacache\Documents\Claude\Projects\Ad-Hoc\2026-06-bb-bpc-reputacao'
for title,fn in qfiles:
    wsq.cell(r,1,title); wsq.cell(r,1).font=Font(bold=True,color=BLUE); r+=1
    try:
        txt=open(os.path.join(base,fn),encoding='utf-8').read()
    except Exception: txt='(arquivo: '+fn+')'
    for line in txt.split('\n'):
        wsq.cell(r,1,line); wsq.cell(r,1).font=Font(name='Consolas',size=9); r+=1
    r+=1

# ---------- 7 Glossario ----------
tab('7. Glossário','Glossário e definições',
 ['Termos e campos usados nas análises.'],
 [{'headers':['Termo','Definição'],'rows':[
   ['item-dia','1 linha por item (MELI_ID) por dia. Grão da análise de BB.'],
   ['seller-dia','1 linha por seller por dia. Grão da análise de conversão/NMV (reputação é da loja).'],
   ['GANHADOR_BB','1 quando o item do seller é o de menor preço MELI no catálogo. Proxy de liderança de preço — NÃO é o ganhador real do Buy Box.'],
   ['BPC','(VISITS_MATCH + VISITS_CHEAPER) / (VISITS_MATCH + VISITS_CHEAPER + VISITS_EXPENSIVE). Share de visitas em preço competitivo.'],
   ['Real / Current','Real = reputação verdadeira; Current = nível público mostrado ao buyer.'],
   ['Blindado','Current mostra um nível melhor que o Real (MELI "protege" a vitrine).'],
   ['verde / abaixo','verde = green_platinum/gold/silver/green/light_green; abaixo = yellow/orange/red. newbie (seller novo) é excluído.'],
   ['D2C / SELLER','D2C = loja oficial da marca; SELLER = marketplace.'],
   ['ME1 / ME2','% do faturamento por logística própria (ME1) vs logística MELI/Full (ME2).'],
   ['H&B','Heavy & Bulky (ITE_ITEM_HB_FLG / FLG_BULKY): itens pesados (geladeira, lava-roupas, TV, fogão).'],
 ]}])

wb.save(OUT)
print('SALVO:', OUT)
print('ABAS:', wb.sheetnames)
