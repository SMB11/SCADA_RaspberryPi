import time
import logging
from gpiozero import Button
from control import start_filling_machine, start_labeling_machine, stop_filling_machine, stop_labeling_machine, start_blowing_machine, stop_blowing_machine

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

# Define these global variables at the beginning of the file
sensor1_high_start = None
sensor2_high_start = None

# Tracking time and flags for conditions
last_bottle_time = time.time()
labeling_timeout = 5  # Default timeout in seconds, adjustable via the GUI
traffic_threshold_sensor1 = 2  # Default traffic threshold for Sensor1
traffic_threshold_sensor2 = 2  # Default traffic threshold for Sensor2

# Flags for machine stop conditions
labeling_stopped_due_to_timeout = False
filling_stopped_due_to_traffic = False
labeling_stopped_due_to_traffic = False

def initialize_logging():
    logging.basicConfig(filename='machine_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def check_sensor(sensor, sensor_counter, traffic_flag, sensor_number):
    global sensor1_high_start, sensor2_high_start, last_bottle_time

    # Set sensor-specific high_start variable and threshold
    if sensor_number == 1:
        high_start = sensor1_high_start
        traffic_threshold = traffic_threshold_sensor1
    else:
        high_start = sensor2_high_start
        traffic_threshold = traffic_threshold_sensor2

    if sensor.is_pressed:
        # Update the last_bottle_time if Sensor1 is pressed
        if sensor_number == 1:
            last_bottle_time = time.time()  # Update time when bottle passes Sensor1

        # If first detection of high, initialize high start time
        if high_start is None:
            sensor_counter += 1  # Increment counter only when signal first goes high
            logging.info(f"Sensor{sensor_number} detected - Counter: {sensor_counter}")
            high_start = time.time()  # Record the time when traffic starts
            time.sleep(0.2)  # Debounce delay

        # Check if traffic has been sustained beyond threshold
        elif time.time() - high_start >= traffic_threshold and not traffic_flag:
            logging.info(f"Traffic detected on Sensor{sensor_number}")
            traffic_flag = True  # Set traffic flag
    else:
        # Reset traffic and high start when sensor is not pressed
        if traffic_flag:
            logging.info(f"Traffic cleared on Sensor{sensor_number}")
        traffic_flag = False
        high_start = None  # Reset high start

    # Update the sensor-specific high start variable
    if sensor_number == 1:
        sensor1_high_start = high_start
    else:
        sensor2_high_start = high_start

    return sensor_counter, traffic_flag

def check_auto_mode(auto_mode_enabled, stop_filling_for_traffic, sensor1_traffic, stop_labeling_for_traffic, sensor2_traffic, stop_labeling_for_timeout):
    global last_bottle_time, labeling_stopped_due_to_timeout, filling_stopped_due_to_traffic, labeling_stopped_due_to_traffic
    current_time = time.time()

    if auto_mode_enabled:
        # 1. Control the Filling Machine based on Sensor1 traffic
        if stop_filling_for_traffic:
            if sensor1_traffic and not filling_stopped_due_to_traffic:
                logging.info("Auto mode: Stopping filling machine due to traffic near Sensor1")
                stop_filling_machine()
                filling_stopped_due_to_traffic = True
            elif not sensor1_traffic and filling_stopped_due_to_traffic:
                logging.info("Auto mode: Restarting filling machine as traffic near Sensor1 is cleared")
                start_filling_machine()
                filling_stopped_due_to_traffic = False

        # 2. Control the Labeling Machine based on Sensor2 traffic
        if stop_labeling_for_traffic:
            if sensor2_traffic and not labeling_stopped_due_to_traffic:
                logging.info("Auto mode: Stopping labeling machine due to traffic near Sensor2")
                stop_labeling_machine()
                labeling_stopped_due_to_traffic = True

        # 3. Control the Labeling Machine based on Sensor1 inactivity timeout
        if stop_labeling_for_timeout and labeling_working.is_pressed and not sensor1_traffic:
            if (current_time - last_bottle_time) >= labeling_timeout and not labeling_stopped_due_to_timeout:
                logging.info("Auto mode: Stopping labeling machine due to inactivity near Sensor1")
                stop_labeling_machine()
                labeling_stopped_due_to_timeout = True

        # 4. Restart the labeling machine when conditions that caused it to stop are resolved
        if labeling_stopped_due_to_traffic and not sensor2_traffic:
            if not labeling_stopped_due_to_timeout or (current_time - last_bottle_time) < labeling_timeout:
                logging.info("Auto mode: Restarting labeling machine as traffic condition is resolved")
                start_labeling_machine()
                labeling_stopped_due_to_traffic = False

        if labeling_stopped_due_to_timeout and (current_time - last_bottle_time) < labeling_timeout:
            if not labeling_stopped_due_to_traffic or not sensor2_traffic:
                logging.info("Auto mode: Restarting labeling machine as timeout condition is resolved")
                start_labeling_machine()
                labeling_stopped_due_to_timeout = False

        # If both conditions caused the machine to stop, restart only when both are resolved
        if labeling_stopped_due_to_traffic and labeling_stopped_due_to_timeout:
            if not sensor2_traffic and (current_time - last_bottle_time) < labeling_timeout:
                logging.info("Auto mode: Restarting labeling machine as both traffic and timeout conditions are resolved")
                start_labeling_machine()
                labeling_stopped_due_to_traffic = False
                labeling_stopped_due_to_timeout = False

def set_auto_mode(enabled):
    logging.info(f"Auto mode {'enabled' if enabled else 'disabled'}")

def set_labeling_timeout(value):
    global labeling_timeout
    labeling_timeout = value
    logging.info(f"Labeling timeout set to {labeling_timeout} seconds")

def set_traffic_threshold_sensor1(value):
    global traffic_threshold_sensor1
    traffic_threshold_sensor1 = value
    logging.info(f"Traffic threshold for Sensor1 set to {traffic_threshold_sensor1} seconds")

def set_traffic_threshold_sensor2(value):
    global traffic_threshold_sensor2
    traffic_threshold_sensor2 = value
    logging.info(f"Traffic threshold for Sensor2 set to {traffic_threshold_sensor2} seconds")

def reset_counters():
    logging.info("Counters reset")
