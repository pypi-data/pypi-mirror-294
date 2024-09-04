import json
import os

countries: list = []

# Load the timezone data
package_dir = os.path.dirname(__file__)
with open(os.path.join(package_dir, 'timezone_data.json')) as f:
    timezone_data: dict = json.load(f)

def getCountries(func):
    def main(*args, **kwargs):
        l: list = func(*args, **kwargs)
        for i in l:
            if i not in countries:
                countries.append(i)
    return main

@getCountries
def get_countries() -> list:
    """Return a list of all countries available in the dataset."""

    return list(timezone_data.keys())

def get_timezones_by_country(country: str, data: dict = timezone_data) -> list:
    """Return a list of timezones for a given country."""
    return data.get(country, None)

def get_countries_by_timezone(timezone: str) -> list:
    """Return a list of countries that use a specific timezone."""
    countries: list = []
    for country, zones in timezone_data.items():
        if timezone in zones:
            countries.append(country)
    return countries
