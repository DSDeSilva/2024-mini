Exercise 1:
max_bright value was 5315. 
min_bright value was 22485.

Exercise 2:

Exercise 3:
Part 1:
You missed the light 2 / 10 times
Average response time: 263.375 ms
Minimum response time: 229 ms
Maximum response time: 344 ms
[247, 280, 344, 233, 267, 262, 245, 229]


Code to connect raspberry pi to wifi:

import network

ssid = "BU Guest (unencrypted)"  # Replace with your Wi-Fi SSID
password = ""  # Replace with your Wi-Fi password

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    pass  # Wait until the connection is established

print("Connected to Wi-Fi")
print(wlan.ifconfig())  # This will print the Pico's IP address
