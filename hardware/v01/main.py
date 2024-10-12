import gpio_setup
import control
import inputs
from signal import pause

def display_status():
    print("\n-- System Status --")
    print(f"Sensor 1 Bottle Count: {inputs.sensor1_counter}")
    print(f"Sensor 2 Bottle Count: {inputs.sensor2_counter}")

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
        control.start_labeling_machine()
    elif choice == "stop_labeling":
        control.stop_labeling_machine()
    elif choice == "start_filling":
        control.start_filling_machine()
    elif choice == "stop_filling":
        control.stop_filling_machine()
    elif choice == "start_blowing":
        control.start_blowing_machine()
    elif choice == "stop_blowing":
        control.stop_blowing_machine()
    elif choice == "reset_counters":
        inputs.reset_counters()
    elif choice == "exit":
        return False
    else:
        print("Invalid command.")
    return True

def main():
    gpio_setup.initialize_gpio()
    inputs.initialize_sensor_events()

    try:
        while True:
            display_status()
            # Check for traffic
            inputs.check_sensor_traffic(inputs.SENSOR1_PIN, "Sensor 1")
            inputs.check_sensor_traffic(inputs.SENSOR2_PIN, "Sensor 2")
            
            if not manual_control():
                break
            pause()

    except KeyboardInterrupt:
        print("Exiting program...")

    finally:
        gpio_setup.cleanup_gpio()

if __name__ == "__main__":
    main()
