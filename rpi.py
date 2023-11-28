import RPi.GPIO as GPIO
import time
import Adafruit_DHT

# Set GPIO pin numbering mode and set GPIO pins for moisture sensor, relay, and temperature/humidity sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)  # Moisture sensor
GPIO.setup(4, GPIO.OUT)  # Relay
GPIO.setup(22, GPIO.IN)  # Temperature/humidity sensor

# Define the sensor type as DHT11
sensor = Adafruit_DHT.DHT11

while True:
    # Read the temperature and humidity from the DHT11 sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor, 22)

    # Read the analog moisture sensor value
    moisture_value = GPIO.input(18)  # Read digital value from moisture sensor

    # Check if the soil moisture has water content
    if moisture_value == 0:
        # Turn on the water pump
        GPIO.output(4, GPIO.HIGH)
        time.sleep(3)
    else:
        # Turn off the water pump
        GPIO.output(4, GPIO.LOW)

    # Print the temperature, humidity, and moisture percentage values
    print("Temperature: " + str(temperature) + "C")
    print("Humidity: " + str(humidity) + "%")

    # Wait for 1 second before checking again
    time.sleep(1)
