import os
import json
from datetime import datetime

MODULE_DIR = "/mnt/data/hello/modules"
GENE_PROFILE_PATH = "/mnt/data/hello/gene_profile.json"

def extract_gene_profile(module_file):
    try:
        with open(os.path.join(MODULE_DIR, module_file), "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[!] 模組讀取錯誤：{module_file} → {e}")
        return None

    indicators = []
    params = {}

    if "indicators" in data:
        indicators = data["indicators"]
    elif "strategy" in data and "indicators" in data["strategy"]:
        indicators = data["strategy"]["indicators"]

    if "params" in data:
        params = data["params"]
    elif "strategy" in data and "params" in data["strategy"]:
        params = data["strategy"]["params"]

    return {
        "file": module_file,
        "indicators": indicators,
        "params": params,
        "created_at": data.get("timestamp") or data.get("metadata", {}).get("created_at") or datetime.utcnow().isoformat()
    }

def main():
    print("[v21] 啟動策略基因分析器")

    if not os.path.exists(MODULE_DIR):
        print(f"[x] 模組資料夾不存在：{MODULE_DIR}")
        return

    gene_profiles = []
    for fname in os.listdir(MODULE_DIR):
        if fname.endswith(".json") and fname.startswith("mod_"):
            profile = extract_gene_profile(fname)
            if profile:
                gene_profiles.append(profile)

    with open(GENE_PROFILE_PATH, "w") as f:
        json.dump({"timestamp": datetime.utcnow().isoformat(), "profiles": gene_profiles}, f, indent=2)

    print(f"[✓] 基因圖譜建立完成，共記錄 {len(gene_profiles)} 筆模組 → {GENE_PROFILE_PATH}")

if __name__ == "__main__":
    main()
