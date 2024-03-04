from flask import Flask, jsonify
import random  # For simulating real-time data updates
import time

app = Flask(__name__)

# Replace this with your actual data fetching/generation logic
def get_data():
    return {
        'valueTemp': random.randint(28, 35),
        'windSpeed': random.randint(1, 10),
        'windDirec': ['N', 'S', 'E', 'W'][random.randint(0, 3)],
        'humidity':  random.randint(40, 80)
    }

@app.route('/weather_data')
def weather():
    return jsonify(get_data())

if __name__ == '__main__':
    app.run(debug=True, port=5000)  