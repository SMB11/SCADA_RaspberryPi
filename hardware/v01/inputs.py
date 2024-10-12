import time

# Bottle counters
sensor1_counter = 0
sensor2_counter = 0
TRAFFIC_THRESHOLD = 2

# Working bottle counting with events
def sensor1_detected():
    global sensor1_counter
    sensor1_counter += 1
    print(f"Sensor 1: Bottle count = {sensor1_counter}")

def sensor2_detected():
    global sensor2_counter
    sensor2_counter += 1
    print(f"Sensor 2: Bottle count = {sensor2_counter}")

# Check traffic using current sensor state and timestamp
def check_traffic(sensor, sensor_name):
    if sensor.is_pressed:
        start_time = time.time()
        while sensor.is_pressed:
            if time.time() - start_time >= TRAFFIC_THRESHOLD:
                print(f"Traffic detected on {sensor_name}")
                return True
    return False

# Initialize sensors with working setup
def initialize_sensor_events():
    SENSOR1_PIN.when_pressed = sensor1_detected
    SENSOR2_PIN.when_pressed = sensor2_detected

# Reset counters
def reset_counters():
    global sensor1_counter, sensor2_counter
    sensor1_counter = 0
    sensor2_counter = 0
    print("Counters reset.")
