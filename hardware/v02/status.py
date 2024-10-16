import time
import logging
from gpiozero import Button

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

def initialize_logging():
    logging.basicConfig(filename='machine_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def check_sensor(sensor, sensor_counter, traffic_flag):
    high_start = None
    if sensor.is_pressed:
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

def check_auto_mode(auto_mode_enabled, stop_filling_for_traffic, sensor1_traffic):
    if auto_mode_enabled and stop_filling_for_traffic and sensor1_traffic:
        logging.info("Auto mode: Stopping filling machine due to traffic near Sensor1")
        stop_filling_machine()

def set_auto_mode(enabled):
    logging.info(f"Auto mode {'enabled' if enabled else 'disabled'}")

def reset_counters():
    logging.info("Counters reset")