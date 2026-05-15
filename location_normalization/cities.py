import pandas as pd

# Data loading

def load_cities(path: str) -> pd.DataFrame:
    """
    Load the reference cities gazetteer.

    Parameters
    ----------
    path : str
        Path to the cities CSV file.

    Returns
    -------
    pandas.DataFrame
    """
    
    cities = pd.read_csv(
        path,
        na_values=["", "NaN"],
        keep_default_na=False
        )
    
    return cities

# Preparation

def prepare_cities_df(cities: pd.DataFrame) -> pd.DataFrame:
    
    # Standardise country naming conventions in the cities gazetteer.
    
    cities = cities.copy()
    cities["country_name"] = cities["country_name"].replace({
        "Fiji Islands": "Fiji",
        "Palestinian Territory Occupied": "Palestinian Territories",
        "The Bahamas": "Bahamas",
        "The Gambia ": "The Gambia",
        "Micronesia": "Federated States of Micronesia",
        "Timor-Leste": "East Timor",
        "Sao Tome and Principe": "São Tomé and Príncipe",
        "Cote D'Ivoire (Ivory Coast)": "Côte d'Ivoire",
    })
    
    return cities

# Gazetteer helpers

def unique_values(
    cities_df,
    column,
    *,
    country_code=None
    ) -> list[str]:
    
    """
    Return unique values from a given column, optionally filtered
    by country code.
    """
    
    if country_code is not None:
        return (
            cities_df[cities_df["country_code"] == country_code][column]
            .dropna()
            .unique()
            .tolist()
        )
        
    return cities_df[column].dropna().unique().tolist()

def get_valid_countries(cities_df: pd.DataFrame) -> dict[str, dict]:
    """
    Build a dictionary of valid country names and ISO codes
    derived from the reference gazetteer.
    """
    
    valid: dict[str, dict] = {
        country: {"iso": code}
        for country, code in zip(
            cities_df["country_name"].unique(),
            cities_df["country_code"].unique(),
        )
    }

    # Manually add missing countries
    valid["Monaco"] = {"iso": "MC"}
    valid["Curaçao"] = {"iso": "CW"}

    # Remove ambiguous or problematic entries
    valid.pop("Congo", None)
    valid.pop("Palau", None)

    # Standardise alternative country names
    renaming = {
        "Palestinian Territory": "Palestinian Territories",
        "Palestinian Territory Occupied": "Palestinian Territories",
    }

    for old, new in renaming.items():
        if old in valid:
            valid[new] = valid.pop(old)

    return valid

# Ambiguity resolution helpers

def resolve_shared_state_code(
    city: str,
    state_code: str,
    cities_df: pd.DataFrame,
    ) -> str:
    
    """
    Resolve ambiguous state codes shared between multiple countries
    (currently US / Brazil).
    """
    
    us_match = (
        (cities_df["name"] == city)
        & (cities_df["state_code"] == state_code)
        & (cities_df["country_code"] == "US")
    )

    if us_match.any():
        return "United States"

    br_match = (
        (cities_df["name"] == city)
        & (cities_df["state_code"] == state_code)
        & (cities_df["country_code"] == "BR")
    )

    if br_match.any():
        return "Brazil"

    # Conservative fallback: unresolved shared code
    return "United States"
