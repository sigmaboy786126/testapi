from flask import Flask, jsonify
import os
from functools import wraps

app = Flask(__name__)

# Complete in-memory festival data
FESTIVALS_DATA = {
    "metadata": {
        "title": "Indian Festival & Event Calendar API",
        "description": "A comprehensive collection of festivals, holidays and cultural events across India",
        "country": "India",
        "year": 2024,
        "version": "1.0",
        "note": "Dates for lunar-based festivals may vary slightly by region"
    },
    "festivals": [
        {
            "name": "New Year's Day",
            "type": "International Holiday",
            "description": "Celebration of the new year",
            "date": "2024-01-01",
            "regions": ["All India"],
            "public_holiday": True
        },
        {
            "name": "Republic Day",
            "type": "National Holiday",
            "description": "Celebration of the adoption of the Indian Constitution",
            "date": "2024-01-26",
            "regions": ["All India"],
            "public_holiday": True
        },
        {
            "name": "Holi",
            "type": "Religious Festival",
            "description": "Festival of colors, celebrating the victory of good over evil",
            "date": "2024-03-25",
            "regions": ["North India", "West India", "East India"],
            "public_holiday": True
        },
        {
            "name": "Diwali",
            "type": "Religious Festival",
            "description": "Festival of lights",
            "date": "2024-10-31",
            "regions": ["All India"],
            "public_holiday": True
        },
        {
            "name": "Christmas",
            "type": "Religious Holiday",
            "description": "Celebration of the birth of Jesus Christ",
            "date": "2024-12-25",
            "regions": ["All India"],
            "public_holiday": True
        }
    ],
    "regional_events": [
        {
            "name": "Hornbill Festival",
            "type": "Cultural Festival",
            "description": "Celebration of Naga culture",
            "date": "2024-12-01",
            "duration_days": 10,
            "regions": ["Nagaland"]
        }
    ]
}

# CORS decorator
def cors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = f(*args, **kwargs)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        return response
    return decorated_function

@app.route('/')
@cors
def home():
    return jsonify({
        "message": "Indian Festival & Event Calendar API",
        "status": "success",
        "endpoints": {
            "/festivals": "Get all festivals",
            "/festivals/<name>": "Get festival by name",
            "/festivals/date/<date>": "Get festivals on a specific date (YYYY-MM-DD)",
            "/festivals/month/<month>": "Get festivals in a specific month (1-12)",
            "/festivals/region/<region>": "Get festivals by region",
            "/festivals/type/<type>": "Get festivals by type",
            "/festivals/public": "Get all public holidays",
            "/regional-events": "Get all regional events",
            "/metadata": "Get metadata about the dataset"
        }
    })

@app.route('/festivals')
@cors
def get_all_festivals():
    return jsonify(FESTIVALS_DATA["festivals"])

@app.route('/festivals/<name>')
@cors
def get_festival_by_name(name):
    name_lower = name.lower()
    festival = next((f for f in FESTIVALS_DATA["festivals"] 
                    if name_lower in f["name"].lower()), None)
    
    if festival:
        return jsonify(festival)
    else:
        return jsonify({"error": "Festival not found"}), 404

@app.route('/festivals/date/<date>')
@cors
def get_festivals_by_date(date):
    festivals = [f for f in FESTIVALS_DATA["festivals"] if f["date"] == date]
    return jsonify(festivals)

@app.route('/festivals/month/<int:month>')
@cors
def get_festivals_by_month(month):
    if month < 1 or month > 12:
        return jsonify({"error": "Month must be between 1 and 12"}), 400
    
    festivals = [f for f in FESTIVALS_DATA["festivals"] 
                 if int(f["date"].split('-')[1]) == month]
    return jsonify(festivals)

@app.route('/festivals/region/<region>')
@cors
def get_festivals_by_region(region):
    region_lower = region.lower()
    festivals = [f for f in FESTIVALS_DATA["festivals"] 
                 if any(region_lower == r.lower() for r in f["regions"])]
    return jsonify(festivals)

@app.route('/festivals/type/<festival_type>')
@cors
def get_festivals_by_type(festival_type):
    festivals = [f for f in FESTIVALS_DATA["festivals"] 
                 if f["type"].lower() == festival_type.lower()]
    return jsonify(festivals)

@app.route('/festivals/public')
@cors
def get_public_holidays():
    public_holidays = [f for f in FESTIVALS_DATA["festivals"] 
                       if f["public_holiday"]]
    return jsonify(public_holidays)

@app.route('/regional-events')
@cors
def get_regional_events():
    return jsonify(FESTIVALS_DATA["regional_events"])

@app.route('/metadata')
@cors
def get_metadata():
    return jsonify(FESTIVALS_DATA["metadata"])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
