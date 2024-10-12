sensor1_counter = 0
sensor2_counter = 0
TRAFFIC_THRESHOLD = 2

def sensor1_detected():
    global sensor1_counter
    sensor1_counter += 1
    print(f"Sensor 1: Bottle count = {sensor1_counter}")

def sensor2_detected():
    global sensor2_counter
    sensor2_counter += 1
    print(f"Sensor 2: Bottle count = {sensor2_counter}")

def initialize_sensor_events():
    SENSOR1_PIN.when_pressed = sensor1_detected
    SENSOR2_PIN.when_pressed = sensor2_detected

def reset_counters():
    global sensor1_counter, sensor2_counter
    sensor1_counter = 0
    sensor2_counter = 0
    print("Counters reset.")
