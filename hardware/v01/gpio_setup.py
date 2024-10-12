from gpiozero import Button
from gpiozero import DigitalOutputDevice

# Define GPIO pin assignments based on your original setup
def initialize_gpio():
    global LABELING_START_PIN, LABELING_STOP_PIN, FILLING_STOP_PIN, BLOWING_START_PIN, BLOWING_STOP_PIN
    global SENSOR1_PIN, SENSOR2_PIN

    # Machine control outputs (using DigitalOutputDevice to manage state)
    LABELING_START_PIN = DigitalOutputDevice(4)
    LABELING_STOP_PIN = DigitalOutputDevice(27)
    FILLING_STOP_PIN = DigitalOutputDevice(23)
    BLOWING_START_PIN = DigitalOutputDevice(24)
    BLOWING_STOP_PIN = DigitalOutputDevice(22)

    # Sensors configured with pull-up resistors
    SENSOR1_PIN = Button(19, pull_up=True)
    SENSOR2_PIN = Button(20, pull_up=True)

def cleanup_gpio():
    # Closing outputs for good cleanup
    LABELING_START_PIN.close()
    LABELING_STOP_PIN.close()
    FILLING_STOP_PIN.close()
    BLOWING_START_PIN.close()
