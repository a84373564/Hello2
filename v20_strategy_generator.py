import os
import json
import random
from datetime import datetime

GENE_PROFILE = "/mnt/data/hello/gene_profile.json"
MODULE_DIR = "/mnt/data/hello/modules"
OUTPUT_FILE = f"mod_GEN_{random.randint(1_000_000, 9_999_999)}.json"
OUTPUT_PATH = os.path.join(MODULE_DIR, OUTPUT_FILE)

def load_gene_profile(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[x] 無法讀取基因圖譜：{e}")
        return None

def generate_random_strategy(profile):
    strategy = {}
    for key, values in profile.items():
        if isinstance(values, list) and values:
            strategy[key] = random.choice(values)
    return strategy

def generate_module(profile):
    logic = generate_random_strategy(profile)
    return {
        "strategy": {
            "source": "v20_strategy_generator",
            "created_at": datetime.utcnow().isoformat(),
            "logic": logic
        },
        "score": 0,
        "profit": 0,
        "history": [],
        "file": OUTPUT_FILE
    }

def save_module(data, path):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[+] 產生新模組：{path}")
    except Exception as e:
        print(f"[x] 儲存模組失敗：{e}")

if __name__ == "__main__":
    profile = load_gene_profile(GENE_PROFILE)
    if not profile:
        print("[x] 無法生成模組，缺少基因圖譜")
        exit(1)

    module = generate_module(profile)
    save_module(module, OUTPUT_PATH)
