from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# set API_KEY with 'export/set GOOGLE_MAPS_API_KEY=""'
API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
GEOCODE_ENDPOINT = "https://maps.googleapis.com/maps/api/geocode/json"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    try:
        if data["action"] == "addressToLatLng":
            lat, lng = get_lat_lng(data["input"])
            return jsonify({"lat": lat, "lng": lng})
        elif data["action"] == "latLngToAddress":
            address = get_address_from_lat_lng(data["lat"], data["lng"])
            return jsonify({"address": address})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route("/bounding_box", methods=["POST"])
def bounding_box():
    data = request.get_json()
    try:
        if "city" in data:
            result = get_city_bounding_box(data["city"])
            return jsonify(result)
        else:
            raise ValueError("City name not provided in the request.")
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_lat_lng(address):
    endpoint = GEOCODE_ENDPOINT
    params = {"address": address, "key": API_KEY}
    response = requests.get(endpoint, params=params)
    if response.status_code == 200 and response.json()["status"] == "OK":
        location = response.json()["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    raise ValueError("Failed to convert the given input. Please ensure it's correct.")

def get_address_from_lat_lng(lat, lng):
    endpoint = GEOCODE_ENDPOINT
    params = {"latlng": f"{lat},{lng}", "key": API_KEY}
    response = requests.get(endpoint, params=params)
    if response.status_code == 200 and response.json()["status"] == "OK":
        return response.json()["results"][0]["formatted_address"]
    raise ValueError("Failed to convert the given input. Please ensure it's correct.")

def get_city_bounding_box(city_name):
    params = {"address": city_name, "key": API_KEY}
    response = requests.get(GEOCODE_ENDPOINT, params=params)
    
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


if __name__ == "__main__":
    app.run(debug=True, port=5101)
