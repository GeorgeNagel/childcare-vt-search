import json
from pathlib import Path
from collections import defaultdict
from datetime import date

DATA_FOLDER = Path("data")
DETAILS_DATA_FOLDER = DATA_FOLDER / "details"
DOCS_FOLDER = Path("docs")
OUTPUT_PATH = DOCS_FOLDER / "statistics.json"
aggregate = defaultdict(
    lambda: {
        "infant_availability": 0,
        "toddler_availability": 0,
        "infant_capacity": 0,
        "toddler_capacity": 0,
    }
)
places_with_infant_availability = []
places_with_toddler_availability = []

todays_date = date.today().isoformat()

for file in DETAILS_DATA_FOLDER.glob("*.json"):
    with open(file) as f:
        data = json.load(f)
        place_name = data["metadata"]["name"]
        for date, counts in data.get("stats_by_date", {}).items():
            aggregate[date]["infant_availability"] += counts.get(
                "infant_availability", 0
            )
            aggregate[date]["toddler_availability"] += counts.get(
                "toddler_availability", 0
            )
            aggregate[date]["infant_capacity"] += counts.get("infant_capacity", 0)
            aggregate[date]["toddler_capacity"] += counts.get("toddler_capacity", 0)

            # Make special mention of places that have current availabilities
            if date != todays_date:
                continue
            if counts.get("infant_availability", 0) > 0:
                places_with_infant_availability.append(place_name)
            if counts.get("toddler_availability", 0) > 0:
                places_with_toddler_availability.append(place_name)


# Convert to regular dict
result = {
    "stats_by_date": dict(aggregate),
    "places_with_infant_availability": places_with_infant_availability,
    "places_with_toddler_availability": places_with_toddler_availability,
}

# Write to output file
with open(OUTPUT_PATH, "w") as f:
    json.dump(result, f, indent=2)
