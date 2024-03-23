# Piradar
# decoder.py

"""
ADSB decoder
Returns some demo aircraft for testing for now
"""

def get():
    aircraft = {
        "40779a": {
            "lat": 51.5,
            "lng": -0.3,
            "heading": 70,
            "altitude": 2000,
            "speed": 300,
            "vspeed": 10,
            "icon": "plane",
            "icao24": "40779a",
            "callsign": "BAW282"
        },

        "7c4928": {
            "lat": 51.4,
            "lng": -0.2,
            "heading": 350,
            "altitude": 1500,
            "speed": 200,
            "vspeed": -10,
            "icon": "plane",
            "icao24": "7c4928",
            "callsign": "QFA2"
        },

        "helicopter": {
            "lat": 51.6,
            "lng": -0.1,
            "heading": 90,
            "altitude": 500,
            "speed": 30,
            "vspeed": 5,
            "icon": "helicopter",
            "icao24": "helicopter"
        },

        "ufo": {
            "lat": 51.55,
            "lng": 0,
            "heading": 30,
            "icon": "other",
            "icao24": "ufo"
        }
    }
    
    return aircraft
