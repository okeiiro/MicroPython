import network
import time
from umqtt.simple import MQTTClient
import machine

# Replace with your Wi-Fi credentials
SSID = "ALHN-A839_plus"
PASSWORD = "7588176552"

# MQTT Broker details
BROKER = "192.168.1.68"  # Replace with the broker's IP address
TOPIC = b"sensor/ph"  # Topic to subscribe to

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# Wait for the connection to the Wi-Fi network
while not wlan.isconnected():
    print("Connecting to Wi-Fi...")
    time.sleep(1)
print("Connected to Wi-Fi")
print("IP Address:", wlan.ifconfig()[0])

# Initialize the ADC for the temperature sensor
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)  # ADC to voltage conversion factor

# Connect to the MQTT broker
client = MQTTClient("pico_pub",BROKER)

try:
    client.connect()
    print("Connected to MQTT broker")
except OSError as e:
    print(f"Failed to connect to MQTT broker: {e}")
    while True:
        time.sleep(1)  # Wait indefinitely in case of a connection error
    # or handle reconnect logic here

# Function to read temperature from the onboard sensor
def read_temperature():
    reading = sensor_temp.read_u16() * conversion_factor
    # Convert voltage reading to temperature in Celsius
    temperature_c = 27 - (reading - 0.706)/0.001721
    return temperature_c

# Function to get a formatted timestamp
def get_timestamp():
    t = time.localtime()
    return "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(t[0], t[1], t[2], t[3], t[4], t[5])

# Publish temperature data every 5 seconds
try:
    while True:
        temperature = read_temperature()
        timestamp = get_timestamp()
        message = f"{{\"temperature\": {temperature:.2f}, \"timestamp\": \"{timestamp}\"}}"
        client.publish(TOPIC, message)
        print(f"Published: {message}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Disconnected from broker")
    client.disconnect()

