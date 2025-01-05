from concurrent.futures import ThreadPoolExecutor
import json
import requests

country_names = [
    "Poland",
    "Germany",
    "France",
    "Italy",
    "Spain",
    "Norway",
    "Sweden",
    "Finland",
    "Denmark",
    "Portugal",
    "Austria",
    "Switzerland",
    "Greece",
    "Hungary",
    "Belgium",
    "Netherlands",
    "Czech Republic",
    "Slovakia",
    "Croatia",
    "Estonia"
]

def load_json(country):
    url = f'http://universities.hipolabs.com/search?country={country}'
    response = requests.get(url)
    return response.json()



with ThreadPoolExecutor(max_workers=20) as executor:
    jsons = executor.map(load_json, country_names)

countries = {}
for json_country in jsons:
    if json_country is not None and json_country != []:
        names = []
        for j in json_country:
            names.append(j["name"])

        countries[json_country[0]["country"]] = names


print(json.dumps(countries, indent=4, sort_keys=True))