import os
import json
from collections import Counter
from statistics import mean

SCORES_FILE = "/mnt/data/hello/module_scores.json"
GENE_FILE = "/mnt/data/hello/gene_profile.json"
RISK_REPORT = "/mnt/data/hello/system_risk_report.json"

if not os.path.exists(SCORES_FILE) or not os.path.exists(GENE_FILE):
    print("[x] 缺少必要資料：module_scores.json 或 gene_profile.json")
    exit(1)

with open(SCORES_FILE, "r") as f:
    scores = json.load(f)

with open(GENE_FILE, "r") as f:
    gene = json.load(f)

sharpe_vals = []
profit_vals = []
drawdown_vals = []

for mod in scores.values():
    sharpe_vals.append(mod.get("sharpe", 0))
    profit_vals.append(mod.get("profit", 0))
    drawdown_vals.append(mod.get("drawdown", 0))

indicator_counts = Counter()
for entry in gene.get("profiles", []):
    indicators = entry.get("indicators", [])
    indicator_counts.update(indicators)

top_indicators = indicator_counts.most_common(3)

report = {
    "summary": {
        "module_count": len(scores),
        "avg_sharpe": round(mean(sharpe_vals), 4) if sharpe_vals else 0,
        "avg_profit": round(mean(profit_vals), 4) if profit_vals else 0,
        "avg_drawdown": round(mean(drawdown_vals), 4) if drawdown_vals else 0,
    },
    "top_indicators": [{"name": k, "count": v} for k, v in top_indicators],
    "overused_indicators": [
        {"name": k, "count": v, "percent": round(v / len(gene["profiles"]) * 100, 2)}
        for k, v in indicator_counts.items() if v / len(gene["profiles"]) > 0.4
    ]
}

with open(RISK_REPORT, "w") as f:
    json.dump(report, f, indent=2)

print(f"[✓] 系統風險報告完成 → {RISK_REPORT}")
