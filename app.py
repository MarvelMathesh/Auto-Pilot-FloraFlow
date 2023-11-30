from flask import Flask, render_template
from flask_socketio import SocketIO
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import serial
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)

# Open serial communication with the Arduino to receive moisture value
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Open serial communication with the Arduino

# Set GPIO pin numbering mode and set GPIO pins for moisture sensor, relay, and temperature/humidity sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)  # Moisture sensor
GPIO.setup(4, GPIO.OUT)  # Relay
GPIO.setup(22, GPIO.IN)  # Temperature/humidity sensor

# Define the sensor type as DHT11
sensor = Adafruit_DHT.DHT11
moisture_percentage = 0
pump_status = False  # Initialize pump status

def read_sensor_data():
    global moisture_percentage
    # Read the moisture value from the serial communication with the Arduino
    if ser.inWaiting():
        data = ser.readline().decode('utf-8')  # Read the data from the Arduino and convert it to an integer
        if data.startswith('Soil Val: '):
            moisture_percentage = int(data.split('Soil Val: ')[1])

    # Read the temperature and humidity from the DHT11 sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor, 22)

    return temperature, humidity, moisture_percentage

def control_water_pump():
    global pump_status
    if moisture_percentage < 50:
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
        time.sleep(5)  # Update every 5 seconds

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    Thread(target=background_thread).start()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
