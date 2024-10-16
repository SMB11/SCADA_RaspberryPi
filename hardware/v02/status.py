import time
import logging
from gpiozero import Button
from control import stop_filling_machine, stop_labeling_machine

# Define GPIO pins for sensors and statuses
sensor1 = Button(13, pull_up=True)
sensor2 = Button(26, pull_up=True)
labeling_working = Button(20, pull_up=True)
labeling_alarm = Button(19, pull_up=True)
filling_working = Button(16, pull_up=True)
filling_alarm = Button(21, pull_up=True)
blowing_working = Button(18, pull_up=True)
blowing_alarm = Button(10, pull_up=True)
labeling_idle = Button(12, pull_up=True)
filling_idle = Button(5, pull_up=True)

last_bottle_time = time.time()  # Track the last time a bottle was detected
labeling_timeout = 5  # Default timeout in seconds, adjustable via the GUI

def initialize_logging():
    logging.basicConfig(filename='machine_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def check_sensor(sensor, sensor_counter, traffic_flag):
    high_start = None
    if sensor.is_pressed:
        global last_bottle_time
        last_bottle_time = time.time()  # Update last detected bottle time
        if high_start is None:
            sensor_counter += 1
            logging.info(f"{sensor.pin} detected - Counter: {sensor_counter}")
            time.sleep(0.2)
            high_start = time.time()
        elif time.time() - high_start >= 2:  # TRAFFIC_THRESHOLD
            traffic_flag = True
            logging.info(f"Traffic detected on {sensor.pin}")
    else:
        if traffic_flag:
            logging.info(f"Traffic cleared on {sensor.pin}")
        traffic_flag = False
    return sensor_counter, traffic_flag

def check_auto_mode(auto_mode_enabled, stop_filling_for_traffic, sensor1_traffic, stop_labeling_for_traffic, sensor2_traffic):
    global last_bottle_time
    if auto_mode_enabled:
        current_time = time.time()

        if stop_filling_for_traffic and sensor1_traffic:
            logging.info("Auto mode: Stopping filling machine due to traffic near Sensor1")
            stop_filling_machine()

        if stop_labeling_for_traffic and sensor2_traffic:
            logging.info("Auto mode: Stopping labeling machine due to traffic near Sensor2")
            stop_labeling_machine()

        # Stop labeling if no bottles have passed sensor1 within the specified timeout
        if labeling_working.is_pressed and (current_time - last_bottle_time) >= labeling_timeout:
            logging.info("Auto mode: Stopping labeling machine due to inactivity near Sensor1")
            stop_labeling_machine()

def set_auto_mode(enabled):
    logging.info(f"Auto mode {'enabled' if enabled else 'disabled'}")

def set_labeling_timeout(value):
    global labeling_timeout
    labeling_timeout = value
    logging.info(f"Labeling timeout set to {labeling_timeout} seconds")

def reset_counters():
    logging.info("Counters reset")