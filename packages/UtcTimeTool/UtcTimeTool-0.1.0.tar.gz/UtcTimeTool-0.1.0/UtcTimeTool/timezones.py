import json
import os

# Load the timezone data
package_dir = os.path.dirname(__file__)
with open(os.path.join(package_dir, 'timezone_data.json')) as f:
    timezone_data: dict = json.load(f)

def get_countries() -> list:
    """Return a list of all countries available in the dataset."""
    return list(timezone_data.keys())

def get_timezones_by_country(country: str):
    """Return a list of timezones for a given country."""
    return timezone_data.get(country, None)

def get_countries_by_timezone(timezone: str) -> list:
    """Return a list of countries that use a specific timezone."""
    countries: list = []
    for country, zones in timezone_data.items():
        if timezone in zones:
            countries.append(country)
    return countries
