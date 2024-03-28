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
    def handle_airport_info_query(code, routing=None):
        airport = backend.lookup.airport(code)
        airport["routing"] = routing
        emit("lookup.airport", airport)

    @socketio.on("lookup.route")
    def handle_route_info_query(callsign):
        emit("lookup.route", backend.lookup.route(callsign))

    @socketio.on("lookup.add_origin")
    def handle_add_origin(callsign, origin):
        backend.lookup.add_origin(callsign, origin)

    @socketio.on("lookup.add_destination")
    def handle_add_destination(callsign, destination):
        backend.lookup.add_destination(callsign, destination)

    @socketio.on("lookup.all")
    def handle_all_info_query(aircraft_address, callsign):
        info = {}
        info["airline"] = backend.lookup.airline(callsign)
        info["aircraft"] = backend.lookup.aircraft(aircraft_address)
        info["callsign"] = callsign

        route = backend.lookup.route(callsign)
        # This is really messy but JS was annoying me so I had to solve it here
        if route:
            info["origin"] = backend.lookup.airport(route["origin"]) if "origin" in route else None
            info["destination"] = backend.lookup.airport(route["destination"]) if "destination" in route else None
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
    backend.lookup.check()
    start()
