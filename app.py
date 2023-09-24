from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# set API_KEY with 'export GOOGLE_MAPS_API_KEY=""'
API_KEY = "AIzaSyBbl9eDdehQIm75FCYuvp4SRIoym6UCvo8"
GEOCODE_ENDPOINT = "https://maps.googleapis.com/maps/api/geocode/json"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    try:
        action = data.get("action")
        if action == "addressToLatLng":
            result = get_lat_lng_from_address(data["input"], API_KEY)
        elif action == "latLngToAddress":
            result = get_address_from_lat_lng(data["lat"], data["lng"], API_KEY)
        else:
            return jsonify({"error": "Invalid action."}), 400

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/bounding_box", methods=["POST"])
def bounding_box():
    data = request.get_json()
    try:
        if "city" in data:
            result = get_city_bounding_box(data["city"], API_KEY)
            return jsonify(result)
        else:
            raise ValueError("City name not provided in the request.")
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
def get_lat_lng_from_address(address, api_key):
    params = {"address": address, "key": api_key}
    response = requests.get(GEOCODE_ENDPOINT, params=params)
    if response.status_code == 200 and response.json()["status"] == "OK":
        location = response.json()["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    raise ValueError("Failed to convert the given input. Please ensure it's correct.")

def get_address_from_lat_lng(lat, lng, api_key):
    params = {"latlng": f"{lat},{lng}", "key": api_key}
    response = requests.get(GEOCODE_ENDPOINT, params=params)
    if response.status_code == 200 and response.json()["status"] == "OK":
        return response.json()["results"][0]["formatted_address"]
    raise ValueError("Failed to convert the given input. Please ensure it's correct.")

def get_city_bounding_box(city_name, api_key):
    params = {"address": city_name, "key": api_key}
    response = requests.get(GEOCODE_ENDPOINT, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK" and len(data["results"]) > 0:
            location = data["results"][0]["geometry"]["location"]
            lat = location["lat"]
            lng = location["lng"]
            buffer = 0.1  # Example buffer (adjust as needed)
            min_lat = lat - buffer
            max_lat = lat + buffer
            min_lng = lng - buffer
            max_lng = lng + buffer
            return {
                "min_lat": min_lat,
                "max_lat": max_lat,
                "min_lng": min_lng,
                "max_lng": max_lng
            }
        else:
            raise ValueError("Geocoding API response error")
    else:
        raise ValueError("Failed to fetch data from the Geocoding API. Status code:", response.status_code)

if __name__ == "__main__":
    app.run(debug=True, port=5101)
