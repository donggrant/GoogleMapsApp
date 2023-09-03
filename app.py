from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# set API_KEY with 'export GOOGLE_MAPS_API_KEY=""'
API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    try:
        if data["direction"] == "1":
            lat, lng = get_lat_lng(data["input"], API_KEY)
            return jsonify({"lat": lat, "lng": lng})
        elif data["direction"] == "2":
            address = get_address_from_lat_lng(data["lat"], data["lng"], API_KEY)
            return jsonify({"address": address})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_lat_lng(address, api_key):
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": api_key}
    response = requests.get(endpoint, params=params)
    if response.status_code == 200 and response.json()["status"] == "OK":
        location = response.json()["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    raise ValueError("Failed to convert the given input. Please ensure it's correct.")

def get_address_from_lat_lng(lat, lng, api_key):
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"latlng": f"{lat},{lng}", "key": api_key}
    response = requests.get(endpoint, params=params)
    if response.status_code == 200 and response.json()["status"] == "OK":
        return response.json()["results"][0]["formatted_address"]
    raise ValueError("Failed to convert the given input. Please ensure it's correct.")

if __name__ == "__main__":
    app.run(debug=True, port=5101)
