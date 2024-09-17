
from machine import Pin
import time
import random
import json
import urequests  # MicroPython's requests library to send HTTP requests
import network



N: int = 10  # Now we do 10 flashes
sample_ms = 10.0
on_ms = 500

SSID = "Laptop"
Password = "password"
Key = "2A8W6P3T1W5WGJ6Z"
ThingspeakURL = "http://api.thingspeak.com/update"

def wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print("Connecting to", SSID)
    wlan.connect(SSID, Password)
    timeout = 10  # timeout in seconds
    start_time = time.time()
    while not wlan.isconnected():
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            print("Connection failed")
            return
        print("Connecting...")
        time.sleep(1)
    print("Connected to:", wlan.ifconfig())
    
def upload(AvgR, MinR, MaxR,status_message,score):
    try:
        url = f"{ThingspeakURL}?api_key={Key}&field1={AvgR}&field2={MinR}&field3={MaxR}&status={status_message}&field4={score}"
        print(f"Constructed URL: {url}")  # Debugging
        response = urequests.get(url)
        print(f"Response from ThingSpeak: {response.text}")
        response.close()
    except Exception as e:
        print(f"Error sending data to ThingSpeak: {e}")

        
def random_time_interval(tmin: float, tmax: float) -> float:
    """return a random time interval between max and min"""
    return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
    # Let user know game started / is over
    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)


'''def write_json(json_filename: str, data: dict) -> None:
    """Writes data to a JSON file."""
    with open(json_filename, "w") as f:
        json.dump(data, f)'''


def scorer(t: list[int | None]) -> dict:
    # Collate results
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]

    if t_good:
        avg_response = sum(t_good) / len(t_good)
        min_response = min(t_good)
        max_response = max(t_good)
    else:
        avg_response = min_response = max_response = None

    print(f"Average response time: {avg_response} ms")
    print(f"Minimum response time: {min_response} ms")
    print(f"Maximum response time: {max_response} ms")

    # Store the results in a dictionary
    data = {
        "misses": misses,
        "average_response_time": avg_response,
        "min_response_time": min_response,
        "max_response_time": max_response,
        "score": len(t_good) / len(t)  # Score: non-misses / total flashes
    }
    score = len(t_good) / len(t)

    return avg_response, min_response, max_response, data, score


'''def upload_data(data: dict) -> None:
    """Uploads the result to the Node.js server."""
    
    url = "http://10.193.85.151:3000/upload"  # Use your Node.js server IP and port
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = urequests.post(url, data=json.dumps(data), headers=headers)
        print("Data uploaded successfully:", response.text)
    except Exception as e:
        print("Failed to upload data:", e)'''


if __name__ == "__main__":
    # Initialize the LED and button
    wifi()
    led = Pin("LED", Pin.OUT)
    button = Pin(16, Pin.IN, Pin.PULL_UP)

    t: list[int | None] = []

    # Start the game with blinks
    blinker(3, led)

    # Collect response times for N flashes
    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))  # Random delay before the next flash

        led.high()
        tic = time.ticks_ms()
        t0 = None

        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:  # LED stays on for 'on_ms' ms
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()  # Turn off LED when the button is pressed
                break
        t.append(t0)  # Record response time or None if missed

        led.low()  # Ensure LED is off

    # End the game with blinks
    blinker(5, led)

    # Calculate results
    avg_response, min_response, max_response, data, score = scorer(t)

    '''# Save results to a JSON file
    now: tuple[int] = time.localtime()
    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    filename = f"score-{now_str}.json"
    write_json(filename, data)'''

    # Upload the data to your server
    #print("testtestest: ", avg_response)
    #test_upload()
    msg = f"Avgerage%20Response%20Time:%20{avg_response}%0AMinimum%20Response%20Time:%20{min_response}%0AMaximum%20Response%20Time:%20{max_response}%20Score:%20{score}"
    upload(avg_response, min_response, max_response,msg,score)

