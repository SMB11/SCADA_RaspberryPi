import time
from gpiozero import Button
from control import start_labeling_machine, stop_labeling_machine, start_filling_machine, stop_filling_machine, start_blowing_machine, stop_blowing_machine

# Initialize counters and traffic thresholds
sensor1_counter = 0
sensor2_counter = 0
TRAFFIC_THRESHOLD = 2  # Time in seconds to consider traffic

# Define GPIO pins for the sensors and machine status
sensor1 = Button(13, pull_up=True)
sensor2 = Button(26, pull_up=True)

# Machine status pins (replace with actual initialization)
labeling_working = Button(21, pull_up=True)
labeling_alarm = Button(19, pull_up=True)
filling_working = Button(16, pull_up=True)
filling_alarm = Button(5, pull_up=True)
blowing_working = Button(18, pull_up=True)
blowing_alarm = Button(10, pull_up=True)

def display_status():
    print("\n-- System Status --")
    print(f"Labeling Working: {'Pressed' if labeling_working.is_pressed else 'Released'}")
    print(f"Labeling Alarm: {'Pressed' if labeling_alarm.is_pressed else 'Released'}")
    print(f"Filling Working: {'Pressed' if filling_working.is_pressed else 'Released'}")
    print(f"Filling Alarm: {'Pressed' if filling_alarm.is_pressed else 'Released'}")
    print(f"Blowing Working: {'Pressed' if blowing_working.is_pressed else 'Released'}")
    print(f"Blowing Alarm: {'Pressed' if blowing_alarm.is_pressed else 'Released'}")
    print(f"Sensor1 Counter: {sensor1_counter}")
    print(f"Sensor2 Counter: {sensor2_counter}")
    print("\n")

def manual_control():
    command = input("Enter command (start_labeling, stop_labeling, start_filling, stop_filling, start_blowing, stop_blowing, reset, status, exit): ").strip()
    if command == "start_labeling":
        start_labeling_machine()
    elif command == "stop_labeling":
        stop_labeling_machine()
    elif command == "start_filling":
        start_filling_machine()
    elif command == "stop_filling":
        stop_filling_machine()
    elif command == "start_blowing":
        start_blowing_machine()
    elif command == "stop_blowing":
        stop_blowing_machine()
    elif command == "reset":
        global sensor1_counter, sensor2_counter
        sensor1_counter = 0
        sensor2_counter = 0
        print("Counters reset.")
    elif command == "status":
        display_status()
    elif command == "exit":
        return False
    else:
        print("Invalid command. Try again.")
    return True

def check_sensor(sensor, sensor_counter, high_start):
    # Count bottle passing if sensor is pressed
    if sensor.is_pressed:
        if high_start is None:
            # Only increment counter if not under traffic detection
            sensor_counter += 1
            print(f"Sensor detected, count updated: {sensor_counter}")
            time.sleep(0.2)  # Debounce
            return sensor_counter, time.time()  # Start traffic timer after count
        else:
            # Traffic detected, do not increment counter
            if time.time() - high_start >= TRAFFIC_THRESHOLD:
                print(f"Traffic detected on sensor")
                return sensor_counter, None  # Reset timer after detecting traffic
    else:
        # Sensor is not pressed, reset traffic timer
        return sensor_counter, None

    return sensor_counter, high_start

def main():
    global sensor1_counter, sensor2_counter
    sensor1_high_start = None
    sensor2_high_start = None
    last_status_display = time.time()
    status_interval = 5  # Update status display every 5 seconds

    try:
        while True:
            # Check sensor1
            sensor1_counter, sensor1_high_start = check_sensor(sensor1, sensor1_counter, sensor1_high_start)

            # Check sensor2
            sensor2_counter, sensor2_high_start = check_sensor(sensor2, sensor2_counter, sensor2_high_start)

            # Display status every 5 seconds
            if time.time() - last_status_display >= status_interval:
                display_status()
                last_status_display = time.time()

            # Allow for manual control at intervals
            if not manual_control():
                break

            # Short sleep to avoid excessive CPU usage
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting program...")

if __name__ == "__main__":
    main()
