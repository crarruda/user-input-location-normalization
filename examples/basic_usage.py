# exemples/basic_usage.py

# Example script demonstrating basic usage of the location normalization module.
from geopy.geocoders import Nominatim

from src.cities import load_cities, prepare_cities_df
from src import normalize_location


# Setup

CITIES_PATH = "data/cities.csv"
UNIDENTIFIED = "unidentified"

cities = prepare_cities_df(
    load_cities(CITIES_PATH)
)

geolocator = Nominatim(
    user_agent="user-input-location-normalization-test"
)

# Test cases

test_locations = [
    # Deterministic (regex / gazetteer)
    "Lisbon, Portugal",
    "London",
    "CA",
    "TX",
    "São Paulo, BR",

    # Likely geocoding fallback
    "Reykjavik",
    "Helsinki",
    "Tallinn",

    # Garbage / ambiguous
    "Somewhere over the rainbow",
    "🌍",
    "",
    None,
]

# Run tests

for loc in test_locations:
    country = normalize_location(
        raw_location=loc,
        cities_df=cities,
        unidentified_label=UNIDENTIFIED,
        use_geocoding=True,
        geolocator=geolocator,
    )

    print(f"Input: {loc!r:30} → Output: {country}")

