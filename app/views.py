from flask import Blueprint, render_template, request, jsonify
from .helpers import get_lat_lng, get_address_from_lat_lng, get_city_bounding_box

bp = Blueprint('app', __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/convert", methods=["POST"])
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
    
@bp.route("/bounding_box", methods=["POST"])
def bounding_box():
    data = request.get_json()
    try:
        if data["action"] == "getBoundingBox":
            result = get_city_bounding_box(data["input"])
            return jsonify(result)
        else:
            raise ValueError("City name not provided in the request.")
    except Exception as e:
        return jsonify({"error": str(e)}), 400