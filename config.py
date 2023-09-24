import os

class Config:
    # set API_KEY with 'export/set GOOGLE_MAPS_API_KEY=""'
    API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
    GEOCODE_ENDPOINT = "https://maps.googleapis.com/maps/api/geocode/json"