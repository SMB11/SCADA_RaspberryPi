from gpio_setup import *
from inputs import *
from signal import pause

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

def main():
    print("Starting system. Press Ctrl+C to exit.")
    while True:
        display_status()
        reset_choice = input("Press 'r' to reset counters or Enter to continue: ").lower()
        if reset_choice == 'r':
            reset_counters()
        # Continuously wait for button presses (bottle detection)
        pause()  # Keeps the program running, waiting for the sensor events

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting program...")
