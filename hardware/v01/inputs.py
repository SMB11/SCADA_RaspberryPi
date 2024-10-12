
import time

sensor1_counter = 0
sensor2_counter = 0

TRAFFIC_THRESHOLD = 2
COUNT_THRESHOLD = 0.2

def is_labeling_machine_working():
    return LABELING_WORKING_PIN.is_pressed

def is_labeling_machine_in_alarm():
    return LABELING_ALARM_PIN.is_pressed

def is_filling_machine_working():
    return FILLING_WORKING_PIN.is_pressed

def check_sensor1_traffic():
    start_time = time.time()
    while SENSOR1_PIN.is_pressed:
        if time.time() - start_time >= TRAFFIC_THRESHOLD:
            return True
    return False

def check_sensor2_traffic():
    start_time = time.time()
    while SENSOR2_PIN.is_pressed:
        if time.time() - start_time >= TRAFFIC_THRESHOLD:
            return True
    return False

def count_sensor1_bottle():
    global sensor1_counter
    if SENSOR1_PIN.is_pressed:
        time.sleep(COUNT_THRESHOLD)
        if not SENSOR1_PIN.is_pressed:
            sensor1_counter += 1
            print(f"Bottle counted on Sensor1: {sensor1_counter}")

def count_sensor2_bottle():
    global sensor2_counter
    if SENSOR2_PIN.is_pressed:
        time.sleep(COUNT_THRESHOLD)
        if not SENSOR2_PIN.is_pressed:
            sensor2_counter += 1
            print(f"Bottle counted on Sensor2: {sensor2_counter}")

def reset_counters():
    global sensor1_counter, sensor2_counter
    sensor1_counter = 0
    sensor2_counter = 0
    print("Bottle counters reset.")
