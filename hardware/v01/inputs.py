import time
# Define counters for Sensor1 and Sensor2
sensor1_counter = 0
sensor2_counter = 0

sensor1_high_start = None
sensor2_high_start = None


TRAFFIC_THRESHOLD = 2  # Adjust this value as needed
COUNT_THRESHOLD = 0.2  # Time in seconds for detecting a passing bottle


def is_labeling_machine_working(GPIO, LABELING_WORKING_PIN):
    return GPIO.input(LABELING_WORKING_PIN)

def is_labeling_machine_in_alarm(GPIO, LABELING_ALARM_PIN):
    return GPIO.input(LABELING_ALARM_PIN)

def is_labeling_machine_alarm_handled(GPIO, LABELING_ALARM_HANDLED_PIN):
    return GPIO.input(LABELING_ALARM_HANDLED_PIN)

def is_filling_machine_working(GPIO, FILLING_WORKING_PIN):
    return GPIO.input(FILLING_WORKING_PIN)

def is_filling_machine_in_alarm(GPIO, FILLING_ALARM_PIN):
    return GPIO.input(FILLING_ALARM_PIN)

def is_filling_machine_alarm_handled(GPIO, FILLING_ALARM_HANDLED_PIN):
    return GPIO.input(FILLING_ALARM_HANDLED_PIN)

def is_blowing_machine_working(GPIO, BLOWING_WORKING_PIN):
    return GPIO.input(BLOWING_WORKING_PIN)

def is_blowing_machine_in_alarm(GPIO, BLOWING_ALARM_PIN):
    return GPIO.input(BLOWING_ALARM_PIN)

def is_sensor1_triggered(GPIO, SENSOR1_PIN):
    return GPIO.input(SENSOR1_PIN)

def is_sensor2_triggered(GPIO, SENSOR2_PIN):
    return GPIO.input(SENSOR2_PIN)


def check_sensor1_traffic(GPIO, SENSOR1_PIN):
    global sensor1_high_start
    if GPIO.input(SENSOR1_PIN) == GPIO.HIGH:
        if sensor1_high_start is None:
            sensor1_high_start = time.time()
        elif time.time() - sensor1_high_start >= TRAFFIC_THRESHOLD:
            sensor1_high_start = None  # Reset after detecting traffic
            return True
    else:
        sensor1_high_start = None  # Reset if sensor goes low
    return False

def check_sensor2_traffic(GPIO, SENSOR2_PIN):
    global sensor2_high_start
    if GPIO.input(SENSOR2_PIN) == GPIO.HIGH:
        if sensor2_high_start is None:
            sensor2_high_start = time.time()
        elif time.time() - sensor2_high_start >= TRAFFIC_THRESHOLD:
            sensor2_high_start = None  # Reset after detecting traffic
            return True
    else:
        sensor2_high_start = None  # Reset if sensor goes low
    return False

def count_sensor1_bottle(GPIO, SENSOR1_PIN):
    global sensor1_counter
    if GPIO.input(SENSOR1_PIN) == GPIO.HIGH:
        time.sleep(COUNT_THRESHOLD)  # Ensure it's a passing bottle
        if GPIO.input(SENSOR1_PIN) == GPIO.LOW:
            sensor1_counter += 1
            print(f"Bottle counted on Sensor1: {sensor1_counter}")

def count_sensor2_bottle(GPIO, SENSOR2_PIN):
    global sensor2_counter
    if GPIO.input(SENSOR2_PIN) == GPIO.HIGH:
        time.sleep(COUNT_THRESHOLD)  # Ensure it's a passing bottle
        if GPIO.input(SENSOR2_PIN) == GPIO.LOW:
            sensor2_counter += 1
            print(f"Bottle counted on Sensor2: {sensor2_counter}")

def reset_counters():
    global sensor1_counter, sensor2_counter
    sensor1_counter = 0
    sensor2_counter = 0
    print("Bottle counters reset.")





