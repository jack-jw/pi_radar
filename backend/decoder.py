# Piradar
# decoder.py

"""
ADSB decoder
Returns some demo aircraft for testing for now
"""

from json import load

def get():
    with open("./backend/demos.json") as f:
        return load(f)
