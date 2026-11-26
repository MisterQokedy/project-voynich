import json, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, numpy as np
V='./work/'; O=V+'paper/figures/'
BLUE,ORANGE,GRAY,LG,TXT='#257de0','#f47230','#8a8a8a','#c8c8c8','#191919'
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#999','axes.labelcolor':TXT,'xtick.color':'#555','ytick.color':'#555','axes.grid':True,'grid.color':'#eee'})
# Fig 1: sheet order p-values
q=['1','2','3','4','5','6','7','13','20']; p={'TF-IDF':[.95,.99,.34,.79,.90,.78,.97,.75,.45],'LSA':[.97,.23,.06,.45,.98,.92,.89,.42,.12],'Jaccard':[.78,.69,.59,.76,.89,.72,.97,.56,.28]}
fig,ax=plt.subplots(figsize=(7,3.8)); x=np.arange(len(q))
for (k,v),m,dx in zip(p.items(),['o','s','^'],[-.18,0,.18]): ax.scatter(x+dx,v,marker=m,s=40,color=BLUE if k=='TF-IDF' else (ORANGE if k=='LSA' else GRAY),label=k,edgecolor='white',linewidth=1.5,zorder=3)
ax.axhline(.05,color=TXT,lw=1,ls='--'); ax.text(8.45,.07,'p = 0.05',ha='right',fontsize=8,color='#555')
ax.set_xticks(x,['Q'+i for i in q]); ax.set_ylim(0,1.02); ax.set_ylabel('p vs shuffled-page null'); ax.legend(frameon=False,ncol=3,loc='upper left',bbox_to_anchor=(0,-0.12),fontsize=8)
ax.set_title('Text cannot recover sheet order: no quire beats shuffled pages',fontsize=11,loc='left',color=TXT)
fig.tight_layout(); fig.savefig(O+'fig1_sheet_order_pvalues.png',dpi=200)
# Fig 2: language test
d=json.load(open(V+'language_test/results/res.json'))
grp={'Natural languages':(['latin_isidore','latin_caesar','ME_cury','EME_culpeper','italian_dante','german_faust'],GRAY,'o'),
 'Voynich (A, B, all)':(['voynich','voynich_A','voynich_B'],BLUE,'o'),
 'Ciphers & generators':(['C1_verbose_latin','C2_sorted_latin','G1_timm','G2_rugg'],ORANGE,'D'),
 'Shuffled / noise':(['ctrl_voynich_shuffled','N1_uniform_noise','N2_freq_noise'],LG,'x')}
fig,ax=plt.subplots(figsize=(6,4.2))
for g,(ks,c,m) in grp.items():
    xs=[s['S1_h2'] for k in ks for s in d[k]]; ys=[s['S6_orderMI'] for k in ks for s in d[k]]
    ax.scatter(xs,ys,color=c,marker=m,s=36 if m!='x' else 30,label=g,edgecolor='white' if m!='x' else None,linewidth=1,zorder=3)
ax.set_xlabel('Character predictability h2 (bits; lower = more predictable)'); ax.set_ylabel('Word-order information (bits)')
ax.legend(frameon=False,fontsize=8); ax.set_title('Voynich sits outside every plain language tested',fontsize=11,loc='left',color=TXT)
fig.tight_layout(); fig.savefig(O+'fig2_language_space.png',dpi=200)
# Fig 3: generator scores on held-out halves
dirs=['orig','swap','r0ab','r0ba','r1ab','r1ba']; z=json.load(open(V+'s6z/score_z1b.json')); y=json.load(open(V+'s6z/score_s6y.json'))
rows=[('Shuffled Voynich',[s for k in dirs for s in z[k]['shuffle']],LG),('Timm generator',[s for k in dirs for s in z[k]['timm']],GRAY),
      ('S6-Y',[s for k in dirs for s in y[k]['gen']],ORANGE),('S6-Z1b (frozen)',[s for k in dirs for s in z[k]['gen']],BLUE)]
fig,ax=plt.subplots(figsize=(7,3.2)); rng=np.random.default_rng(0)
for i,(n,v,c) in enumerate(rows):
    ax.scatter(np.array(v)+rng.uniform(-.15,.15,len(v)),i+rng.uniform(-.12,.12,len(v)),color=c,s=22,edgecolor='white',linewidth=.8,zorder=3)
    ax.plot([np.mean(v)]*2,[i-.3,i+.3],color=TXT,lw=2); ax.text(np.mean(v),i+.36,f'{np.mean(v):.1f}',ha='center',fontsize=8,color=TXT)
ax.set_yticks(range(4),[r[0] for r in rows]); ax.set_xlim(5,24.5); ax.set_xlabel('Statistics in the Voynich band on held-out sheets (of 24)')
ax.set_title('Copy-and-vary generator vs controls, held-out sheets',fontsize=11,loc='left',color=TXT)
fig.tight_layout(); fig.savefig(O+'fig3_generator_scores.png',dpi=200)
