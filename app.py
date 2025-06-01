from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)
from dotenv import load_dotenv
# Replace with your OpenWeatherMap API key
load_dotenv('.env')  # Load environment variables from .env file

API_KEY = os.getenv('OPENWEATHER_API_KEY')
print(f"Loaded API_KEY: {API_KEY}")  # Debug print
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower().strip()
    
    # Simple greeting responses
    if user_message in ['hi', 'hello', 'hey']:
        return jsonify({'response': 'Hello! Ask me about the weather in any city.'})
    elif user_message in ['bye', 'goodbye']:
        return jsonify({'response': 'Goodbye! Stay dry!'})
    
    # Assume the message is a city name for weather query
    try:
        params = {
            'q': user_message,
            'appid': API_KEY,
            'units': 'metric'  # Use Celsius
        }
        response = requests.get(WEATHER_API_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            weather = data['weather'][0]['description'].capitalize()
            temp = data['main']['temp']
            city = data['name']
            return jsonify({
                'response': f"The weather in {city} is {weather} with a temperature of {temp}°C."
            })
        else:
            return jsonify({'response': 'Sorry, I couldn’t find that city. Try another one!'})
    except Exception as e:
        return jsonify({'response': 'Oops! Something went wrong while fetching the weather.'})

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)