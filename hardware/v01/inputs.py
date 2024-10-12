import time
from gpio_setup import sensor1, sensor2

# Initialize counters and threshold
sensor1_counter = 0
sensor2_counter = 0
TRAFFIC_THRESHOLD = 2  # Time in seconds to consider traffic

def check_sensor1():
    global sensor1_counter
    if sensor1.is_pressed:
        sensor1_counter += 1
        print(f"Sensor1 count: {sensor1_counter}")
        time.sleep(0.1)  # Debounce delay

def check_sensor2():
    global sensor2_counter
    if sensor2.is_pressed:
        sensor2_counter += 1
        print(f"Sensor2 count: {sensor2_counter}")
        time.sleep(0.1)  # Debounce delay

def detect_traffic(sensor, high_start):
    if sensor.is_pressed:
        if high_start is None:
            return time.time()
        elif time.time() - high_start >= TRAFFIC_THRESHOLD:
            print("Traffic detected!")
            return None  # Reset after detection
    else:
        return None
    return high_start

def reset_counters():
    global sensor1_counter, sensor2_counter
    sensor1_counter = 0
    sensor2_counter = 0
    print("Counters reset.")
