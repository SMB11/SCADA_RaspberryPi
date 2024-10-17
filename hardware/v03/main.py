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
root.configure(bg="#f5f5f5")

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
    labeling_status_label.config(text=f"Labeling Working: {'Active' if labeling_working.is_pressed else 'Inactive'}")
    labeling_alarm_label.config(text=f"Labeling Alarm: {'Active' if labeling_alarm.is_pressed else 'Inactive'}")
    filling_status_label.config(text=f"Filling Working: {'Active' if filling_working.is_pressed else 'Inactive'}")
    filling_alarm_label.config(text=f"Filling Alarm: {'Active' if filling_alarm.is_pressed else 'Inactive'}")
    blowing_status_label.config(text=f"Blowing Working: {'Active' if blowing_working.is_pressed else 'Inactive'}")
    blowing_alarm_label.config(text=f"Blowing Alarm: {'Active' if blowing_alarm.is_pressed else 'Inactive'}")
    labeling_idle_label.config(text=f"Labeling Idle: {'Idle' if labeling_idle.is_pressed else 'Inactive'}")
    filling_idle_label.config(text=f"Filling Idle: {'Idle' if filling_idle.is_pressed else 'Inactive'}")

    root.after(100, update_gui)

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
frame_bg = "#e0e0e0"
button_font = ("Arial", 12, "bold")

# Create main frames for better structure
control_frame = tk.Frame(root, bg=frame_bg, padx=10, pady=10)
status_frame = tk.Frame(root, bg=frame_bg, padx=10, pady=10)
control_frame.pack(fill="both", expand=True)
status_frame.pack(fill="both", expand=True)

# Tabs within control frame
tab_control = ttk.Notebook(control_frame)
manual_tab = ttk.Frame(tab_control)
auto_tab = ttk.Frame(tab_control)
settings_tab = ttk.Frame(tab_control)
tab_control.add(manual_tab, text="Manual Control")
tab_control.add(auto_tab, text="Automatic Control")
tab_control.add(settings_tab, text="Settings")
tab_control.pack(expand=1, fill="both", padx=5, pady=5)

# Manual Control Tab
for btn_text, command in [("Start Labeling", start_labeling_machine), ("Stop Labeling", stop_labeling_machine),
                          ("Start Filling", start_filling_machine), ("Stop Filling", stop_filling_machine),
                          ("Start Blowing", start_blowing_machine), ("Stop Blowing", stop_blowing_machine),
                          ("Reset Counters", reset_gui_counters)]:
    tk.Button(manual_tab, text=btn_text, command=command, font=button_font, bg=label_bg).pack(pady=2, fill="x")

# Automatic Control Tab
for text, var in [("Stop Filling Machine for Sensor1 Traffic", stop_filling_for_traffic),
                  ("Stop Labeling Machine for Sensor2 Traffic", stop_labeling_for_traffic),
                  ("Stop Labeling Machine if Sensor1 Inactive", stop_labeling_for_timeout)]:
    tk.Checkbutton(auto_tab, text=text, variable=var, font=label_font).pack(anchor="w", pady=2, padx=5)
tk.Button(auto_tab, text="Enable Auto Mode", command=toggle_auto_mode, font=button_font).pack(pady=5)

# Settings Tab
for text, var, update_func in [("Labeling Machine Timeout (seconds):", labeling_timeout_value, update_labeling_timeout),
                               ("Traffic Threshold (seconds):", traffic_threshold_value, update_traffic_threshold)]:
    tk.Label(settings_tab, text=text, font=label_font).pack(anchor="w", pady=2, padx=5)
    tk.Entry(settings_tab, textvariable=var).pack(pady=2, padx=5)
    tk.Button(settings_tab, text="Update", command=update_func, font=label_font).pack(pady=2)

# Status labels layout
sensor1_label = tk.Label(status_frame, text=f"Sensor1 Counter: {sensor1_counter}", font=label_font, bg=frame_bg)
sensor2_label = tk.Label(status_frame, text=f"Sensor2 Counter: {sensor2_counter}", font=label_font, bg=frame_bg)
sensor1_traffic_label = tk.Label(status_frame, text="Sensor1 Traffic: Clear", font=label_font, bg=frame_bg)
sensor2_traffic_label = tk.Label(status_frame, text="Sensor2 Traffic: Clear", font=label_font, bg=frame_bg)
labeling_status_label = tk.Label(status_frame, text="Labeling Working: Inactive", font=label_font, bg=frame_bg)
labeling_alarm_label = tk.Label(status_frame, text="Labeling Alarm: Inactive", font=label_font, bg=frame_bg)
filling_status_label = tk.Label(status_frame, text="Filling Working: Inactive", font=label_font, bg=frame_bg)
filling_alarm_label = tk.Label(status_frame, text="Filling Alarm: Inactive", font=label_font, bg=frame_bg)
blowing_status_label = tk.Label(status_frame, text="Blowing Working: Inactive", font=label_font, bg=frame_bg)
blowing_alarm_label = tk.Label(status_frame, text="Blowing Alarm: Inactive", font=label_font, bg=frame_bg)
labeling_idle_label = tk.Label(status_frame, text="Labeling Idle: Inactive", font=label_font, bg=frame_bg)
filling_idle_label = tk.Label(status_frame, text="Filling Idle: Inactive", font=label_font, bg=frame_bg)

# Packing all status labels in status frame
for label in [sensor1_label, sensor2_label, sensor1_traffic_label, sensor2_traffic_label, 
              labeling_status_label, labeling_alarm_label, filling_status_label, filling_alarm_label,
              blowing_status_label, blowing_alarm_label, labeling_idle_label, filling_idle_label]:
    label.pack(anchor="w", pady=1, padx=5)

# Mode status label at the bottom
mode_status_label = tk.Label(root, text="Manual Mode Enabled", font=("Arial", 14, "bold"), bg="#cfd8dc")
mode_status_label.pack(fill="x", pady=10)

# Start GUI update loop
update_gui()
root.mainloop()