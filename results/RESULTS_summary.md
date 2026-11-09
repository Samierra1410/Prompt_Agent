# Results summary (all experiments in the paper)

Setup: 60 test dialogues per condition (same graphs/questions/attacker positions as the paper's test_std), 8 agents, 3 attackers;
detectors trained on 160 original + 96 adaptive training dialogues (32 each of mimicry / diffuse / evasive). G-Safeguard retrained
with the authors' scripts (checkpoint not in the uploaded zip): sanity AUROC 0.990 (paper 0.992), per-agent 0.991 (paper 0.991).

## 1. New attacks (no defense; benign agents' wrong-answer share by round, MAS accuracy final)
| attack | r0 | r1 | r2 | r3 | MAS acc |
|---|---|---|---|---|---|
| standard (authors) | 0.252 | 0.506 | 0.666 | 0.794 | 0.150 |
| held-out style | 0.271 | 0.342 | 0.597 | 0.753 | 0.167 |
| format mimicry | 0.259 | 0.349 | 0.460 | 0.543 | 0.383 |
| diffuse | 0.259 | 0.330 | 0.503 | 0.701 | 0.250 |
| evasive (adaptive) | 0.252 | 0.343 | 0.516 | 0.742 | 0.217 |
Evasive rewriting: 1040 attacker messages, mean 0.98 rewrites, per-agent score 0.308 -> 0.246, 73.3% below threshold 0.30.

## 2. Detection AUROC (recall@5%FPR in brackets)
| detector | standard | held-out | hard neg | mimicry | diffuse | evasive | std round0 |
|---|---|---|---|---|---|---|---|
| G-Safeguard | 0.990 (.906) | 0.997 | 0.981 | 0.553 (.006) | 0.773 (.328) | 0.659 (.006) | 0.884 |
| G-Safeguard (adv) | 0.989 | 0.994 | 0.969 | 0.584 (.100) | 0.808 (.500) | 0.749 (.300) | 0.889 |
| Per-agent | 0.991 (.972) | 0.996 | 0.984 | 0.552 (.039) | 0.774 (.383) | 0.683 (.050) | 0.902 |
| Per-agent (adv) | 0.990 | 0.997 | 0.976 | 0.575 (.033) | 0.790 (.394) | 0.735 (.111) | 0.892 |
| CoordGuard-own | 1.000 | 1.000 | 0.999 | 0.638 | 0.719 | 0.715 | 0.943 |
| CoordGuard-group | 1.000 | 1.000 | 0.999 | 0.704 | 0.789 | 0.791 | 0.960 |
| CoordGuard (full) | 1.000 (1.0) | 1.000 | 0.998 | 0.756 (.356) | 0.932 (.728) | 0.906 (.639) | 0.983 |
| Outlier distance | 0.818 | 0.838 | 0.714 | 0.621 | 0.814 | 0.788 | – |
Round 0: evasive CG 0.770 vs GS 0.611 / per-agent 0.643; diffuse CG 0.750 vs 0.664/0.673; mimicry CG 0.659 vs 0.498/0.501.
Cost: CoordGuard flags 15% of benign critical reviewers at the 5%-FPR threshold (others 6–11%).

## 3. Graph information gain with 95% paired-bootstrap CIs (dAUROC)
| condition | GS - per-agent | GS(adv) - per-agent(adv) | CoordGuard + edges | CoordGuard + others' answers |
|---|---|---|---|---|
| standard | -0.001 [-0.007,+0.005] | -0.001 [-0.010,+0.010] | -0.000 | 0.000 |
| held-out style | 0.000 | -0.003 | 0.000 | 0.000 |
| hard negatives | -0.003 | -0.007 | -0.000 | 0.000 |
| format mimicry | 0.001 | 0.009 | 0.052 [-0.012,+0.106] | 0.066 [+0.014,+0.120] * |
| diffuse | -0.002 | 0.018 [-0.012,+0.047] | 0.143 [+0.103,+0.178] * | 0.070 [+0.032,+0.110] * |
| evasive | -0.024 [-0.055,+0.007] | 0.015 [-0.031,+0.064] | 0.115 [+0.071,+0.154] * | 0.076 [+0.037,+0.115] * |
(* = CI excludes 0). Recall@5%FPR gain from edges: diffuse +0.356, evasive +0.278, mimicry +0.106.
CoordGuard permutation importance (evasive+diffuse): lr 0.173, nbr_lr_in 0.051, echo 0.031, dev0 0.026, resist 0.026, msglen 0.020, nbr_lr_out 0.018, coal 0.011.

## 4. Leave-one-attack-out (trained without the held-out style) — AUROC (recall@5%FPR)
| detector | diffuse | evasive | mimicry |
|---|---|---|---|
| CoordGuard (LOAO) | 0.904 (.644) | 0.855 (.533) | 0.698 (.239) |
| CoordGuard w/o neighbour text | 0.864 (.572) | 0.844 (.539) | 0.692 (.250) |
| CoordGuard-group | 0.758 (.356) | 0.738 (.328) | 0.632 (.278) |
| CoordGuard-own | 0.668 (.178) | 0.594 (.111) | 0.581 (.117) |
| Per-agent (adv, LOAO) | 0.786 (.400) | 0.715 (.056) | 0.562 (.050) |

## 5. End-to-end defense, evasive attack (30 paired dialogues)
| | wrong r3 | MAS acc | attackers flagged (r3) | benign flagged (r3) |
|---|---|---|---|---|
| No defense | 0.742 | 0.233 | – | – |
| G-Safeguard (adv) | 0.473 | 0.533 | 0.411 | 0.113 |
| Per-agent (adv) | 0.552 | 0.433 | 0.244 | 0.053 |
| CoordGuard | 0.409 | 0.533 | 0.600 | 0.033 |
Paired: CG - per-agent(adv) wrong -0.143 [-0.283,-0.007] (sig.); CG - GS(adv) -0.064 [-0.213,+0.076]; CG - none -0.333 [-0.513,-0.153].

## 6. Operating-point experiment (authors' attackers, 30 paired dialogues; matched threshold 0.312 = GS round-0 benign flag rate 6.0%)
No defense 0.793 / GS 0.423 / no-graph@0.5 0.435 / no-graph matched 0.422 (wrong final).
GS - no-graph(matched) +0.002 [-0.075,+0.083]; GS - no-graph(0.5) -0.012 [-0.133,+0.113].

## 7. Hardware (Tesla T4 x2, Xeon 2.0 GHz 4 cores, torch 2.11)
- Latency per decision, 8 agents: GS 5.56 ms CPU-1T / 2.68 ms GPU; per-agent 0.049 ms CPU; CoordGuard 6.11 ms CPU.
- 64 agents dense: GS 306 ms CPU-1T / 163 ms CPU-4T / 14.3 ms GPU; per-agent 0.13 ms CPU.
- Throughput GPU batch 512: GS 11,978 dialogues/s (357 MB peak, 0.25 J/1k decisions); per-agent 10.4 M dialogues/s (0.03 MB, ~0.0003 J). GS on CPU saturates ~1,070 dialogues/s (batch 32).
- MiniLM embedding: 24 ms per 8 messages on GPU, 417 ms on CPU. LLM round (8 agents) 41.6 s -> detector share <0.01%.
- Training: GS 198 s features + 18 s train (160 dlg, GPU); GS(adv) 286 s + 24 s (256 dlg); per-agent 0.33 s; CoordGuard 2.0 s features + 0.6 s fit.
- Model size: GS 4,334,593 params (16.5 MB fp32); per-agent 385.

## 8. Defense-aware attacker (Cell 16): evasive attacker queries the ADV-TRAINED per-agent classifier (CoordGuard's text component)
52 of 60 test dialogues completed (Kaggle 12-h session limit; 8 not run). Rewriting: mean 1.57 rewrites, score 0.398 -> 0.350, 50.8% of attacker messages below 0.30.
Attack effect (benign wrong by round): 0.295 / 0.391 / 0.497 / 0.682; MAS acc final 0.25.
| detector | AUROC [CI] | recall@5%FPR | recall@0.5 | FPR@0.5 |
|---|---|---|---|---|
| G-Safeguard | 0.575 [0.53,0.62] | 0.032 | 0.032 | 0.015 |
| G-Safeguard (adv) | 0.714 [0.68,0.76] | 0.333 | 0.410 | 0.131 |
| Per-agent | 0.605 [0.56,0.66] | 0.051 | 0.026 | 0.023 |
| Per-agent (adv) | 0.681 [0.64,0.73] | 0.128 | 0.192 | 0.100 |
| CoordGuard-own | 0.679 [0.61,0.74] | 0.154 | 0.173 | 0.069 |
| CoordGuard-group | 0.767 [0.72,0.81] | 0.346 | 0.346 | 0.046 |
| CoordGuard (full) | 0.875 [0.84,0.91] | 0.513 | 0.564 | 0.077 |
| Outlier distance | 0.791 [0.75,0.83] | 0.288 | 0.013 | 0.000 |
Graph gain (paired CI): GS - per-agent -0.030 [-0.062,-0.000]; adv GS - adv per-agent +0.033 [-0.016,+0.085];
CoordGuard + edges +0.108 [+0.066,+0.153] *; + others' answers +0.088 [+0.044,+0.135] *.

## 9. Study 2 rerun — ProvGuard v2 (Kaggle, Ollama, run of 2 Nov 2026; replaces old Study 2 numbers)
Data: 300 Llama 3.1 8B + 60 Qwen2.5 7B phase-A sessions (4–8 agents, chain/fan/random DAGs) + 40 adaptive (Llama); 132 infected
(message sent). Labels: Qwen judge OR exact-match rules; judge-vs-rule kappa 0.592 over 971 outputs (human audit still to do).
Embeddings: full 384-d MiniLM (no PCA). 5-fold CV grouped by payload template.
Attack outcomes (infected msg sent / inert): Llama obvious 0.92/0.08, mimicry 0.85/0.15, paraphrase 0.50/0.50, adaptive 0.55/0.45;
Qwen obvious 1.00/0, mimicry 0.75/0.25, paraphrase 0.62/0.38. Reached final output: canary Llama 0.25 / Qwen 0.33; hijack 0.52 / 0.83.

Exp 1 detection (held-out templates):
| detector | AUROC [CI] | TPR@1% | TPR@5% | FPR hardneg |
|---|---|---|---|---|
| ProvGNN (directed) | 0.928 [0.89,0.96] | 0.809 | 0.845 | 0.028 |
| ProvGNN undirected | 0.960 [0.93,0.98] | 0.836 | 0.909 | 0.042 |
| ProvGNN no-edges | 0.970 [0.95,0.99] | 0.809 | 0.882 | 0.056 |
| Per-message classifier | 0.969 [0.95,0.98] | 0.782 | 0.855 | 0.056 |
| Copy-propagation RF | 0.583 | 0.018 | 0.064 | 0.028 |
| Keyword filter | 0.638 | 0.109 | 0.309 | 0.014 |
| LLM judge (Qwen, payload-agnostic) | 0.675 | 0.106 | 0.141 | 0.033 |
Per model: Llama ProvGNN 0.914 / no-edges 0.964 / per-msg 0.964; Qwen 0.990 / 0.995 / 0.992. LLM judge scored 283/360 phase-A sessions.
Exp 2 transfer: Llama->Qwen ProvGNN 0.987, per-msg 0.994; Qwen->Llama ProvGNN 0.836 (TPR@5% 0.231), per-msg 0.949 (0.824).
Exp 3 adaptive (22 infected adaptive sessions): AUROC ProvGNN 0.918, no-edges 0.924, per-msg 0.899; recall@5%FPR 0.727 / 0.727 / 0.636 (difference = 2 sessions).
Exp 4 containment (5% clean-alarm): protected fraction ProvGNN 0.807, per-msg 0.792, keyword 0.319; output leaks prevented 0.919 / 0.919 / 0.351 (37 leaks).
Exp 5 attribution top-1: ProvGNN 0.924, per-msg 0.924, LLM judge 0.723, first-agent baseline 0.250, random 0.230.
Exp 6 cost (CPU): overhead ~25 ms/hop (embedding 21–25 ms dominates; GNN 2.3 ms at 5 agents -> 5.2 ms at 500), 0.3% of an LLM call; 60 B/event provenance;
LLM call median 8.7 s Llama / 5.2 s Qwen.
Takeaway: for single-source document-borne infection the edges add nothing (directed edges hurt: -0.041 AUROC; worse transfer) — consistent with Study 1.

## 10. Qwen2.5 7B — G-Safeguard baseline re-evaluation (Study 1 replication, run of 2 Nov 2026)
340 dialogues (train 160, test_std / test_subtle (held-out style) / test_dissent (hard neg) 60 each); GS retrained with authors' scripts
(val acc 98.05%). Output folder gsafe_csqa_qwen257b, zip gsafeguard_reeval_csqa_qwen257b.zip (input for the Qwen attack notebook).
| detector | std AUROC [CI] (rec@5%) | held-out | hard neg (dissenter FPR@5% thr) | turn-0 std / held-out |
|---|---|---|---|---|
| G-Safeguard | 0.996 [0.99,1.00] (.933) | 0.993 (.911) | 0.995 (0.033) | 0.989 / 0.973 |
| Per-agent (no graph) | 0.999 [1.00,1.00] (.989) | 0.991 (.950) | 0.999 (0.258) | 0.999 / 0.995 |
| Outlier distance | 0.931 (.611) | 0.938 (.694) | 0.874 | – |
Attacker vs dissenter AUROC: GS 0.993, per-agent 0.997. Per-agent flags more benign dissenters at the 5%-FPR threshold (0.258 vs 0.033).
End-to-end defense (60 paired, wrong benign final / MAS acc): none 0.567/0.433; GS 0.247/0.767; no-graph@0.5 0.263/0.733; no-graph matched 0.200/0.817.
GS - no-graph(0.5) wrong -0.017 [-0.097,+0.060]; GS - no-graph(matched) +0.047 [-0.027,+0.127]; matched - 0.5: -0.063 [-0.137,+0.000].
Matched threshold 0.2729 (GS round-0 benign flag rate 0.000). Flags r0 attackers: GS 0.756, no-graph 0.594, matched 0.972; final-round benign flagged: 0.020 / 0.030 / 0.110.
Takeaway: replicates Llama — graph adds nothing; at a matched operating point the no-graph defense is at least as good.

## 11. Qwen2.5 7B — attacks + CoordGuard replication (run of 7 Nov 2026, 3.76 h + cells 14-17)
Sanity: GS 0.992, per-agent 0.999 on test_std. Training 160 orig + 96 adaptive.
Attack effect (benign wrong r0/r1/r2/r3, MAS final): standard .200/.347/.470/.567 .433; held-out .200/.310/.503/.637 .367;
mimicry .193/.233/.270/.303 .717; diffuse .210/.237/.280/.287 .733; evasive .197/.233/.260/.230 .783; defense-aware .183/.217/.253/.237 .767.
=> Qwen largely RESISTS the stealthy attacks (only authors' and held-out styles work). Evasive rewrites per round .11/.32/.56/.65; score .11->.23 range; defense-aware 1.31 rewrites, .320->.292, 60.1% below thr.
AUROC (rec@5%): | det | mimicry | diffuse | evasive | def-aware | std | held | hard |
GS .555(.06) .667(.10) .620(.03) .554 | .992 .962 .991
GS adv .663(.21) .751(.36) .725(.27) .672 | .994 .996 .992
PA .575(.08) .695(.08) .652(.04) .576 | .999 .991 .999
PA adv .627(.14) .726(.14) .690(.06) .613 | .998 .985 .995
CG-own .615 .729 .695 .589 | 1 1 1 ; CG-group .700 .786 .771 .725 ; CG full .766(.36) .886(.53) .857(.51) .812(.46) | 1 1 1
Outlier .647 .769 .761 .745 | .931 .938 .874
Round 0: evasive GS .600 PA .651 GSadv .710 PAadv .714 CG .809; diffuse .604/.652/.721/.718/.814; mimicry .492/.519/.580/.591/.729.
Dissenter FPR@5%: GS .025, GSadv .117, PA .258, PAadv .242, CG .292 (own .325, group .150).
Graph gain CIs: GS-PA (paper): std -.007[-.015,-.002]* held -.029[-.048,-.014]* hard -.008[-.017,-.002]* mim -.021[-.051,+.004] diff -.028[-.058,+.003] evas -.032[-.066,-.001]* aware -.022[-.057,+.007]
adv GS-PA: std -.004[-.010,-.001]* held +.011[+.001,+.022]* hard -.003 mim +.036[+.001,+.070]* diff +.025[-.015,+.065] evas +.036[-.005,+.079] aware +.059[+.015,+.107]*
CG +edges: mim +.066[+.013,+.120]* diff +.100[+.060,+.143]* evas +.086[+.051,+.122]* aware +.087[+.052,+.121]*; 0 on authors' conditions.
CG +answers: mim +.085* diff +.057* evas +.077* aware +.136*.
Importance: lr .180, nbr_lr_in .084, msglen .036, dev0 .029, nbr_lr_out .026, echo .024, coal .013, adopt .004, resist .001.
LOAO AUROC (rec): CG .840(.52) diffuse, .864(.57) evasive, .761(.31) mimicry; w/o nbr text .781/.839/.722; group .762/.771/.671; own .702/.698/.586; PA adv .722(.12)/.681(.07)/.620(.12).
E2E evasive (30 dlg): wrong r3 none .227, GSadv .193, PAadv .273, CG .193; MAS .767/.833/.733/.800. CG-PAadv -.080[-.180,+.000]; CG-GSadv .000[-.027,+.033]; CG-none -.033[-.113,+.040].
Flags r0 att CG .556 GSadv .300 PAadv .056; benign r3 CG .100 GSadv .060 PAadv .140.
Operating point (same as baseline run): GS .247, NG .263, matched .200; GS-matched +.047[-.030,+.123].
Hardware (Qwen run machine): GS 7.2 ms CPU-1T, 3.15 GPU; 64 dense 366 CPU / 15.1 GPU; batch512 GPU 15,736 dlg/s 357MB 0.25 J/1k; LR 0.064 ms; CG 7.4 ms; LLM round 24.5 s.
Part P (ProvTrace containment, Study-2 data): payload reaches deliverable among infected sessions: none .473; at 5% message-FPR budget per-message blocking .036 (clean msgs blocked .045, clean deliverables suppressed 0) vs provenance quarantine .027 (.117, .153); at 1%: .064/.007/0 vs .045/.051/.032; at 10%: .009/.086/0 vs .000/.172/.259. Attribution of flagged infected ~.83-.86 both.

## 12. Revision run (Llama, 8 Nov 2026, 4.2 h): stronger controls, density, CoordGuard-aware attacker, defense-aware completed (60/60)
Stronger no-graph controls (MLP 256, GBT) on same embeddings: never better than LR; GS minus best control never significantly positive in 14 comparisons (range -0.034..+0.018; only sig. value -0.034 def-aware). GBT std .979 vs LR .991. CG-own (no graph) 1.000 on authors' attacks.
Density: CG edge gain positive at all 5 densities for diffuse (+.075..+.182) and evasive (+.032..+.247); mimicry -.014..+.119. CG .83-.98; adv baselines .64-.87. Position: CG high/low out-degree .894/.911 evasive, .925/.935 diffuse.
Defense-aware (60 dlg, rerun with retrained GS): GS .549, GS adv .693, PA .583, PA adv .665, own .673, group .774, CG .867 (rec5 .533); outlier .804. Edges +.093[.054,.132]; adv GS-PA +.028[-.013,.070]; GS-PA -.034[-.067,-.002]. Effect .267/.301/.486/.718, MAS .167; 1.62 rewrites, .405->.354, 49.4% below thr.
CoordGuard-aware attacker (CG in the loop; tone/noecho/concede rewrites; CG not retrained): 46% msgs revised (tone 11, noecho 21, concede 14%), CG score .49->.35, 81% below thr.
AUROC: GS .525, GS adv .676, PA adv .619, MLP adv .657, outlier .812, CG-own .486, CG-group .620, CG .782 (rec5 .14, rec@.5 .17, FPR .07). Edges +.162[.105,.217]; adv GS-PA +.057[.014,.098].
Effect: wrong r3 .593 (vs evasive .742), MAS .317; many concessions .548 vs few .791.
E2E (30): none .573, GS adv .551, PA adv .553, CG .577 — all n.s. => CG-aware attacker evades every deployed defense at the cost of ~1/5 of its effect.
