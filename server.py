from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from os import urandom
#import decoder

def run():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = urandom(24)
    socketio = SocketIO(app)

    @app.route('/')
    def index():
        return render_template('map.html')
        
    @socketio.on('refresh')
    def send_aircraft():
        #aircraft = decoder.get_aircraft()
        emit('aircraft', aircraft)

    socketio.run(app)
