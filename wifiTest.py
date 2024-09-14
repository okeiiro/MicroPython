import network
import time

# Replace these with your actual Wi-Fi credentials
SSID = "ALHN-A839_plus"
PASSWORD = "7588176552"

# Initialize the Wi-Fi interface
wlan = network.WLAN(network.STA_IF)

# Activate the interface
wlan.active(True)

# Attempt to connect to the Wi-Fi network
wlan.connect(SSID, PASSWORD)

# Wait for the connection to succeed or fail
max_wait = 10  # Number of seconds to wait before giving up
while max_wait > 0:
    if wlan.isconnected():
        break
    print('Waiting for connection...')
    time.sleep(1)
    max_wait -= 1

# Check if connected and print the result
if wlan.isconnected():
    print('Connected to Wi-Fi!')
    print('IP Address:', wlan.ifconfig()[0])
else:
    print('Failed to connect to Wi-Fi')

