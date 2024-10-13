import time
import tkinter as tk
from tkinter import ttk
from gpiozero import Button
from control import start_labeling_machine, stop_labeling_machine, start_filling_machine, stop_filling_machine, start_blowing_machine, stop_blowing_machine

# Initialize counters, traffic flags, and automatic mode
sensor1_counter = 0
sensor2_counter = 0
TRAFFIC_THRESHOLD = 2  # Time in seconds to consider traffic
sensor1_traffic = False
sensor2_traffic = False
automatic_mode = False  # Start with manual mode

# Define GPIO pins directly for sensors and machine statuses
sensor1 = Button(13, pull_up=True)
sensor2 = Button(26, pull_up=True)
labeling_working = Button(21, pull_up=True)
labeling_alarm = Button(19, pull_up=True)
filling_working = Button(16, pull_up=True)
filling_alarm = Button(5, pull_up=True)
blowing_working = Button(18, pull_up=True)
blowing_alarm = Button(10, pull_up=True)

# Function to check sensor and increment counter if necessary, with persistent traffic detection
def check_sensor(sensor, sensor_counter, high_start, traffic_flag):
    if sensor.is_pressed:
        if high_start is None:
            sensor_counter += 1
            traffic_flag = False  # Reset traffic on new count
            time.sleep(0.2)  # Debounce
            return sensor_counter, time.time(), traffic_flag
        elif time.time() - high_start >= TRAFFIC_THRESHOLD:
            traffic_flag = True
            return sensor_counter, high_start, traffic_flag
    else:
        traffic_flag = False
        return sensor_counter, None, traffic_flag

    return sensor_counter, high_start, traffic_flag

# Function to handle automatic mode logic
def handle_automatic_mode():
    if automatic_mode:
        if sensor1_traffic:
            if filling_working.is_pressed:
                stop_filling_machine()
            if blowing_working.is_pressed:
                stop_blowing_machine()
        else:
            if not filling_working.is_pressed:
                start_filling_machine()
            if not blowing_working.is_pressed:
                start_blowing_machine()

        if sensor2_traffic and labeling_working.is_pressed:
            stop_labeling_machine()
        elif not sensor2_traffic and not labeling_working.is_pressed:
            start_labeling_machine()

# Function to update counters, machine statuses, traffic status, and handle automatic mode
def update_gui():
    global sensor1_counter, sensor2_counter, sensor1_high_start, sensor2_high_start, sensor1_traffic, sensor2_traffic
    sensor1_counter, sensor1_high_start, sensor1_traffic = check_sensor(sensor1, sensor1_counter, sensor1_high_start, sensor1_traffic)
    sensor2_counter, sensor2_high_start, sensor2_traffic = check_sensor(sensor2, sensor2_counter, sensor2_high_start, sensor2_traffic)

    # Update counter labels
    sensor1_label.config(text=f"Sensor1 Counter: {sensor1_counter}")
    sensor2_label.config(text=f"Sensor2 Counter: {sensor2_counter}")
    sensor1_traffic_label.config(text=f"Sensor1 Traffic: {'Detected' if sensor1_traffic else 'Clear'}")
    sensor2_traffic_label.config(text=f"Sensor2 Traffic: {'Detected' if sensor2_traffic else 'Clear'}")

    # Update machine status labels
    labeling_status_label.config(text=f"Labeling Working: {'Active' if labeling_working.is_pressed else 'Inactive'}")
    labeling_alarm_label.config(text=f"Labeling Alarm: {'Active' if labeling_alarm.is_pressed else 'Inactive'}")
    filling_status_label.config(text=f"Filling Working: {'Active' if filling_working.is_pressed else 'Inactive'}")
    filling_alarm_label.config(text=f"Filling Alarm: {'Active' if filling_alarm.is_pressed else 'Inactive'}")
    blowing_status_label.config(text=f"Blowing Working: {'Active' if blowing_working.is_pressed else 'Inactive'}")
    blowing_alarm_label.config(text=f"Blowing Alarm: {'Active' if blowing_alarm.is_pressed else 'Inactive'}")

    # Handle automatic mode logic
    handle_automatic_mode()

    # Schedule the next update
    root.after(100, update_gui)

# Function to toggle automatic mode
def toggle_automatic_mode():
    global automatic_mode
    automatic_mode = not automatic_mode
    mode_button.config(text="Automatic Mode" if not automatic_mode else "Manual Mode")

# Function to reset the counters
def reset_counters():
    global sensor1_counter, sensor2_counter
    sensor1_counter = 0
    sensor2_counter = 0
    sensor1_label.config(text=f"Sensor1 Counter: {sensor1_counter}")
    sensor2_label.config(text=f"Sensor2 Counter: {sensor2_counter}")

# Function to save settings
def save_settings():
    global TRAFFIC_THRESHOLD
    try:
        TRAFFIC_THRESHOLD = float(traffic_threshold_entry.get())
        print(f"Settings updated: Traffic Detection Time = {TRAFFIC_THRESHOLD} seconds")
    except ValueError:
        print("Invalid input for traffic detection time")

# Initialize GUI
root = tk.Tk()
root.title("Bottling Line Control System")
root.geometry("400x500")

# Create Tab Control
tab_control = ttk.Notebook(root)

# Main Tab
main_tab = ttk.Frame(tab_control)
tab_control.add(main_tab, text='Main')

# Settings Tab
settings_tab = ttk.Frame(tab_control)
tab_control.add(settings_tab, text='Settings')

# Display the tab control
tab_control.pack(expand=1, fill="both")

# Main Tab Widgets
sensor1_label = ttk.Label(main_tab, text=f"Sensor1 Counter: {sensor1_counter}")
sensor1_label.pack(pady=5)
sensor2_label = ttk.Label(main_tab, text=f"Sensor2 Counter: {sensor2_counter}")
sensor2_label.pack(pady=5)
sensor1_traffic_label = ttk.Label(main_tab, text="Sensor1 Traffic: Clear")
sensor1_traffic_label.pack(pady=5)
sensor2_traffic_label = ttk.Label(main_tab, text="Sensor2 Traffic: Clear")
sensor2_traffic_label.pack(pady=5)

labeling_status_label = ttk.Label(main_tab, text="Labeling Working: Inactive")
labeling_status_label.pack(pady=5)
labeling_alarm_label = ttk.Label(main_tab, text="Labeling Alarm: Inactive")
labeling_alarm_label.pack(pady=5)
filling_status_label = ttk.Label(main_tab, text="Filling Working: Inactive")
filling_status_label.pack(pady=5)
filling_alarm_label = ttk.Label(main_tab, text="Filling Alarm: Inactive")
filling_alarm_label.pack(pady=5)
blowing_status_label = ttk.Label(main_tab, text="Blowing Working: Inactive")
blowing_status_label.pack(pady=5)
blowing_alarm_label = ttk.Label(main_tab, text="Blowing Alarm: Inactive")
blowing_alarm_label.pack(pady=5)

ttk.Button(main_tab, text="Start Labeling", command=start_labeling_machine).pack(pady=5)
ttk.Button(main_tab, text="Stop Labeling", command=stop_labeling_machine).pack(pady=5)
ttk.Button(main_tab, text="Start Filling", command=start_filling_machine).pack(pady=5)
ttk.Button(main_tab, text="Stop Filling", command=stop_filling_machine).pack(pady=5)
ttk.Button(main_tab, text="Start Blowing", command=start_blowing_machine).pack(pady=5)
ttk.Button(main_tab, text="Stop Blowing", command=stop_blowing_machine).pack(pady=5)
ttk.Button(main_tab, text="Reset Counters", command=reset_counters).pack(pady=5)
mode_button = ttk.Button(main_tab, text="Automatic Mode", command=toggle_automatic_mode)
mode_button.pack(pady=5)

# Settings Tab Widgets
ttk.Label(settings_tab, text="Traffic Detection Time (seconds):").pack(pady=10)
traffic_threshold_entry = ttk.Entry(settings_tab)
traffic_threshold_entry.insert(0, str(TRAFFIC_THRESHOLD))
traffic_threshold_entry.pack(pady=5)

save_button = ttk.Button(settings_tab, text="Save Settings", command=save_settings)
save_button.pack(pady=10)

# Start the GUI update loop
sensor1_high_start = None
sensor2_high_start = None
update_gui()

# Run the GUI event loop
root.mainloop()