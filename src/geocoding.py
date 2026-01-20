import time
from typing import Optional

from geopy.exc import (
    GeocoderServiceError,
    GeocoderTimedOut,
    GeocoderUnavailable,
)

# Geocoding fallback

def geocode_country(
    location: str,
    *,
    geolocator,
    valid_countries: set[str],
    retries: int = 3,
    timeout: int = 10,
    ) -> Optional[str]:
    
    """
    Resolve a country name from a free-text location string using
    an external geocoding service (e.g. Nominatim).

    This function is intended as a last-resort when deterministic
    pattern matching fails.

    Parameters
    ----------
    location : str
        Free-text user-input location.
    geolocator :
        A geopy geolocator instance (injected by the caller).
    valid_countries : set[str]
        Set of acceptable country names.
    retries : int, optional
        Number of retry attempts on transient failures.
    timeout : int, optional
        Request timeout in seconds.

    Returns
    -------
    str or None
        Country name if resolved and validated, otherwise None.
    """
    if not location or geolocator is None:
        return None

    for attempt in range(retries):
        try:
            result = geolocator.geocode(
                location,
                exactly_one=True,
                language="en",
                timeout=timeout,
            )

            if not result or not result.address:
                return None

            # Nominatim returns a comma-separated address string.
            # We conservatively extract the last component as country.
            country = result.address.split(",")[-1].strip()

            if country in valid_countries:
                return country

            return None

        except (
            GeocoderServiceError,
            GeocoderTimedOut,
            GeocoderUnavailable,
        ):
            if attempt < retries - 1:
                # Exponential backoff: 1s, 2s, 4s, ...
                time.sleep(2 ** attempt)

    return None
