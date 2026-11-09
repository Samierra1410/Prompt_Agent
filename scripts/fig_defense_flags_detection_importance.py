import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
OUT="./"
plt.rcParams.update({"font.family":"serif","font.size":7.5,"axes.labelsize":7.5,"axes.titlesize":8,"xtick.labelsize":7,"ytick.labelsize":7,
  "legend.fontsize":7,"axes.spines.top":False,"axes.spines.right":False,"pdf.fonttype":42,"axes.linewidth":0.6,"lines.linewidth":1.3})
R=[0,1,2,3]
D={"Llama 3.1 8B, run A":{"wrong":{"No defense":[.347,.632,.778,.859],"G-Safeguard":[.352,.373,.401,.401],"No graph":[.322,.405,.489,.563]},
                          "mas":{"No defense":[.533,.267,.200,.100],"G-Safeguard":[.533,.567,.533,.500],"No graph":[.533,.500,.433,.333]}},
   "Llama 3.1 8B, run B":{"wrong":{"No defense":[.339,.596,.750,.829],"G-Safeguard":[.315,.449,.465,.430],"No graph":[.342,.432,.486,.464]},
                          "mas":{"No defense":[.533,.400,.267,.167],"G-Safeguard":[.567,.567,.500,.500],"No graph":[.533,.467,.500,.533]}},
   "Qwen2.5 7B":{"wrong":{"No defense":[.200,.347,.470,.567],"G-Safeguard":[.197,.237,.247,.247],"No graph":[.207,.267,.267,.263]},
                 "mas":{"No defense":[.800,.700,.533,.433],"G-Safeguard":[.800,.800,.750,.767],"No graph":[.800,.767,.733,.733]}}}
STY={"No defense":dict(color="0.55",ls="--",marker="^",mfc="0.55"),"G-Safeguard":dict(color="black",ls="-",marker="o",mfc="black"),
     "No graph":dict(color="black",ls=":",marker="s",mfc="white")}
LAB={"No defense":"No defense","G-Safeguard":"G-Safeguard","No graph":"Per-agent classifier (no graph)"}
fig,ax=plt.subplots(2,3,figsize=(7.0,3.1),sharex=True)
for j,(name,d) in enumerate(D.items()):
    for i,(m,yl) in enumerate([("wrong","Wrong-answer share"),("mas","MAS accuracy")]):
        a=ax[i,j]
        for k in STY: a.plot(R,d[m][k],label=LAB[k],ms=3.8,mec="black",mew=0.6,**STY[k])
        a.set_ylim(0,1); a.set_xticks(R)
        if i==0: a.set_title(name)
        if i==1: a.set_xlabel("Round")
        if j==0: a.set_ylabel(yl)
h,l=ax[0,0].get_legend_handles_labels()
fig.legend(h,l,loc="upper center",ncol=3,frameon=False,bbox_to_anchor=(0.5,1.04))
fig.tight_layout(rect=(0,0,1,0.94),pad=0.3); fig.savefig(OUT+"fig_defense_rounds.pdf",bbox_inches="tight"); plt.close(fig)

F={"Llama 3.1 8B (run B)":{"att":{"G-Safeguard":[.578,.900,.911,.911],"No graph":[.489,.844,.944,.967]},"ben":{"G-Safeguard":[.060,.007,0,0],"No graph":[.047,.027,.013,.013]}},
   "Qwen2.5 7B":{"att":{"G-Safeguard":[.756,.944,.944,.944],"No graph":[.594,1,1,1]},"ben":{"G-Safeguard":[0,.010,.027,.020],"No graph":[0,.013,.017,.030]}}}
fig,ax=plt.subplots(1,2,figsize=(3.45,1.85),sharey=True)
for j,(name,d) in enumerate(F.items()):
    a=ax[j]
    for k,mk,fc in [("G-Safeguard","o","black"),("No graph","s","white")]:
        a.plot(R,d["att"][k],color="black",ls="-",marker=mk,mfc=fc,ms=3.6,mew=0.6,label=f"{'G-Safeguard' if k=='G-Safeguard' else 'No graph'}: attackers")
        a.plot(R,d["ben"][k],color="0.5",ls=":",marker=mk,mfc=fc,mec="0.5",ms=3,mew=0.6,label=f"{'G-Safeguard' if k=='G-Safeguard' else 'No graph'}: benign")
    a.set_title(name); a.set_xticks(R); a.set_xlabel("Round"); a.set_ylim(-0.03,1.03)
ax[0].set_ylabel("Share flagged")
h,l=ax[0].get_legend_handles_labels()
fig.legend(h,l,loc="upper center",ncol=2,frameon=False,bbox_to_anchor=(0.5,1.2),fontsize=6.5)
fig.tight_layout(pad=0.3); fig.savefig(OUT+"fig_flags.pdf",bbox_inches="tight"); plt.close(fig)

# detection under coordinated attacks: grouped bars
conds=["Mimicry","Diffuse","Evasive","Def.-aware"]
dets=[("G-Safeguard (adv.)",[.584,.808,.749,.714],"white","////"),("Per-agent (adv.)",[.575,.790,.735,.681],"white","...."),
      ("CoordGuard: own",[.638,.719,.715,.679],"0.85",""),("CoordGuard: + answers",[.704,.789,.791,.767],"0.55",""),("CoordGuard: + edges",[.756,.932,.906,.875],"black","")]
fig,a=plt.subplots(figsize=(3.45,2.0)); x=np.arange(4); w=0.16
for k,(n,v,fc,h) in enumerate(dets):
    a.bar(x+(k-2)*w,v,w,color=fc,edgecolor="black",hatch=h,lw=0.5,label=n)
a.set_xticks(x); a.set_xticklabels(conds); a.set_ylim(0.5,1.0); a.set_ylabel("Agent-level AUROC")
a.axhline(0.5,color="black",lw=0.6)
a.legend(loc="upper center",bbox_to_anchor=(0.5,-0.13),ncol=3,frameon=False,fontsize=6.3,handlelength=1.6)
fig.tight_layout(pad=0.3); fig.savefig(OUT+"fig_newdet.pdf",bbox_inches="tight"); plt.close(fig)

# permutation importance
imp=[("text score (own)",.173),("in-neighbours' text score",.051),("echo",.031),("round-0 deviation",.026),("resistance",.026),("message length",.020),("out-neighbours' text score",.018),("coalition size",.011)]
fig,a=plt.subplots(figsize=(3.3,1.7)); y=np.arange(len(imp))[::-1]
edge={"in-neighbours' text score","echo","resistance","out-neighbours' text score"}
a.barh(y,[v for _,v in imp],color=["black" if n in edge else "white" for n,_ in imp],edgecolor="black",lw=0.6)
a.set_yticks(y); a.set_yticklabels([n for n,_ in imp]); a.set_xlabel("Mean AUROC drop when permuted")
fig.tight_layout(pad=0.3); fig.savefig(OUT+"fig_importance.pdf",bbox_inches="tight"); plt.close(fig)
