import RPi.GPIO as GPIO
import time
import Adafruit_DHT

# Init
GPIO.setmode(GPIO.BCM)
# Moisture sensor
GPIO.setup(18, GPIO.IN)
# Relay (water pump)
GPIO.setup(4, GPIO.OUT)
# Temperature and Humidity sensor
GPIO.setup(22, GPIO.IN)
sensor = Adafruit_DHT.DHT11

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, 22)
    moisture_value = GPIO.input(18)
    moisture_percentage = (moisture_value / 1023) * 100
    if moisture_percentage < 50:
        GPIO.output(4, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(4, GPIO.LOW)
        # Print the temperature and humidity values
        print("Temperature: " + str(temperature) + "C")
        print("Humidity: " + str(humidity) + "%")
        print("Moisture: " + str(moisture_percentage) + "%")
    else:
        time.sleep(1)
