import os
import json
from datetime import datetime

SCORES_FILE = "/mnt/data/hello/module_scores.json"
HISTORY_FILE = "/mnt/data/hello/performance_history.json"

# 讀取歷史績效
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        history_data = json.load(f)
else:
    history_data = {}

# 檢查最新模組評分是否存在
if not os.path.exists(SCORES_FILE):
    print("[x] 找不到 module_scores.json，請先執行 v10 評估器")
    exit(1)

with open(SCORES_FILE, "r") as f:
    scores = json.load(f)

now = datetime.utcnow().isoformat()

# 更新每個模組的績效紀錄
for mod, data in scores.items():
    if mod not in history_data:
        history_data[mod] = []
    history_data[mod].append({
        "timestamp": now,
        "score": data.get("score", 0),
        "profit": data.get("profit", 0),
        "sharpe": data.get("sharpe", 0),
        "drawdown": data.get("drawdown", 0),
        "win_rate": data.get("win", 0)
    })

# 儲存更新後的績效紀錄
with open(HISTORY_FILE, "w") as f:
    json.dump(history_data, f, indent=2)

print(f"[✓] 績效追蹤完成，共記錄 {len(history_data)} 支模組歷史")
