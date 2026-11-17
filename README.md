# The Graph Matters Only When Attackers Coordinate — artifact

Code and data for the paper *"The Graph Matters Only When Attackers Coordinate: Evasive Multi-Agent Attacks and a Coordination-Aware Defense"* (anonymous submission).

The repository contains:

- **GraphGap**: matched no-graph controls for measuring how much a topology-aware detector gains from the communication graph.
- **The re-evaluation of G-Safeguard** (ACL 2025) with its released code.
- **Coordinated attacks**: format mimicry, diffuse persuasion and detector-evading, plus a defense-aware variant.
- **CoordGuard**, a coordination-aware detector, plus an attacker that queries CoordGuard itself.
- **Study 2**: a document-borne prompt-infection testbed with provenance graphs.

Everything runs on free hardware: one machine with two NVIDIA T4 GPUs (16 GB each), 4 CPU cores and 30 GB RAM, with open models served locally by Ollama. No paid API is used. All notebooks were run on Kaggle (GPU T4 x2, Internet on).

## Repository layout

```
notebooks/
  01_gsafeguard_reevaluation.ipynb          Study 1: G-Safeguard vs. matched no-graph control (detection,
                                            end-to-end defense, operating point)
  02_attacks_and_coordguard.ipynb           Coordinated attacks, adversarially trained baselines, CoordGuard,
                                            leave-one-attack-out, graph-gain CIs, end-to-end defense,
                                            operating point, hardware cost, defense-aware attacker
  03_controls_and_coordguard_aware_attack.ipynb
                                            Stronger no-graph controls (MLP, GBT), results by graph density,
                                            CoordGuard-aware attacker and its end-to-end defense
  04_provguard_document_infection.ipynb     Study 2: sessions, labels, ProvGNN vs. per-message classifier,
                                            transfer, adaptive payloads, containment, attribution, cost
coordguard/cg.py                            CoordGuard feature extraction (18 features in three tiers)
scripts/                                    Monochrome figure scripts used for the paper
results/RESULTS_summary.md                  All numbers reported in the paper, by experiment
data/gsafeguard_reeval_csqa_llama318b.zip   Study-1 dialogues (Llama 3.1 8B): 160 train, 3 x 60 test
                                            conditions, 60 defense runs
data/attack_defense_csqa_llama318b.zip      Coordinated-attack dialogues (Llama): 3 x 60 test, 96 adaptive
                                            training, 120 end-to-end defense runs; trained CoordGuard
                                            and per-agent models; results file
```

With both zips attached, notebook `03` rebuilds the full Llama state without regenerating any dialogue.

## Reproducing the paper

Each notebook regenerates its data, trains every detector and writes every table, saving results as it goes. If a session stops, re-run the notebook with its previous output attached as input; it continues where it stopped.

1. **Study 1 (G-Safeguard re-evaluation).** Run `01` once with `MODEL = "llama3.1:8b"` and once with `MODEL = "qwen2.5:7b"`. About 7 GPU-hours per model. It writes `gsafeguard_reeval_csqa_<model>.zip`.
   - You can skip generating the Llama run by attaching `data/gsafeguard_reeval_csqa_llama318b.zip` instead.
2. **Attacks and CoordGuard.** Attach the matching output of step 1 and run `02`, with the same `MODEL`. Llama takes about 12 GPU-hours (two sessions); Qwen about 5. It writes `attack_defense_csqa_<model>.zip`.
3. **Additional experiments (Llama).** Attach the outputs of steps 1 and 2 and run `03`. About 4 GPU-hours.
4. **Study 2 (document-borne infection).** Run `04` with `PRESET = "kaggle_gpu"`. About 1.5–2 GPU-hours. It writes `provguard_outputs.zip`.

The authors' G-Safeguard repository is cloned at run time and used unmodified. It has no license, so no part of it is redistributed here. The only addition is a three-line shim that provides `torch_scatter.scatter_mean` through PyTorch Geometric.

Batched LLM generation is not bit-exact, so we release the generated dialogues. Every analysis can be reproduced exactly from them.

Seeds:
- 42 for generation, splits and CoordGuard;
- 0-2 for ProvGNN.

## Using CoordGuard on your own dialogues

```python
import joblib, coordguard.cg as cg
bundle = joblib.load("coordguard_full.joblib")       # trained by notebook 02 (models/ folder of its output)
scores = cg.score(bundle, communication_data, E, adj, t)   # one score per agent after round t
```

The inputs are:

- `communication_data`: per round, a list of `[agent_id, message]`;
- `E`: MiniLM embeddings with shape `[rounds, agents, 384]`;
- `adj`: the adjacency matrix.

## Safety

All attacks target multiple-choice questions or use harmless payloads: a fake token (`PT-7F3A-91QX`), a fictional vendor ("Northwind Cloud") and an off-task "quarterly sync checklist" reminder. No real systems or users were involved.

## License

Our code is released under the MIT License (see `LICENSE`). Third-party code that is cloned at run time keeps its own terms.
