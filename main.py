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
        return render_template("map.html", initial="J", colour="steelblue")

    @app.route("/map")
    def map():
        return render_template("map.html")

    @socketio.on("connect")
    def handle_connect():
        emit("decoder.get", backend.decoder.get())

    @socketio.on("lookup.airline")
    def handle_aircraft_info_query(callsign):
        emit("lookup.airline", backend.lookup.airline(callsign))

    @socketio.on("lookup.aircraft")
    def handle_aircraft_info_query(address):
        emit("lookup.aircraft", backend.lookup.aircraft(address))

    @socketio.on("lookup.airport")
    def handle_aircraft_info_query(code):
        emit("lookup.airport", backend.lookup.airport(code))

    @socketio.on("lookup.route")
    def handle_aircraft_info_query(callsign):
        emit("lookup.route", backend.lookup.route(callsign))
        
    @socketio.on("lookup.all")
    def handle_all_info_query(aircraft_address, callsign):
        info = {}
        info["airline"] = backend.lookup.airline(callsign)
        info["aircraft"] = backend.lookup.aircraft(aircraft_address)
        
        route = backend.lookup.route(callsign)

        if route:
            info["origin"] = backend.lookup.airport(route["Origin"])
            info["destination"] = backend.lookup.airport(route["Destination"])
        else:
            info["origin"] = info["destination"] = None

        emit("lookup.all", info)

    @socketio.on("disconnect")
    def handle_disconnect():
        print("Client disconnected")

    socket_thread = Thread(target=socketio.run, args=(app, "0.0.0.0", 5001))
    socket_thread.start()

if __name__ == "__main__":
    start()
