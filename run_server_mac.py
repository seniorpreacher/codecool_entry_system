import os
from app import app
from flask import render_template, request
from flask_socketio import emit, SocketIO
from time import sleep
#from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import reader_mac

# DOCS https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
#executor = ThreadPoolExecutor(2)
#app.config['SECRET_KEY'] = os.getpid()
socketio = SocketIO(app)
thread = None
client = None

def send_code(message):
    global client
    print("-- Emitting card id: " + message)
    print(client)
    if client:
        client.emit('rfid', message,  broadcast=True)
    #socketio.emit('rfid', message)

#@app.route('/')
#def hello_world():
#    return render_template('rfid_test.html')

#@app.route('/test')
#def emit_test():
#    send_code('yee')
#    return 'sent'

def run_background_reader():
    #sleep(2)
    #i = 0
    reader_mac.read_data_of_available_device(send_code)
    #while True:

    #    i += 1
    #    print('plutty' + str(i))
    #    send_code('plutty' + str(i))
    #    sleep(1)
#    return 'sent'

def run_background_reader2(sender_func):
    sleep(1)
    i = 0
    while not input("brekk"):
        i += 1
        sender_func('plutty' + str(i))
        #sleep(1)

@socketio.on('connect')
def on_connect():
    global client
    client = request
    print(client)

def run_server():
    global thread
    if __name__ == '__main__':
        if thread is None:
            thread = Thread(target=run_background_reader2, args=(send_code,))
            thread.start()
        socketio.run(app, debug=False)
#def init():
#    executor.submit(run_server)
    #executor.submit(run_background_reader)

#init()
try:
    run_server()
except KeyboardInterrupt as e:
    exit()
