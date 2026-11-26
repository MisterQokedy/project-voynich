# Figures 5-8 for the paper. Values are the headline numbers recorded in CONSOLIDATED_FINDINGS.md.
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, numpy as np
O='./work/paper/figures/'
BLUE,ORANGE,GRAY,LG,TXT='#257de0','#f47230','#8a8a8a','#c8c8c8','#191919'
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#999','axes.labelcolor':TXT,'xtick.color':'#555','ytick.color':'#555','axes.grid':True,'grid.color':'#eee','axes.axisbelow':True})
def rng_bar(ax,labels,lo,hi,cols):
    y=np.arange(len(labels))
    for i,(a,b,c) in enumerate(zip(lo,hi,cols)):
        ax.barh(i,b,color=c,height=.6,alpha=.35 if a!=b else 1); ax.barh(i,a,color=c,height=.6)
        ax.text(b+max(hi)*.01,i,f'{a:g}' if a==b else f'{a:g}–{b:g}',va='center',fontsize=8,color=TXT)
    ax.set_yticks(y,labels); ax.invert_yaxis()
# Fig 5: line and paragraph starts
fig,ax=plt.subplots(figsize=(7,2.6))
rng_bar(ax,['Paragraph starts with a gallows glyph','Other lines start with y, s or d','Same glyphs at mid-line word starts'],[80,42,12],[86,48,13],[BLUE,BLUE,GRAY])
ax.set_xlim(0,100); ax.set_xlabel('% of lines or words (range over ZL3b-n, IT2a-n, RF1b-e)')
ax.set_title('Line and paragraph openings follow their own rules',fontsize=11,loc='left',color=TXT)
fig.tight_layout(); fig.savefig(O+'fig5_line_starts.png',dpi=200)
# Fig 6: boundary coupling
L=['Voynich (3 transliterations)','German herbarium','Sanskrit (sandhi)','Tagalog (sandhi)','Abbreviated Latin MSS','Latin','Gibberish (Gaskell & Bowern)','Timm generator (fitted)','Naibbe cipher']
lo=[.16,.18,.20,.19,.05,.03,.015,.007,.002]; hi=[.19,.18,.25,.23,.05,.03,.015,.010,.002]
fig,ax=plt.subplots(figsize=(7,3.6)); rng_bar(ax,L,lo,hi,[BLUE,GRAY,GRAY,GRAY,GRAY,GRAY,ORANGE,ORANGE,ORANGE])
ax.set_xlabel('Last glyph → next word\'s first glyph (bits above shuffle)'); ax.set_xlim(0,.29)
ax.set_title('Word boundaries carry natural-language-strength coupling',fontsize=11,loc='left',color=TXT)
fig.tight_layout(); fig.savefig(O+'fig6_boundary_coupling.png',dpi=200)
# Fig 7: one-off words
fig,axs=plt.subplots(1,2,figsize=(7,2.8))
for ax,(t,v) in zip(axs,[('Share of one-off words',[.138,.077,.08]),('One-offs within one edit of previous 40 words',[.083,.23,.25])]):
    ax.bar(['Voynich','S6-Y','S6-Z1b'],v,color=[BLUE,ORANGE,ORANGE],width=.6)
    for i,x in enumerate(v): ax.text(i,x+.004,f'{x:.3g}',ha='center',fontsize=8)
    ax.set_title(t,fontsize=9,loc='left',color=TXT)
fig.suptitle('The generator makes rare words by local edits; the manuscript does not',fontsize=11,x=.02,ha='left',color=TXT)
fig.tight_layout(); fig.savefig(O+'fig7_oneoffs.png',dpi=200)
# Fig 8: P3-c line-edge pen form, Voynich vs control hand (P3-e)
fig,ax=plt.subplots(figsize=(7,2.9))
grp=['Line-initial vs mid-line','Line-final vs mid-line']
vv=[.641,.587]; cc=[.681,.556]; y=np.arange(2)
ax.barh(y-.18,vv,height=.34,color=BLUE,label='Voynich (P3-c)')
ax.barh(y+.18,cc,height=.34,color=GRAY,label='Control hand, BSB Clm 5905, 1479 (P3-e)')
for i in range(2):
    ax.text(vv[i]+.003,i-.18,f'{vv[i]:.3f}',va='center',fontsize=8); ax.text(cc[i]+.003,i+.18,f'{cc[i]:.3f}',va='center',fontsize=8)
ax.axvline(.5,color=TXT,lw=1,ls='--'); ax.text(.502,1.55,'chance',fontsize=7,color='#555')
ax.set_xlim(.45,.72); ax.set_yticks(y,grp); ax.invert_yaxis(); ax.set_xlabel('Held-out AUC (glyph pen form, size removed)')
ax.legend(fontsize=8,loc='lower right',frameon=False)
ax.set_title('A dated Latin hand marks line starts at least as strongly',fontsize=11,loc='left',color=TXT)
fig.tight_layout(); fig.savefig(O+'fig8_line_edge_penform.png',dpi=200)
