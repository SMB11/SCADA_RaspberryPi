import time
import logging
from gpiozero import Button
from control import start_filling_machine, start_labeling_machine, stop_filling_machine, stop_labeling_machine

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
traffic_threshold = 2  # Default traffic threshold, adjustable via the GUI
# Add a flag to track whether the labeling machine was stopped due to timeout

labeling_stopped_due_to_timeout = False
def initialize_logging():
    logging.basicConfig(filename='machine_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def check_sensor(sensor, sensor_counter, traffic_flag, traffic_threshold):
    high_start = None
    if sensor.is_pressed:
        global last_bottle_time
        last_bottle_time = time.time()  # Update last detected bottle time
        if high_start is None:
            sensor_counter += 1
            logging.info(f"{sensor.pin} detected - Counter: {sensor_counter}")
            time.sleep(0.2)
            high_start = time.time()
        elif time.time() - high_start >= traffic_threshold:  # Use traffic threshold here
            traffic_flag = True
            logging.info(f"Traffic detected on {sensor.pin}")
    else:
        if traffic_flag:
            logging.info(f"Traffic cleared on {sensor.pin}")
        traffic_flag = False
    return sensor_counter, traffic_flag

def check_auto_mode(auto_mode_enabled, stop_filling_for_traffic, sensor1_traffic, stop_labeling_for_traffic, sensor2_traffic, stop_labeling_for_timeout):
    global last_bottle_time
    if auto_mode_enabled:
        current_time = time.time()

        # Stop and restart filling machine based on Sensor1 traffic
        if stop_filling_for_traffic:
            if sensor1_traffic:
                logging.info("Auto mode: Stopping filling machine due to traffic near Sensor1")
                stop_filling_machine()
            else:
                logging.info("Auto mode: Restarting filling machine as traffic near Sensor1 is cleared")
                start_filling_machine()

        # Stop and restart labeling machine based on Sensor2 traffic
        if stop_labeling_for_traffic:
            if sensor2_traffic:
                logging.info("Auto mode: Stopping labeling machine due to traffic near Sensor2")
                stop_labeling_machine()
            else:
                logging.info("Auto mode: Restarting labeling machine as traffic near Sensor2 is cleared")
                start_labeling_machine()

        # Stop labeling if enabled and no bottles have passed sensor1 within the specified timeout
        if stop_labeling_for_timeout:
            if labeling_working.is_pressed and (current_time - last_bottle_time) >= labeling_timeout:
                if not labeling_stopped_due_to_timeout:
                    logging.info("Auto mode: Stopping labeling machine due to inactivity near Sensor1")
                    stop_labeling_machine()
                    labeling_stopped_due_to_timeout = True  # Mark the machine as stopped due to timeout
            elif labeling_stopped_due_to_timeout and sensor1.is_pressed:
                # Restart only if the machine was stopped due to timeout and new bottles are passing
                logging.info("Auto mode: Restarting labeling machine after inactivity near Sensor1 resolved")
                start_labeling_machine()
                labeling_stopped_due_to_timeout = False  # Reset the flag after restarting
                
def set_auto_mode(enabled):
    logging.info(f"Auto mode {'enabled' if enabled else 'disabled'}")

def set_labeling_timeout(value):
    global labeling_timeout
    labeling_timeout = value
    logging.info(f"Labeling timeout set to {labeling_timeout} seconds")

def set_traffic_threshold(value):
    global traffic_threshold
    traffic_threshold = value
    logging.info(f"Traffic threshold set to {traffic_threshold} seconds")

def reset_counters():
    logging.info("Counters reset")