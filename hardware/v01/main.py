import RPi.GPIO as GPIO
import gpio_setup
import control
import inputs
import time

# Define GPIO pins
SENSOR1_PIN = None  # Replace with actual pin number
SENSOR2_PIN = None
LABELING_START_PIN = None
LABELING_STOP_PIN = None
FILLING_STOP_PIN = None
BLOWING_START_PIN = None
BLOWING_STOP_PIN = None
LABELING_WORKING_PIN = None
LABELING_ALARM_PIN = None
LABELING_ALARM_HANDLED_PIN = None
FILLING_WORKING_PIN = None
FILLING_ALARM_PIN = None
FILLING_ALARM_HANDLED_PIN = None
BLOWING_WORKING_PIN = None
BLOWING_ALARM_PIN = None

def display_status():
    print("\n-- System Status --")
    print(f"Sensor1 Bottle Count: {inputs.sensor1_counter}")
    print(f"Sensor2 Bottle Count: {inputs.sensor2_counter}")
    print(f"Labeling Working: {inputs.is_labeling_machine_working(GPIO, LABELING_WORKING_PIN)}")
    print(f"Labeling Alarm: {inputs.is_labeling_machine_in_alarm(GPIO, LABELING_ALARM_PIN)}")
    print(f"Filling Working: {inputs.is_filling_machine_working(GPIO, FILLING_WORKING_PIN)}")
    print(f"Filling Alarm: {inputs.is_filling_machine_in_alarm(GPIO, FILLING_ALARM_PIN)}")
    print(f"Blowing Working: {inputs.is_blowing_machine_working(GPIO, BLOWING_WORKING_PIN)}")
    print(f"Blowing Alarm: {inputs.is_blowing_machine_in_alarm(GPIO, BLOWING_ALARM_PIN)}\n")

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
        control.start_labeling_machine(GPIO, LABELING_START_PIN, LABELING_STOP_PIN)
    elif choice == "stop_labeling":
        control.stop_labeling_machine(GPIO, LABELING_START_PIN, LABELING_STOP_PIN)
    elif choice == "start_filling":
        control.start_filling_machine(GPIO, FILLING_STOP_PIN)
    elif choice == "stop_filling":
        control.stop_filling_machine(GPIO, FILLING_STOP_PIN)
    elif choice == "start_blowing":
        control.start_blowing_machine(GPIO, BLOWING_START_PIN, BLOWING_STOP_PIN)
    elif choice == "stop_blowing":
        control.stop_blowing_machine(GPIO, BLOWING_START_PIN, BLOWING_STOP_PIN)
    elif choice == "reset_counters":
        inputs.reset_counters()
    elif choice == "exit":
        return False
    else:
        print("Invalid command. Please try again.")
    
    return True

def main():
    gpio_setup.initialize_gpio(GPIO, LABELING_START_PIN, LABELING_STOP_PIN, FILLING_STOP_PIN, BLOWING_START_PIN, BLOWING_STOP_PIN,
                               LABELING_WORKING_PIN, LABELING_ALARM_PIN, LABELING_ALARM_HANDLED_PIN,
                               FILLING_WORKING_PIN, FILLING_ALARM_PIN, FILLING_ALARM_HANDLED_PIN,
                               BLOWING_WORKING_PIN, BLOWING_ALARM_PIN, SENSOR1_PIN, SENSOR2_PIN)

    try:
        while True:
            # Count bottles passing sensors
            inputs.count_sensor1_bottle(GPIO, SENSOR1_PIN)
            inputs.count_sensor2_bottle(GPIO, SENSOR2_PIN)

            # Check for traffic on Sensor1 and Sensor2
            if inputs.check_sensor1_traffic(GPIO, SENSOR1_PIN):
                print("Traffic detected on Sensor1!")

            if inputs.check_sensor2_traffic(GPIO, SENSOR2_PIN):
                print("Traffic detected on Sensor2!")

            # Display status periodically
            display_status()

            # Allow for manual control
            if not manual_control():
                break

            # Short delay to reduce CPU usage
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Exiting program...")

    finally:
        gpio_setup.cleanup_gpio(GPIO)

if __name__ == "__main__":
    main()
