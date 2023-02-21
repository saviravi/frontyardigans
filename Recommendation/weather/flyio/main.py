from pickle import load
from flask import Flask, jsonify
from weathertypes import Station, WeatherDay

app = Flask(__name__)

# Load weather station data
with open('data.pickle', 'rb') as f:
    data: list[Station] = load(f)

@app.route('/')
def index():
    return jsonify(data)

@app.route('/cities')
def cities():
    cities = [station.city_name for station in data]
    return jsonify(cities)

@app.route('/cities/<name>')
def cities_detail(name):
    for station in data:
        if station.city_name.lower() == name.lower():
            return jsonify(station.weather)
    
    return "city not found", 400

@app.errorhandler(404)
def page_not_found(e):
    return '404 not found'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)