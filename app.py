from flask import Flask, render_template
from flask_socketio import SocketIO
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import serial
import re
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)

# Open serial communication with the Arduino to receive moisture value
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Open serial communication with the Arduino

# Set GPIO pin numbering mode and set GPIO pins for moisture sensor, relay, and temperature/humidity sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)  # Relay
GPIO.setup(22, GPIO.IN)  # Temperature/humidity sensor

# Define the sensor type as DHT11
sensor = Adafruit_DHT.DHT11
moisture_percentage = 0
pump_status = False  # Initialize pump status
pump_trigger = 60  # Default pump trigger level
moisture_history = []

def read_sensor_data():
    global moisture_percentage

    # Read the moisture value from the serial communication with the Arduino
    if ser.inWaiting():
        data = ser.readline().decode('utf-8')
        match = re.search(r"Soil Val: (\d+)", data)
        if match:
            moisture_percentage = int(match.group(1))

    # Read the temperature and humidity from the DHT11 sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor, 22)

    # Update moisture history
    moisture_history.append(moisture_percentage)
    if len(moisture_history) > 10:  # Keep only the last 10 data points for the graph
        moisture_history.pop(0)

    return temperature, humidity, moisture_percentage

def control_water_pump():
    global pump_status
    if moisture_percentage < pump_trigger:
        # Turn on the water pump
        GPIO.output(4, GPIO.HIGH)
        pump_status = True
    else:
        # Turn off the water pump
        GPIO.output(4, GPIO.LOW)
        pump_status = False

def background_thread():
    while True:
        temperature, humidity, moisture = read_sensor_data()
        control_water_pump()
        socketio.emit('sensor_update', {'temperature': temperature, 'humidity': humidity, 'moisture': moisture})
        socketio.emit('pump_status', {'pump_status': pump_status})
        socketio.emit('moisture_history', {'moisture_history': moisture_history})
        time.sleep(5)  # Update every 5 seconds

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    Thread(target=background_thread).start()

@socketio.on('set_pump_trigger')
def handle_set_pump_trigger(data):
    global pump_trigger
    pump_trigger = int(data['pump_trigger'])

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
