import json
from pathlib import Path
from collections import defaultdict

DATA_FOLDER = Path("data")
DETAILS_DATA_FOLDER = DATA_FOLDER / "details"
OUTPUT_PATH = DATA_FOLDER / "statistics.json"
aggregate = defaultdict(lambda: {"infant": 0, "toddler": 0})

for file in DETAILS_DATA_FOLDER.glob("*.json"):
    with open(file) as f:
        data = json.load(f)
        for date, counts in data.get("availability", {}).items():
            aggregate[date]["infant"] += counts.get("infant", 0)
            aggregate[date]["toddler"] += counts.get("toddler", 0)

# Convert to regular dict
result = {"availability": dict(aggregate)}

# Write to output file
with open(OUTPUT_PATH, "w") as f:
    json.dump(result, f, indent=2)
