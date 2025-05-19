# v18_mutation_mixer.py
# 從 elite_modules.json 中擷取 top 模組，突變參數並生成新模組 JSON

import json
import os
import random
from datetime import datetime

ELITE_PATH = "/mnt/data/hello/elite_modules.json"
TEMPLATE_PATH = "/mnt/data/hello/template_logic.py"
OUTPUT_DIR = "/mnt/data/hello/modules"
MAX_GENERATE = 3  # 每次產生幾支突變模組

POSSIBLE_INDICATORS = ["rsi", "macd", "ema", "ma", "atr"]

def load_elite():
    if not os.path.exists(ELITE_PATH):
        print("[!] 找不到 elite_modules.json")
        return []
    with open(ELITE_PATH, "r") as f:
        data = json.load(f)
    return data.get("elite_modules", [])

def generate_mutation(base_file):
    symbol = base_file.split("_")[1]
    new_id = str(random.randint(1000000000, 9999999999))
    indicators = random.sample(POSSIBLE_INDICATORS, k=random.randint(2, 4))
    params = {ind: random.randint(5, 40) for ind in indicators}
    return {
        "file": f"mod_{symbol}_{new_id}.json",
        "symbol": symbol,
        "indicators": indicators,
        "params": params,
        "created": datetime.utcnow().isoformat()
    }

def save_module(mod):
    path = os.path.join(OUTPUT_DIR, mod["file"])
    with open(path, "w") as f:
        json.dump(mod, f, indent=2)
    print(f"[+] 產生突變模組：{path}")

def main():
    elite = load_elite()
    if not elite:
        print("[x] 無法突變：elite_modules 為空")
        return
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    base_modules = random.sample(elite, k=min(len(elite), MAX_GENERATE))
    for base in base_modules:
        mod = generate_mutation(base["file"])
        save_module(mod)

if __name__ == "__main__":
    main()
