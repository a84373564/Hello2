# 檔案：v19_strategy_fusioner.py
import os
import json
import random
from datetime import datetime

ELITE_PATH = "/mnt/data/hello/elite_modules.json"
MODULE_DIR = "/mnt/data/hello/modules"
FUSED_PREFIX = "mod_FUSED_"
FUSED_FILE = f"{FUSED_PREFIX}{random.randint(1_000_000, 9_999_999)}.json"
FUSED_PATH = os.path.join(MODULE_DIR, FUSED_FILE)

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[x] 無法讀取 JSON：{e}")
        return None

def load_module_data(filename):
    path = os.path.join(MODULE_DIR, filename)
    if not os.path.exists(path):
        print(f"[!] 模組遺失：{filename}")
        return None
    return load_json(path)

def fuse_logic(mod1, mod2):
    avg_score = round((mod1["score"] + mod2["score"]) / 2, 4)
    avg_profit = round((mod1["profit"] + mod2["profit"]) / 2, 4)
    return {
        "strategy": {
            "fused_from": [mod1["file"], mod2["file"]],
            "logic": {
                "avg_score": avg_score,
                "avg_profit": avg_profit,
            },
        },
        "metadata": {
            "created_at": datetime.utcnow().isoformat(),
            "source": "v19_strategy_fusioner"
        }
    }

elite_data = load_json(ELITE_PATH)
if not elite_data or "elite_modules" not in elite_data:
    print("[x] 無法讀取 elite_modules.json 或格式錯誤")
    exit(1)

elite = [m for m in elite_data["elite_modules"] if "file" in m and "score" in m and "profit" in m]
if len(elite) < 2:
    print("[x] elite_modules 數量不足")
    exit(1)

mod1, mod2 = random.sample(elite, 2)

if not (load_module_data(mod1["file"]) and load_module_data(mod2["file"])):
    print("[x] 模組讀取失敗，跳過融合")
    exit(1)

fused = fuse_logic(mod1, mod2)

with open(FUSED_PATH, "w") as f:
    json.dump(fused, f, indent=2)
print(f"[+] 產生融合模組：{FUSED_PATH}")
