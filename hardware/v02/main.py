import time
import tkinter as tk
from tkinter import ttk
import logging
from control import start_labeling_machine, stop_labeling_machine, start_filling_machine, stop_filling_machine, start_blowing_machine, stop_blowing_machine
from status import check_sensor, check_auto_mode, initialize_logging, reset_counters, set_auto_mode, sensor1, sensor2, set_labeling_timeout, set_traffic_threshold

# Initialize logging
initialize_logging()

# Create the main Tkinter window
root = tk.Tk()
root.title("Bottling Line Control System")

# Initialize auto mode variables after creating the root window
stop_filling_for_traffic = tk.BooleanVar()
stop_labeling_for_traffic = tk.BooleanVar()
stop_labeling_for_timeout = tk.BooleanVar()  # New variable for labeling timeout
labeling_timeout_value = tk.IntVar(value=5)  # Default timeout in seconds
traffic_threshold_value = tk.IntVar(value=2)  # Default traffic threshold in seconds

# Function to update the labeling timeout from settings tab
def update_labeling_timeout():
    set_labeling_timeout(labeling_timeout_value.get())

# Function to update the traffic threshold from settings tab
def update_traffic_threshold():
    set_traffic_threshold(traffic_threshold_value.get())

# Initialize counters and traffic thresholds
sensor1_counter = 0
sensor2_counter = 0
sensor1_traffic = False
sensor2_traffic = False
auto_mode_enabled = False

def update_gui():
    global sensor1_counter, sensor2_counter, sensor1_traffic, sensor2_traffic
    sensor1_counter, sensor1_traffic = check_sensor(sensor1, sensor1_counter, sensor1_traffic, traffic_threshold_value.get())
    sensor2_counter, sensor2_traffic = check_sensor(sensor2, sensor2_counter, sensor2_traffic, traffic_threshold_value.get())
    check_auto_mode(auto_mode_enabled, stop_filling_for_traffic.get(), sensor1_traffic, stop_labeling_for_traffic.get(), sensor2_traffic, stop_labeling_for_timeout.get())

    # Update the counter labels
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

    # Update the auto mode status
    mode_status_label.config(text="Auto Mode Enabled" if auto_mode_enabled else "Manual Mode Enabled")

    # Schedule the next update
    root.after(100, update_gui)

# Function to toggle auto mode
def toggle_auto_mode():
    global auto_mode_enabled
    auto_mode_enabled = not auto_mode_enabled
    set_auto_mode(auto_mode_enabled)
    mode_status_label.config(text="Auto Mode Enabled" if auto_mode_enabled else "Manual Mode Enabled")

# Initialize GUI components (manual tab, auto tab, settings tab, etc.)
tab_control = ttk.Notebook(root)
manual_tab = ttk.Frame(tab_control)
auto_tab = ttk.Frame(tab_control)
settings_tab = ttk.Frame(tab_control)
tab_control.add(manual_tab, text="Manual Control")
tab_control.add(auto_tab, text="Automatic Control")
tab_control.add(settings_tab, text="Settings")
tab_control.pack(expand=1, fill="both")

# Manual Control Tab
tk.Button(manual_tab, text="Start Labeling", command=start_labeling_machine).pack()
tk.Button(manual_tab, text="Stop Labeling", command=stop_labeling_machine).pack()
tk.Button(manual_tab, text="Start Filling", command=start_filling_machine).pack()
tk.Button(manual_tab, text="Stop Filling", command=stop_filling_machine).pack()
tk.Button(manual_tab, text="Start Blowing", command=start_blowing_machine).pack()
tk.Button(manual_tab, text="Stop Blowing", command=stop_blowing_machine).pack()
tk.Button(manual_tab, text="Reset Counters", command=reset_counters).pack()

# Automatic Control Tab
tk.Checkbutton(auto_tab, text="Stop Filling Machine for Sensor1 Traffic", variable=stop_filling_for_traffic).pack()
tk.Checkbutton(auto_tab, text="Stop Labeling Machine for Sensor2 Traffic", variable=stop_labeling_for_traffic).pack()
tk.Checkbutton(auto_tab, text="Stop Labeling Machine if Sensor1 Inactive", variable=stop_labeling_for_timeout).pack()
tk.Button(auto_tab, text="Enable Auto Mode", command=toggle_auto_mode).pack()

# Settings Tab
tk.Label(settings_tab, text="Labeling Machine Timeout (seconds):").pack()
tk.Entry(settings_tab, textvariable=labeling_timeout_value).pack()
tk.Button(settings_tab, text="Update Timeout", command=update_labeling_timeout).pack()

tk.Label(settings_tab, text="Traffic Threshold (seconds):").pack()
tk.Entry(settings_tab, textvariable=traffic_threshold_value).pack()
tk.Button(settings_tab, text="Update Threshold", command=update_traffic_threshold).pack()

# Common labels for both tabs
sensor1_label = tk.Label(root, text=f"Sensor1 Counter: {sensor1_counter}")
sensor1_label.pack()
sensor2_label = tk.Label(root, text=f"Sensor2 Counter: {sensor2_counter}")
sensor2_label.pack()
sensor1_traffic_label = tk.Label(root, text="Sensor1 Traffic: Clear")
sensor1_traffic_label.pack()
sensor2_traffic_label = tk.Label(root, text="Sensor2 Traffic: Clear")
sensor2_traffic_label.pack()

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
labeling_idle_label = tk.Label(root, text="Labeling Idle: Inactive")
labeling_idle_label.pack()
filling_idle_label = tk.Label(root, text="Filling Idle: Inactive")
filling_idle_label.pack()

# Add mode status label at the bottom of the GUI
mode_status_label = tk.Label(root, text="Manual Mode Enabled", font=("Arial", 14))
mode_status_label.pack(pady=10)

# Start the GUI loop
sensor1_high_start = None
sensor2_high_start = None
update_gui()
root.mainloop()