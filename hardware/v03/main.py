import time
import tkinter as tk
from tkinter import ttk
import logging
from control import start_labeling_machine, stop_labeling_machine, start_filling_machine, stop_filling_machine, start_blowing_machine, stop_blowing_machine
from status import check_sensor, check_auto_mode, initialize_logging, reset_counters, set_auto_mode, sensor1, sensor2, set_labeling_timeout, set_traffic_threshold, labeling_working, labeling_alarm, filling_working, filling_alarm, blowing_working, blowing_alarm, labeling_idle, filling_idle

# Initialize logging
initialize_logging()

# Create the main Tkinter window
root = tk.Tk()
root.title("Bottling Line Control System")
root.geometry("1000x600")  # Set a fixed window size

# Initialize auto mode variables
stop_filling_for_traffic = tk.BooleanVar()
stop_labeling_for_traffic = tk.BooleanVar()
stop_labeling_for_timeout = tk.BooleanVar()
labeling_timeout_value = tk.IntVar(value=5)
traffic_threshold_value = tk.IntVar(value=2)

# Function to validate and retrieve integer values with a default fallback
def safe_get_int(var, default):
    try:
        return int(var.get())
    except (tk.TclError, ValueError):
        var.set(default)
        print(f"Invalid input. Reset to default: {default}")
        return default

# Update functions with feedback
def update_labeling_timeout():
    timeout = safe_get_int(labeling_timeout_value, 5)
    set_labeling_timeout(timeout)
    print(f"Labeling timeout updated to: {timeout}")

def update_traffic_threshold():
    threshold = safe_get_int(traffic_threshold_value, 2)
    set_traffic_threshold(threshold)
    print(f"Traffic threshold updated to: {threshold}")

# Initialize counters and flags
sensor1_counter = 0
sensor2_counter = 0
sensor1_traffic = False
sensor2_traffic = False
auto_mode_enabled = False

# GUI update loop with counter reset and auto mode control
def update_gui():
    global sensor1_counter, sensor2_counter, sensor1_traffic, sensor2_traffic
    traffic_threshold = safe_get_int(traffic_threshold_value, 2)
    sensor1_counter, sensor1_traffic = check_sensor(sensor1, sensor1_counter, sensor1_traffic, traffic_threshold)
    sensor2_counter, sensor2_traffic = check_sensor(sensor2, sensor2_counter, sensor2_traffic, traffic_threshold)

    check_auto_mode(auto_mode_enabled, stop_filling_for_traffic.get(), sensor1_traffic, stop_labeling_for_traffic.get(), sensor2_traffic, stop_labeling_for_timeout.get())

    # Update counter and status labels
    sensor1_label.config(text=f"Sensor1 Counter: {sensor1_counter}")
    sensor2_label.config(text=f"Sensor2 Counter: {sensor2_counter}")
    sensor1_traffic_label.config(text=f"Sensor1 Traffic: {'Detected' if sensor1_traffic else 'Clear'}")
    sensor2_traffic_label.config(text=f"Sensor2 Traffic: {'Detected' if sensor2_traffic else 'Clear'}")
    mode_status_label.config(text="Auto Mode Enabled" if auto_mode_enabled else "Manual Mode Enabled")

    # Update machine status labels
    update_status(labeling_status_label, labeling_working.is_pressed)
    update_status(labeling_alarm_label, labeling_alarm.is_pressed)
    update_status(filling_status_label, filling_working.is_pressed)
    update_status(filling_alarm_label, filling_alarm.is_pressed)
    update_status(blowing_status_label, blowing_working.is_pressed)
    update_status(blowing_alarm_label, blowing_alarm.is_pressed)
    update_status(labeling_idle_label, labeling_idle.is_pressed)
    update_status(filling_idle_label, filling_idle.is_pressed)

    root.after(100, update_gui)

# Helper function for updating status labels with color
def update_status(label, status):
    label.config(text=("Active" if status else "Inactive"), fg=("green" if status else "red"))

# Toggle auto mode
def toggle_auto_mode():
    global auto_mode_enabled
    auto_mode_enabled = not auto_mode_enabled
    set_auto_mode(auto_mode_enabled)
    print("Auto Mode Enabled" if auto_mode_enabled else "Manual Mode Enabled")
    mode_status_label.config(text="Auto Mode Enabled" if auto_mode_enabled else "Manual Mode Enabled")

# Reset counters with feedback
def reset_gui_counters():
    global sensor1_counter, sensor2_counter
    sensor1_counter, sensor2_counter = 0, 0
    reset_counters()
    print("Counters have been reset.")
    sensor1_label.config(text=f"Sensor1 Counter: {sensor1_counter}")
    sensor2_label.config(text=f"Sensor2 Counter: {sensor2_counter}")

# Styling elements
label_bg = "#ffffff"
label_font = ("Arial", 10)
frame_bg = "#f2f2f2"
button_font = ("Arial", 12, "bold")

# Main layout frames
status_panel = tk.Frame(root, width=300, bg=frame_bg, padx=10, pady=10)
control_panel = tk.Frame(root, bg=frame_bg, padx=10, pady=10)
status_panel.pack(side="left", fill="y")
control_panel.pack(side="right", expand=True, fill="both")

# Status Frame Layout
tk.Label(status_panel, text="System Status", font=("Arial", 16, "bold"), bg=frame_bg).grid(row=0, column=0, columnspan=2, pady=10)
sensor1_label = tk.Label(status_panel, text="Sensor1 Counter: 0", font=label_font, bg=frame_bg)
sensor1_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=2)
sensor2_label = tk.Label(status_panel, text="Sensor2 Counter: 0", font=label_font, bg=frame_bg)
sensor2_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=2)
sensor1_traffic_label = tk.Label(status_panel, text="Sensor1 Traffic: Clear", font=label_font, bg=frame_bg)
sensor1_traffic_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=2)
sensor2_traffic_label = tk.Label(status_panel, text="Sensor2 Traffic: Clear", font=label_font, bg=frame_bg)
sensor2_traffic_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=2)

# Status indicators for machines
tk.Label(status_panel, text="Labeling", font=("Arial", 14, "bold"), bg=frame_bg).grid(row=5, column=0, pady=10, sticky="w")
labeling_status_label = tk.Label(status_panel, text="Inactive", font=label_font, bg=frame_bg)
labeling_status_label.grid(row=5, column=1, sticky="e")
labeling_alarm_label = tk.Label(status_panel, text="Inactive", font=label_font, bg=frame_bg)
labeling_alarm_label.grid(row=6, column=1, sticky="e")
labeling_idle_label = tk.Label(status_panel, text="Inactive", font=label_font, bg=frame_bg)
labeling_idle_label.grid(row=7, column=1, sticky="e")

tk.Label(status_panel, text="Filling", font=("Arial", 14, "bold"), bg=frame_bg).grid(row=8, column=0, pady=10, sticky="w")
filling_status_label = tk.Label(status_panel, text="Inactive", font=label_font, bg=frame_bg)
filling_status_label.grid(row=8, column=1, sticky="e")
filling_alarm_label = tk.Label(status_panel, text="Inactive", font=label_font, bg=frame_bg)
filling_alarm_label.grid(row=9, column=1, sticky="e")
filling_idle_label = tk.Label(status_panel, text="Inactive", font=label_font, bg=frame_bg)
filling_idle_label.grid(row=10, column=1, sticky="e")

tk.Label(status_panel, text="Blowing", font=("Arial", 14, "bold"), bg=frame_bg).grid(row=11, column=0, pady=10, sticky="w")
blowing_status_label = tk.Label(status_panel, text="Inactive", font=label_font, bg=frame_bg)
blowing_status_label.grid(row=11, column=1, sticky="e")
blowing_alarm_label = tk.Label(status_panel, text="Inactive", font=label_font, bg=frame_bg)
blowing_alarm_label.grid(row=12, column=1, sticky="e")

# Control Tabs in Control Panel
tab_control = ttk.Notebook(control_panel)
manual_tab = ttk.Frame(tab_control)
auto_tab = ttk.Frame(tab_control)
settings_tab = ttk.Frame(tab_control)
tab_control.add(manual_tab, text="Manual Control")
tab_control.add(auto_tab, text="Automatic Control")
tab_control.add(settings_tab, text="Settings")
tab_control.pack(expand=True, fill="both", padx=5, pady=5)

# Manual Control Tab
tk.Button(manual_tab, text="Start Labeling", command=start_labeling_machine, font=button_font).pack(pady=5)
tk.Button(manual_tab, text="Stop Labeling", command=stop_labeling_machine, font=button_font).pack(pady=5)
tk.Button(manual_tab, text="Start Filling", command=start_filling_machine, font=button_font).pack(pady=5)
tk.Button(manual_tab, text="Stop Filling", command=stop_filling_machine, font=button_font).pack(pady=5)
tk.Button(manual_tab, text="Start Blowing", command=start_blowing_machine, font=button_font).pack(pady=5)
tk.Button(manual_tab, text="Stop Blowing", command=stop_blowing_machine, font=button_font).pack(pady=5)
tk.Button(manual_tab, text="Reset Counters", command=reset_gui_counters, font=button_font).pack(pady=5)

# Automatic Control Tab
tk.Checkbutton(auto_tab, text="Stop Filling Machine for Sensor1 Traffic", variable=stop_filling_for_traffic).pack(pady=5)
tk.Checkbutton(auto_tab, text="Stop Labeling Machine for Sensor2 Traffic", variable=stop_labeling_for_traffic).pack(pady=5)
tk.Checkbutton(auto_tab, text="Stop Labeling Machine if Sensor1 Inactive", variable=stop_labeling_for_timeout).pack(pady=5)
tk.Button(auto_tab, text="Enable Auto Mode", command=toggle_auto_mode, font=button_font).pack(pady=10)

# Settings Tab
tk.Label(settings_tab, text="Labeling Machine Timeout (seconds):", font=label_font).pack(pady=5)
tk.Entry(settings_tab, textvariable=labeling_timeout_value, font=label_font).pack(pady=5)
tk.Button(settings_tab, text="Update Timeout", command=update_labeling_timeout, font=button_font).pack(pady=5)
tk.Label(settings_tab, text="Traffic Threshold (seconds):", font=label_font).pack(pady=5)
tk.Entry(settings_tab, textvariable=traffic_threshold_value, font=label_font).pack(pady=5)
tk.Button(settings_tab, text="Update Threshold", command=update_traffic_threshold, font=button_font).pack(pady=5)

# Mode status label at the bottom of the status panel
mode_status_label = tk.Label(status_panel, text="Manual Mode Enabled", font=("Arial", 14, "bold"), bg=frame_bg)
mode_status_label.grid(row=13, column=0, columnspan=2, pady=10)

# Start GUI update loop
update_gui()
root.mainloop()