import time
from gpio_setup import *

# Initialize counters and thresholds
sensor1_counter = 0
sensor2_counter = 0
TRAFFIC_THRESHOLD = 2  # Time in seconds to consider traffic

def check_sensor1():
    global sensor1_counter
    if sensor1.is_pressed:
        sensor1_counter += 1
        print(f"Sensor1 detected, count updated: {sensor1_counter}")
        time.sleep(0.1)  # Debounce

def check_sensor2():
    global sensor2_counter
    if sensor2.is_pressed:
        sensor2_counter += 1
        print(f"Sensor2 detected, count updated: {sensor2_counter}")
        time.sleep(0.1)  # Debounce

def detect_traffic(sensor, high_start, sensor_name):
    if sensor.is_pressed:
        if high_start is None:
            print(f"Starting traffic timer for {sensor_name}")
            return time.time()
        elif time.time() - high_start >= TRAFFIC_THRESHOLD:
            print(f"Traffic detected on {sensor_name}")
            return None  # Reset timer after detection
    else:
        return None  # Reset if sensor is not high
    return high_start

def reset_counters():
    global sensor1_counter, sensor2_counter
    sensor1_counter = 0
    sensor2_counter = 0
    print("Counters reset.")
