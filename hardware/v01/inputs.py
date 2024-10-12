import time

sensor1_counter = 0
sensor2_counter = 0
TRAFFIC_THRESHOLD = 2
COUNT_THRESHOLD = 0.2

sensor1_high_start = None
sensor2_high_start = None

def is_labeling_machine_working():
    return labeling_working.is_pressed

def is_labeling_machine_in_alarm():
    return labeling_alarm.is_pressed

def is_labeling_machine_alarm_handled():
    return labeling_alarm_handled.is_pressed

def is_filling_machine_working():
    return filling_working.is_pressed

def is_filling_machine_in_alarm():
    return filling_alarm.is_pressed

def is_filling_machine_alarm_handled():
    return filling_alarm_handled.is_pressed

def is_blowing_machine_working():
    return blowing_working.is_pressed

def is_blowing_machine_in_alarm():
    return blowing_alarm.is_pressed

def check_sensor1_traffic():
    global sensor1_high_start
    if sensor1.is_pressed:
        if sensor1_high_start is None:
            sensor1_high_start = time.time()
        elif time.time() - sensor1_high_start >= TRAFFIC_THRESHOLD:
            sensor1_high_start = None
            return True
    else:
        sensor1_high_start = None
    return False

def check_sensor2_traffic():
    global sensor2_high_start
    if sensor2.is_pressed:
        if sensor2_high_start is None:
            sensor2_high_start = time.time()
        elif time.time() - sensor2_high_start >= TRAFFIC_THRESHOLD:
            sensor2_high_start = None
            return True
    else:
        sensor2_high_start = None
    return False

def count_sensor1_bottle():
    global sensor1_counter
    if sensor1.is_pressed:
        time.sleep(COUNT_THRESHOLD)
        if not sensor1.is_pressed:
            sensor1_counter += 1
            print(f"Bottle counted on Sensor1: {sensor1_counter}")

def count_sensor2_bottle():
    global sensor2_counter
    if sensor2.is_pressed:
        time.sleep(COUNT_THRESHOLD)
        if not sensor2.is_pressed:
            sensor2_counter += 1
            print(f"Bottle counted on Sensor2: {sensor2_counter}")

def reset_counters():
    global sensor1_counter, sensor2_counter
    sensor1_counter = 0
    sensor2_counter = 0
    print("Bottle counters reset.")
