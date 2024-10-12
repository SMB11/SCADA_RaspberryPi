
import gpio_setup
import control
import inputs
import time

def display_status():
    print("\n-- System Status --")
    print(f"Sensor1 Bottle Count: {inputs.sensor1_counter}")
    print(f"Sensor2 Bottle Count: {inputs.sensor2_counter}")
    print(f"Labeling Working: {inputs.is_labeling_machine_working()}")
    print(f"Labeling Alarm: {inputs.is_labeling_machine_in_alarm()}")
    print(f"Filling Working: {inputs.is_filling_machine_working()}")
    print(f"Traffic on Sensor1: {inputs.check_sensor1_traffic()}")
    print(f"Traffic on Sensor2: {inputs.check_sensor2_traffic()}\n")

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
        print("Invalid command. Please try again.")
    
    return True

def main():
    gpio_setup.initialize_gpio()

    try:
        while True:
            inputs.count_sensor1_bottle()
            inputs.count_sensor2_bottle()

            # Display the status
            display_status()
            
            # Manual control
            if not manual_control():
                break

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Exiting program...")

    finally:
        gpio_setup.cleanup_gpio()

if __name__ == "__main__":
    main()
