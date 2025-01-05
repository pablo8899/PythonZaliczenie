import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np


stations = [
    "WŁODAWA",
    "SIEDLCE",
    "TERESPOL",
    "TOMASZÓW LUBELSKI"
]

def get_xml():
    url = "https://danepubliczne.imgw.pl/api/data/meteo/format/xml"
    response = requests.get(url)
    return response.text

def draw(wind_speeds):
    
    plt.title("Średnie prędkości wiatrów dla wybranych stacji")
    plt.ylabel("Średnia prędkość wiatru")
    plt.bar(wind_speeds.keys(), wind_speeds.values())
    plt.show()


def main():
    root = ET.fromstring(get_xml())
    wind_speeds = {}
    for station in root.findall("item"):
        station_name = station.find("nazwa_stacji").text
        wind_speed = station.find("wiatr_srednia_predkosc").text
        if station_name in stations and wind_speed:
            wind_speeds[station_name] = float(wind_speed)

    draw(wind_speeds)

if __name__ == "__main__":
    main()
