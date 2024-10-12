import time
from control import *
from inputs import *
from gpio_setup import labeling_working, labeling_alarm, filling_working, filling_alarm, blowing_working, blowing_alarm

def display_status():
    print("\n-- System Status --")
    print(f"Labeling Working: {'Pressed' if labeling_working.is_pressed else 'Released'}")
    print(f"Labeling Alarm: {'Pressed' if labeling_alarm.is_pressed else 'Released'}")
    print(f"Filling Working: {'Pressed' if filling_working.is_pressed else 'Released'}")
    print(f"Filling Alarm: {'Pressed' if filling_alarm.is_pressed else 'Released'}")
    print(f"Blowing Working: {'Pressed' if blowing_working.is_pressed else 'Released'}")
    print(f"Blowing Alarm: {'Pressed' if blowing_alarm.is_pressed else 'Released'}\n")


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
    try:
        while True:
            # Continuously check the status of all inputs
            display_status()

            # Check sensors for counting bottles
            check_sensor1()
            check_sensor2()

            # You can also implement other checks here

            # Short delay to avoid high CPU usage
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting program...")


if __name__ == "__main__":
    main()
