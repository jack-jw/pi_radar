# Piradar
# server.py

"""
Control the HTTP server

Functions:
    start()
"""

from os import urandom
from threading import Thread
from flask import Flask, render_template
from flask_socketio import SocketIO#, emit
import backend

def start():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = urandom(24)
    socketio = SocketIO(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/map')
    def map():
        return render_template('map.html')

    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('info')
    def handle_aircraft_info_query(address):
        emit('info', backend.lookup.aircraft(address))

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    socket_thread = Thread(target=socketio.run, args=(app, 'localhost', 5001))
    #socket_thread.daemon = True
    socket_thread.start()

if __name__ == "__main__":
    start()
