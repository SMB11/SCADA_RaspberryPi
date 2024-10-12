import time
import tkinter as tk
from gpiozero import Button
from control import start_labeling_machine, stop_labeling_machine, start_filling_machine, stop_filling_machine, start_blowing_machine, stop_blowing_machine

# Initialize counters and traffic thresholds
sensor1_counter = 0
sensor2_counter = 0
TRAFFIC_THRESHOLD = 2  # Time in seconds to consider traffic
sensor1_traffic = False
sensor2_traffic = False

# Define GPIO pins directly for sensors and machine statuses
sensor1 = Button(13, pull_up=True)
sensor2 = Button(26, pull_up=True)
labeling_working = Button(21, pull_up=True)
labeling_alarm = Button(19, pull_up=True)
filling_working = Button(16, pull_up=True)
filling_alarm = Button(5, pull_up=True)
blowing_working = Button(18, pull_up=True)
blowing_alarm = Button(10, pull_up=True)

# Function to check sensor and increment counter if necessary, with traffic detection
def check_sensor(sensor, sensor_counter, high_start):
    global sensor1_traffic, sensor2_traffic

    if sensor == sensor1:
        traffic_flag = sensor1_traffic
    else:
        traffic_flag = sensor2_traffic

    if sensor.is_pressed:
        if high_start is None:
            sensor_counter += 1
            traffic_flag = False  # Reset traffic flag on new count
            time.sleep(0.2)  # Debounce
            return sensor_counter, time.time(), traffic_flag
        elif time.time() - high_start >= TRAFFIC_THRESHOLD:
            traffic_flag = True  # Set traffic flag when threshold is exceeded
            return sensor_counter, None, traffic_flag
    else:
        return sensor_counter, None, False  # Reset traffic flag when sensor is not pressed
    return sensor_counter, high_start, traffic_flag

# Function to update counters, machine statuses, and traffic status
def update_gui():
    global sensor1_counter, sensor2_counter, sensor1_high_start, sensor2_high_start, sensor1_traffic, sensor2_traffic
    sensor1_counter, sensor1_high_start, sensor1_traffic = check_sensor(sensor1, sensor1_counter, sensor1_high_start)
    sensor2_counter, sensor2_high_start, sensor2_traffic = check_sensor(sensor2, sensor2_counter, sensor2_high_start)

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

    # Schedule the next update
    root.after(100, update_gui)

# Function to reset the counters
def reset_counters():
    global sensor1_counter, sensor2_counter
    sensor1_counter = 0
    sensor2_counter = 0
    sensor1_label.config(text=f"Sensor1 Counter: {sensor1_counter}")
    sensor2_label.config(text=f"Sensor2 Counter: {sensor2_counter}")

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
