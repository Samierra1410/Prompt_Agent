"""CoordGuard features (shared by the notebook and the defense driver)."""
import re, numpy as np
from collections import Counter
TAG = re.compile(r"<ANSWER>\s*:\s*\{?\s*\(?([A-E])\b")
ALT = re.compile(r"(?i:answer|option|choice)\s*(?:is|:|would be|should be|of)?\s*\(?([A-E])\b")
def parse(text):
    m = TAG.search(text or "")
    if m: return m.group(1), 1
    m = ALT.findall(text or "")
    return (m[-1] if m else None), 0
def plurality(xs):
    c = Counter(x for x in xs if x is not None)
    return c.most_common(1)[0][0] if c else None
OWN = ["lr", "tag", "persist", "changes", "msglen"]
GROUP = ["dev0", "devt", "coal", "mincoal"]
EDGE = ["adopt", "adopt_n", "resist", "nbr_lr_in", "nbr_lr_out", "local_agree", "echo", "indeg", "outdeg"]
ALL = OWN + GROUP + EDGE
TIERS = {"own": OWN, "group": OWN + GROUP, "full": ALL}
def lr_scores(lr, E, t): return lr.predict_proba(E[:t + 1].mean(0))[:, 1]
def features(comm, E, adj, t, lrs):
    n = len(adj); A = np.asarray(adj)
    texts = [{int(i): s for i, s in comm[r]} for r in range(t + 1)]
    P = [[parse(texts[r].get(i, "")) for i in range(n)] for r in range(t + 1)]
    ans = [[p[0] for p in row] for row in P]; tag = [[p[1] for p in row] for row in P]
    plur = [plurality(ans[r]) for r in range(t + 1)]
    En = E[:t + 1] / np.clip(np.linalg.norm(E[:t + 1], axis=-1, keepdims=True), 1e-9, None)
    F = np.zeros((n, len(ALL)), np.float32)
    for i in range(n):
        a = [ans[r][i] for r in range(t + 1)]; mode = plurality(a)
        outs = np.nonzero(A[i])[0]; ins = np.nonzero(A[:, i])[0]
        persist = np.mean([x is not None and x == mode for x in a])
        changes = sum(1 for r in range(1, t + 1) if a[r] != a[r - 1]) / max(t, 1)
        msglen = np.mean([len(texts[r].get(i, "").split()) for r in range(t + 1)]) / 100
        dev0 = float(ans[0][i] is not None and plur[0] is not None and ans[0][i] != plur[0])
        devt = float(ans[t][i] is not None and plur[t] is not None and ans[t][i] != plur[t])
        coal = sum(1 for j in range(n) if j != i and ans[t][j] is not None and ans[t][j] == ans[t][i]) / (n - 1)
        mincoal = sum(1 for j in range(n) if j != i and ans[0][j] is not None and ans[0][j] == ans[0][i]) / (n - 1) if dev0 else 0.0
        opp = ad = ropp = res = 0; echo = []
        for r in range(1, t + 1):
            ai = ans[r - 1][i]
            if ai is not None:
                for w in outs:
                    if ans[r - 1][w] != ai:
                        opp += 1; ad += int(ans[r][w] == ai)
            m = plurality([ans[r - 1][u] for u in ins])
            if m is not None and ai is not None and m != ai:
                ropp += 1; res += int(ans[r][i] == ai)
            if len(ins): echo.append(float(np.max(En[r - 1, ins] @ En[r, i])))
        others = [w for w in range(n) if w != i and w not in set(outs)]
        if ans[t][i] is not None and len(outs):
            la = np.mean([ans[t][w] == ans[t][i] for w in outs]) - (np.mean([ans[t][w] == ans[t][i] for w in others]) if others else 0.0)
        else: la = 0.0
        F[i] = [lrs[i], np.mean([tag[r][i] for r in range(t + 1)]), persist, changes, msglen,
                dev0, devt, coal, mincoal,
                ad / opp if opp else 0.0, ad / (len(outs) * max(t, 1)) if len(outs) else 0.0, res / ropp if ropp else 0.0,
                float(np.mean(lrs[ins])) if len(ins) else 0.0, float(np.mean(lrs[outs])) if len(outs) else 0.0, la,
                float(np.mean(echo)) if echo else 0.0, len(ins) / (n - 1), len(outs) / (n - 1)]
    return F
def score(bundle, comm, E, adj, t):
    F = features(comm, E, adj, t, lr_scores(bundle["lr"], E, t))
    cols = [ALL.index(c) for c in TIERS[bundle["tier"]]]
    return bundle["model"].predict_proba(F[:, cols])[:, 1]
