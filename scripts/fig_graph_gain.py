import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
plt.rcParams.update({"font.family":"serif","font.size":7.5,"axes.labelsize":7.5,"xtick.labelsize":6.8,"ytick.labelsize":7,"legend.fontsize":7,
  "axes.spines.top":False,"axes.spines.right":False,"pdf.fonttype":42,"axes.linewidth":0.6,"axes.titlesize":8})
conds=["Std.","Style","Hard\nneg.","Mimic-\nry","Diffuse","Evasive","Def.-\naware"]
L_gs=[(-.001,-.010,.010),(-.003,None,None),(-.007,None,None),(.009,None,None),(.018,-.012,.047),(.015,-.031,.064),(.028,-.013,.070)]
L_cg=[(0,None,None),(0,None,None),(0,None,None),(.052,-.012,.106),(.143,.103,.178),(.115,.071,.154),(.093,.054,.132)]
Q_gs=[(-.004,-.010,-.001),(.011,.001,.022),(-.003,-.009,.002),(.036,.001,.070),(.025,-.015,.065),(.036,-.005,.079),(.059,.015,.107)]
Q_cg=[(0,0,0),(0,0,0),(0,0,0),(.066,.013,.120),(.100,.060,.143),(.086,.051,.122),(.087,.052,.121)]
fig,axs=plt.subplots(2,1,figsize=(3.45,3.5),sharex=True)
for a,(title,gs,cg) in zip(axs,[("Llama 3.1 8B agents",L_gs,L_cg),("Qwen2.5 7B agents",Q_gs,Q_cg)]):
    a.axhline(0,color="black",lw=0.6); a.axvspan(2.5,6.6,color="0.92",lw=0,zorder=0)
    for vals,dx,mk,fc,lab in [(gs,-0.14,"s","white","G-Safeguard $-$ per-agent (both adv.-trained)"),(cg,0.14,"o","black","CoordGuard: + graph edges")]:
        for i,(v,lo,hi) in enumerate(vals):
            if lo is not None: a.plot([i+dx,i+dx],[lo,hi],color="black",lw=0.9)
            a.plot(i+dx,v,mk,mfc=fc,mec="black",ms=4,mew=0.8,label=lab if i==0 else None)
    a.set_ylim(-0.04,0.2); a.set_xlim(-0.5,6.6); a.set_ylabel(r"$\hat\Delta_G$ (AUROC)")
    a.text(-0.4,0.18,title,fontsize=7.5,weight="bold")
    a.text(4.55,0.18,"coordinated (this paper)",ha="center",fontsize=6.8,style="italic")
axs[1].set_xticks(range(7)); axs[1].set_xticklabels(conds)
h,l=axs[0].get_legend_handles_labels()
fig.legend(h,l,loc="lower center",bbox_to_anchor=(0.5,-0.06),ncol=1,frameon=False)
fig.tight_layout(pad=0.2,rect=(0,0.06,1,1)); fig.savefig("./fig_gain.pdf",bbox_inches="tight")
