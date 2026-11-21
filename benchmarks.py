import json
from pathlib import Path
from datetime import datetime, timezone

def save_benchmarks(data: dict, output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        **data
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path
