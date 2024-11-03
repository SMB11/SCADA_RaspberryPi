import time
import customtkinter
import logging
from status import start_labeling_machine, stop_labeling_machine, start_filling_machine, stop_filling_machine, start_blowing_machine, stop_blowing_machine, \
    check_sensor, check_auto_mode, initialize_logging, set_auto_mode, sensor1, sensor2, set_labeling_timeout, set_traffic_threshold_sensor1, set_traffic_threshold_sensor2, \
    labeling_working, filling_working, blowing_working, labeling_alarm, filling_alarm, blowing_alarm, labeling_idle, filling_idle, set_blowing_stop_delay

# Initialize logging
initialize_logging()

# Set the appearance mode and color theme
customtkinter.set_appearance_mode("Dark")  # Options: "System" (default), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Options: "blue" (default), "green", "dark-blue"

# Main window setup
root = customtkinter.CTk()
root.title("Bottling Line Control System")
root.geometry("1200x750")  # Adjust based on your screen dimensions

# Initialize counters and flags
sensor1_counter = 0
sensor2_counter = 0
sensor1_traffic = False
sensor2_traffic = False
auto_mode_enabled = False

# Define color mappings for machine status
status_colors = {"active": "#3ba55d", "stopped": "#d32f2f", "idle": "#f9a825"}

# Canvas for bottling line visualization
canvas = customtkinter.CTkCanvas(root, width=700, height=700)
canvas.grid(row=0, column=0, rowspan=2, padx=5, pady=5)

# Layout based on your image
blowing_rect = canvas.create_rectangle(50, 50, 200, 100, fill=status_colors["idle"], outline="white", width=2)
canvas.create_text(125, 75, text="Blowing Machine", anchor="center", font=("Arial", 12), fill="white")
canvas.create_line(200, 75, 350, 75, arrow='last', width=2, fill="white")

filling_rect = canvas.create_rectangle(350, 150, 500, 200, fill=status_colors["idle"], outline="white", width=2)
canvas.create_text(425, 175, text="Filling Machine", anchor="center", font=("Arial", 12), fill="white")
canvas.create_line(425, 100, 425, 150, arrow='last', width=2, fill="white")

labeling_rect = canvas.create_rectangle(50, 250, 200, 300, fill=status_colors["idle"], outline="white", width=2)
canvas.create_text(125, 275, text="Labeling Machine", anchor="center", font=("Arial", 12), fill="white")
canvas.create_line(200, 275, 350, 275, arrow='last', width=2, fill="white")

packing_rect = canvas.create_rectangle(350, 350, 500, 400, fill=status_colors["idle"], outline="white", width=2)
canvas.create_text(425, 375, text="Packing Machine", anchor="center", font=("Arial", 12), fill="white")
canvas.create_line(425, 300, 425, 350, arrow='last', width=2, fill="white")

# Status frame for counters and traffic indicators
status_frame = customtkinter.CTkFrame(root)
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

    # Update sensors and check for traffic
    sensor1_counter, sensor1_traffic = check_sensor(sensor1, sensor1_counter, sensor1_traffic, sensor_number=1)
    sensor2_counter, sensor2_traffic = check_sensor(sensor2, sensor2_counter, sensor2_traffic, sensor_number=2)

    # Check auto mode
    check_auto_mode(
        auto_mode_enabled,
        stop_filling_for_traffic.get(),
        sensor1_traffic,
        stop_labeling_for_traffic.get(),
        sensor2_traffic,
        stop_labeling_for_timeout.get(),
        stop_blowing_for_filling_stopped.get()  # New parameter
    )

    # Update the colors based on machine status
    canvas.itemconfig(blowing_rect, fill=get_status_color(blowing_working.is_pressed, blowing_alarm.is_pressed))
    canvas.itemconfig(filling_rect, fill=get_status_color(filling_working.is_pressed, filling_alarm.is_pressed))
    canvas.itemconfig(labeling_rect, fill=get_status_color(labeling_working.is_pressed, labeling_alarm.is_pressed))
    canvas.itemconfig(packing_rect, fill=status_colors["idle"])  # Assume packing machine is always idle

    # Update sensor counters and traffic indicators
    sensor1_label.configure(text=f"Sensor1 Counter: {sensor1_counter}")
    sensor2_label.configure(text=f"Sensor2 Counter: {sensor2_counter}")
    sensor1_traffic_label.configure(text=f"Sensor1 Traffic: {'Detected' if sensor1_traffic else 'Clear'}")
    sensor2_traffic_label.configure(text=f"Sensor2 Traffic: {'Detected' if sensor2_traffic else 'Clear'}")

    # Update machine statuses in system status tab
    blowing_status_label.configure(text=f"Blowing Working: {'Active' if blowing_working.is_pressed else 'Inactive'}")
    filling_status_label.configure(text=f"Filling Working: {'Active' if filling_working.is_pressed else 'Inactive'}")
    labeling_status_label.configure(text=f"Labeling Working: {'Active' if labeling_working.is_pressed else 'Inactive'}")

    blowing_alarm_label.configure(text=f"Blowing Alarm: {'Active' if blowing_alarm.is_pressed else 'Inactive'}")
    filling_alarm_label.configure(text=f"Filling Alarm: {'Active' if filling_alarm.is_pressed else 'Inactive'}")
    labeling_alarm_label.configure(text=f"Labeling Alarm: {'Active' if labeling_alarm.is_pressed else 'Inactive'}")

    labeling_idle_label.configure(text=f"Labeling Idle: {'Idle' if labeling_idle.is_pressed else 'Inactive'}")
    filling_idle_label.configure(text=f"Filling Idle: {'Idle' if filling_idle.is_pressed else 'Inactive'}")

    root.after(100, update_bottling_line)

# Toggle auto mode
def toggle_auto_mode():
    global auto_mode_enabled
    auto_mode_enabled = not auto_mode_enabled
    set_auto_mode(auto_mode_enabled)
    auto_mode_indicator.configure(text="Auto Mode Enabled" if auto_mode_enabled else "Manual Mode Enabled")
    print("Auto Mode Enabled" if auto_mode_enabled else "Manual Mode Enabled")  # Terminal feedback

# Function to reset counters
def reset_counters():
    global sensor1_counter, sensor2_counter
    sensor1_counter = 0
    sensor2_counter = 0
    logging.info("Counters reset")
    print("Counters reset.")

# Populate Status Frame with sensor and traffic status
sensor1_label = customtkinter.CTkLabel(status_frame, text=f"Sensor1 Counter: {sensor1_counter}", font=("Arial", 12))
sensor1_label.pack(pady=5)
sensor2_label = customtkinter.CTkLabel(status_frame, text=f"Sensor2 Counter: {sensor2_counter}", font=("Arial", 12))
sensor2_label.pack(pady=5)
sensor1_traffic_label = customtkinter.CTkLabel(status_frame, text="Sensor1 Traffic: Clear", font=("Arial", 12))
sensor1_traffic_label.pack(pady=5)
sensor2_traffic_label = customtkinter.CTkLabel(status_frame, text="Sensor2 Traffic: Clear", font=("Arial", 12))
sensor2_traffic_label.pack(pady=5)

# Tab control setup
tab_control = customtkinter.CTkTabview(root)
tab_control.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

# Create tabs
tab_control.add("Manual Control")
tab_control.add("Automatic Control")
tab_control.add("Settings")
tab_control.add("System Status")

manual_tab = tab_control.tab("Manual Control")
auto_tab = tab_control.tab("Automatic Control")
settings_tab = tab_control.tab("Settings")
status_tab = tab_control.tab("System Status")

# Manual Control Tab
for text, cmd in [("Start Labeling", start_labeling_machine), ("Stop Labeling", stop_labeling_machine),
                  ("Start Filling", start_filling_machine), ("Stop Filling", stop_filling_machine),
                  ("Start Blowing", start_blowing_machine), ("Stop Blowing", stop_blowing_machine),
                  ("Reset Counters", reset_counters)]:
    button = customtkinter.CTkButton(manual_tab, text=text, command=cmd)
    button.pack(padx=5, pady=5, fill='x')

# Automatic Control Tab
stop_filling_for_traffic = customtkinter.BooleanVar()
stop_labeling_for_traffic = customtkinter.BooleanVar()
stop_labeling_for_timeout = customtkinter.BooleanVar()
stop_blowing_for_filling_stopped = customtkinter.BooleanVar()  # New variable

customtkinter.CTkCheckBox(auto_tab, text="Stop Filling for Sensor1 Traffic", variable=stop_filling_for_traffic).pack(anchor="w", padx=5, pady=5)
customtkinter.CTkCheckBox(auto_tab, text="Stop Labeling for Sensor2 Traffic", variable=stop_labeling_for_traffic).pack(anchor="w", padx=5, pady=5)
customtkinter.CTkCheckBox(auto_tab, text="Stop Labeling if Sensor1 Inactive", variable=stop_labeling_for_timeout).pack(anchor="w", padx=5, pady=5)
customtkinter.CTkCheckBox(auto_tab, text="Stop Blowing if Filling Stopped", variable=stop_blowing_for_filling_stopped).pack(anchor="w", padx=5, pady=5)
customtkinter.CTkButton(auto_tab, text="Toggle Auto Mode", command=toggle_auto_mode).pack(padx=5, pady=10, fill='x')

# Auto Mode Indicator
auto_mode_indicator = customtkinter.CTkLabel(root, text="Manual Mode Enabled", font=("Arial", 14))
auto_mode_indicator.grid(row=0, column=1, padx=5, pady=5, sticky="s")

# Settings Tab
labeling_timeout_value = customtkinter.StringVar(value='5')
traffic_threshold_value_sensor1 = customtkinter.StringVar(value='2')
traffic_threshold_value_sensor2 = customtkinter.StringVar(value='2')
blowing_stop_delay_value = customtkinter.StringVar(value='5')  # New variable

def update_labeling_timeout():
    try:
        value = int(labeling_timeout_value.get())
        set_labeling_timeout(value)
        print(f"Labeling timeout updated to {value} seconds")
    except ValueError:
        print("Invalid input for labeling timeout")

def update_traffic_threshold_sensor1():
    try:
        value = int(traffic_threshold_value_sensor1.get())
        set_traffic_threshold_sensor1(value)
        print(f"Traffic threshold for Sensor1 updated to {value} seconds")
    except ValueError:
        print("Invalid input for Sensor1 traffic threshold")

def update_traffic_threshold_sensor2():
    try:
        value = int(traffic_threshold_value_sensor2.get())
        set_traffic_threshold_sensor2(value)
        print(f"Traffic threshold for Sensor2 updated to {value} seconds")
    except ValueError:
        print("Invalid input for Sensor2 traffic threshold")

def update_blowing_stop_delay():
    try:
        value = int(blowing_stop_delay_value.get())
        set_blowing_stop_delay(value)
        print(f"Blowing stop delay updated to {value} seconds")
    except ValueError:
        print("Invalid input for blowing stop delay")

customtkinter.CTkLabel(settings_tab, text="Labeling Timeout (s):").pack(anchor="w", padx=5, pady=5)
customtkinter.CTkEntry(settings_tab, textvariable=labeling_timeout_value).pack(fill="x", padx=5, pady=5)
customtkinter.CTkButton(settings_tab, text="Update Timeout", command=update_labeling_timeout).pack(pady=5, padx=5, fill='x')

customtkinter.CTkLabel(settings_tab, text="Traffic Threshold Sensor1 (s):").pack(anchor="w", padx=5, pady=5)
customtkinter.CTkEntry(settings_tab, textvariable=traffic_threshold_value_sensor1).pack(fill="x", padx=5, pady=5)
customtkinter.CTkButton(settings_tab, text="Update Threshold Sensor1", command=update_traffic_threshold_sensor1).pack(pady=5, padx=5, fill='x')

customtkinter.CTkLabel(settings_tab, text="Traffic Threshold Sensor2 (s):").pack(anchor="w", padx=5, pady=5)
customtkinter.CTkEntry(settings_tab, textvariable=traffic_threshold_value_sensor2).pack(fill="x", padx=5, pady=5)
customtkinter.CTkButton(settings_tab, text="Update Threshold Sensor2", command=update_traffic_threshold_sensor2).pack(pady=5, padx=5, fill='x')

customtkinter.CTkLabel(settings_tab, text="Blowing Stop Delay (s):").pack(anchor="w", padx=5, pady=5)
customtkinter.CTkEntry(settings_tab, textvariable=blowing_stop_delay_value).pack(fill="x", padx=5, pady=5)
customtkinter.CTkButton(settings_tab, text="Update Blowing Stop Delay", command=update_blowing_stop_delay).pack(pady=5, padx=5, fill='x')

# System Status Tab for machine statuses
blowing_status_label = customtkinter.CTkLabel(status_tab, text="Blowing Working: Inactive", font=("Arial", 12))
blowing_status_label.pack(pady=5)
filling_status_label = customtkinter.CTkLabel(status_tab, text="Filling Working: Inactive", font=("Arial", 12))
filling_status_label.pack(pady=5)
labeling_status_label = customtkinter.CTkLabel(status_tab, text="Labeling Working: Inactive", font=("Arial", 12))
labeling_status_label.pack(pady=5)

blowing_alarm_label = customtkinter.CTkLabel(status_tab, text="Blowing Alarm: Inactive", font=("Arial", 12))
blowing_alarm_label.pack(pady=5)
filling_alarm_label = customtkinter.CTkLabel(status_tab, text="Filling Alarm: Inactive", font=("Arial", 12))
filling_alarm_label.pack(pady=5)
labeling_alarm_label = customtkinter.CTkLabel(status_tab, text="Labeling Alarm: Inactive", font=("Arial", 12))
labeling_alarm_label.pack(pady=5)

labeling_idle_label = customtkinter.CTkLabel(status_tab, text="Labeling Idle: Inactive", font=("Arial", 12))
labeling_idle_label.pack(pady=5)
filling_idle_label = customtkinter.CTkLabel(status_tab, text="Filling Idle: Inactive", font=("Arial", 12))
filling_idle_label.pack(pady=5)

# Start the main loop
update_bottling_line()
root.mainloop()
