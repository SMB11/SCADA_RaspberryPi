import time
import tkinter as tk
import logging
from gpiozero import Button
from control import start_labeling_machine, stop_labeling_machine, start_filling_machine, stop_filling_machine, start_blowing_machine, stop_blowing_machine

# Initialize counters and traffic thresholds
sensor1_counter = 0
sensor2_counter = 0
TRAFFIC_THRESHOLD = 2  # Time in seconds to consider traffic
sensor1_traffic = False
sensor2_traffic = False

# Configure logging
logging.basicConfig(filename='machine_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Define GPIO pins directly for sensors and machine statuses
sensor1 = Button(13, pull_up=True)
sensor2 = Button(26, pull_up=True)
labeling_working = Button(20, pull_up=True)
labeling_alarm = Button(19, pull_up=True)
filling_working = Button(16, pull_up=True)
filling_alarm = Button(21, pull_up=True)
blowing_working = Button(18, pull_up=True)
blowing_alarm = Button(10, pull_up=True)
labeling_idle = Button(12, pull_up=True)  # GPIO for labeling idle status
filling_idle = Button(5, pull_up=True)   # GPIO for filling idle status

# Track previous states for logging only when a status change occurs
prev_labeling_status = None
prev_filling_status = None
prev_blowing_status = None
prev_labeling_idle = None
prev_filling_idle = None

# Function to check sensor and increment counter if necessary, with persistent traffic detection
def check_sensor(sensor, sensor_counter, high_start, traffic_flag):
    if sensor.is_pressed:
        if high_start is None:
            # New detection, increment counter and start traffic timer
            sensor_counter += 1
            traffic_flag = False  # Reset traffic on new count
            logging.info(f"{sensor.pin} detected - Counter: {sensor_counter}")
            time.sleep(0.2)  # Debounce
            return sensor_counter, time.time(), traffic_flag
        elif time.time() - high_start >= TRAFFIC_THRESHOLD:
            # Keep traffic detected until sensor goes low
            if not traffic_flag:
                logging.info(f"Traffic detected on {sensor.pin}")
            traffic_flag = True
            return sensor_counter, high_start, traffic_flag
    else:
        if traffic_flag:
            logging.info(f"Traffic cleared on {sensor.pin}")
        # Sensor is released, clear traffic
        traffic_flag = False
        return sensor_counter, None, traffic_flag

    return sensor_counter, high_start, traffic_flag

# Function to update counters, machine statuses, and traffic status
def update_gui():
    global sensor1_counter, sensor2_counter, sensor1_high_start, sensor2_high_start, sensor1_traffic, sensor2_traffic
    global prev_labeling_status, prev_filling_status, prev_blowing_status, prev_labeling_idle, prev_filling_idle
    
    sensor1_counter, sensor1_high_start, sensor1_traffic = check_sensor(sensor1, sensor1_counter, sensor1_high_start, sensor1_traffic)
    sensor2_counter, sensor2_high_start, sensor2_traffic = check_sensor(sensor2, sensor2_counter, sensor2_high_start, sensor2_traffic)

    # Log machine status changes only if there is a change
    
    current_labeling_alarm = labeling_alarm.is_pressed
    if current_labeling_alarm != prev_labeling_alarm:
        logging.info(f"Labeling Alarm: {'Active' if current_labeling_alarm else 'Inactive'}")
        prev_labeling_alarm = current_labeling_alarm  # Update previous state to current

    current_filling_alarm = filling_alarm.is_pressed
    if current_filling_alarm != prev_filling_alarm:
        logging.info(f"Filling Alarm: {'Active' if current_filling_alarm else 'Inactive'}")
        prev_filling_alarm = current_filling_alarm  # Update previous state to current

    
    current_labeling_status = labeling_working.is_pressed
    if current_labeling_status != prev_labeling_status:
        logging.info(f"Labeling Working: {'Active' if current_labeling_status else 'Inactive'}")
        prev_labeling_status = current_labeling_status

    current_filling_status = filling_working.is_pressed
    if current_filling_status != prev_filling_status:
        logging.info(f"Filling Working: {'Active' if current_filling_status else 'Inactive'}")
        prev_filling_status = current_filling_status

    current_blowing_status = blowing_working.is_pressed
    if current_blowing_status != prev_blowing_status:
        logging.info(f"Blowing Working: {'Active' if current_blowing_status else 'Inactive'}")
        prev_blowing_status = current_blowing_status

    # Log idle status changes only if there is a change
    current_labeling_idle = labeling_idle.is_pressed
    if current_labeling_idle != prev_labeling_idle:
        logging.info(f"Labeling Idle: {'Idle' if current_labeling_idle else 'Active'}")
        prev_labeling_idle = current_labeling_idle

    current_filling_idle = filling_idle.is_pressed
    if current_filling_idle != prev_filling_idle:
        logging.info(f"Filling Idle: {'Idle' if current_filling_idle else 'Active'}")
        prev_filling_idle = current_filling_idle

    # Update counter labels
    sensor1_label.config(text=f"Sensor1 Counter: {sensor1_counter}")
    sensor2_label.config(text=f"Sensor2 Counter: {sensor2_counter}")

    # Update traffic status labels
    sensor1_traffic_label.config(text=f"Sensor1 Traffic: {'Detected' if sensor1_traffic else 'Clear'}")
    sensor2_traffic_label.config(text=f"Sensor2 Traffic: {'Detected' if sensor2_traffic else 'Clear'}")

    # Update machine status labels
    labeling_status_label.config(text=f"Labeling Working: {'Active' if labeling_working.is_pressed else 'Inactive'}")
    labeling_alarm_label.config(text=f"Labeling Alarm: {'Active' if labeling_alarm.is_pressed else 'Inactive'}")
    filling_status_label.config(text=f"Filling Working: {'Active' if filling_working.is_pressed else 'Inactive'}")
    filling_alarm_label.config(text=f"Filling Alarm: {'Active' if filling_alarm.is_pressed else 'Inactive'}")
    blowing_status_label.config(text=f"Blowing Working: {'Active' if blowing_working.is_pressed else 'Inactive'}")
    blowing_alarm_label.config(text=f"Blowing Alarm: {'Active' if blowing_alarm.is_pressed else 'Inactive'}")

    # Update idle status labels
    labeling_idle_label.config(text=f"Labeling Idle: {'Idle' if labeling_idle.is_pressed else 'Inactive'}")
    filling_idle_label.config(text=f"Filling Idle: {'Idle' if filling_idle.is_pressed else 'Inactive'}")

    # Schedule the next update
    root.after(100, update_gui)

# Function to reset the counters
def reset_counters():
    global sensor1_counter, sensor2_counter
    sensor1_counter = 0
    sensor2_counter = 0
    sensor1_label.config(text=f"Sensor1 Counter: {sensor1_counter}")
    sensor2_label.config(text=f"Sensor2 Counter: {sensor2_counter}")
    logging.info("Counters reset")

# Initialize GUI
root = tk.Tk()
root.title("Bottling Line Control System")

# Labels for displaying counter values
sensor1_label = tk.Label(root, text=f"Sensor1 Counter: {sensor1_counter}")
sensor1_label.pack()
sensor2_label = tk.Label(root, text=f"Sensor2 Counter: {sensor2_counter}")
sensor2_label.pack()

# Labels for traffic status
sensor1_traffic_label = tk.Label(root, text="Sensor1 Traffic: Clear")
sensor1_traffic_label.pack()
sensor2_traffic_label = tk.Label(root, text="Sensor2 Traffic: Clear")
sensor2_traffic_label.pack()

# Labels for machine statuses
labeling_status_label = tk.Label(root, text="Labeling Working: Inactive")
labeling_status_label.pack()
labeling_alarm_label = tk.Label(root, text="Labeling Alarm: Inactive")
labeling_alarm_label.pack()
filling_status_label = tk.Label(root, text="Filling Working: Inactive")
filling_status_label.pack()
filling_alarm_label = tk.Label(root, text="Filling Alarm: Inactive")
filling_alarm_label.pack()
blowing_status_label = tk.Label(root, text="Blowing Working: Inactive")
blowing_status_label.pack()
blowing_alarm_label = tk.Label(root, text="Blowing Alarm: Inactive")
blowing_alarm_label.pack()

# Labels for idle statuses
labeling_idle_label = tk.Label(root, text="Labeling Idle: Inactive")
labeling_idle_label.pack()
filling_idle_label = tk.Label(root, text="Filling Idle: Inactive")
filling_idle_label.pack()

# Buttons for controlling the machines
tk.Button(root, text="Start Labeling", command=start_labeling_machine).pack()
tk.Button(root, text="Stop Labeling", command=stop_labeling_machine).pack()
tk.Button(root, text="Start Filling", command=start_filling_machine).pack()
tk.Button(root, text="Stop Filling", command=stop_filling_machine).pack()
tk.Button(root, text="Start Blowing", command=start_blowing_machine).pack()
tk.Button(root, text="Stop Blowing", command=stop_blowing_machine).pack()

# Button to reset counters
tk.Button(root, text="Reset Counters", command=reset_counters).pack()

# Start the GUI update loop
sensor1_high_start = None
sensor2_high_start = None
update_gui()

# Run the GUI event loop
root.mainloop()
