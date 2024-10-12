import time
from control import *
from inputs import *

def display_status():
    print("\n-- System Status --")
    print(f"Sensor1 Bottle Count: {sensor1_counter}")
    print(f"Sensor2 Bottle Count: {sensor2_counter}")
    print(f"Labeling Working: {is_labeling_machine_working()}")
    print(f"Labeling Alarm: {is_labeling_machine_in_alarm()}")
    print(f"Filling Working: {is_filling_machine_working()}")
    print(f"Filling Alarm: {is_filling_machine_in_alarm()}")
    print(f"Blowing Working: {is_blowing_machine_working()}")
    print(f"Blowing Alarm: {is_blowing_machine_in_alarm()}\n")

def manual_control():
    print("Available commands:")
    print("1. start_labeling")
    print("2. stop_labeling")
    print("3. start_filling")
    print("4. stop_filling")
    print("5. start_blowing")
    print("6. stop_blowing")
    print("7. reset_counters")
    print("8. exit")
    choice = input("Enter command: ")
    if choice == "start_labeling":
        start_labeling_machine()
    elif choice == "stop_labeling":
        stop_labeling_machine()
    elif choice == "start_filling":
        start_filling_machine()
    elif choice == "stop_filling":
        stop_filling_machine()
    elif choice == "start_blowing":
        start_blowing_machine()
    elif choice == "stop_blowing":
        stop_blowing_machine()
    elif choice == "reset_counters":
        reset_counters()
    elif choice == "exit":
        return False
    else:
        print("Invalid command. Please try again.")
    return True

def main():
    try:
        while True:
            count_sensor1_bottle()
            count_sensor2_bottle()
            if check_sensor1_traffic():
                print("Traffic detected on Sensor1!")
            if check_sensor2_traffic():
                print("Traffic detected on Sensor2!")
            display_status()
            if not manual_control():
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting program...")

if __name__ == "__main__":
    main()
