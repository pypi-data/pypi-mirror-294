def validate_country(country: str, available_countries: list):
    """Validate if the provided country is in the available countries list."""
    if country not in available_countries:
        raise ValueError(f"{country} is not a valid country in the dataset.")
