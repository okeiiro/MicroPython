import network
import time
from umqtt.simple import MQTTClient
import machine
from machine import Pin, SPI, ADC,I2C
import sh1107
import gc
import sys
import framebuf
import array

# Replace with your Wi-Fi credentials
SSID = "00DLINK"
PASSWORD = "00000000"

# MQTT Broker details
BROKER = "192.168.1.104"  # Replace with the broker's IP address
TOPIC = b"tank1/pond123/ph/sensor456"  # Topic to subscribe to

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


# Connect to the MQTT broker
client = MQTTClient("pico_pub", BROKER)
client.connect()



# init I2C (GPIO 2 for SDA and GPIO 3 for SCL)
i2c = I2C(1, scl=Pin(3), sda=Pin(2))

# address of the pH sensor of Atlas Scientific
ph_sensor_address = 0x63


# Initialize SPI
spi1 = SPI(1, baudrate=1_000_000, sck=Pin(14), mosi=Pin(15), miso=Pin(12))
print('SPI created: {} bytes free'.format(gc.mem_free()))

# Initialize the display
display = sh1107.SH1107_SPI(128, 64, spi1, dc=Pin(21), res=Pin(20), cs=Pin(13))
print('Display created: {} bytes free'.format(gc.mem_free()))



def read_values_ph():
    try:
        # send command to pH sensor to request reading from it
        i2c.writeto(ph_sensor_address, b'R')
        
        # wait for the sensor to process the command
        time.sleep(2)
        
        result = i2c.readfrom(ph_sensor_address, 7)
        
        # Decode bytes and remove non-printable characters
        decoded_result = result.decode('utf-8')
        cleaned_result = decoded_result.replace('\x01', '')
        
        # Strip any remaining unwanted whitespace (just character handling)
        pH_value = cleaned_result.strip()
        
        return pH_value
    
    except Exception as e:
        print("Error reading pH value:", e)
        return None

  

# Publish pH data and display it on OLED screen every 2 seconds
try:
    while True:
        pH = read_values_ph()
        display.sleep(False)
        display.fill(0)
        display.text('pH: ', 0, 0, 1)
        display.text(''+str(pH),0,20,1)
        message = f"{{\"pH\": {pH:.2f}\"}}"
        client.publish(TOPIC, message)
        print(f"Published: {message}")
        time.sleep(2)
        display.show
        
except KeyboardInterrupt:
    print("Disconnected from broker")
    client.disconnect()




