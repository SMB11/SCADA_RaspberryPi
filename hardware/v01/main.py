import time
from control import *
from inputs import *
from gpio_setup import *

def display_status():
    print("\n-- System Status --")
    print(f"Sensor1 Bottle Count: {sensor1_counter}")
    print(f"Sensor2 Bottle Count: {sensor2_counter}")
    print(f"Labeling Working: {labeling_working.is_pressed}")
    print(f"Labeling Alarm: {labeling_alarm.is_pressed}")
    print(f"Filling Working: {filling_working.is_pressed}")
    print(f"Filling Alarm: {filling_alarm.is_pressed}")
    print(f"Blowing Working: {blowing_working.is_pressed}")
    print(f"Blowing Alarm: {blowing_alarm.is_pressed}\n")

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
        reset_counters()
    elif command == "status":
        display_status()
    elif command == "exit":
        return False
    else:
        print("Invalid command. Try again.")
    return True

def main():
    sensor1_high_start = None
    sensor2_high_start = None

    try:
        while True:
            check_sensor1()
            check_sensor2()
            sensor1_high_start = detect_traffic(sensor1, sensor1_high_start)
            sensor2_high_start = detect_traffic(sensor2, sensor2_high_start)

            if not manual_control():
                break
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting program...")

if __name__ == "__main__":
    main()
