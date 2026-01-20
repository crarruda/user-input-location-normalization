from typing import Optional

from .patterns import (
    build_country_patterns,
    parse_country_from_location,
)
from .geocoding import geocode_country
from .cities import get_valid_countries


def normalize_location(
    raw_location: Optional[str],
    *,
    cities_df,
    unidentified_label: str = "unidentified",
    use_geocoding: bool = True,
    geolocator=None,
    ) -> str:
    
    """
    Normalize a user-input location string to a country-level label.

    The normalization follows a strict hierarchy:
    1. Deterministic pattern-based matching (regex + gazetteer)
    2. Optional external geocoding fallback
    3. Explicit unidentified label

    Parameters
    ----------
    raw_location : str or None
        Free-text user-input location.
    cities_df : pandas.DataFrame
        Prepared reference cities gazetteer.
    unidentified_label : str, optional
        Label returned when no reliable country can be determined.
    use_geocoding : bool, optional
        Whether to use external geocoding as a fallback.
    geolocator : optional
        A geopy geolocator instance, required if use_geocoding=True.

    Returns
    -------
    str
        Normalized country name or unidentified_label.
    """

    # Basic input validation

    if raw_location is None:
        return unidentified_label

    location = str(raw_location).strip()
    if not location:
        return unidentified_label

    # Deterministic pattern-based resolution

    patterns = build_country_patterns(
        cities_df=cities_df,
        unidentified_label=unidentified_label,
    )

    country = parse_country_from_location(
        location=location,
        patterns=patterns,
        unidentified_label=unidentified_label,
        cities_df=cities_df,
    )

    if country:
        return country

    # Geocoding fallback

    if use_geocoding:
        if geolocator is None:
            raise ValueError(
                "use_geocoding=True requires a geolocator instance."
            )

        valid_countries = set(
            get_valid_countries(cities_df).keys()
        )

        country = geocode_country(
            location=location,
            geolocator=geolocator,
            valid_countries=valid_countries,
        )

        if country:
            return country

    # Final fallback

    return unidentified_label

print("Loaded normalizer.py")