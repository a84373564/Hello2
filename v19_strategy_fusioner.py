import json
import hashlib
from datetime import datetime

SOURCE = "/mnt/data/hello/elite_modules.json"
DEST_DIR = "/mnt/data/hello/modules"

def load_elite_modules(path):
    try:
        with open(path, "r") as f:
            data = json.load(f)
        return data.get("elite_modules", [])
    except Exception as e:
        print(f"[!] 無法讀取 elite_modules：{e}")
        return []

def fuse_modules(modules):
    if len(modules) < 2:
        print("[!] 少於兩個模組，跳過融合")
        return None

    avg_score = sum(m["score"] for m in modules) / len(modules)
    avg_profit = sum(m["profit"] for m in modules) / len(modules)

    fused = {
        "strategy": "fused_elite",
        "components": [m["file"] for m in modules],
        "score": round(avg_score, 4),
        "profit": round(avg_profit, 4),
        "timestamp": datetime.utcnow().isoformat()
    }

    uid = hashlib.sha1(json.dumps(fused).encode()).hexdigest()[:10]
    fused_filename = f"{DEST_DIR}/mod_FUSED_{uid}.json"

    with open(fused_filename, "w") as f:
        json.dump(fused, f, indent=2)

    print(f"[+] 產生融合模組：{fused_filename}")
    return fused

if __name__ == "__main__":
    elite = load_elite_modules(SOURCE)
    fuse_modules(elite)
