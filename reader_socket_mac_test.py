from flask import Flask, render_template
from flask_socketio import emit, SocketIO
import os
from time import sleep
from concurrent.futures import ThreadPoolExecutor

# DOCS https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
executor = ThreadPoolExecutor(2)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getpid()
socketio_server = SocketIO(app, message_queue='amqp://localhost/entry')
socketio_client = SocketIO(message_queue='amqp://localhost/entry')

def send_code(message):
    print('Sending code: ' + message)
    socketio_client.emit('rfid', message)

@app.route('/')
def hello_world():
    return render_template('rfid_test.html')

@app.route('/test')
def emit_test():
    send_code('yee')
    return 'sent'

def run_background_reader():
    i = 0
    while True:
        i += 1
        print('plutty' + str(i))
        send_code('plutty' + str(i))
        sleep(1)

def run_server():
    if __name__ == '__main__':
        socketio_server.run(app)

def init():
    executor.submit(run_background_reader)
    executor.submit(run_server)

init()
