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
root.geometry("1100x600")

# Canvas for bottling line visualization
canvas = tk.Canvas(root, width=500, height=400, bg="white")
canvas.grid(row=0, column=0, rowspan=2, padx=20, pady=20)

# Define color mappings for machine status
status_colors = {"active": "green", "stopped": "red", "idle": "yellow"}

# Create bottling line elements on the Canvas
blowing_rect = canvas.create_rectangle(30, 50, 110, 130, fill=status_colors["idle"], outline="black", width=2)
canvas.create_text(70, 140, text="Blowing Machine")
canvas.create_line(120, 90, 180, 90, arrow=tk.LAST, width=3)  # Conveyor

filling_rect = canvas.create_rectangle(190, 50, 270, 130, fill=status_colors["idle"], outline="black", width=2)
canvas.create_text(230, 140, text="Filling Machine")
canvas.create_line(280, 90, 340, 90, arrow=tk.LAST, width=3)  # Conveyor

labeling_rect = canvas.create_rectangle(350, 50, 430, 130, fill=status_colors["idle"], outline="black", width=2)
canvas.create_text(390, 140, text="Labeling Machine")
canvas.create_line(440, 90, 500, 90, arrow=tk.LAST, width=3)  # Conveyor

packing_rect = canvas.create_rectangle(510, 50, 590, 130, fill=status_colors["idle"], outline="black", width=2)
canvas.create_text(550, 140, text="Packing Machine")

# Function to get color based on machine status
def get_status_color(working, alarm):
    if alarm:
        return status_colors["stopped"]
    elif working:
        return status_colors["active"]
    else:
        return status_colors["idle"]

# Function to update machine colors and status labels on the Canvas
def update_bottling_line():
    # Update colors for each machine based on status
    canvas.itemconfig(blowing_rect, fill=get_status_color(blowing_working.is_pressed, blowing_alarm.is_pressed))
    canvas.itemconfig(filling_rect, fill=get_status_color(filling_working.is_pressed, filling_alarm.is_pressed))
    canvas.itemconfig(labeling_rect, fill=get_status_color(labeling_working.is_pressed, labeling_alarm.is_pressed))

    # Schedule next update
    root.after(1000, update_bottling_line)

# Tab control for manual, automatic, and settings tabs
tab_control = ttk.Notebook(root)
manual_tab = ttk.Frame(tab_control)
auto_tab = ttk.Frame(tab_control)
settings_tab = ttk.Frame(tab_control)
tab_control.add(manual_tab, text="Manual Control")
tab_control.add(auto_tab, text="Automatic Control")
tab_control.add(settings_tab, text="Settings")
tab_control.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

# Manual Control Tab
tk.Button(manual_tab, text="Start Labeling", command=start_labeling_machine).pack()
tk.Button(manual_tab, text="Stop Labeling", command=stop_labeling_machine).pack()
tk.Button(manual_tab, text="Start Filling", command=start_filling_machine).pack()
tk.Button(manual_tab, text="Stop Filling", command=stop_filling_machine).pack()
tk.Button(manual_tab, text="Start Blowing", command=start_blowing_machine).pack()
tk.Button(manual_tab, text="Stop Blowing", command=stop_blowing_machine).pack()
tk.Button(manual_tab, text="Reset Counters", command=reset_counters).pack()

# Automatic Control Tab
stop_filling_for_traffic = tk.BooleanVar()
stop_labeling_for_traffic = tk.BooleanVar()
stop_labeling_for_timeout = tk.BooleanVar()
tk.Checkbutton(auto_tab, text="Stop Filling for Sensor1 Traffic", variable=stop_filling_for_traffic).pack()
tk.Checkbutton(auto_tab, text="Stop Labeling for Sensor2 Traffic", variable=stop_labeling_for_traffic).pack()
tk.Checkbutton(auto_tab, text="Stop Labeling if Sensor1 Inactive", variable=stop_labeling_for_timeout).pack()
tk.Button(auto_tab, text="Enable Auto Mode", command=lambda: set_auto_mode(True)).pack()

# Settings Tab
labeling_timeout_value = tk.IntVar(value=5)
traffic_threshold_value = tk.IntVar(value=2)
tk.Label(settings_tab, text="Labeling Timeout (s):").pack()
tk.Entry(settings_tab, textvariable=labeling_timeout_value).pack()
tk.Button(settings_tab, text="Update Timeout", command=lambda: set_labeling_timeout(labeling_timeout_value.get())).pack()
tk.Label(settings_tab, text="Traffic Threshold (s):").pack()
tk.Entry(settings_tab, textvariable=traffic_threshold_value).pack()
tk.Button(settings_tab, text="Update Threshold", command=lambda: set_traffic_threshold(traffic_threshold_value.get())).pack()

# Common Labels and Status Frames
status_frame = tk.Frame(root, bg="white", padx=10, pady=10)
status_frame.grid(row=1, column=1, sticky="nsew")
sensor1_label = tk.Label(status_frame, text="Sensor1 Counter: 0", bg="white")
sensor2_label = tk.Label(status_frame, text="Sensor2 Counter: 0", bg="white")
sensor1_traffic_label = tk.Label(status_frame, text="Sensor1 Traffic: Clear", bg="white")
sensor2_traffic_label = tk.Label(status_frame, text="Sensor2 Traffic: Clear", bg="white")
sensor1_label.pack()
sensor2_label.pack()
sensor1_traffic_label.pack()
sensor2_traffic_label.pack()

# Start updating the bottling line visual
update_bottling_line()

# Run the main loop
root.mainloop()