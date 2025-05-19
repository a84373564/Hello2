# v17_elite_saver.py
# [v17] Elite 儲存器：每輪選出前 5 高分模組並儲存至 elite_modules.json

import os
import json
from datetime import datetime

SCORE_FILE = "/mnt/data/hello/module_scores.json"
ELITE_FILE = "/mnt/data/hello/elite_modules.json"
TOP_N = 5

def load_scores(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[x] 無法讀取模組分數：{e}")
        return {}

def save_elite(data, path):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[✓] 已儲存 elite_modules 至 {path}")
    except Exception as e:
        print(f"[x] 儲存 elite_modules 失敗：{e}")

def build_elite_modules(score_data, top_n=5):
    sorted_items = sorted(
        [(k, v) for k, v in score_data.items() if isinstance(v, dict)],
        key=lambda x: x[1].get("score", 0),
        reverse=True
    )
    top_modules = sorted_items[:top_n]
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "elite_modules": [
            {"file": k, "score": v.get("score", 0), "profit": v.get("profit", 0)}
            for k, v in top_modules
        ]
    }

if __name__ == "__main__":
    scores = load_scores(SCORE_FILE)
    elite = build_elite_modules(scores, TOP_N)
    save_elite(elite, ELITE_FILE)
