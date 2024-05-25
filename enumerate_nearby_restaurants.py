import requests
from dotenv import load_dotenv
import os

def get_nearby_restaurants(api_key: str, lat: float, lon: float, radius: int = 500, type: str = "restaurant"):
    """_summary_

    Args:
        api_key (str): GOOGLE_MAPS_API_KEY
        lat (float): latitude, 緯度
        lon (float): longitude, 経度
        radius (int, optional): search range. Defaults to 1000.
        type (str, optional): place type. Defaults to "restaurant".

    Raises:
        Exception: Failed to fetch data

    Returns:
        dict: place list from Google Maps API
    """    
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": api_key,
        "location": f"{lat},{lon}",
        "radius": radius,
        "keyword": type,
        "language": "ja"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.text}")
    places = response.json().get("results", [])
    return places


def get_place_details(api_key: str, place_id: str):
    url = f"https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "key": api_key,
        "place_id": place_id
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.text}")
    
    details = response.json().get("result", {})
    return details

def main():
    load_dotenv()
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    lat = 35.7143416
    lon = 139.7619679
    places = get_nearby_restaurants(api_key, lat, lon)
    for place in places:
        details = get_place_details(api_key, place["place_id"])
        name = details.get("name", "N/A")
        opening_hours = details.get("opening_hours", {}).get("weekday_text", [])
        print(f"Name: {name}")
        print()


if __name__ == "__main__":
    main()
    