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
root.geometry("1100x700")

# Canvas for bottling line visualization
canvas = tk.Canvas(root, width=800, height=600, bg="lightgray")
canvas.grid(row=0, column=0, rowspan=2, padx=20, pady=20)

# Define color mappings for machine status
status_colors = {"active": "green", "stopped": "red", "idle": "yellow"}

# Create bottling line elements on the Canvas according to the structure in the image
blowing_rect = canvas.create_rectangle(50, 50, 250, 130, fill=status_colors["idle"], outline="black", width=2)
canvas.create_text(150, 90, text="Bottle Blowing Machine", anchor="center")
canvas.create_line(250, 90, 350, 90, arrow=tk.LAST, width=3)  # Conveyor 1

filling_rect = canvas.create_rectangle(350, 160, 550, 240, fill=status_colors["idle"], outline="black", width=2)
canvas.create_text(450, 200, text="Bottle Filling Machine", anchor="center")
canvas.create_line(250, 200, 350, 200, arrow=tk.LAST, width=3)  # Conveyor 2

labeling_rect = canvas.create_rectangle(50, 270, 250, 350, fill=status_colors["idle"], outline="black", width=2)
canvas.create_text(150, 310, text="Bottle Labeling Machine", anchor="center")
canvas.create_line(250, 310, 350, 310, arrow=tk.LAST, width=3)  # Conveyor 3

packing_rect = canvas.create_rectangle(350, 380, 550, 460, fill=status_colors["idle"], outline="black", width=2)
canvas.create_text(450, 420, text="Bottle Packing Machine", anchor="center")
canvas.create_line(250, 420, 350, 420, arrow=tk.LAST, width=3)  # Conveyor 4

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
    canvas.itemconfig(packing_rect, fill=status_colors["idle"])  # Assuming packing is always idle

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

# Common Status Frame
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