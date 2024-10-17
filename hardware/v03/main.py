import time
import tkinter as tk
from tkinter import ttk
from status import start_labeling_machine, stop_labeling_machine, start_filling_machine, stop_filling_machine, start_blowing_machine, stop_blowing_machine, \
    check_sensor, check_auto_mode, initialize_logging, reset_counters, set_auto_mode, sensor1, sensor2, set_labeling_timeout, set_traffic_threshold, \
    labeling_working, filling_working, blowing_working, labeling_alarm, filling_alarm, blowing_alarm, labeling_idle, filling_idle

# Initialize logging
initialize_logging()

# Main window setup
root = tk.Tk()
root.title("Bottling Line Control System")
root.geometry("1200x750")  # Adjust based on your screen dimensions

# Initialize counters and flags
sensor1_counter = 0
sensor2_counter = 0
sensor1_traffic = False
sensor2_traffic = False
auto_mode_enabled = False

# Define color mappings for machine status
status_colors = {"active": "green", "stopped": "red", "idle": "yellow"}

# Canvas for bottling line visualization
canvas = tk.Canvas(root, width=700, height=700, bg="lightgray")
canvas.grid(row=0, column=0, rowspan=2, padx=5, pady=5)

# Layout based on your image
blowing_rect = canvas.create_rectangle(50, 50, 200, 100, fill=status_colors["idle"], outline="black", width=2)
canvas.create_text(125, 75, text="Blowing Machine", anchor="center", font=("Arial", 9))
canvas.create_line(200, 75, 350, 75, arrow=tk.LAST, width=2)

filling_rect = canvas.create_rectangle(350, 150, 500, 200, fill=status_colors["idle"], outline="black", width=2)
canvas.create_text(425, 175, text="Filling Machine", anchor="center", font=("Arial", 9))
canvas.create_line(425, 100, 425, 150, arrow=tk.LAST, width=2)

labeling_rect = canvas.create_rectangle(50, 250, 200, 300, fill=status_colors["idle"], outline="black", width=2)
canvas.create_text(125, 275, text="Labeling Machine", anchor="center", font=("Arial", 9))
canvas.create_line(200, 275, 350, 275, arrow=tk.LAST, width=2)

packing_rect = canvas.create_rectangle(350, 350, 500, 400, fill=status_colors["idle"], outline="black", width=2)
canvas.create_text(425, 375, text="Packing Machine", anchor="center", font=("Arial", 9))
canvas.create_line(425, 300, 425, 350, arrow=tk.LAST, width=2)

# Status frame for counters and traffic indicators
status_frame = tk.Frame(root, bg="white", relief=tk.RAISED, borderwidth=1)
status_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

# Function to get color based on machine status
def get_status_color(working, alarm):
    if alarm:
        return status_colors["stopped"]
    elif working:
        return status_colors["active"]
    else:
        return status_colors["idle"]

# Function to update sensor counts, traffic status, and visual indicators
def update_bottling_line():
    global sensor1_counter, sensor2_counter, sensor1_traffic, sensor2_traffic
    traffic_threshold = safe_get_int(traffic_threshold_value, 2)

    # Update sensors and check for traffic
    sensor1_counter, sensor1_traffic = check_sensor(sensor1, sensor1_counter, sensor1_traffic, traffic_threshold)
    sensor2_counter, sensor2_traffic = check_sensor(sensor2, sensor2_counter, sensor2_traffic, traffic_threshold)

    # Check auto mode
    check_auto_mode(auto_mode_enabled, stop_filling_for_traffic.get(), sensor1_traffic, stop_labeling_for_traffic.get(), sensor2_traffic, stop_labeling_for_timeout.get())

    # Update the colors based on machine status
    canvas.itemconfig(blowing_rect, fill=get_status_color(blowing_working.is_pressed, blowing_alarm.is_pressed))
    canvas.itemconfig(filling_rect, fill=get_status_color(filling_working.is_pressed, filling_alarm.is_pressed))
    canvas.itemconfig(labeling_rect, fill=get_status_color(labeling_working.is_pressed, labeling_alarm.is_pressed))
    canvas.itemconfig(packing_rect, fill=status_colors["idle"])  # Assume packing machine is always idle

    # Update sensor counters and traffic indicators
    sensor1_label.config(text=f"Sensor1 Counter: {sensor1_counter}")
    sensor2_label.config(text=f"Sensor2 Counter: {sensor2_counter}")
    sensor1_traffic_label.config(text=f"Sensor1 Traffic: {'Detected' if sensor1_traffic else 'Clear'}")
    sensor2_traffic_label.config(text=f"Sensor2 Traffic: {'Detected' if sensor2_traffic else 'Clear'}")

    root.after(100, update_bottling_line)

# Validation function for integer values with feedback
def safe_get_int(var, default):
    try:
        return int(var.get())
    except (tk.TclError, ValueError):
        var.set(default)
        print(f"Invalid input. Reset to default: {default}")
        return default

# Toggle auto mode
def toggle_auto_mode():
    global auto_mode_enabled
    auto_mode_enabled = not auto_mode_enabled
    set_auto_mode(auto_mode_enabled)
    auto_mode_indicator.config(text="Auto Mode Enabled" if auto_mode_enabled else "Manual Mode Enabled")
    print("Auto Mode Enabled" if auto_mode_enabled else "Manual Mode Enabled")  # Terminal feedback

# Populate Status Frame with sensor and traffic status
sensor1_label = tk.Label(status_frame, text=f"Sensor1 Counter: {sensor1_counter}", bg="white", font=("Arial", 10))
sensor1_label.pack(pady=5)
sensor2_label = tk.Label(status_frame, text=f"Sensor2 Counter: {sensor2_counter}", bg="white", font=("Arial", 10))
sensor2_label.pack(pady=5)
sensor1_traffic_label = tk.Label(status_frame, text="Sensor1 Traffic: Clear", bg="white", font=("Arial", 10))
sensor1_traffic_label.pack(pady=5)
sensor2_traffic_label = tk.Label(status_frame, text="Sensor2 Traffic: Clear", bg="white", font=("Arial", 10))
sensor2_traffic_label.pack(pady=5)

# Tab control setup
tab_control = ttk.Notebook(root)
manual_tab = ttk.Frame(tab_control)
auto_tab = ttk.Frame(tab_control)
settings_tab = ttk.Frame(tab_control)
status_tab = ttk.Frame(tab_control)
tab_control.add(manual_tab, text="Manual Control")
tab_control.add(auto_tab, text="Automatic Control")
tab_control.add(settings_tab, text="Settings")
tab_control.add(status_tab, text="System Status")
tab_control.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

# Manual Control Tab
for text, cmd in [("Start Labeling", start_labeling_machine), ("Stop Labeling", stop_labeling_machine),
                  ("Start Filling", start_filling_machine), ("Stop Filling", stop_filling_machine),
                  ("Start Blowing", start_blowing_machine), ("Stop Blowing", stop_blowing_machine),
                  ("Reset Counters", reset_counters)]:
    tk.Button(manual_tab, text=text, command=cmd).pack(padx=5, pady=2)

# Automatic Control Tab
stop_filling_for_traffic = tk.BooleanVar()
stop_labeling_for_traffic = tk.BooleanVar()
stop_labeling_for_timeout = tk.BooleanVar()
tk.Checkbutton(auto_tab, text="Stop Filling for Sensor1 Traffic", variable=stop_filling_for_traffic).pack(anchor="w", padx=5, pady=2)
tk.Checkbutton(auto_tab, text="Stop Labeling for Sensor2 Traffic", variable=stop_labeling_for_traffic).pack(anchor="w", padx=5, pady=2)
tk.Checkbutton(auto_tab, text="Stop Labeling if Sensor1 Inactive", variable=stop_labeling_for_timeout).pack(anchor="w", padx=5, pady=2)
tk.Button(auto_tab, text="Toggle Auto Mode", command=toggle_auto_mode).pack(padx=5, pady=5)

# Auto Mode Indicator
auto_mode_indicator = tk.Label(root, text="Manual Mode Enabled", font=("Arial", 12), bg="lightgrey")
auto_mode_indicator.grid(row=0, column=1, padx=5, pady=5, sticky="s")

# Settings Tab
labeling_timeout_value = tk.IntVar(value=5)
traffic_threshold_value = tk.IntVar(value=2)
tk.Label(settings_tab, text="Labeling Timeout (s):").pack(anchor="w", padx=5, pady=2)
tk.Entry(settings_tab, textvariable=labeling_timeout_value).pack(fill="x", padx=5, pady=2)
tk.Button(settings_tab, text="Update Timeout", command=lambda: set_labeling_timeout(labeling_timeout_value.get())).pack(pady=5)
tk.Label(settings_tab, text="Traffic Threshold (s):").pack(anchor="w", padx=5, pady=2)
tk.Entry(settings_tab, textvariable=traffic_threshold_value).pack(fill="x", padx=5, pady=2)
tk.Button(settings_tab, text="Update Threshold", command=lambda: set_traffic_threshold(traffic_threshold_value.get())).pack(pady=5)

# System Status Tab for machine statuses
for machine, status in [("Blowing", blowing_working), ("Filling", filling_working), ("Labeling", labeling_working)]:
    tk.Label(status_tab, text=f"{machine} Working: {'Active' if status.is_pressed else 'Inactive'}", bg="white", font=("Arial", 10)).pack(pady=5)

for machine, status in [("Filling", filling_idle), ("Labeling", labeling_idle)]:
    tk.Label(status_tab, text=f"{machine} Idle: {'Active' if status.is_pressed else 'Inactive'}", bg="white", font=("Arial", 10)).pack(pady=5)    
    
for machine, status in [("Blowing Alarm", blowing_alarm), ("Filling Alarm", filling_alarm), ("Labeling Alarm", labeling_alarm)]:
    tk.Label(status_tab, text=f"{machine}: {'Active' if status.is_pressed else 'Inactive'}", bg="white", font=("Arial", 10)).pack(pady=5)

# Start the main loop
update_bottling_line()
root.mainloop()