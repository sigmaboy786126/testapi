from flask import Flask, jsonify
import os
from functools import wraps

app = Flask(__name__)

# Complete in-memory festival data
FESTIVALS_DATA = {
    "metadata": {
        "title": "Complete Indian Festival Database",
        "description": "Comprehensive collection of all Indian festivals with historical context",
        "country": "India", 
        "year": 2024,
        "version": "2.0",
        "last_updated": "2024-01-20",
        "note": "Dates based on Hindu lunar calendar may vary slightly by region"
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
            "name": "Lohri",
            "type": "Harvest Festival",
            "description": "Punjabi festival marking the end of winter with bonfires and traditional dances",
            "date": "2024-01-13",
            "regions": ["Punjab", "Haryana", "Delhi", "Himachal Pradesh"],
            "public_holiday": True
        },
        {
            "name": "Makar Sankranti",
            "type": "Harvest Festival",
            "description": "Marks the sun's transition into Capricorn and the end of winter. Celebrated with kite flying and sweets made of jaggery and sesame",
            "date": "2024-01-15",
            "regions": ["Andhra Pradesh", "Telangana", "Karnataka", "Maharashtra", "Gujarat", "Rajasthan", "Uttar Pradesh", "Bihar", "West Bengal"],
            "public_holiday": True
        },
        {
            "name": "Pongal",
            "type": "Harvest Festival", 
            "description": "Four-day Tamil harvest festival thanking nature and farm animals. Features rice boiled in milk until it overflows - symbolizing abundance",
            "date": "2024-01-15",
            "regions": ["Tamil Nadu", "Puducherry"],
            "public_holiday": True
        },
        {
            "name": "Republic Day",
            "type": "National Holiday",
            "description": "Commemorates the adoption of India's Constitution on January 26, 1950. Features grand parade in New Delhi showcasing military might and cultural diversity",
            "date": "2024-01-26", 
            "regions": ["All India"],
            "public_holiday": True
        },
        {
            "name": "Vasant Panchami",
            "type": "Religious Festival",
            "description": "Dedicated to Goddess Saraswati, the deity of knowledge, music and arts. People wear yellow clothes and offer prayers to seek wisdom",
            "date": "2024-02-14",
            "regions": ["North India", "West India", "East India"],
            "public_holiday": False
        },
        {
            "name": "Maha Shivaratri",
            "type": "Religious Festival",
            "description": "The Great Night of Shiva dedicated to Lord Shiva's cosmic dance. Devotees fast, meditate and offer prayers throughout the night",
            "date": "2024-03-08",
            "regions": ["All India"],
            "public_holiday": True
        },
        {
            "name": "Holi",
            "type": "Religious Festival", 
            "description": "Festival of colors celebrating the victory of good over evil and the arrival of spring. Derived from the legend of Prahlad and Holika",
            "date": "2024-03-25",
            "regions": ["North India", "West India", "East India"],
            "public_holiday": True
        },
        {
            "name": "Good Friday",
            "type": "Religious Holiday",
            "description": "Christian holiday commemorating the crucifixion of Jesus Christ and his death at Calvary",
            "date": "2024-03-29",
            "regions": ["All India"],
            "public_holiday": True
        },
        {
            "name": "Easter Sunday",
            "type": "Religious Holiday",
            "description": "Christian holiday celebrating the resurrection of Jesus Christ from the dead",
            "date": "2024-03-31",
            "regions": ["All India"],
            "public_holiday": False
        },
        {
            "name": "Ugadi",
            "type": "New Year Festival",
            "description": "Telugu and Kannada New Year marking the beginning of a new Hindu lunar calendar. Special dishes with six tastes symbolize life's experiences",
            "date": "2024-04-09",
            "regions": ["Andhra Pradesh", "Telangana", "Karnataka"],
            "public_holiday": True
        },
        {
            "name": "Gudi Padwa",
            "type": "New Year Festival",
            "description": "Marathi and Konkani New Year celebrating the arrival of spring and harvest season. Homes decorated with rangoli and Gudi displays",
            "date": "2024-04-09",
            "regions": ["Maharashtra", "Goa"],
            "public_holiday": True
        },
        {
            "name": "Vishu",
            "type": "New Year Festival",
            "description": "Malayali New Year festival featuring Vishu Kani arrangement and Vishu Kaineettam gift giving traditions",
            "date": "2024-04-14",
            "regions": ["Kerala"],
            "public_holiday": True
        },
        {
            "name": "Baisakhi",
            "type": "Harvest Festival",
            "description": "Sikh New Year and harvest festival commemorating the formation of Khalsa Panth by Guru Gobind Singh in 1699",
            "date": "2024-04-13",
            "regions": ["Punjab", "Haryana"],
            "public_holiday": True
        },
        {
            "name": "Ram Navami",
            "type": "Religious Festival",
            "description": "Celebrates the birth of Lord Rama, the seventh avatar of Vishnu and hero of the epic Ramayana",
            "date": "2024-04-17",
            "regions": ["All India"],
            "public_holiday": True
        },
        {
            "name": "Mahavir Jayanti",
            "type": "Religious Festival",
            "description": "Birth anniversary of Lord Mahavira, the 24th and last Tirthankara of Jainism who established central tenets of Jain philosophy",
            "date": "2024-04-21",
            "regions": ["All India"],
            "public_holiday": True
        },
        {
            "name": "Eid al-Fitr",
            "type": "Religious Festival",
            "description": "Marks the end of Ramadan, the Islamic holy month of fasting. Muslims offer prayers, exchange gifts and share meals",
            "date": "2024-04-11",
            "regions": ["All India"],
            "public_holiday": True
        },
        {
            "name": "Maharashtra Day",
            "type": "Regional Holiday",
            "description": "Commemorates the formation of Maharashtra state from the Bombay Presidency on May 1, 1960",
            "date": "2024-05-01",
            "regions": ["Maharashtra"],
            "public_holiday": True
        },
        {
            "name": "Buddha Purnima",
            "type": "Religious Festival",
            "description": "Celebrates the birth, enlightenment and death (Parinirvana) of Gautama Buddha, founder of Buddhism",
            "date": "2024-05-23",
            "regions": ["All India"],
            "public_holiday": True
        },
        {
            "name": "Eid al-Adha",
            "type": "Religious Festival",
            "description": "Festival of Sacrifice commemorating Prophet Ibrahim's willingness to sacrifice his son as an act of obedience to God",
            "date": "2024-06-17",
            "regions": ["All India"],
            "public_holiday": True
        },
        {
            "name": "Rath Yatra",
            "type": "Religious Festival",
            "description": "Chariot festival of Lord Jagannath featuring massive chariots pulled through streets of Puri. One of oldest rituals in India",
            "date": "2024-07-07",
            "regions": ["Odisha", "West Bengal", "Jharkhand"],
            "public_holiday": True
        },
        {
            "name": "Muharram (Ashura)",
            "type": "Religious Festival",
            "description": "Islamic day of mourning for the martyrdom of Imam Hussain, grandson of Prophet Muhammad at Battle of Karbala",
            "date": "2024-07-17",
            "regions": ["All India"],
            "public_holiday": True
        },
        {
            "name": "Independence Day",
            "type": "National Holiday",
            "description": "Celebrates India's independence from British rule on August 15, 1947. Flag hoisting ceremonies across the country",
            "date": "2024-08-15",
            "regions": ["All India"],
            "public_holiday": True
        },
        {
            "name": "Raksha Bandhan",
            "type": "Cultural Festival",
            "description": "Celebrates the bond between brothers and sisters. Sisters tie sacred threads (rakhi) on brothers' wrists who vow to protect them",
            "date": "2024-08-19",
            "regions": ["North India", "West India", "Central India"],
            "public_holiday": False
        },
        {
            "name": "Pateti (Parsi New Year)",
            "type": "New Year Festival",
            "description": "Parsi New Year and day of repentance marking the creation of the universe and beginning of Zoroastrian calendar",
            "date": "2024-08-16",
            "regions": ["Maharashtra", "Gujarat"],
            "public_holiday": True
        },
        {
            "name": "Janmashtami",
            "type": "Religious Festival",
            "description": "Celebrates the birth of Lord Krishna, the eighth avatar of Vishnu. Features Dahi Handi ritual with human pyramids",
            "date": "2024-08-26",
            "regions": ["All India"],
            "public_holiday": True
        },
        {
            "name": "Ganesh Chaturthi",
            "type": "Religious Festival",
            "description": "10-day festival celebrating the birth of Lord Ganesha, the remover of obstacles. Idols immersed in water on final day",
            "date": "2024-09-07",
            "regions": ["Maharashtra", "Goa", "Karnataka", "Andhra Pradesh", "Telangana"],
            "public_holiday": True
        },
        {
            "name": "Onam",
            "type": "Harvest Festival",
            "description": "Kerala's harvest festival celebrating King Mahabali's annual return. Features flower decorations, boat races and grand feasts",
            "date": "2024-09-15",
            "regions": ["Kerala"],
            "public_holiday": True
        },
        {
            "name": "Eid-e-Milad-un-Nabi (Mawlid)",
            "type": "Religious Festival",
            "description": "Celebrates the birthday of the Islamic prophet Muhammad with prayers, processions and religious gatherings",
            "date": "2024-09-16",
            "regions": ["All India"],
            "public_holiday": True
        },
        {
            "name": "Navratri",
            "type": "Religious Festival",
            "description": "Nine-night festival dedicated to Goddess Durga and her various forms. Features fasting, prayer and traditional Garba dances",
            "date": "2024-10-03",
            "regions": ["All India"],
            "public_holiday": False
        },
        {
            "name": "Dussehra",
            "type": "Religious Festival",
            "description": "Celebrates the victory of Lord Rama over demon king Ravana. Features Ramlila performances and burning of Ravana effigies",
            "date": "2024-10-12",
            "regions": ["All India"],
            "public_holiday": True
        },
        {
            "name": "Diwali",
            "type": "Religious Festival",
            "description": "Festival of lights celebrating Lord Rama's return to Ayodhya after 14 years of exile. Homes decorated with diyas and rangoli",
            "date": "2024-10-31",
            "regions": ["All India"],
            "public_holiday": True
        },
        {
            "name": "Chhath Puja",
            "type": "Religious Festival",
            "description": "Ancient Hindu festival dedicated to the Sun God. Involves fasting, holy bathing and offering prayers to rising and setting sun",
            "date": "2024-11-07",
            "regions": ["Bihar", "Uttar Pradesh", "Jharkhand"],
            "public_holiday": True
        },
        {
            "name": "Guru Nanak Jayanti",
            "type": "Religious Festival",
            "description": "Celebrates the birth of Guru Nanak Dev, the founder of Sikhism and first of the ten Sikh Gurus",
            "date": "2024-11-15",
            "regions": ["Punjab", "Haryana", "Delhi", "Himachal Pradesh"],
            "public_holiday": True
        },
        {
            "name": "Christmas",
            "type": "Religious Holiday",
            "description": "Celebrates the birth of Jesus Christ with midnight mass, carol singing and exchange of gifts. Homes decorated with Christmas trees",
            "date": "2024-12-25",
            "regions": ["All India"],
            "public_holiday": True
        }
    ],
    "regional_events": [
        {
            "name": "Kumbh Mela",
            "type": "Religious Gathering",
            "description": "Mass Hindu pilgrimage of faith and largest peaceful gathering in world. Held every 12 years at four riverbank pilgrimage sites",
            "frequency": "Every 12 years",
            "next_occurrence": "2025",
            "regions": ["Uttar Pradesh", "Madhya Pradesh", "Maharashtra"]
        },
        {
            "name": "Hornbill Festival",
            "type": "Cultural Festival",
            "description": "Celebration of Naga culture featuring traditional music, dance, crafts and food from all Naga tribes. Promotes cultural preservation",
            "date": "2024-12-01",
            "duration_days": 10,
            "regions": ["Nagaland"]
        },
        {
            "name": "Surajkund International Craft Mela",
            "type": "Cultural Fair",
            "description": "International crafts fair showcasing traditional handicrafts and handlooms from India and other countries",
            "date": "2024-02-02",
            "duration_days": 15,
            "regions": ["Haryana"]
        },
        {
            "name": "Goa Carnival",
            "type": "Cultural Festival",
            "description": "Pre-Lenten festival celebrated in Goa with colorful parades, floats, dances and music reflecting Portuguese influence",
            "date": "2024-02-10",
            "duration_days": 4,
            "regions": ["Goa"]
        },
        {
            "name": "Thrissur Pooram",
            "type": "Cultural Festival",
            "description": "Kerala's most spectacular temple festival featuring magnificent elephant processions and traditional percussion performances",
            "date": "2024-05-10",
            "duration_days": 3,
            "regions": ["Kerala"]
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
