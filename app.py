from flask import Flask, jsonify
import requests

app = Flask(__name__)

# API Keys (Replace with your actual keys)
OPENWEATHERMAP_API_KEY = '9cef1f68ce953c6fdcd4ff77a902ddfe'
TOMTOM_API_KEY = 'DXAeazkkWp6Cy9d6RBHtqgAUtG2TQZeB'

# Pollution Prediction - OpenWeatherMap API
def get_pollution_data(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHERMAP_API_KEY}'
    response = requests.get(url)
    return response.json()

# Traffic Prediction - TomTom API
def get_traffic_data(lat, lon):
    url = f'https://api.tomtom.com/traffic/services/4/incidentDetails?bbox={lat},{lon}&key={TOMTOM_API_KEY}'
    response = requests.get(url)
    return response.json()

# Weather Data - OpenWeatherMap API
def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}'
    response = requests.get(url)
    return response.json()

# Geolocation API - TomTom Geocoding API
def get_geolocation(city):
    url = f'https://api.tomtom.com/search/2/geocode/{city}.json?key={TOMTOM_API_KEY}'
    response = requests.get(url)
    return response.json()

# Sunrise and Sunset Times - Sunrise-Sunset API (No API Key Required)
def get_sunrise_sunset_data(lat, lon):
    url = f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&formatted=0'
    response = requests.get(url)
    return response.json()

# Route to get all data
@app.route('/api/scrape_all/<city>/<latitude>/<longitude>', methods=['GET'])
def scrape_all(city, latitude, longitude):
    try:
        # Fetch data from various APIs
        pollution_data = get_pollution_data(latitude, longitude)
        traffic_data = get_traffic_data(latitude, longitude)
        weather_data = get_weather_data(city)
        geolocation_data = get_geolocation(city)
        sunrise_sunset_data = get_sunrise_sunset_data(latitude, longitude)

        # Combine all data in one response
        data = {
            "pollution_data": pollution_data,
            "traffic_data": traffic_data,
            "weather_data": weather_data,
            "geolocation_data": geolocation_data,
            "sunrise_sunset_data": sunrise_sunset_data
        }

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
