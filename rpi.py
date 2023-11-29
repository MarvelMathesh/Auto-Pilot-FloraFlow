import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import serial

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
while True:
    # Read the moisture value from the serial communication with the Arduino
    if ser.inWaiting():
        data = ser.readline().decode('utf-8')  # Read the data from the Arduino and convert it to an integer
        if data.startswith('Soil Val: '):
            moisture_percentage = int(data.split('Soil Val: ')[1])

    # Read the temperature and humidity from the DHT11 sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor, 22)

    # Check if the soil moisture is below the threshold (50%)
    if moisture_percentage < 50:
        # Turn on the water pump
        GPIO.output(4, GPIO.HIGH)
        time.sleep(2)
    else:
        # Turn off the water pump
        GPIO.output(4, GPIO.LOW)

    # Print the temperature, humidity, and moisture percentage values
    print("Temperature: " + str(temperature) + "C")
    print("Humidity: " + str(humidity) + "%")
    print("Moisture: " + str(moisture_percentage) + "%")

    # Wait for 5 second before checking again
    time.sleep(5)

ser.close()  # Close the serial communication with the Arduino
