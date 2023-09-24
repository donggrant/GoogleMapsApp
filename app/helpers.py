from config import Config
import requests

def get_lat_lng(address):
    endpoint = Config.GEOCODE_ENDPOINT
    params = {"address": address, "key": Config.API_KEY}
    response = requests.get(endpoint, params=params)
    if response.status_code == 200 and response.json()["status"] == "OK":
        location = response.json()["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    raise ValueError("Failed to convert the given input. Please ensure it's correct.")

def get_address_from_lat_lng(lat, lng):
    endpoint = Config.GEOCODE_ENDPOINT
    params = {"latlng": f"{lat},{lng}", "key": Config.API_KEY}
    response = requests.get(endpoint, params=params)
    if response.status_code == 200 and response.json()["status"] == "OK":
        return response.json()["results"][0]["formatted_address"]
    raise ValueError("Failed to convert the given input. Please ensure it's correct.")

def get_city_bounding_box(city_name):
    params = {"address": city_name, "key": Config.API_KEY}
    response = requests.get(Config.GEOCODE_ENDPOINT, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        if data["status"] == "OK" and len(data["results"]) > 0:
            location = data["results"][0]["geometry"]["location"]
            lat = location["lat"]
            lng = location["lng"]
            buffer = 0.1  # Example buffer (adjust as needed)

            # Calculate NORTHEAST and SOUTHWEST coordinates
            NORTHEAST_LAT = lat + buffer
            NORTHEAST_LNG = lng + buffer
            SOUTHWEST_LAT = lat - buffer
            SOUTHWEST_LNG = lng - buffer
            
            return {
                "NORTHEAST_LAT": NORTHEAST_LAT,
                "NORTHEAST_LNG": NORTHEAST_LNG,
                "SOUTHWEST_LAT": SOUTHWEST_LAT,
                "SOUTHWEST_LNG": SOUTHWEST_LNG
            }
        else:
            raise ValueError("Geocoding API response error")
    else:
        raise ValueError("Failed to fetch data from the Geocoding API. Status code:", response.status_code)