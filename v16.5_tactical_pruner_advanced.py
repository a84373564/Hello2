import os
import json
import time
from datetime import datetime

MODULE_DIR = "/mnt/data/hello/modules"
LOG_PATH = "/mnt/data/hello/module_scores.json"
HISTORY_PATH = "/mnt/data/hello/performance_history.json"
MAX_KEEP = 100
PROTECT_MINUTES = 30  # 保護 30 分鐘內新模組

print("[v16.5] 啟動進階戰術清理器")

if not os.path.exists(LOG_PATH):
    print("[!] 找不到 module_scores.json，無法進行清理")
    exit(0)

with open(LOG_PATH) as f:
    scores = json.load(f)

sorted_mods = sorted(
    [(k, v) for k, v in scores.items() if "score" in v],
    key=lambda x: x[1]["score"],
    reverse=True
)

keep_set = set(k for k, _ in sorted_mods[:MAX_KEEP])

if os.path.exists(HISTORY_PATH):
    with open(HISTORY_PATH, "r") as f:
        history = json.load(f)
else:
    history = {}

removed = 0
now = time.time()

for fname in os.listdir(MODULE_DIR):
    if not fname.endswith(".json"):
        continue
    if fname not in scores:
        continue
    if fname in keep_set:
        continue

    fpath = os.path.join(MODULE_DIR, fname)
    ctime = os.path.getctime(fpath)
    if now - ctime < PROTECT_MINUTES * 60:
        continue

    os.remove(fpath)
    removed += 1
    if fname in history:
        del history[fname]
    print(f"[×] 移除模組與歷史：{fname}")

with open(HISTORY_PATH, "w") as f:
    json.dump(history, f, indent=2)

print(f"[v16.5] 清理完成，保留 top {MAX_KEEP}，剃除 {removed} 支模組（含歷史）")
