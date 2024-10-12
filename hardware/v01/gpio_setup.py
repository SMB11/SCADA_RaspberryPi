from gpiozero import LED, Button

# Initialize all necessary GPIO components
def initialize_gpio():
    global LABELING_START_PIN, LABELING_STOP_PIN, FILLING_STOP_PIN, BLOWING_START_PIN, BLOWING_STOP_PIN
    global SENSOR1_PIN, SENSOR2_PIN

    # Machine control pins as LEDs for simplicity
    LABELING_START_PIN = LED(4)
    LABELING_STOP_PIN = LED(27)
    FILLING_STOP_PIN = LED(23)
    BLOWING_START_PIN = LED(24)
    BLOWING_STOP_PIN = LED(22)

    # Use pull_up for sensors as with the previously working setup
    SENSOR1_PIN = Button(19, pull_up=True)
    SENSOR2_PIN = Button(20, pull_up=True)

def cleanup_gpio():
    # Close all components at cleanup
    LABELING_START_PIN.close()
    LABELING_STOP_PIN.close()
    FILLING_STOP_PIN.close()
    BLOWING_START_PIN.close()
