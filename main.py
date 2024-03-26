# Piradar
# main.py

"""
For now just starts the HTTP server

Functions:
    start()
"""

from os import urandom
from threading import Thread
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import backend

def start():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = urandom(24)
    socketio = SocketIO(app)

    @app.route("/")
    def index():
        return render_template("map.html", initial="★", colour="dodgerblue")

    @socketio.on("connect")
    def handle_connect():
        emit("decoder.get", backend.decoder.get())

    @socketio.on("lookup.airline")
    def handle_airline_info_query(callsign):
        emit("lookup.airline", backend.lookup.airline(callsign))

    @socketio.on("lookup.aircraft")
    def handle_aircraft_info_query(address):
        emit("lookup.aircraft", backend.lookup.aircraft(address))

    @socketio.on("lookup.airport")
    def handle_airport_info_query(code, request=None):
        airport = backend.lookup.airport(code)
        airport["request"] = request
        emit("lookup.airport", airport)

    @socketio.on("lookup.route")
    def handle_route_info_query(callsign):
        emit("lookup.route", backend.lookup.route(callsign))

    @socketio.on("lookup.add_route")
    def handle_add_route_query(callsign, origin, destination):
        print(callsign, origin, destination)
        if origin:
            origin_icao = backend.lookup.airport(origin)["ICAO code"]
            backend.lookup.add_route(callsign, origin_icao)
        if destination:
            destination_icao = backend.lookup.airport(destination)["ICAO code"]
            backend.lookup.add_route(callsign, None, destination_icao)

    @socketio.on("lookup.all")
    def handle_all_info_query(aircraft_address, callsign):
        info = {}
        info["airline"] = backend.lookup.airline(callsign)
        info["aircraft"] = backend.lookup.aircraft(aircraft_address)
        info["callsign"] = callsign

        route = backend.lookup.route(callsign)
        if route:
            info["origin"] = backend.lookup.airport(route["Origin"]) if "Origin" in route else None
            info["destination"] = backend.lookup.airport(route["Destination"]) if "Destination" in route else None
        else:
            info["origin"] = info["destination"] = None

        emit("lookup.all", info)

    @socketio.on("jetphotos.thumb")
    def handle_thumb_jetphotos_query(tail):
        emit("jetphotos.thumb", {"url": backend.jetphotos.thumb(tail), "tail": tail})

    @socketio.on("disconnect")
    def handle_disconnect():
        print("Client disconnected")

    socket_thread = Thread(target=socketio.run, args=(app, "0.0.0.0", 5001))
    socket_thread.start()

if __name__ == "__main__":
    start()
