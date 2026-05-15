import re
from .cities import resolve_shared_state_code

# Public API (used by normalizer.py)

def build_country_patterns(cities_df, unidentified_label: str) -> dict[str, str]:
    """
    Build deterministic regex patterns mapping user-input location strings
    to country names, using a reference cities gazetteer.

    Parameters
    ----------
    cities_df : pandas.DataFrame
        Prepared cities gazetteer.
    unidentified_label : str
        Label used for non-country / invalid matches.

    Returns
    -------
    dict[str, str]
        Mapping of regex pattern -> country name (or special tokens).
    """
    patterns: dict[str, str] = {}

    # 1. Manual overrides (highest priority)
    patterns.update(_manual_country_patterns())

    # 2. Gazetteer-derived patterns (states, codes, country names)
    patterns.update(_gazetteer_country_patterns(cities_df))

    # 3. Non-country / exclusion patterns
    patterns.update(_non_country_patterns(unidentified_label))

    return patterns

def parse_country_from_location(
    location: str,
    patterns: dict[str, str],
    unidentified_label: str,
    cities_df,
    ) -> str | None:
    
    """
    Parse a country from a free-text location string using deterministic patterns.

    Returns
    -------
    str | None
        Country name if deterministically resolved, otherwise None.
    """
    if location is None:
        return None

    for pattern, country in patterns.items():
        match = re.search(pattern, location, re.IGNORECASE)
        if not match:
            continue

        if country == "Shared":
            # Shared state-code logic (US / BR)
            split = [
                s.strip()
                for s in re.split(re.compile(pattern, re.IGNORECASE), location)
                if s
            ]

            if not split:
                return unidentified_label

            city_match = re.search(r"[A-Za-zÀ-ÖØ-öø-ÿ\s]+", split[0])
            if not city_match:
                return unidentified_label

            city_name = city_match.group().strip()
            state_code = split[-1].strip()

            return resolve_shared_state_code(
                city=city_name,
                state_code=state_code,
                cities_df=cities_df,
            )

        if country == unidentified_label:
            return unidentified_label

        return country

    return None

# Internal helpers

def _manual_country_patterns() -> dict[str, str]:
    """
    Empirically observed abbreviations, misspellings, and aliases
    encountered in UGC platforms.
    """
    return {
        # United Kingdom
        r"\bu\.?k\.?\b|\bgibraltar\b|\bcayman\b|\bnotts\b|\bmidlands\b": "United Kingdom",
        r"\bisle\sof\sman\b|\blo+ndon\b|\bmanchester\b|\bliverpool[a-z\s]*\b": "United Kingdom",

        # United States
        r"\bu\.?s\.?a?\.?\b|\bcal+i?for?ni?a\b|\bnew\syork\b|\bvegas\b": "United States",
        r"\bseat+le\b|\bchic?ago\b|\bphila\b|\blahaina?\b": "United States",

        # Other explicit cases
        r"\bh\.?k\.?\b|\bhong\skong\b": "China",
        r"\bn\.?z\.?\b|\bcook\sislands\b": "New Zealand",
        r"\bitalia\b": "Italy",
        r"\btürkiye\b|\bbodrum\b": "Turkey",
        r"\bkosovo\b": "Serbia",
        r"\bgreenland\b": "Denmark",
    }


def _gazetteer_country_patterns(cities_df) -> dict[str, str]:
    """
    Build regex patterns from the cities gazetteer:
    - country names
    - state codes for selected countries
    """
    patterns: dict[str, str] = {}

    # Country names
    for country in cities_df["country_name"].dropna().unique():
        patterns[rf"\b{re.escape(country)}\b"] = country

    # State-code logic (US / BR / CA)
    us_states = set(
        cities_df[cities_df["country_code"] == "US"]["state_code"].dropna().unique()
    )
    br_states = set(
        cities_df[cities_df["country_code"] == "BR"]["state_code"].dropna().unique()
    )
    ca_states = set(
        cities_df[cities_df["country_code"] == "CA"]["state_code"].dropna().unique()
    )

    shared = us_states & br_states
    unique_us = us_states - shared
    unique_br = br_states - shared

    if unique_us:
        patterns[rf"\b({'|'.join(map(re.escape, unique_us))})\b"] = "United States"

    if unique_br:
        patterns[rf"\b({'|'.join(map(re.escape, unique_br))})\b"] = "Brazil"

    if ca_states:
        patterns[rf"\b({'|'.join(map(re.escape, ca_states))})\b"] = "Canada"

    if shared:
        patterns[rf"\b({'|'.join(map(re.escape, shared))})\b"] = "Shared"

    return patterns


def _non_country_patterns(unidentified_label: str) -> dict[str, str]:
    """
    Patterns that should explicitly *not* resolve to countries.
    """
    not_countries = [
        "world",
        "europe",
        "asia",
        "africa",
        "oceania",
        "south america",
        "north america",
        "caribbean",
        "middle east",
        "antarctica",
        "mediterranean",
        "not found",
    ]

    return {
        rf"\b({'|'.join(map(re.escape, not_countries))})\b": unidentified_label,
        r"\b[0-9]+\b": unidentified_label,
    }
    

