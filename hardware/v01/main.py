import gpio_setup
import inputs
import control
from signal import pause

def display_status():
    print("\n-- Status --")
    print(f"Sensor 1 count: {inputs.sensor1_counter}")
    print(f"Sensor 2 count: {inputs.sensor2_counter}")

def manual_control():
    print("Commands:")
    print("1. Start labeling")
    print("2. Stop labeling")
    print("3. Start filling")
    print("4. Stop filling")
    print("5. Start blowing")
    print("6. Stop blowing")
    print("7. Reset counts")
    print("8. Exit")

    choice = input("Choose command: ")
    if choice == "1":
        control.start_labeling_machine()
    elif choice == "2":
        control.stop_labeling_machine()
    elif choice == "3":
        control.start_filling_machine()
    elif choice == "4":
        control.stop_filling_machine()
    elif choice == "5":
        control.start_blowing_machine()
    elif choice == "6":
        control.stop_blowing_machine()
    elif choice == "7":
        inputs.reset_counters()
    elif choice == "8":
        return False
    else:
        print("Invalid choice.")
    return True

def main():
    gpio_setup.initialize_gpio()
    inputs.initialize_sensor_events()

    try:
        while True:
            display_status()
            inputs.check_traffic(inputs.SENSOR1_PIN, "Sensor 1")
            inputs.check_traffic(inputs.SENSOR2_PIN, "Sensor 2")
            if not manual_control():
                break
            pause()  # Maintains the event-driven counting

    except KeyboardInterrupt:
        print("Program interrupted.")

    finally:
        gpio_setup.cleanup_gpio()

if __name__ == "__main__":
    main()
